import re

def validar_nombre(nombre):
        """
        True: Solo letras (incluye tildes/ñ) y espacios. Mínimo 2 caracteres.
        False: Números, símbolos o vacío.
        """
        if not nombre: return False
        patron = r"^[A-Za-zÁ-ÉÍÓÚáéíóúñÑ\s]{2,}$"
        return bool(re.match(patron, nombre))

def validar_telefono(telefono):
        """
        True: Solo números. Longitud entre 7 y 15 dígitos. Acepta '+' al inicio.
        False: Letras, espacios intermedios o longitud incorrecta.
        """
        if not telefono: return False
        patron = r"^\+?[0-9]{7,15}$"
        return bool(re.match(patron, telefono))

    
def validar_email(email):
            """
        True: Formato estándar (texto@dominio.algo).
        False: Falta @, falta punto, espacios, etc.
        """
            if not email: return False
            patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return bool(re.match(patron, email))

