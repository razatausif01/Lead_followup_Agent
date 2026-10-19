# app/rag/ingest.py
from pathlib import Path

import chromadb

# ingest.py -> rag -> app -> project root
ROOT = Path(__file__).resolve().parents[2]
KB_DIR = ROOT / "data" / "kb"
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION_NAME = "kb_docs"
MAX_CHUNK_CHARS = 500


def _chunk_text(text: str) -> list[str]:
    """Paragraphs ko jod ke ~500 character ke chunks banata hai."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if current and len(current) + len(p) > MAX_CHUNK_CHARS:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        chunks.append(current)
    return chunks


def ingest() -> int:
    """data/kb ki .md/.txt files padh ke Chroma me daalta hai. Kitne chunks gaye, wo return karta hai."""
    files = sorted(list(KB_DIR.glob("*.md")) + list(KB_DIR.glob("*.txt")))
    if not files:
        print(f"{KB_DIR} me koi .md/.txt file nahi mili")
        return 0

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Har baar fresh banao, taaki purane chunks duplicate na hon
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)

    ids, docs, metas = [], [], []
    for f in files:
        for i, chunk in enumerate(_chunk_text(f.read_text(encoding="utf-8"))):
            ids.append(f"{f.stem}-{i}")
            docs.append(chunk)
            metas.append({"source": f.name})

    collection.add(ids=ids, documents=docs, metadatas=metas)
    print(f"{len(files)} files se {len(docs)} chunks save hue")
    return len(docs)


if __name__ == "__main__":
    ingest()