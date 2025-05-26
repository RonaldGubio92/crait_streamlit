import streamlit as st
import os
from transportistas.db import registrar_consumo

def show_transportistas():
    st.title("🚚 Registro de Consumo de Combustible")
    st.write("Registra el consumo de combustible de los camiones.")

    opcion = st.radio("Opciones", ["Registrar consumo", "Consultar consumos"])
    if opcion == "Registrar consumo":
        with st.form("form_consumo_combustible"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre")
                apellido = st.text_input("Apellido")
                cedula = st.text_input("Cédula")
            with col2:
                placa = st.text_input("Placa del camión")
                valor = st.number_input("Valor (USD)", min_value=0.0, step=0.01, format="%.2f")
                foto_voucher = st.file_uploader("Foto del voucher", type=["jpg", "jpeg", "png", "pdf"])  # Permite imagen o PDF
            submitted = st.form_submit_button("Registrar consumo")

        if submitted:
            if not (nombre and apellido and cedula and placa and valor and foto_voucher):
                st.error("Todos los campos son obligatorios.")
            else:
                carpeta_destino = "transportistas/vouchers"
                os.makedirs(carpeta_destino, exist_ok=True)
                ruta_archivo = os.path.join(carpeta_destino, foto_voucher.name)
                with open(ruta_archivo, "wb") as f:
                    f.write(foto_voucher.read())
                registrar_consumo(nombre, apellido, cedula, placa, valor, ruta_archivo)
                st.success("Consumo registrado exitosamente.")
                if foto_voucher.type.startswith("image/"):
                    st.image(ruta_archivo, caption="Voucher", use_container_width=True)
                elif foto_voucher.type == "application/pdf":
                    st.info(f"Archivo PDF guardado: {ruta_archivo}")
        st.button("Volver al menú", on_click=lambda: st.session_state.update({"current_page": "menu"}))
    else:
        from transportistas.consulta_combustible import show_consulta_combustible
        show_consulta_combustible()
