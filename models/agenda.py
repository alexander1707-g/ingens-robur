class Agenda:
    """Representa una colección de contactos gestionados en memoria.

    Esta clase actúa como una capa de modelo de datos para manipular una lista
    de objetos contacto (asumiendo que estos objetos tienen un atributo 'nombre').
    Es la encargada de realizar operaciones de búsqueda y gestión de la lista
    principal de contactos.
    """
    def __init__(self):
        """Inicializa la clase Agenda.

        Crea una lista vacía donde se almacenarán los objetos contacto.
        """
        # La lista de objetos contacto. Se espera que cada objeto tenga un atributo 'nombre'.
        self.contactos = []

    def esta_vacia(self) -> bool:
        """Verifica si la lista de contactos está vacía.

        Returns:
            bool: True si no hay contactos en la agenda, False en caso contrario.
        """
        return len(self.contactos) == 0

    def cargar_contactos(self, lista: list):
        """Sobreescribe la lista actual de contactos con una nueva lista.

        Este método se utiliza generalmente para cargar los datos recuperados
        de la base de datos a la agenda en memoria.

        Args:
            lista: Una lista de objetos que representan contactos. Se asume que
                   cada objeto en la lista es un contacto válido.
        """
        self.contactos = lista

    def buscar_exacta(self, nombre: str) -> list:
        """Busca contactos cuyo nombre coincide exactamente con el texto proporcionado.

        La búsqueda no es sensible a mayúsculas o minúsculas.

        Args:
            nombre: La cadena de texto (nombre completo) a buscar.

        Returns:
            list: Una lista de objetos contacto que coinciden exactamente con el
                  nombre proporcionado. La lista estará vacía si no hay coincidencias.
        """
        # Convierte el nombre de búsqueda a minúsculas para una comparación insensible a mayúsculas.
        nombre = nombre.lower()
        
        return [
            # Se asegura de que el objeto contacto (c) tenga el atributo 'nombre',
            # que este sea una cadena de texto, y luego realiza la comparación exacta.
            c for c in self.contactos
            if hasattr(c, "nombre") and isinstance(c.nombre, str) and c.nombre.lower() == nombre
        ]

    def buscar_parcial(self, texto: str) -> list:
        """Busca contactos cuyo nombre contiene el texto proporcionado.

        La búsqueda parcial no es sensible a mayúsculas o minúsculas.

        Args:
            texto: La subcadena de texto a buscar dentro de los nombres de los contactos.

        Returns:
            list: Una lista de objetos contacto que contienen el texto de búsqueda en
                  su nombre. La lista estará vacía si no hay coincidencias.
        """
        # Convierte el texto de búsqueda a minúsculas para una comparación insensible.
        texto = texto.lower()
        
        # Filtra los contactos donde el texto se encuentra en el nombre del contacto.
        return [c for c in self.contactos if texto in c.nombre.lower()]