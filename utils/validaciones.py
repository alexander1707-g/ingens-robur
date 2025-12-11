import re

def validar_nombre(nombre):
    """Valida si un nombre es válido según las reglas de la agenda.

    Args:
        nombre (str): La cadena de texto a validar.

    Returns:
        bool: 
            True: Si contiene solo letras (incluye tildes/ñ) y espacios, 
                  y tiene un mínimo de 2 caracteres.
            False: Si contiene números, símbolos o si está vacío.
    """
    if not nombre: return False
    patron = r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{2,}$"
    return bool(re.match(patron, nombre))

def validar_telefono(telefono):
    """Valida si un número de teléfono tiene un formato aceptable.

    Acepta el formato nacional o internacional básico.

    Args:
        telefono (str): La cadena de texto del número de teléfono.

    Returns:
        bool:
            True: Si contiene solo números, con longitud entre 7 y 15 dígitos.
                  Acepta un signo '+' opcional al inicio.
            False: Si contiene letras, espacios intermedios, o si la longitud 
                   está fuera del rango [7, 15].
    """
    if not telefono: return False
    patron = r"^\+?[0-9]{7,15}$"
    return bool(re.match(patron, telefono))

def validar_email(email):
    """Valida si una cadena de texto tiene el formato estándar de correo electrónico.

    Args:
        email (str): La cadena de texto del correo electrónico.

    Returns:
        bool:
            True: Si coincide con el formato estándar (texto@dominio.algo).
            False: Si le falta el '@', le falta el punto después del dominio, 
                   contiene espacios o es una cadena vacía.
    """
    if not email: return False
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(patron, email))