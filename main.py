from models.contacto import Contacto
from models.agenda import Agenda
from utils.validaciones import *

def menu():

    print("\n\n1. Agregar contacto")
    print("2.d Mostrar todos los contactos")
    print("3. Buscar contacto por nombre")
    print("4. Eliminar contacto")
    print("5. Modificar contacto")

agenda = Agenda()

while True:
    menu()
    opcion = input("Ingresa una opcion: ")

    if (opcion == '1'):

        while True:
            nombre = input("Ingresa el nombre del contacto: ")
            if not validar_nombre(nombre):
                print("Nombre invalido")
                break

            telefono = input("Ingresa el telefono del contacto: ")
            if not validar_telefono(telefono):
                print("Telefono invalido")
                break

            email = input("Ingresa el email del contacto: ")
            if not validar_email(email):
                print("Email invalido")
                break

            nuevo_contacto = Contacto(nombre , telefono, email)
            agenda.agregar_contacto(nuevo_contacto)
            break

    elif (opcion == '2'):
        if not agenda.contactos:
            print("No hay contactos para mostrar")
            continue
        else: 
            agenda.mostrar_contactos()

    elif (opcion == '3'):
        nombre = input("Ingresa el nombre del contacto: ")
        if not validar_nombre(nombre):
            print("Nombre invalido")
            continue
        agenda.buscar_contacto_nombre(nombre)

    elif (opcion == '4'):
        nombre = input("Ingresa el nombre del contacto: ")
        if not validar_nombre(nombre):
            print("Nombre invalido")
            continue
        contacto = agenda.buscar_contacto_nombre(nombre)
        agenda.eliminar_contacto(contacto)

    elif (opcion == '5'):
        nombre = input("Ingresa el nombre del contacto: ")
        if not validar_nombre(nombre):
            print("Nombre invalido")
            continue
        contacto = agenda.buscar_contacto_nombre(nombre)

        if contacto:
            agenda.modificar_contacto(contacto)
        else:
            print("No existe el contacto")


