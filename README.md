Invoice Information Extraction System using AI

Overview
This project extracts structured information from invoice PDFs using a Flask web application and a vision language model. Users upload invoices, the system processes the document, extracts key fields, and stores them in a database for later viewing and download.

Features
- Upload invoice PDFs
- Convert PDF page to image
- Extract invoice details using a Vision LLM
- Store results in SQLite database
- View extracted invoices in web interface
- Download original PDF

Extracted Fields
- Seller Name
- Buyer Name
- Invoice Number / GST Number
- Invoice Date
- Total Amount

Tech Stack
Backend: Python, Flask, SQLAlchemy
AI: Ollama Vision Model (LLaMA Vision)
Document Processing: PyMuPDF
Database: SQLite


Project Structure
invoice-extraction/
│
├── app/
├── templates/
├── static/
├── uploads/
├── instance/
│
├── run.py
├── requirements.txt
└── README.md


Installation
1. Clone the repository
git clone https://github.com//invoice-extraction.git

2. Install dependencies
pip install -r requirements.txt
Running the Application
python run.py

Open browser:
http://localhost:5000
Future Improvements
- Support multiple invoice formats
- Add table extraction
- Improve LLM prompting
- Deploy using Docker
License
MIT License
