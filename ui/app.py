"""
ui/app.py
Class App utama — menggabungkan semua Mixin dan mengelola navigasi antar halaman.
"""

import customtkinter as ctk
from core.database import init_db
from core.data_manager import load_data, save_data

from ui.login_page import LoginMixin
from ui.admin_page import AdminMixin
from ui.profil_page import ProfilMixin
from ui.kegiatan_page import KegiatanMixin
from ui.export_page import ExportMixin


class App(LoginMixin, AdminMixin, ProfilMixin, KegiatanMixin, ExportMixin, ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("📋 Rekap Kegiatan Kerja Praktek")
        self.geometry("1100x700")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State aplikasi
        self.current_user = None
        self.data = None
        self.editing_idx = None
        self.admin_editing_user = None

        init_db()

        # Container utama untuk setiap "halaman" top-level
        self.login_container = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_container = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_container = ctk.CTkFrame(self, fg_color="transparent")

        # Bangun semua UI (tapi hanya login yang ditampilkan)
        self.build_login_ui()
        self.build_dashboard_ui()
        self.build_admin_dashboard_ui()

        self.show_login_page()

    # ── Navigasi antar halaman ──────────────────────────────────────────────

    def show_login_page(self):
        self.dashboard_container.pack_forget()
        self.admin_container.pack_forget()
        self.login_container.pack(fill="both", expand=True)

    def show_dashboard_page(self):
        self.login_container.pack_forget()
        self.admin_container.pack_forget()
        self.dashboard_container.pack(fill="both", expand=True)
        self.data = load_data(self.current_user)
        self.refresh_ui_with_data()
        self.show_page("kegiatan")

    def show_admin_page(self):
        self.login_container.pack_forget()
        self.dashboard_container.pack_forget()
        self.admin_container.pack(fill="both", expand=True)
        self.refresh_admin_table()

    # ── Dashboard user biasa ────────────────────────────────────────────────

    def build_dashboard_ui(self):
        sidebar = ctk.CTkFrame(self.dashboard_container, width=220,
                               corner_radius=0, fg_color="#1a1a2e")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="📋 Rekap KP",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#e94560").pack(pady=(30, 5))
        ctk.CTkLabel(sidebar, text="Kerja Praktek Logger",
                     font=ctk.CTkFont(size=12),
                     text_color="#888").pack(pady=(0, 30))

        self.main_frame = ctk.CTkFrame(self.dashboard_container,
                                       fg_color="#16213e", corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.pages = {}
        btn_data = [("👤  Profil", "profil"), ("📝  Kegiatan", "kegiatan"), ("📤  Export", "export")]
        for text, name in btn_data:
            btn = ctk.CTkButton(sidebar, text=text, font=ctk.CTkFont(size=15), height=45,
                                fg_color="transparent", hover_color="#e94560", anchor="w",
                                command=lambda n=name: self.show_page(n))
            btn.pack(fill="x", padx=15, pady=4)

        ctk.CTkButton(sidebar, text="🚪 Logout", font=ctk.CTkFont(size=15), height=45,
                      fg_color="transparent", hover_color="#c0392b", anchor="w",
                      command=self.handle_logout).pack(side="bottom", fill="x", padx=15, pady=20)

        # Bangun sub-halaman
        self.build_profil_page()
        self.build_kegiatan_page()
        self.build_export_page()

    def refresh_ui_with_data(self):
        """Sinkronisasi semua widget dengan data yang sudah dimuat."""
        for key, entry in self.profil_entries.items():
            entry.delete(0, "end")
            entry.insert(0, self.data["profil"].get(key, ""))
        self.refresh_table()

    def show_page(self, name: str):
        """Tampilkan sub-halaman dashboard tertentu."""
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill="both", expand=True, padx=20, pady=20)

    def save_current_data(self):
        """Simpan data user yang sedang login."""
        if self.current_user and self.data:
            save_data(self.current_user, self.data)
