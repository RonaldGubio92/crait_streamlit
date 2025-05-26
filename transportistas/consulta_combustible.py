import streamlit as st
import pandas as pd
import pymssql
from datetime import datetime
import os
import base64


"""def get_connection():
    return pymssql.connect(
        server='SQL5105.site4now.net',
        user='db_a56ecc_enedb_admin',
        password='enedPassword524152',
        database='db_a56ecc_enedb'
    )
"""

def get_connection():
    return pymssql.connect(
        server='SQL5105.site4now.net',
        user='db_a56ecc_enedb_admin',
        password='enedPassword524152',
        database='db_a56ecc_enedb'
    )



def consultar_consumos(fecha_inicio=None, fecha_fin=None, placa=None, empleado=None):
    conn = get_connection()
    cursor = conn.cursor(as_dict=True)
    query = "SELECT * FROM ConsumoCombustible WHERE 1=1"
    params = []
    if fecha_inicio:
        query += " AND fecha >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND fecha <= %s"
        params.append(fecha_fin)
    if placa:
        query += " AND placa = %s"
        params.append(placa)
    if empleado:
        query += " AND (nombre LIKE %s OR apellido LIKE %s)"
        params.extend([f"%{empleado}%", f"%{empleado}%"])
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def show_consulta_combustible():
    st.title("🔎 Consulta de Consumo de Combustible")
    st.write("Filtra los registros por fecha, placa o empleado.")

    col1, col2, col3 = st.columns(3)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio", value=None, key="fecha_inicio")
    with col2:
        fecha_fin = st.date_input("Fecha fin", value=None, key="fecha_fin")
    with col3:
        placa = st.text_input("Placa del camión (opcional)")
    empleado = st.text_input("Nombre o apellido del empleado (opcional)")

    if st.button("Buscar"):
        fi = datetime.combine(fecha_inicio, datetime.min.time()) if fecha_inicio else None
        ff = datetime.combine(fecha_fin, datetime.max.time()) if fecha_fin else None
        data = consultar_consumos(fi, ff, placa.strip() or None, empleado.strip() or None)
        if data:
            df = pd.DataFrame(data)
            # Mostrar suma total del valor
            if 'valor' in df.columns:
                st.success(f"Suma total del valor: ${df['valor'].sum():,.2f}")
            # Crear columna de enlace de descarga (HTML) en vez de botón interactivo
            def make_download_link(row):
                file_path = row['foto_voucher']
                file_name = os.path.basename(file_path)
                try:
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                        b64 = base64.b64encode(file_bytes).decode()
                    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        mime = 'image/png' if file_name.lower().endswith('.png') else 'image/jpeg'
                    elif file_name.lower().endswith('.pdf'):
                        mime = 'application/pdf'
                    else:
                        mime = 'application/octet-stream'
                    href = f'<a href="data:{mime};base64,{b64}" download="{file_name}">Descargar voucher</a>'
                    return href
                except Exception as e:
                    return f"<span style='color:red'>No disponible</span>"
            df_viz = df.drop(columns=['foto_voucher']) if 'foto_voucher' in df.columns else df.copy()
            df_viz['Descargar voucher'] = df.apply(make_download_link, axis=1)
            st.write(df_viz.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No se encontraron registros con los filtros seleccionados.")
    st.button("Volver al menú", on_click=lambda: st.session_state.update({"current_page": "menu"}))
