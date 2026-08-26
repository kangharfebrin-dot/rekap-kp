"""
ui/kegiatan_page.py
KegiatanMixin — berisi UI dan logika untuk halaman catatan kegiatan harian.
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class KegiatanMixin:

    def build_kegiatan_page(self):
        page = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pages["kegiatan"] = page

        ctk.CTkLabel(page, text="Catatan Kegiatan Harian",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")

        # Form input
        form = ctk.CTkFrame(page, fg_color="#1a1a2e", corner_radius=12)
        form.pack(fill="x", pady=10)

        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(12, 5))

        ctk.CTkLabel(row1, text="Tanggal:").pack(side="left")
        self.date_entry = DateEntry(row1, width=14, date_pattern="dd/mm/yyyy",
                                   background="#e94560", foreground="white")
        self.date_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(row1, text="Minggu ke:").pack(side="left")
        self.minggu_var = ctk.StringVar(value="1")
        ctk.CTkOptionMenu(row1, variable=self.minggu_var,
                          values=[str(i) for i in range(1, 25)],
                          width=80, fg_color="#e94560").pack(side="left", padx=5)

        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row2, text="Kegiatan:").pack(anchor="w")
        self.kegiatan_text = ctk.CTkTextbox(row2, height=60, fg_color="#16213e", corner_radius=8)
        self.kegiatan_text.pack(fill="x", pady=3)

        row3 = ctk.CTkFrame(form, fg_color="transparent")
        row3.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row3, text="Keterangan/Hasil:").pack(anchor="w")
        self.keterangan_text = ctk.CTkTextbox(row3, height=40, fg_color="#16213e", corner_radius=8)
        self.keterangan_text.pack(fill="x", pady=3)

        btn_row = ctk.CTkFrame(form, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(5, 12))

        self.add_btn = ctk.CTkButton(btn_row, text="➕ Tambah", fg_color="#e94560",
                                     hover_color="#c81e45", command=self.add_kegiatan)
        self.add_btn.pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="🗑️ Hapus Pilihan", fg_color="#c0392b",
                      hover_color="#922b21", command=self.delete_kegiatan).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="🔄 Batal Edit", fg_color="#555",
                      hover_color="#777", command=self.cancel_edit).pack(side="left")

        # Tabel kegiatan
        table_frame = ctk.CTkFrame(page, fg_color="#1a1a2e", corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a1a2e", foreground="white",
                        fieldbackground="#1a1a2e", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#e94560", foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#e94560")])

        cols = ("no", "tanggal", "minggu", "kegiatan", "keterangan")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        for cid, txt, w in [("no", "No", 40), ("tanggal", "Tanggal", 100),
                             ("minggu", "Minggu", 70), ("kegiatan", "Kegiatan", 350),
                             ("keterangan", "Keterangan", 250)]:
            self.tree.heading(cid, text=txt)
            self.tree.column(cid, width=w, minwidth=40)

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", pady=10, padx=(0, 10))

        self.tree.bind("<Double-1>", self.on_double_click)

        self.count_label = ctk.CTkLabel(page, text="", font=ctk.CTkFont(size=12), text_color="#888")
        self.count_label.pack(anchor="w")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.data and "kegiatan" in self.data:
            for i, k in enumerate(self.data["kegiatan"]):
                self.tree.insert("", "end", values=(
                    i + 1, k["tanggal"], f"Minggu {k['minggu']}",
                    k["kegiatan"], k["keterangan"]
                ))
        self.update_count()

    def update_count(self):
        if hasattr(self, "count_label") and self.data and "kegiatan" in self.data:
            self.count_label.configure(text=f"Total: {len(self.data['kegiatan'])} kegiatan tercatat")

    def add_kegiatan(self):
        tanggal = self.date_entry.get()
        minggu = self.minggu_var.get()
        kegiatan = self.kegiatan_text.get("1.0", "end").strip()
        keterangan = self.keterangan_text.get("1.0", "end").strip()

        if not kegiatan:
            messagebox.showwarning("Peringatan", "Kegiatan tidak boleh kosong!")
            return

        entry = {"tanggal": tanggal, "minggu": minggu,
                 "kegiatan": kegiatan, "keterangan": keterangan}

        if self.editing_idx is not None:
            self.data["kegiatan"][self.editing_idx] = entry
            self.editing_idx = None
            self.add_btn.configure(text="➕ Tambah")
        else:
            self.data["kegiatan"].append(entry)

        self.save_current_data()
        self.clear_form()
        self.refresh_table()

    def delete_kegiatan(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih kegiatan yang ingin dihapus!")
            return
        idx = self.tree.index(sel[0])
        if messagebox.askyesno("Konfirmasi", "Hapus kegiatan ini?"):
            self.data["kegiatan"].pop(idx)
            self.save_current_data()
            self.cancel_edit()
            self.refresh_table()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        k = self.data["kegiatan"][idx]
        self.editing_idx = idx
        self.add_btn.configure(text="✏️ Update")

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, k["tanggal"])
        self.minggu_var.set(k["minggu"])
        self.kegiatan_text.delete("1.0", "end")
        self.kegiatan_text.insert("1.0", k["kegiatan"])
        self.keterangan_text.delete("1.0", "end")
        self.keterangan_text.insert("1.0", k["keterangan"])

    def cancel_edit(self):
        self.editing_idx = None
        self.add_btn.configure(text="➕ Tambah")
        self.clear_form()

    def clear_form(self):
        self.kegiatan_text.delete("1.0", "end")
        self.keterangan_text.delete("1.0", "end")
