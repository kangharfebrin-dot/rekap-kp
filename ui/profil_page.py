"""
ui/profil_page.py
ProfilMixin — berisi UI dan logika untuk halaman profil mahasiswa.
"""

import customtkinter as ctk
from tkinter import messagebox


class ProfilMixin:

    def build_profil_page(self):
        page = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.pages["profil"] = page

        ctk.CTkLabel(page, text="Data Profil Kerja Praktek",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 15))

        self.profil_entries = {}
        sections = [
            ("Data Mahasiswa", [
                ("Nama Lengkap", "nama"), ("NIM", "nim"), ("Program Studi", "prodi"),
                ("Fakultas", "fakultas"), ("Universitas", "universitas")
            ]),
            ("Data Perusahaan/Instansi", [
                ("Nama Perusahaan", "perusahaan"), ("Alamat", "alamat_perusahaan"),
                ("Periode Mulai (dd/mm/yyyy)", "periode_mulai"),
                ("Periode Selesai (dd/mm/yyyy)", "periode_selesai")
            ]),
            ("Data Pembimbing", [
                ("Dosen Pembimbing", "dosen_pembimbing"),
                ("Pembimbing Lapangan", "pembimbing_lapangan")
            ])
        ]

        for sec_title, fields in sections:
            f = ctk.CTkFrame(page, fg_color="#1a1a2e", corner_radius=12)
            f.pack(fill="x", pady=8)
            ctk.CTkLabel(f, text=sec_title, font=ctk.CTkFont(size=15, weight="bold"),
                         text_color="#e94560").pack(anchor="w", padx=15, pady=(12, 5))
            for label, key in fields:
                row = ctk.CTkFrame(f, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=3)
                ctk.CTkLabel(row, text=label, width=220, anchor="w").pack(side="left")
                e = ctk.CTkEntry(row, width=400, placeholder_text=f"Masukkan {label.lower()}")
                e.pack(side="left", padx=(10, 0))
                self.profil_entries[key] = e

        ctk.CTkButton(page, text="💾  Simpan Profil", font=ctk.CTkFont(size=14, weight="bold"),
                      height=42, fg_color="#e94560", hover_color="#c81e45",
                      command=self.save_profil).pack(pady=15)

    def save_profil(self):
        for key, entry in self.profil_entries.items():
            self.data["profil"][key] = entry.get().strip()
        self.save_current_data()
        messagebox.showinfo("Sukses", "Profil berhasil disimpan!")
