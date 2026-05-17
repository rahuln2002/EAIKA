from pathlib import Path

from pypdf import PdfReader


def load_pdf(
    file_path: str,
) -> str:
    """
    Extract text from PDF document.
    """

    if not Path(file_path).exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(file_path)

    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)
