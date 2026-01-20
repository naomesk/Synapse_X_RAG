import sqlite3 as sq3

sq3.connect("rag_rdb.db")
conn = sq3.connect("rag_rdb.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS documents ( 
               document_id TEXT PRIMARY KEY, 
               filename TEXT, 
               content_type TEXT, 
               created_at datetime);""") 

cursor.execute("""CREATE TABLE IF NOT EXISTS chunks (
               chunk_id TEXT PRIMARY KEY,
               document_id TEXT,
               content TEXT,
               position INTEGER,
               FOREIGN KEY(document_id) REFERENCES documents(document_id));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS metadata (
               chunk_id TEXT PRIMARY KEY,
               metadata_key TEXT,
               metadata_value TEXT,
               FOREIGN KEY(chunk_id) REFERENCES chunks(chunk_id));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS embeddings (
               embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
               chunk_id TEXT, 
               embedding_data BLOB,
               FOREIGN KEY(chunk_id) REFERENCES chunks(chunk_id));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS query_logs (
                query_id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT,
                timestamp datetime,
                execution_time REAL);""")

conn.commit()
conn.close()


