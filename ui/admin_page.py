"""
ui/admin_page.py
AdminMixin — berisi UI dan logika untuk halaman admin (manajemen user).
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from core.database import (
    fetch_all_users_db, register_user_db, update_user_db, delete_user_db
)


class AdminMixin:

    def build_admin_dashboard_ui(self):
        sidebar = ctk.CTkFrame(self.admin_container, width=220, corner_radius=0, fg_color="#1a1a2e")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="👑 Admin Panel", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#e94560").pack(pady=(30, 5))
        ctk.CTkLabel(sidebar, text="Manajemen Sistem", font=ctk.CTkFont(size=12),
                     text_color="#888").pack(pady=(0, 30))

        btn = ctk.CTkButton(sidebar, text="👥  Manage Users", font=ctk.CTkFont(size=15), height=45,
                            fg_color="transparent", hover_color="#e94560", anchor="w")
        btn.pack(fill="x", padx=15, pady=4)

        ctk.CTkButton(sidebar, text="🚪 Logout", font=ctk.CTkFont(size=15), height=45,
                      fg_color="transparent", hover_color="#c0392b", anchor="w",
                      command=self.handle_logout).pack(side="bottom", fill="x", padx=15, pady=20)

        main = ctk.CTkFrame(self.admin_container, fg_color="#16213e", corner_radius=0)
        main.pack(side="right", fill="both", expand=True)

        page = ctk.CTkFrame(main, fg_color="transparent")
        page.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(page, text="Manajemen Pengguna (CRUD)",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")

        # Form CRUD Admin
        admin_form = ctk.CTkFrame(page, fg_color="#1a1a2e", corner_radius=12)
        admin_form.pack(fill="x", pady=10)

        row1 = ctk.CTkFrame(admin_form, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(12, 5))

        ctk.CTkLabel(row1, text="Username:").pack(side="left")
        self.admin_user_entry = ctk.CTkEntry(row1, width=150)
        self.admin_user_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row1, text="Password:").pack(side="left", padx=(10, 0))
        self.admin_pass_entry = ctk.CTkEntry(row1, width=150, show="*")
        self.admin_pass_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row1, text="Role:").pack(side="left", padx=(10, 0))
        self.admin_role_var = ctk.StringVar(value="user")
        ctk.CTkOptionMenu(row1, variable=self.admin_role_var, values=["user", "admin"],
                          width=100, fg_color="#e94560").pack(side="left", padx=5)

        btn_row = ctk.CTkFrame(admin_form, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(5, 12))

        self.admin_add_btn = ctk.CTkButton(btn_row, text="➕ Tambah Akun",
                                           fg_color="#e94560", hover_color="#c81e45",
                                           command=self.admin_add_user)
        self.admin_add_btn.pack(side="left", padx=(0, 8))

        ctk.CTkButton(btn_row, text="🗑️ Hapus Akun", fg_color="#c0392b", hover_color="#922b21",
                      command=self.admin_delete_user).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="🔄 Batal Edit", fg_color="#555", hover_color="#777",
                      command=self.admin_cancel_edit).pack(side="left")

        # Table
        table_frame = ctk.CTkFrame(page, fg_color="#1a1a2e", corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a1a2e", foreground="white",
                        fieldbackground="#1a1a2e", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#e94560", foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#e94560")])

        cols = ("no", "username", "role", "nama", "nim", "perusahaan", "jml")
        self.admin_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        for cid, txt, w in [("no", "No", 40), ("username", "Username", 120), ("role", "Role", 80),
                             ("nama", "Nama Lengkap", 150), ("nim", "NIM", 90),
                             ("perusahaan", "Perusahaan", 150), ("jml", "Jml Keg", 70)]:
            self.admin_tree.heading(cid, text=txt)
            self.admin_tree.column(cid, width=w, minwidth=50)

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.admin_tree.yview)
        self.admin_tree.configure(yscrollcommand=sb.set)
        self.admin_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", pady=10, padx=(0, 10))

        self.admin_tree.bind("<Double-1>", self.on_admin_double_click)

        self.admin_count_label = ctk.CTkLabel(page, text="", font=ctk.CTkFont(size=12),
                                              text_color="#888")
        self.admin_count_label.pack(anchor="w", pady=5)

    def on_admin_double_click(self, event):
        sel = self.admin_tree.selection()
        if not sel:
            return
        item = self.admin_tree.item(sel[0])
        uname = item['values'][1]
        role = item['values'][2]

        self.admin_editing_user = uname
        self.admin_add_btn.configure(text="✏️ Update Akun")
        self.admin_user_entry.delete(0, "end")
        self.admin_user_entry.insert(0, uname)
        self.admin_user_entry.configure(state="disabled")
        self.admin_pass_entry.delete(0, "end")
        self.admin_role_var.set(role)

    def admin_cancel_edit(self):
        self.admin_editing_user = None
        self.admin_add_btn.configure(text="➕ Tambah Akun")
        self.admin_user_entry.configure(state="normal")
        self.admin_user_entry.delete(0, "end")
        self.admin_pass_entry.delete(0, "end")
        self.admin_role_var.set("user")

    def admin_add_user(self):
        uname = self.admin_user_entry.get().strip().lower()
        pwd = self.admin_pass_entry.get()
        role = self.admin_role_var.get()

        if not uname:
            messagebox.showwarning("Peringatan", "Username tidak boleh kosong!")
            return

        if self.admin_editing_user:
            if self.admin_editing_user == self.current_user and role != 'admin':
                messagebox.showwarning("Peringatan",
                                       "Anda tidak bisa mengubah role Anda sendiri menjadi user!")
                return
            update_user_db(self.admin_editing_user, pwd, role)
            messagebox.showinfo("Sukses", f"Akun '{self.admin_editing_user}' berhasil diupdate!")
            self.admin_cancel_edit()
            self.refresh_admin_table()
        else:
            if not pwd:
                messagebox.showwarning("Peringatan", "Password tidak boleh kosong untuk akun baru!")
                return
            if register_user_db(uname, pwd, role):
                messagebox.showinfo("Sukses", f"Akun '{uname}' berhasil dibuat!")
                self.admin_cancel_edit()
                self.refresh_admin_table()
            else:
                messagebox.showwarning("Peringatan", "Username sudah terdaftar!")

    def refresh_admin_table(self):
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        users = fetch_all_users_db()
        for i, u in enumerate(users):
            self.admin_tree.insert("", "end", values=(i + 1, u[0], u[1], u[2], u[3], u[4], u[5]))
        self.admin_count_label.configure(text=f"Total: {len(users)} pengguna terdaftar")

    def admin_delete_user(self):
        sel = self.admin_tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih user yang ingin dihapus!")
            return
        item = self.admin_tree.item(sel[0])
        uname = item['values'][1]
        role = item['values'][2]

        if role == 'admin' and uname == self.current_user:
            messagebox.showwarning("Peringatan",
                                   "Anda tidak bisa menghapus akun Anda sendiri saat sedang login!")
            return

        if messagebox.askyesno("Konfirmasi",
                               f"Apakah Anda yakin ingin menghapus pengguna '{uname}'?\n"
                               f"Catatan: Data laporan mereka akan tetap tersimpan sebagai arsip."):
            delete_user_db(uname)
            self.admin_cancel_edit()
            self.refresh_admin_table()
            messagebox.showinfo("Sukses", f"Pengguna '{uname}' berhasil dihapus.")
