"""
core/database.py
Semua fungsi yang berhubungan dengan SQLite:
- hash_password
- init_db
- verify_login_db
- register_user_db
- fetch_all_users_db
- update_user_db
- delete_user_db
"""

import sqlite3, hashlib, json, os
from core.config import DB_FILE, USERS_FILE
from core.data_manager import get_data_file


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if "role" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('admin', hash_password('admin123'), 'admin')
        )

    conn.commit()

    if os.path.exists(USERS_FILE):
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] <= 1:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                    for user, pwd in users.items():
                        if user != 'admin':
                            cursor.execute(
                                "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                                (user, hash_password(pwd), 'user')
                            )
                    conn.commit()
                    os.rename(USERS_FILE, USERS_FILE + ".bak")
                except Exception:
                    pass
    conn.close()


def verify_login_db(username: str, password: str):
    """Kembalikan (True, role) jika berhasil, atau (False, None)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True, row[1]
    return False, None


def register_user_db(username: str, password: str, role: str = 'user') -> bool:
    """Daftarkan user baru. Kembalikan True jika sukses, False jika username sudah ada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def fetch_all_users_db() -> list:
    """
    Kembalikan list tuple:
    (username, role, nama, nim, perusahaan, jml_kegiatan)
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    rows = cursor.fetchall()
    conn.close()

    detailed_rows = []
    for uname, role in rows:
        nama = "-"
        nim = "-"
        perusahaan = "-"
        jml_keg = 0
        file_path = get_data_file(uname)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    nama = data.get("profil", {}).get("nama", "-")
                    nim = data.get("profil", {}).get("nim", "-")
                    perusahaan = data.get("profil", {}).get("perusahaan", "-")
                    jml_keg = len(data.get("kegiatan", []))
            except Exception:
                pass
        detailed_rows.append((uname, role, nama, nim, perusahaan, jml_keg))
    return detailed_rows


def update_user_db(username: str, password: str, role: str):
    """Update password dan/atau role user. Jika password kosong, hanya role yang diupdate."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if password:
        cursor.execute(
            "UPDATE users SET password = ?, role = ? WHERE username = ?",
            (hash_password(password), role, username)
        )
    else:
        cursor.execute(
            "UPDATE users SET role = ? WHERE username = ?",
            (role, username)
        )
    conn.commit()
    conn.close()


def delete_user_db(username: str):
    """Hapus user dari database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
