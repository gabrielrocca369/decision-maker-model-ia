# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import json
import xml.etree.ElementTree as ET
import logging
import sqlite3  # Exemplo para conexão com SQLite
# Importar outros conectores de banco de dados conforme necessário

def import_file():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        if not file_path:
            print("Nenhum arquivo selecionado.")
            return None

        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path, encoding='utf-8')
        elif file_path.endswith('.xml'):
            df = parse_xml(file_path)
        else:
            raise ValueError("Formato de arquivo nao suportado. Suporta .csv, .xlsx, .json, .xml.")

        return df
    except Exception as e:
        logging.error(f"Erro ao importar arquivo: {e}")
        print(f"Erro ao importar arquivo: {e}")
        return None

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        all_records = []

        # Supondo que cada filho de root seja um registro
        for elem in root:
            record = {}
            for subelem in elem:
                record[subelem.tag] = subelem.text
            all_records.append(record)

        df = pd.DataFrame(all_records)
        return df
    except Exception as e:
        logging.error(f"Erro ao analisar arquivo XML: {e}")
        print(f"Erro ao analisar arquivo XML: {e}")
        return None

def import_from_database(db_type, connection_params, query):
    try:
        if db_type == 'sqlite':
            conn = sqlite3.connect(connection_params['database'])
        # Adicionar suporte para outros bancos de dados, como PostgreSQL ou MySQL
        else:
            raise ValueError("Tipo de banco de dados nao suportado.")

        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
