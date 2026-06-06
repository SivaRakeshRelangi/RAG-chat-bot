def chunk_text(pages, size=500, overlap=100):
    chunks = []

    for p in pages:
        words = p["text"].split()

        for i in range(0, len(words), size - overlap):
            chunk = " ".join(words[i:i+size])

            chunks.append({
                "text": chunk,
                "page": p["page"]
            })

    return chunks