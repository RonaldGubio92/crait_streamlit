import streamlit as st
from soporte_tecnico.ticket import create_ticket
from soporte_tecnico.dashboard import mostrar_dashboard
from soporte_tecnico.usuarios import gestionar_usuarios
from soporte_tecnico.db import get_admin_email
from soporte_tecnico.estadisticas import mostrar_dashboard_estadistico

def show_soporte_tecnico(user):
    st.title("🛠 Soporte Técnico")
    st.write("Gestión de soporte técnico.")

    # Menú lateral dinámico y permisos según rol
    if user['rol'] == 'admin':
        opcion = st.sidebar.radio("Opciones", [
            "Crear Ticket", "Ver Tickets", "Gestionar Usuarios", "Dashboard Estadístico", "Volver al menú"
        ])
    else:
        opcion = st.sidebar.radio("Opciones", [
            "Crear Ticket", "Ver Tickets", "Volver al menú"
        ])

    # Crear ticket
    if opcion == "Crear Ticket":
        st.subheader("🆕 Crear nuevo ticket")
        st.info(f"Ticket creado por: {user['nombre']} ({user['rol']}, {user.get('departamento', 'Sin departamento')})")
        titulo = st.text_input("Título del ticket")
        descripcion = st.text_area("Descripción del problema")
        if st.button("Crear Ticket"):
            if titulo and descripcion:
                ticket_id = create_ticket(
                    titulo, descripcion,
                    user['id'], user['email'], get_admin_email()
                )
                if ticket_id:
                    st.success(f"✅ Ticket #{ticket_id} creado exitosamente")
                else:
                    st.error("❌ Error al crear el ticket")
            else:
                st.warning("⚠️ Todos los campos son obligatorios")

    # Ver dashboard de tickets
    elif opcion == "Ver Tickets":
        mostrar_dashboard(user)

    # Gestión de usuarios (solo admin)
    elif opcion == "Gestionar Usuarios":
        gestionar_usuarios()

    # Gestión de estadísticas (solo admin)
    elif opcion == "Dashboard Estadístico":
        mostrar_dashboard_estadistico()

    # Volver al menú
    elif opcion == "Volver al menú":
        st.session_state.current_page = "menu"
       # st.session_state['usuario'] = None
        st.rerun()
    #if st.button("Volver al menú"):
         #   st.session_state.current_page = "menu"
