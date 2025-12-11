class Contacto:
    """Representa un contacto individual con sus datos personales.

    Los atributos principales de un contacto son su identificador único (ID),
    nombre, número de teléfono y dirección de correo electrónico.
    """
    def __init__(self, nombre: str, telefono: str, email: str, id: int = None):
        """Inicializa un nuevo objeto Contacto.

        Args:
            nombre: El nombre del contacto. Se convierte explícitamente a cadena.
            telefono: El número de teléfono del contacto.
            email: La dirección de correo electrónico del contacto.
            id: El identificador único del contacto en la base de datos. Es opcional
                y se usa principalmente cuando se carga el contacto desde la DB.
        """
        self.id = id
        self.nombre = str(nombre)
        self.telefono = telefono
        self.email = email

    def mostrar_info_contacto(self) -> str:
        """Genera una cadena de texto formateada con toda la información del contacto.

        Returns:
            str: Una cadena que incluye el ID, Nombre, Teléfono y Email del contacto.
        """
        return f"[ID:{self.id}] Nombre: {self.nombre} - Telefono: {self.telefono} - Email: {self.email}"
    
    def __str__(self) -> str:
        """Define la representación en cadena del objeto para impresión.

        Returns:
            str: La información detallada del contacto, obtenida de `mostrar_info_contacto`.
        """
        return self.mostrar_info_contacto()