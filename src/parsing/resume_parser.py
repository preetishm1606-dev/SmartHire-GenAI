from pypdf import PdfReader


def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page_number, page in enumerate(reader.pages):

        try:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        except Exception as e:
            print(
                f"Error reading page "
                f"{page_number + 1}: {e}"
            )

    return text