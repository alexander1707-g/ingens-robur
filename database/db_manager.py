import sqlite3
from models.contacto import Contacto


DB_FILE = "agenda.db"


def conectar():
    return sqlite3.connect(DB_FILE)


def crear_tabla():
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        con.commit()
    except Exception as e:
        print("Error creando tabla:", e)
    finally:
        con.close()


def insertar_contacto(nombre, telefono, email):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
            (nombre, telefono, email)
        )
        con.commit()
    except Exception as e:
        print("Error insertando contacto:", e)
    finally:
        con.close()


def obtener_todos():
    lista = []
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("SELECT id, nombre, telefono, email FROM contactos")
        filas = cur.fetchall()

        for f in filas:
            lista.append(Contacto(f[1], f[2], f[3], f[0]))

    except Exception as e:
        print("Error obteniendo contactos:", e)
    finally:
        con.close()

    return lista


def eliminar_por_nombre(nombre):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM contactos WHERE LOWER(nombre)=LOWER(?)", (nombre,))
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Error eliminando:", e)
        return False
    finally:
        con.close()


def buscar_parcial(texto):
    lista = []
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT id, nombre, telefono, email FROM contactos WHERE LOWER(nombre) LIKE ?",
            (f"%{texto.lower()}%",)
        )
        filas = cur.fetchall()

        for f in filas:
            lista.append(Contacto(f[1], f[2], f[3], f[0]))

    except Exception as e:
        print("Error en búsqueda parcial:", e)
    finally:
        con.close()

    return lista

def modificar_contacto(id, nuevo_nombre, nuevo_telefono, nuevo_email):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("""
            UPDATE contactos
            SET nombre = ?, telefono = ?, email = ?
            WHERE id = ?
        """, (nuevo_nombre, nuevo_telefono, nuevo_email, id))

        con.commit()
        return cur.rowcount > 0  # True si se modifico algo
    except Exception as e:
        print("Error modificando contacto:", e)
        return False
    finally:
        con.close()