from pypdf import PdfReader


def read_all_pages(file):
    reader = PdfReader(file)
    full_text = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        full_text.append(text)

    return "\n".join(full_text)


def read_text_file(file):
    raw = file.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")
