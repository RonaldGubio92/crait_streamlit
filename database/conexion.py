import pymssql
import secrets as st

def get_connection():
    return pymssql.connect(
        server=st.secrets["database"]["server"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"]
    )

def verificar_usuario(nombre_usuario, contrasena):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol FROM usuarios WHERE usuario=%s AND estado = 'activo'", (nombre_usuario,))
        row = cursor.fetchone()
        conn.close()

        if row:
            contrasena_db, rol = row
            if contrasena == contrasena_db:
                return rol
        return None
    except Exception as e:
        print("Error:", e)
        return None
