 
import streamlit as st

def show_vacaciones():
    st.title("🌴 Vacaciones")
    st.write("Solicitudes y gestión de vacaciones.")
    st.button("Volver al menú", on_click=lambda: st.session_state.update({"current_page": "menu"}))
