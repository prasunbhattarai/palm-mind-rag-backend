from langchain_text_splitters import RecursiveCharacterTextSplitter


def fix_chunking(text:str, chunck_size: int = 100, overlap: int = 20):
    chunks =[]
    start = 0

    while start < len(text):
        end = start + chunck_size

        chunks.append(text[start:end])

        start += chunck_size - overlap
    
    return chunks


def recursive_chunk(text: str, chunk_size: int = 200, overlap: int = 40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)
