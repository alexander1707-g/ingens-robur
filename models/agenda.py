class Agenda:
    def __init__(self):
        self.contactos = []

    def esta_vacia(self):
        return len(self.contactos) == 0

    def cargar_contactos(self, lista):
        self.contactos = lista

    def buscar_exacta(self, nombre):
        nombre = nombre.lower()
        return [
            c for c in self.contactos
            if hasattr(c, "nombre") and isinstance(c.nombre, str) and c.nombre.lower() == nombre
        ]

    def buscar_parcial(self, texto):
        texto = texto.lower()
        return [c for c in self.contactos if texto in c.nombre.lower()]