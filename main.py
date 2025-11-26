from models.agenda import Agenda
import database.db_manager as db
from utils.validaciones import validar_nombre, validar_telefono, validar_email


def mostrar_menu():
    print("\n===== AGENDA =====")
    print("1. Agregar contacto")
    print("2. Ver contactos")
    print("3. Eliminar contacto por nombre")
    print("4. Buscar exacta")
    print("5. Buscar parcial")
    print("6. Modificar contacto")
    print("7. Salir")


def main():
    db.crear_tabla()

    agenda = Agenda()
    agenda.cargar_contactos(db.obtener_todos())

    while True:
        mostrar_menu()
        op = input("Opcion: ")

        if op == "1":
            nombre = input("Nombre: ")
            telefono = input("Telefono: ")
            email = input("Email: ")

            if not validar_nombre(nombre):
                print("Nombre invalido")
                continue
            if not validar_telefono(telefono):
                print("Telefono invalido")
                continue
            if not validar_email(email):
                print("Email invalido")
                continue

            db.insertar_contacto(nombre, telefono, email)
            agenda.cargar_contactos(db.obtener_todos())
            print("Contacto agregado")

        elif op == "2":
            if agenda.esta_vacia():
                print("Agenda vacia")
            else:
                for c in agenda.contactos:
                    print(c)

        elif op == "3":
            nombre = input("Nombre exacto a eliminar: ")
            if db.eliminar_por_nombre(nombre):
                agenda.cargar_contactos(db.obtener_todos())
                print("Eliminado")
            else:
                print("No existe ese contacto")

        elif op == "4":
            nombre = input("Nombre exacto: ")
            res = agenda.buscar_exacta(nombre)
            if res:
                for c in res:
                    print(c)
            else:
                print("Nada encontrado")

        elif op == "5":
            texto = input("Buscar por texto: ")
            res = db.buscar_parcial(texto)
            if res:
                for c in res:
                    print(c)
            else:
                print("Nada encontrado")

        elif op == "6":
            if agenda.esta_vacia():
                print("Agenda vacía.")
                continue

            print("\n=== Contactos ===")
            for c in agenda.contactos:
                print(c)

            try:
                id_mododificar = int(input("\nID del contacto a modificar: "))
            except ValueError:
                print("ID invalido")
                continue

            nuevo_nombre = input("Nuevo nombre: ")
            if not validar_nombre(nuevo_nombre):
                print("Nombre invalido")
                continue

            nuevo_telefono = input("Nuevo teléfono: ")
            if not validar_telefono(nuevo_telefono):
                print("Telefono invalido")
                continue

            nuevo_email = input("Nuevo email: ")
            if not validar_email(nuevo_email):
                print("Email invalido")
                continue

            if db.modificar_contacto(id_mododificar, nuevo_nombre, nuevo_telefono, nuevo_email):
                agenda.cargar_contactos(db.obtener_todos())
                print("Contacto modificado correctamente")
            else:
                print("No se encontro ese ID")
        else:
            print("Opcion invalida")

main()
