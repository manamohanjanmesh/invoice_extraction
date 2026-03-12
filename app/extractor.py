import json
import base64
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def extract_invoice_details_from_api(image_path):
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        prompt = """
        Extract the following details from this invoice image:
        - Seller Name
        - Buyer Name
        - GST No or Invoice No
        - Invoice Date
        - Total Amount

        Format the output as a clean JSON object with these exact keys:
        "seller_name", "buyer_name", "gst_or_invoice_no", "invoice_date", "total_amount".
        If a value is not found, use "N/A". Respond with ONLY the JSON object.
        """

        payload = {
            "model": "llama3.2-vision:q4_K_M",
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            "format": "json"
        }

        headers = {
            "ngrok-skip-browser-warning": "true"
        }

        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        generated_text = response.json().get("response", "{}")
        extracted_data = json.loads(generated_text)

        return extracted_data

    except:
        return None