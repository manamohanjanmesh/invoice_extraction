from .database import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_name = db.Column(db.String(255), nullable=False, default="N/A")
    buyer_name = db.Column(db.String(255), nullable=False, default="N/A")
    invoice_date = db.Column(db.String(50), nullable=False, default="N/A")
    gst_invoice_no = db.Column(db.String(50), nullable=False, default="N/A")
    total_amount = db.Column(db.String(50), nullable=False, default="N/A")
    pdf_file = db.Column(db.LargeBinary, nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Invoice {self.id}: {self.seller_name}>"