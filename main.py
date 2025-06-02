import os
from tkinter import messagebox, Tk
from res import TXT_IPS
from res.interface import AppGUI

def main():
    if not os.path.exists(TXT_IPS):
        with open(TXT_IPS, 'w') as f:
            pass
        messagebox.showinfo("Notice", f"{TXT_IPS} created. Add lines in the format: line_name,ip")
        return

    with open(TXT_IPS, 'r') as f:
        pairs = [tuple(map(str.strip, line.split(',', 1))) for line in f if line.strip() and ',' in line]

    root = Tk()
    app = AppGUI(root, pairs)
    root.mainloop()

if __name__ == "__main__":
    main()