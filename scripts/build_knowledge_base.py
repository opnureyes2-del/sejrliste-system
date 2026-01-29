#!/usr/bin/env python3
"""
ChromaDB Knowledge Base Builder
================================
Indekserer alle vigtige .md filer fra projektet til en søgbar knowledge base.

Brug:
    python3 scripts/build_knowledge_base.py          # Byg/genbyg knowledge base
    python3 scripts/build_knowledge_base.py --query "Hvad er LINEN?"   # Søg
    python3 scripts/build_knowledge_base.py --stats   # Vis statistik

Database gemmes i: ~/.project_db/
"""

import chromadb
import os
import sys
import json
from pathlib import Path

DB_PATH = os.path.expanduser("~/.project_db")

# Nøgle-mapper der skal indekseres
SOURCE_DIRS = [
    ("/home/rasmus/Desktop/HOW TO USE A CLAUDE OPUS/", "claude_guide"),
    ("/home/rasmus/Desktop/MIN ADMIRAL/", "admiral"),
    ("/home/rasmus/Desktop/INTRO FOLDER SYSTEM/", "intro"),
    ("/home/rasmus/Desktop/sejrliste systemet/", "sejrliste"),
]

# Mapper der springes over
SKIP_DIRS = {"90_ARCHIVE", ".git", "node_modules", "__pycache__", "venv"}


def collect_documents():
    """Samler alle .md filer fra nøgle-mapperne."""
    all_files = {}  # filepath -> source_name (dedup by path)

    for base_path, source_name in SOURCE_DIRS:
        if not os.path.isdir(base_path):
            print(f"  ⚠️  Mappe ikke fundet: {base_path}")
            continue

        for root, dirs, files in os.walk(base_path):
            # Skip uønskede mapper
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for fname in files:
                if fname.endswith('.md'):
                    fpath = os.path.join(root, fname)
                    all_files[fpath] = source_name

    return all_files


def build_knowledge_base():
    """Bygger ChromaDB knowledge base fra alle nøgle-dokumenter."""
    print("🔨 Bygger ChromaDB Knowledge Base...")
    print(f"📁 Database: {DB_PATH}\n")

    client = chromadb.PersistentClient(path=DB_PATH)

    # Slet eksisterende collection (fresh start)
    try:
        client.delete_collection("cirkelline_docs")
        print("🗑️  Gammel collection slettet")
    except Exception:
        pass

    collection = client.create_collection(
        name="cirkelline_docs",
        metadata={
            "description": "Cirkelline project knowledge base",
            "hnsw:space": "cosine"  # Cosine similarity for bedre semantisk søgning
        }
    )

    all_files = collect_documents()

    documents = []
    ids = []
    metadatas = []
    skipped = 0

    for fpath, source_name in sorted(all_files.items()):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip meget små filer (< 50 tegn)
            if len(content) < 50:
                skipped += 1
                continue

            # Truncér meget store filer (> 30K) — ChromaDB embeddings virker
            # bedst med kortere tekster
            if len(content) > 30000:
                content = content[:30000] + "\n\n[TRUNCATED - original: {} chars]".format(len(content))

            # Unikt ID fra fuld sti
            doc_id = fpath.replace("/", "__").replace(" ", "-")

            documents.append(content)
            ids.append(doc_id)
            metadatas.append({
                "source": source_name,
                "filename": os.path.basename(fpath),
                "filepath": fpath,
                "size": len(content)
            })
        except Exception as e:
            print(f"  ❌ Fejl ved {fpath}: {e}")
            continue

    # Tilføj i batches (ChromaDB anbefaler max ~40 ad gangen for store docs)
    BATCH_SIZE = 20
    total_added = 0
    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i+BATCH_SIZE]
        batch_ids = ids[i:i+BATCH_SIZE]
        batch_meta = metadatas[i:i+BATCH_SIZE]

        collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_meta)
        total_added += len(batch_docs)
        print(f"  📦 Batch {i//BATCH_SIZE + 1}: {len(batch_docs)} dokumenter tilføjet")

    # Statistik
    source_counts = {}
    for m in metadatas:
        s = m['source']
        source_counts[s] = source_counts.get(s, 0) + 1

    print(f"\n{'='*50}")
    print(f"✅ ChromaDB Knowledge Base KLAR!")
    print(f"📚 Dokumenter indekseret: {total_added}")
    print(f"⏭️  Skipped (for små): {skipped}")
    print(f"💾 Database: {DB_PATH}")
    print(f"\nKilder:")
    for s, c in sorted(source_counts.items()):
        print(f"  - {s}: {c} filer")

    return total_added


def smart_query(question, n_results=3):
    """Søg i knowledge base — returnér kun relevante dokumenter."""
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        collection = client.get_collection("cirkelline_docs")
    except Exception:
        print("❌ Knowledge base ikke fundet. Kør først: python3 build_knowledge_base.py")
        return None

    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    print(f"\n🔍 Søgning: \"{question}\"")
    print(f"📚 Fandt {len(results['documents'][0])} relevante dokumenter:\n")

    total_chars = 0
    for i, (doc, meta, dist) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        relevance = max(0, 1 - dist)  # Cosine: 0=perfekt match, 2=helt ulig
        preview = doc[:200].replace('\n', ' ')
        total_chars += len(doc)
        print(f"  {i+1}. [{meta['source']}] {meta['filename']}")
        print(f"     Relevans: {relevance:.1%} | Størrelse: {meta['size']} tegn")
        print(f"     Preview: {preview}...")
        print()

    # Token estimat
    approx_tokens = total_chars // 4
    print(f"📊 Total kontekst: ~{approx_tokens} tokens (i stedet for hele basen)")

    context = "\n---\n".join(results['documents'][0])
    return context


def show_stats():
    """Vis statistik for knowledge base."""
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        collection = client.get_collection("cirkelline_docs")
    except Exception:
        print("❌ Knowledge base ikke fundet. Kør først: python3 build_knowledge_base.py")
        return

    count = collection.count()
    print(f"\n📊 Knowledge Base Statistik")
    print(f"{'='*40}")
    print(f"📚 Totalt dokumenter: {count}")
    print(f"💾 Database: {DB_PATH}")

    # Hent alle metadata
    all_data = collection.get()
    source_counts = {}
    total_size = 0
    for meta in all_data['metadatas']:
        s = meta.get('source', 'unknown')
        source_counts[s] = source_counts.get(s, 0) + 1
        total_size += meta.get('size', 0)

    print(f"📏 Total størrelse: {total_size / 1024:.1f} KB")
    print(f"\nKilder:")
    for s, c in sorted(source_counts.items()):
        print(f"  - {s}: {c} filer")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stats":
            show_stats()
        elif sys.argv[1] == "--query":
            if len(sys.argv) > 2:
                question = " ".join(sys.argv[2:])
                smart_query(question)
            else:
                print("Brug: python3 build_knowledge_base.py --query \"dit spørgsmål\"")
        else:
            print("Brug:")
            print("  python3 build_knowledge_base.py          # Byg knowledge base")
            print("  python3 build_knowledge_base.py --query \"...\"  # Søg")
            print("  python3 build_knowledge_base.py --stats   # Statistik")
    else:
        build_knowledge_base()
