# Clase contacto 
class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def mostrar_info_contacto(self):
        print(f"Nombre: {self.nombre}")
        print(f"Telefono: {self.telefono}")
        print(f"Email: {self.email}")
        print("------------------------")
