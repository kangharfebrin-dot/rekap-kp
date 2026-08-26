"""
core/data_manager.py
Fungsi untuk membaca dan menyimpan data JSON per-user.
"""

import json, os
from core.config import DATA_DIR


def get_data_file(username: str) -> str:
    """Kembalikan path file JSON untuk user tertentu."""
    return os.path.join(DATA_DIR, f"data_kp_{username}.json")


def load_data(username: str) -> dict:
    """Muat data dari file JSON user. Kembalikan struktur default jika belum ada."""
    file_path = get_data_file(username)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "profil": {
            "nama": "", "nim": "", "prodi": "", "fakultas": "", "universitas": "",
            "perusahaan": "", "alamat_perusahaan": "", "periode_mulai": "",
            "periode_selesai": "", "dosen_pembimbing": "", "pembimbing_lapangan": ""
        },
        "kegiatan": []
    }


def save_data(username: str, data: dict):
    """Simpan data ke file JSON user."""
    file_path = get_data_file(username)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
