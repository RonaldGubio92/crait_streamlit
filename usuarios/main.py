 
import streamlit as st
from usuarios.creacion_usuarios.main import show_creacion_usuarios

def show_usuarios():
    st.title("👥 Gestión de Usuarios")
    opcion = st.selectbox("Opciones", ["Crear Usuario"])
    if opcion == "Crear Usuario":
        show_creacion_usuarios()
    if st.button("Volver al menú"):
        st.session_state.current_page = "menu"
