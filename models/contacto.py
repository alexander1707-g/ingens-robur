# Clase contacto 
class Contacto:
    def __init__(self, nombre, telefono, email, id = None):
        self.id = id
        self.nombre = str(nombre)
        self.telefono = telefono
        self.email = email

    def mostrar_info_contacto(self):
        return f"[ID:{self.id}] Nombre: {self.nombre} - Telefono: {self.telefono} - Email: {self.email}"
    
    def __str__(self):
        return self.mostrar_info_contacto()
