import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from . import ASSETS_DIR, TXT_IPS
from .scraping import fetch_table_names, download_table
import logging

class AppGUI:
    def __init__(self, root, pairs):
        self.root = root
        self.root.title("Watch Table Reader - A.A.P. - v1.0.1")
        self.pairs = pairs
        self.widgets = []

        self.ICON_DOWNLOAD = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, 'download_icon.png')).resize((20, 20)))
        self.ICON_DELETE = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, 'delete_icon.png')).resize((20, 20)))

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Headers
        tk.Label(self.scroll_frame, text="Line", width=20, font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(self.scroll_frame, text="IP", width=20, font=("Arial", 10, "bold")).grid(row=0, column=1)

        for i, (line, ip) in enumerate(self.pairs, start=1):
            self.add_row(i, line, ip)

        tk.Button(self.root, text="Add IP", command=self.add_new_ip).pack(pady=10)

    def add_row(self, idx, line, ip):
        lbl_line = tk.Label(self.scroll_frame, text=line, width=20)
        lbl_ip = tk.Label(self.scroll_frame, text=ip, width=20)

        btn_frame = tk.Frame(self.scroll_frame)
        btn_download = tk.Button(btn_frame, image=self.ICON_DOWNLOAD,
                                 command=lambda l=line, i=ip: self.download_tables(l, i))
        btn_delete = tk.Button(btn_frame, image=self.ICON_DELETE,
                               command=lambda: self.delete_row(line, ip, [lbl_line, lbl_ip, btn_frame]))

        btn_download.pack(side=tk.LEFT)
        btn_delete.pack(side=tk.LEFT)

        lbl_line.grid(row=idx, column=0)
        lbl_ip.grid(row=idx, column=1)
        btn_frame.grid(row=idx, column=2)

    def download_tables(self, line, ip):
        try:
            tables = fetch_table_names(ip)
            if not tables:
                messagebox.showinfo("No Tables", "No observation tables found.")
                return

            win = tk.Toplevel(self.root)
            win.title(f"Select Tables for {line} - {ip}")

            tk.Label(win, text="Select tables to download:", font=("Arial", 10, "bold")).pack(pady=5)

            var_dict = {}
            for name in tables:
                var = tk.BooleanVar()
                cb = tk.Checkbutton(win, text=name, variable=var)
                cb.pack(anchor='w')
                var_dict[name] = var

            def download_selected():
                selected = [name for name, var in var_dict.items() if var.get()]
                if not selected:
                    messagebox.showwarning("No Selection", "Please select at least one table.")
                    return
                success = []
                for name in selected:
                    try:
                        filename = download_table(ip, name, tables[name], line)
                        if filename:
                            success.append(filename)
                    except Exception as e:
                        logging.exception(f"Failed to download table {name} from {ip}")
                        messagebox.showerror("Error", f"Error downloading {name}: {e}")
                if success:
                    messagebox.showinfo("Success", f"Downloaded:\n" + "\n".join(success))
                win.destroy()

            tk.Button(win, text="Download", command=download_selected).pack(pady=10)

        except Exception as e:
            logging.exception("Error fetching table names")
            messagebox.showerror("Error", str(e))

    def delete_row(self, line, ip, widgets):
        if not messagebox.askyesno("Confirm", f"Delete {line},{ip}?"):
            return
        try:
            with open(TXT_IPS, 'r') as f:
                lines = f.readlines()
            with open(TXT_IPS, 'w') as f:
                for l in lines:
                    if l.strip() != f"{line},{ip}":
                        f.write(l.rstrip('\n') + '\n')
            for w in widgets:
                w.destroy()
        except Exception as e:
            logging.exception("Failed to delete row")
            messagebox.showerror("Error", str(e))

    def add_new_ip(self):
        def save():
            line = entry_line.get().strip()
            ip = entry_ip.get().strip()
            if not line or not ip:
                messagebox.showwarning("Missing Fields", "Line and IP required.")
                return
            with open(TXT_IPS, 'a') as f:
                f.write(f"{line},{ip}\n")
            self.pairs.append((line, ip))
            self.add_row(len(self.pairs), line, ip)
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Add IP")

        tk.Label(win, text="Line Name:").grid(row=0, column=0)
        entry_line = tk.Entry(win, width=30)
        entry_line.grid(row=0, column=1)

        tk.Label(win, text="IP Address:").grid(row=1, column=0)
        entry_ip = tk.Entry(win, width=30)
        entry_ip.grid(row=1, column=1)

        tk.Button(win, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)