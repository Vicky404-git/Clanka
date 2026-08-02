import os
import json
import sqlite3
import sqlite_vss
import ollama
from pathlib import Path

# ==========================================
# CLANKA RAG ENGINE v2.1 (SQLite-VSS)
# ==========================================

EMBED_MODEL = "nomic-embed-text"
DB_PATH = "memory/clanka.db"
IGNORE_DIRS = {'.git', '.venv', '__pycache__', 'build', 'clanka.egg-info', 'node_modules', 'memory'}

def get_embedding(text):
    """Pings local Ollama to turn text into a 768-dimensional math vector."""
    try:
        response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"[!] Embedding failed: {e}")
        return None

def get_db():
    """Connects to SQLite and loads the C-level Vector Search extension."""
    # Ensure memory dir exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vss.load(db)
    db.row_factory = sqlite3.Row
    return db

def init_db(db):
    """Creates the standard table for text and the virtual table for math."""
    # Table 1: The actual code/text
    db.execute('''
        CREATE TABLE IF NOT EXISTS chunks (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            content TEXT
        )
    ''')
    # Table 2: The virtual vector index (768 dimensions for nomic-embed-text)
    db.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS vss_chunks USING vss0(
            vector(768)
        )
    ''')
    db.commit()

def build_index(directory="."):
    """Scans files, chunks them, and stores them in SQLite."""
    print(f"[*] Clanka is building SQLite index for '{directory}'...")
    
    db = get_db()
    
    # Nuke the old index if it exists so we don't duplicate
    db.execute("DROP TABLE IF EXISTS chunks")
    db.execute("DROP TABLE IF EXISTS vss_chunks")
    init_db(db)
    
    chunk_count = 0
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        for file in files:
            if not file.endswith(('.py', '.md', '.txt', '.sh', '.toml')):
                continue
                
            filepath = Path(root) / file
            try:
                content = filepath.read_text(errors='ignore')
                chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 40]
                
                for chunk in chunks:
                    vec = get_embedding(chunk)
                    if vec:
                        # 1. Insert the text
                        cursor = db.execute(
                            "INSERT INTO chunks (file_path, content) VALUES (?, ?)", 
                            (str(filepath), chunk)
                        )
                        # 2. Insert the vector linked by rowid
                        db.execute(
                            "INSERT INTO vss_chunks (rowid, vector) VALUES (?, ?)", 
                            (cursor.lastrowid, json.dumps(vec))
                        )
                        chunk_count += 1
                        
            except Exception as e:
                print(f"[dim]Skipped {filepath}: {e}[/dim]")

    db.commit()
    db.close()
    
    # Delete the old JSON bloat if it's still there
    old_json = Path("memory/clanka_memory.json")
    if old_json.exists():
        old_json.unlink()
        
    print(f"[+] Indexing complete. Saved {chunk_count} chunks to SQLite ({DB_PATH}).")

def search(query, top_k=3):
    """Uses SQLite native vector search to find relevant code."""
    if not os.path.exists(DB_PATH):
        print("[!] DB empty. Run 'uv run python core/rag.py index' first.")
        return []

    query_vec = get_embedding(query)
    if not query_vec: return []

    db = get_db()
    
    # The magic SQL query that does the math at C-level speed
    cursor = db.execute("""
        SELECT chunks.file_path, chunks.content, vss_chunks.distance
        FROM vss_chunks
        INNER JOIN chunks ON vss_chunks.rowid = chunks.rowid
        WHERE vss_search(vss_chunks.vector, ?)
        LIMIT ?
    """, (json.dumps(query_vec), top_k))
    
    results = []
    for row in cursor.fetchall():
        results.append((
            row['distance'], 
            {"file": row['file_path'], "content": row['content']}
        ))
        
    db.close()
    return results

# ==========================================
# STANDALONE TESTING
# ==========================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "index":
        build_index()
    elif len(sys.argv) > 2 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:])
        print(f"[*] Searching SQLite for: '{query}'")
        results = search(query)
        for score, doc in results:
            print(f"\n[Distance: {score:.4f}] File: {doc['file']}")
            print(f"Content: {doc['content'][:200]}...")
