"""
core/config.py
Konstanta path yang digunakan di seluruh aplikasi.
"""

import os

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(DATA_DIR, "database_kp.db")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
