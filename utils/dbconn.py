import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "vault.sqlite"


# ====================
# USER
# ====================
def fetch_user():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT salt, hash, encrypted_secret FROM user WHERE id = 1")
        return cursor.fetchone()

def setup_user(salt :bytes, hash: bytes, encrypted_secret: bytes = None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (id, salt, hash, encrypted_secret) VALUES (1, ?, ?, ?)", (salt, hash, encrypted_secret))


# ====================
# VAULT ENTRY
# ====================
def get_entries():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, ciphertext FROM vault")
        return cursor.fetchall()

def save_entry(title, ciphertext) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vault (title, ciphertext) 
                        VALUES (?, ?);
            """, (title, ciphertext))
            return True
        except:
            return False

def delete_entry(id) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vault WHERE id = ?", (id,))
            return True
        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            return False



# ====================
# 2FA
# ====================
def save_2fa(secret: bytes) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET encrypted_secret = ? WHERE id = 1", (secret,))
            return True
        except sqlite3.Error as e:
            print(f"DB Error saving 2FA: {e}")
            return False
        
def get_2fa():
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT encrypted_secret FROM user WHERE id = 1")
            result = cursor.fetchone()

            if result and result[0] is not None:
                return result[0]  
            return None
            
        except sqlite3.Error as e:
            print(f"DB Error fetching 2FA: {e}")
            return None
        
def delete_2fa() -> True:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET encrypted_secret = NULL WHERE id = 1")
            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False



def init_db():

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                salt BLOB NOT NULL,
                hash BLOB NOT NULL,
                encrypted_secret BLOB);
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                ciphertext BLOB NOT NULL);
        """)
