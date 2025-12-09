import sqlite3
import os
import sys

# La base de datos debe estar en la raíz del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(project_root, 'agenda.db')

# Función de conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- FUNCIONES CORE CRUD (4 Campos: id, nombre, telefono, email) ---

def crear_tabla():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Intentar crear la nueva tabla con 4 campos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT
        )
    """)

    # 2. Verificar si la tabla 'contactos' (la antigua con 'notas') existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contactos'")
    if cursor.fetchone():
        try:
            # 3. Copiar datos relevantes de la tabla antigua a la nueva
            # Si la tabla 'contactos' aún tiene la columna 'notas' y la nueva no,
            # solo copiamos las columnas que coinciden (id, nombre, telefono, email).
            cursor.execute("INSERT INTO contactos_new (id, nombre, telefono, email) SELECT id, nombre, telefono, email FROM contactos")
            
            # 4. Eliminar la tabla antigua para limpiarla
            cursor.execute("DROP TABLE contactos")
            
        except sqlite3.OperationalError as e:
            # Esto puede ocurrir si ya eliminamos la columna 'notas' manualmente o si la tabla antigua no existía como esperábamos
            print(f"Advertencia durante la migración de tabla: {e}")

    # 5. Renombrar la tabla nueva (y correcta) a 'contactos'
    cursor.execute("ALTER TABLE contactos_new RENAME TO contactos")
    
    conn.commit()
    conn.close()

def insertar_contacto(nombre, telefono, email):
    # ¡Corregido! Solo acepta 3 argumentos de datos.
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)"
    cursor.execute(sql, (nombre, telefono, email))
    conn.commit()
    conn.close()

def obtener_contactos(filtro_busqueda=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filtro_busqueda and filtro_busqueda != "Buscar contacto...":
        busqueda = f"%{filtro_busqueda}%"
        # Seleccionamos solo los 4 campos (id, nombre, telefono, email)
        sql = """
            SELECT id, nombre, telefono, email FROM contactos 
            WHERE nombre LIKE ? OR telefono LIKE ? OR email LIKE ?
            ORDER BY nombre
        """
        cursor.execute(sql, (busqueda, busqueda, busqueda))
    else:
        # Seleccionamos solo los 4 campos (id, nombre, telefono, email)
        sql = "SELECT id, nombre, telefono, email FROM contactos ORDER BY nombre"
        cursor.execute(sql)
        
    return cursor.fetchall()

def actualizar_contacto(id_contacto, nombre, telefono, email):
    # ¡Corregido! Solo acepta 4 argumentos (ID + 3 campos de datos).
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE contactos SET nombre = ?, telefono = ?, email = ?
        WHERE id = ?
    """
    cursor.execute(sql, (nombre, telefono, email, id_contacto))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def eliminar_contacto(id_contacto):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM contactos WHERE id = ?"
    cursor.execute(sql, (id_contacto,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def obtener_contacto_por_id(id_contacto):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT id, nombre, telefono, email FROM contactos WHERE id = ?"
    cursor.execute(sql, (id_contacto,))
    contacto = cursor.fetchone()
    conn.close()
    return contacto