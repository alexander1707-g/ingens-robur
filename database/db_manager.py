import sqlite3

def crear_base_datos_de_tablas():
    """Crea la conexión y la tabla si no existe"""
    conn = sqlite3.connect('mi_agenda.db') 
    cursor = conn.cursor()
    
    # Diseño de la tabla compatible con los atributos de la clase
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT,
        
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos y tabla verificadas exitosamente.")