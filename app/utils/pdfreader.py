from pypdf import PdfReader


def read_all_pages(file):
    reader = PdfReader(file)
    print(f"Total Pages: {len(reader.pages)}")
    
    full_text = []
    
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        full_text.append(text)
            
    return "\n".join(full_text)
