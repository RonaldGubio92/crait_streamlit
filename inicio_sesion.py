import streamlit as st
from database.conexion import verificar_usuario
from usuarios.main import show_usuarios
from transportistas.main import show_transportistas
from soporte_tecnico.main import show_soporte_tecnico
from vacaciones.main import show_vacaciones
import os
import base64


def base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
#logotipo de la marca 
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64_image(logo_path)}" width="150">
        </div>
    """, unsafe_allow_html=True)

# Diccionario de roles y accesos
menu_roles = {
    "admin": ["Usuarios", "Transportistas", "Soporte Técnico", "Vacaciones"],
    "tecnico": ["Transportistas", "Vacaciones"],
    "administrativo": ["Soporte Técnico"]
}





# Iconos para módulos
icons = {
    "Usuarios": "👥",
    "Transportistas": "🚚",
    "Soporte Técnico": "🛠️",
    "Vacaciones": "🌴"
}

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None
    #st.session_state.nombre = None
    st.session_state.rol = None
    st.session_state.current_page = "login"

# Función de login
def login():
    st.title("🔐 Inicio de Sesión")

    with st.form(key="login_form"):
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")

        if submitted:
            user = None
            # Buscar usuario y datos completos
            from soporte_tecnico.db import get_user
            user = get_user(usuario, contrasena)
            if user:
                st.session_state.logged_in = True
                st.session_state.usuario = user
                st.session_state.rol = user['rol']
                st.session_state.current_page = "menu"
                st.rerun()  # fuerza recarga para actualizar estado y mostrar menú
            else:
                st.error("❌ Credenciales incorrectas")

# Menú estilo iPad en 2 columnas con botones Streamlit
def menu():
    st.markdown("""
        <style>
            .card-button {
                width: 220px;
                height: 220px;
                margin: 0 auto 40px auto;
                border-radius: 20px;
                background-color: #ffffff;
                box-shadow: 0 6px 18px rgba(0,0,0,0.12);
                cursor: pointer;
                border: 2.5px solid transparent;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: #333;
                font-weight: 600;
                font-size: 22px;
                user-select: none;
                position: relative;
            }
            .card-button:hover {
                background-color: #f0f4ff;
                border-color: #1f77ff;
            }
            .card-button .icon {
                font-size: 80px;
                margin-bottom: 12px;
                width: 100%;
                text-align: center;
                line-height: 1;
            }
            .card-button div:last-child {
                width: 100%;
                text-align: center;
            }
            /* Ocultar botón real */
            button[title^="Ir a"] {
                position: absolute !important;
                opacity: 0 !important;
                height: 0 !important;
                pointer-events: none !important;
            }
        </style>
    """, unsafe_allow_html=True)




    nombre_usuario = st.session_state.usuario['nombre'] if isinstance(st.session_state.usuario, dict) else st.session_state.usuario
    st.markdown(f"<h2 style='text-align:center;'>Bienvenido, {nombre_usuario.title()} ({st.session_state.rol})</h2>", unsafe_allow_html=True)

    modulos = menu_roles.get(st.session_state.rol, [])
    cols = st.columns(2)

    for i, modulo in enumerate(modulos):
        with cols[i % 2]:
            # Crear tarjeta HTML que lanza el botón invisible
            html_card = f"""
                <div class="card-button" onclick="document.getElementById('btn-{modulo}').click();">
                    <div class="icon">{icons.get(modulo, '📁')}</div>
                    <div>{modulo}</div>
                </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)

            # Botón invisible real (necesario para cambiar de página)
            st.button("Pulsa aquí para ingresar ", key=f"btn-{modulo}", help=f"Ir a {modulo}", use_container_width=True)

            # Acción si el botón fue pulsado
            if st.session_state.get(f"btn-{modulo}"):
                st.session_state.current_page = modulo
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔒 Cerrar sesión"):
        st.session_state.update({
            "logged_in": False,
            "usuario": None,
            "rol": None,
            "current_page": "login"
        })
        st.rerun()



# Navegación principal
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.current_page == "menu":
        menu()
    elif st.session_state.current_page == "Usuarios":
        show_usuarios()
    elif st.session_state.current_page == "Transportistas":
        show_transportistas()
    elif st.session_state.current_page == "Soporte Técnico":
        # Obtener el usuario logueado correctamente
        user = st.session_state.get('usuario')
        if user and isinstance(user, dict):
            show_soporte_tecnico(user)
        else:
            st.error("No hay información de usuario válida para soporte técnico.")
    elif st.session_state.current_page == "Vacaciones":
        show_vacaciones()
