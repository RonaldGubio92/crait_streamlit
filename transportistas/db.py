import pymssql
import os
from datetime import datetime
import streamlit as st


"""
def get_connection():
    return pymssql.connect(
        server='SQL5105.site4now.net',
        user='db_a56ecc_enedb_admin',
        password='enedPassword524152',
        database='db_a56ecc_enedb'
    )
"""

def get_connection():
    try:
        secrets = st.secrets["database"]
    except AttributeError:
        # Fallback para ejecución directa (no con streamlit run)
        import toml
        secrets = toml.load(os.path.join(os.path.dirname(__file__), "..", "..", "secrets.toml"))["database"]
    return pymssql.connect(
        server=secrets["server"],
        user=secrets["user"],
        password=secrets["password"],
        database=secrets["database"]
    )



def registrar_consumo(nombre, apellido, cedula, placa, valor, foto_voucher_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ConsumoCombustible (nombre, apellido, cedula, placa, valor, foto_voucher)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nombre, apellido, cedula, placa, valor, foto_voucher_path))
    conn.commit()
    conn.close()
