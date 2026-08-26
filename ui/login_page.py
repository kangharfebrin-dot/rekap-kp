"""
ui/login_page.py
LoginMixin — berisi UI dan logika untuk halaman login/register.
"""

import customtkinter as ctk
from tkinter import messagebox
from core.database import verify_login_db, register_user_db


class LoginMixin:

    def build_login_ui(self):
        frame = ctk.CTkFrame(self.login_container, width=400, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Login Akun", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))

        self.user_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Username")
        self.user_entry.pack(pady=10, padx=40)

        self.pass_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10, padx=40)

        ctk.CTkButton(frame, text="Login", width=250, font=ctk.CTkFont(weight="bold"),
                      command=self.handle_login).pack(pady=(20, 10))

        ctk.CTkButton(frame, text="Register Baru", width=250, fg_color="transparent",
                      border_width=1, command=self.handle_register).pack(pady=(0, 30))

    def handle_login(self):
        username = self.user_entry.get().strip().lower()
        password = self.pass_entry.get()
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return

        success, role = verify_login_db(username, password)
        if success:
            self.current_user = username
            self.user_entry.delete(0, "end")
            self.pass_entry.delete(0, "end")
            if role == 'admin':
                self.show_admin_page()
            else:
                self.show_dashboard_page()
        else:
            messagebox.showerror("Error", "Username atau Password salah!")

    def handle_register(self):
        username = self.user_entry.get().strip().lower()
        password = self.pass_entry.get()
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return
        if register_user_db(username, password):
            messagebox.showinfo("Sukses", "Akun berhasil dibuat! Silakan login.")
        else:
            messagebox.showwarning("Peringatan", "Username sudah terdaftar!")

    def handle_logout(self):
        self.current_user = None
        self.data = None
        self.show_login_page()
