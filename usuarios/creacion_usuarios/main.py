 
import streamlit as st
from database.conexion import get_connection

def show_creacion_usuarios():
    st.title("➕ Crear Usuario")

    usuario = st.text_input("Nombre de usuario")
    contrasena = st.text_input("Contraseña")
    rol = st.selectbox("Rol", ["superadmin", "admin", "user"])

    if st.button("Guardar"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (%s, %s, %s)",
                       (usuario, contrasena, rol))
        conn.commit()
        conn.close()
        st.success("Usuario creado correctamente.")
