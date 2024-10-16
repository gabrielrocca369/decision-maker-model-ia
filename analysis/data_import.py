import tkinter as tk
from tkinter import filedialog
import logging

def import_file():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path
    except Exception as e:
        logging.error(f"Erro ao importar arquivo: {e}")
        print("Erro ao importar arquivo. Verifique o log para mais detalhes.")
        return None
