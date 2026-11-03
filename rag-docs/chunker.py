def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


if __name__ == "__main__":
    text = open("notes.txt", encoding="utf-8").read()
    chunks = chunk_text(text)
    print("Total chunks:", len(chunks))
    print(chunks[0])
    print("-----")
    print(chunks[1])