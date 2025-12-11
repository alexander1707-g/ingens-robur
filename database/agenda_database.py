"""Módulo para la gestión de contactos en una base de datos SQLite.

Este módulo proporciona funciones de bajo nivel para establecer la conexión a la
base de datos 'agenda.db' y realizar operaciones CRUD (Crear, Leer, Actualizar,
Eliminar) sobre la tabla 'contactos'.

La estructura de la tabla de contactos se define con los siguientes campos:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- nombre: TEXT NOT NULL
- telefono: TEXT NOT NULL
- email: TEXT
"""
import sqlite3
import os
import sys

# La base de datos debe estar en la raíz del proyecto
# Determina la ruta absoluta de la raíz del proyecto para localizar la base de datos.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(project_root, 'agenda.db')


def get_db_connection():
    """Establece y devuelve una conexión a la base de datos SQLite.

    Configura la conexión para que las filas se devuelvan como objetos `sqlite3.Row`,
    permitiendo acceder a los campos por nombre de columna.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos 'agenda.db'.
    """
    conn = sqlite3.connect(DB_PATH)
    # Configura el factory para que devuelva filas accesibles por nombre de columna.
    conn.row_factory = sqlite3.Row
    return conn


# --- FUNCIONES CORE CRUD (4 Campos: id, nombre, telefono, email) ---


def crear_tabla():
    """Crea la tabla 'contactos' y migra datos si es necesario.

    Esta función asegura que la tabla 'contactos' exista con la estructura de
    cuatro campos (id, nombre, telefono, email).

    Si existe una tabla 'contactos' antigua (potencialmente con un campo 'notas'
    que ya no se usa), realiza los siguientes pasos de migración:
    1. Crea una nueva tabla temporal 'contactos_new' con la estructura deseada.
    2. Copia los datos relevantes (id, nombre, telefono, email) de la antigua a la nueva.
    3. Elimina la tabla 'contactos' antigua.
    4. Renombra 'contactos_new' a 'contactos'.

    Lanza advertencias si ocurren errores operativos durante la migración (ej. la
    tabla antigua ya no existe o no tiene las columnas esperadas).
    """
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
            # Se copian solo las columnas que coinciden con la nueva estructura.
            cursor.execute("INSERT INTO contactos_new (id, nombre, telefono, email) SELECT id, nombre, telefono, email FROM contactos")
            
            # 4. Eliminar la tabla antigua para limpiarla
            cursor.execute("DROP TABLE contactos")
            
        except sqlite3.OperationalError as e:
            # Captura errores que indican problemas en la estructura de la tabla antigua.
            print(f"Advertencia durante la migración de tabla: {e}")

    # 5. Renombrar la tabla nueva (y correcta) a 'contactos'
    cursor.execute("ALTER TABLE contactos_new RENAME TO contactos")
    
    conn.commit()
    conn.close()


def insertar_contacto(nombre: str, telefono: str, email: str):
    """Inserta un nuevo contacto en la base de datos.

    Args:
        nombre: El nombre completo del contacto.
        telefono: El número de teléfono del contacto.
        email: La dirección de correo electrónico del contacto (opcional, pero se pasa como argumento).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)"
    # Los valores se pasan como una tupla para prevenir inyección SQL.
    cursor.execute(sql, (nombre, telefono, email))
    conn.commit()
    conn.close()


def obtener_contactos(filtro_busqueda: str = None):
    """Recupera todos los contactos de la base de datos, opcionalmente aplicando un filtro.

    La búsqueda se realiza por coincidencia parcial (LIKE) en los campos 'nombre',
    'telefono' y 'email'. Los resultados se ordenan por nombre.

    Args:
        filtro_busqueda: Cadena de texto para filtrar los contactos. Si es None
                         o igual a "Buscar contacto...", se devuelven todos los contactos.

    Returns:
        list[sqlite3.Row]: Una lista de objetos Row que representan los contactos.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filtro_busqueda and filtro_busqueda != "Buscar contacto...":
        busqueda = f"%{filtro_busqueda}%"
        # Consulta SQL para buscar en nombre, telefono o email.
        sql = """
            SELECT id, nombre, telefono, email FROM contactos 
            WHERE nombre LIKE ? OR telefono LIKE ? OR email LIKE ?
            ORDER BY nombre
        """
        cursor.execute(sql, (busqueda, busqueda, busqueda))
    else:
        # Consulta SQL para obtener todos los contactos.
        sql = "SELECT id, nombre, telefono, email FROM contactos ORDER BY nombre"
        cursor.execute(sql)
        
    return cursor.fetchall()


def actualizar_contacto(id_contacto: int, nombre: str, telefono: str, email: str):
    """Actualiza los datos de un contacto existente usando su ID.

    Args:
        id_contacto: El ID del contacto a actualizar.
        nombre: El nuevo nombre del contacto.
        telefono: El nuevo número de teléfono del contacto.
        email: La nueva dirección de correo electrónico del contacto.

    Returns:
        bool: True si al menos una fila fue afectada (el contacto fue actualizado), False en caso contrario.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE contactos SET nombre = ?, telefono = ?, email = ?
        WHERE id = ?
    """
    # El ID se usa en la cláusula WHERE.
    cursor.execute(sql, (nombre, telefono, email, id_contacto))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


def eliminar_contacto(id_contacto: int):
    """Elimina un contacto de la base de datos por su ID.

    Args:
        id_contacto: El ID del contacto a eliminar.

    Returns:
        bool: True si el contacto fue eliminado (una fila afectada), False en caso contrario.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM contactos WHERE id = ?"
    cursor.execute(sql, (id_contacto,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


def obtener_contacto_por_id(id_contacto: int):
    """Recupera un contacto específico usando su ID.

    Args:
        id_contacto: El ID del contacto a buscar.

    Returns:
        sqlite3.Row or None: Un objeto Row con los datos del contacto si se encuentra, o None si no existe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT id, nombre, telefono, email FROM contactos WHERE id = ?"
    cursor.execute(sql, (id_contacto,))
    contacto = cursor.fetchone()
    conn.close()
    return contacto