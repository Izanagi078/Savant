import fitz  # PyMuPDF
import requests
from io import BytesIO

def extract_text_from_pdf(url: str) -> str:
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return ""

    with fitz.open(stream=BytesIO(response.content), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
            if len(text) > 2000:
                break
        return text.strip()
