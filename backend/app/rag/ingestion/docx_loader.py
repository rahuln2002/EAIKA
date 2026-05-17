from pathlib import Path

from docx import Document


def load_docx(
    file_path: str,
) -> str:
    """
    Extract text from DOCX document.
    """

    if not Path(file_path).exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    document = Document(file_path)

    extracted_text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text.append(paragraph.text)

    return "\n".join(extracted_text)
