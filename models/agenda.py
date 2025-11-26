from contacto import Contacto

# Clase agenda con metodos CRUD integrada con la clase contacto
class Agenda:
    def __init__(self):
        self.contactos = [] # se inicializa la lista de contactos como una lista vacia

    # Metodo para agregar un contacto recibido por parametro a la lista de contactos
    def agregar_contacto(self, contacto):
        self.contactos.append(contacto) # el metodo append agrega un elemento al final de la lista

    # Metodo para mostrar la infomracion de todos los contactos
    def mostrar_contactos(self):
        for contacto in self.contactos:
            contacto.mostrar_info_contacto()

    def eliminar_contacto(self, contacto):
        try:
            self.contactos.remove(contacto)
            print("Contacto eliminado correctamente")
        except ValueError:
            print("El contacto no existe")

    def buscar_contacto_nombre(self, nombre_contacto):
        for contacto in self.contactos:
            if (nombre_contacto == contacto.nombre):
                print("Contacto encontrado!!")
                contacto.mostrar_info_contacto()
                return
            
        print("No se encontro el contacto")

    def buscar_contacto_email(self, email_contacto):
        for contacto in self.contactos:
            if (email_contacto == contacto.email):
                print("Contacto encontrado!!")
                contacto.mostrar_info_contacto()
                break
        
        print("No se encontro el contacto")

    def buscar_contacto_telefono(self, telefono_contacto):
        for contacto in self.contactos:
            if (telefono_contacto == contacto.telefono):
                print("Contacto encontrado!!")
                contacto.mostrar_info_contacto()
                return
            
        print("No se encontro el contacto")

    def busqueda_parcial_nombre(self, nombre):
        encontrados = []
        for c in self.contactos: 
            if nombre.lower() in c.nombre.lower():
                encontrados.append(c)
        return encontrados
    




