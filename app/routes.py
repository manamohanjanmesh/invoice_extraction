import os
import io
import fitz
from flask import Blueprint, request, render_template, redirect, url_for, send_file, current_app
from werkzeug.utils import secure_filename
from .models import Invoice
from .database import db
from .extractor import extract_invoice_details_from_api

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("first_page.html")

@main.route("/extract", methods=["POST"])
def handle_extraction():
    if "file" not in request.files:
        return "No file part in the request", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    pdf_data = file.read()

    with open(filepath, "wb") as f:
        f.write(pdf_data)

    extracted_data = {}

    try:
        doc = fitz.open(filepath)

        if len(doc) > 0:
            page = doc[0]
            pix = page.get_pixmap(dpi=120)

            temp_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "temp_page.jpg")
            pix.save(temp_image_path, "jpeg")

            extracted_data = extract_invoice_details_from_api(temp_image_path)

            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        doc.close()

    except:
        return "Error processing the PDF file.", 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    if not extracted_data:
        return "Failed to extract data from the invoice.", 500

    new_invoice = Invoice(
        seller_name=extracted_data.get("seller_name", "N/A"),
        buyer_name=extracted_data.get("buyer_name", "N/A"),
        invoice_date=extracted_data.get("invoice_date", "N/A"),
        gst_invoice_no=extracted_data.get("gst_or_invoice_no", "N/A"),
        total_amount=str(extracted_data.get("total_amount", "0.00")),
        pdf_file=pdf_data,
        original_filename=filename
    )

    db.session.add(new_invoice)
    db.session.commit()

    return redirect(url_for("main.display_all_invoices"))

@main.route("/invoices")
def display_all_invoices():
    all_invoices = Invoice.query.all()
    return render_template("second_page.html", invoices=all_invoices)

@main.route("/invoice/<int:invoice_id>")
def display_invoice_details(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template("third_page.html", invoice=invoice)

@main.route("/download/<int:invoice_id>")
def download_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    return send_file(
        io.BytesIO(invoice.pdf_file),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=invoice.original_filename
    )