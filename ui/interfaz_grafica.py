"""Módulo Principal de la Interfaz de Usuario (UI) de la Agenda.

Este módulo implementa la interfaz gráfica de la aplicación de agenda
utilizando Tkinter y la librería ttkbootstrap para estilos modernos.

Gestiona las tres vistas principales:
1. Vista Principal (Lista de contactos con búsqueda).
2. Vista de Detalle de Contacto.
3. Vista de Formulario (Creación/Edición de contacto).
4. Vista de Acerca de (Informacion del equipo de desarrollo)

Utiliza el módulo 'agenda_database' (db) para las operaciones CRUD.
"""
import sys
import os
import tkinter as tk
from tkinter import END, messagebox # Importamos messagebox explícitamente
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame
from PIL import Image, ImageTk 
from utils.validaciones import *

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# --- MOCKUP DE BASE DE DATOS Y UTILIDADES ---
from database import agenda_database as db 
from utils.validaciones import * # --- 1. CONSTANTES Y CONFIGURACIÓN ESTÉTICA ---
class Config:
    """Clase que almacena constantes para la configuración estética de la UI.

    Define la paleta de colores y los iconos utilizados en toda la aplicación
    para mantener la consistencia visual.
    """
    # Colores base (Paleta Original Restaurada)
    COLOR_NAVY_PROFUNDO = "#1A2B4C"       # Azul Dominante
    COLOR_DORADO = "#C59D5F"              # Acento Dorado
    COLOR_CREMA_FONDO = "#F5F5F0"         # Fondo Principal
    COLOR_BLANCO = "#FFFFFF"
    
    # Paleta Modal Equipo
    TEAM_BG_DARK = "#0C1524"              
    TEAM_BG_CREAM = "#F2F0E4"             
    TEAM_TEXT_GOLD = "#D4AF37"            
    TEAM_TEXT_WHITE = "#FFFFFF"
    
    # Iconos
    ICON_ATRAS = "⬅"
    ICON_GUARDAR = "💾"
    ICON_EDITAR = "✏️" 
    ICON_BUSCAR = "🔍"
    ICON_ELIMINAR = "🗑️"
    ICON_INFO = "      ℹ️"
    ICON_CROWN = "👑"

# --- 2. UTILIDADES ---
class ImageAdapter:
    """Clase para cargar, redimensionar y gestionar imágenes con PIL y Tkinter.

    Permite manejar logotipos o imágenes de la aplicación de manera eficiente
    y con redimensionamiento dinámico.
    """
    def __init__(self, master, image_path):
        """Inicializa el adaptador de imágenes.

        Args:
            master: El widget padre.
            image_path: Ruta del archivo de imagen a cargar.
        """
        self.master = master
        self.image_path = image_path
        self.original_image = None
        self.tk_image = None
        try:
            self.original_image = Image.open(image_path)
            self.image_loaded = True
        except Exception:
            self.image_loaded = False

    def resize_image(self, width, height):
        """Redimensiona la imagen cargada manteniendo la relación de aspecto.

        Args:
            width: Ancho máximo deseado.
            height: Alto máximo deseado.

        Returns:
            ImageTk.PhotoImage or None: La imagen redimensionada, o None si no se cargó.
        """
        if not self.image_loaded: return None
        original_width, original_height = self.original_image.size
        ratio = min(width / original_width, height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        if new_width <= 0 or new_height <= 0: return None
        resized_img = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_img)
        return self.tk_image

def get_initials(nombre):
    """Calcula las iniciales de un nombre (primera letra de las dos primeras palabras).

    Args:
        nombre: La cadena de texto del nombre completo.

    Returns:
        str: Las iniciales en mayúsculas (ej. "JD"), o "NN" si está vacío.
    """
    parts = nombre.split()
    if not parts: return "NN"
    initials = parts[0][0].upper()
    if len(parts) > 1: initials += parts[1][0].upper()
    return initials

# --- 3. CLASE PRINCIPAL ---
class AgendaApp:
    """Clase principal de la aplicación GUI de Agenda.

    Gestiona la ventana principal, la navegación entre las tres vistas (Lista,
    Detalle, Formulario) y la interacción con la capa de datos (db).
    """
    def __init__(self, master):
        """Inicializa la aplicación.

        Configura la ventana, el estilo, asegura la existencia de la tabla DB 
        y muestra la vista principal.

        Args:
            master: La instancia de la ventana raíz de Tkinter (tk.Tk).
        """
        self.master = master
        self.master.title("AGENDA NORMA INGENS ROBUR - Escritorio")
        self.master.geometry("1100x750")
        
        db.crear_tabla() 
        self._configure_styles()
        
        # Logo para el modal
        logo_path = os.path.join(project_root, 'ui', 'logo_empresa.png') 
        self.team_logo_adapter = ImageAdapter(master, logo_path)
        
        self.show_main_view()
        
    def _configure_styles(self):
        """Configuración avanzada de estilos de ttkbootstrap."""
        self.style = ttk.Style(theme="litera")
        
        # Estilos de Frames
        self.style.configure('Main.TFrame', background=Config.COLOR_CREMA_FONDO)
        self.style.configure('Card.TFrame', background=Config.COLOR_BLANCO)
        
        # Encabezado Azul
        self.style.configure('Header.TFrame', background=Config.COLOR_NAVY_PROFUNDO)
        self.style.configure('Header.TLabel', background=Config.COLOR_NAVY_PROFUNDO, 
                             foreground=Config.COLOR_BLANCO, font=('Helvetica', 20, 'bold'))
        
        # Botones Dorados (Estilo Principal)
        self.style.configure('Gold.TButton', 
                             background=Config.COLOR_DORADO, 
                             foreground=Config.COLOR_NAVY_PROFUNDO, 
                             font=('Helvetica', 11, 'bold'), 
                             bordercolor=Config.COLOR_DORADO,
                             padding=10)
        self.style.map('Gold.TButton', 
                       background=[('active', '#b08d55'), ('pressed', '#a3814d')],
                       foreground=[('active', Config.COLOR_NAVY_PROFUNDO)])
        
        # Botones de Acción en Lista
        self.style.configure('Action.TButton', font=('Helvetica', 12))

    def _clear_view(self):
        """Elimina todos los widgets hijos de la ventana principal para cambiar de vista."""
        for widget in self.master.winfo_children():
            widget.destroy()

    # =========================================================================
    # --- MODAL DE EQUIPO ---
    # =========================================================================
    def _show_team_modal(self):
        """Muestra una ventana superpuesta (modal) con la información del equipo de desarrollo."""
        team_overlay = tk.Frame(self.master, bg=Config.TEAM_BG_DARK)
        team_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        team_overlay.lift()

        tk.Button(team_overlay, text="✕", bg=Config.TEAM_BG_DARK, fg=Config.COLOR_BLANCO,
                  font=("Arial", 16, "bold"), bd=0, cursor="hand2",
                  command=team_overlay.destroy).place(relx=0.97, rely=0.0001, anchor='ne')

        container = tk.Frame(team_overlay, bg=Config.TEAM_BG_DARK)
        container.place(relx=0.5, rely=0.6, anchor='center', relwidth=0.9, relheight=0.85)
        
        # Grid layout
        container.grid_columnconfigure(0, weight=40, uniform="group") 
        container.grid_columnconfigure(1, weight=60, uniform="group") 
        container.grid_rowconfigure(0, weight=1)

        # --- IZQUIERDA: LOGO ---
        left_frame = tk.Frame(container, bg=Config.TEAM_BG_CREAM)
        left_frame.grid(row=0, column=0, sticky="nsew")

        logo_container = tk.Frame(left_frame, bg=Config.TEAM_BG_CREAM)
        logo_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        logo_label = tk.Label(logo_container, bg=Config.TEAM_BG_CREAM)
        logo_label.place(relx=0.5, rely=0.3, anchor='center')

        def update_logo_size(event):
            """Función callback para redimensionar el logo dinámicamente con la ventana."""
            new_width = event.width - 40
            new_height = event.height - 40
            if new_width > 0 and new_height > 0:
                resized_img = self.team_logo_adapter.resize_image(new_width, new_height)
                if resized_img:
                    logo_label.config(image=resized_img)
                else:
                    logo_label.config(text="NORMA INGENS ROBUR", fg="black")

        logo_container.bind("<Configure>", update_logo_size)

        # --- DERECHA: INFO ---
        right_frame = tk.Frame(container, bg=Config.TEAM_BG_DARK)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        # Título
        title_box = tk.Frame(right_frame, bg=Config.TEAM_BG_DARK, highlightbackground=Config.TEAM_TEXT_GOLD, highlightthickness=1)
        title_box.pack(fill='x', pady=(0, 20))
        
        tk.Label(title_box, text=Config.ICON_CROWN, bg=Config.TEAM_BG_DARK, fg=Config.TEAM_TEXT_GOLD, font=("Arial", 22)).pack(side='left', padx=10, pady=10)
        tk.Label(title_box, text="EQUIPO DE TRABAJO", bg=Config.TEAM_BG_DARK, fg=Config.COLOR_DORADO, font=("Helvetica", 18, "bold")).pack(side='left', pady=10)

        # Contenido
        info_content = tk.Frame(right_frame, bg=Config.TEAM_BG_DARK)
        info_content.pack(fill='both', expand=True)

        def create_block(icon, role, name):
            """Crea un bloque de información para un rol/miembro del equipo."""
            block = tk.Frame(info_content, bg=Config.TEAM_BG_DARK)
            block.pack(pady=12, fill='x')
            
            # Icono
            tk.Label(block, text=icon, bg=Config.TEAM_BG_DARK, fg=Config.TEAM_TEXT_GOLD, font=("Arial", 28)).pack(side='left', padx=(0, 20), anchor='n')
            
            # Textos
            txt_frame = tk.Frame(block, bg=Config.TEAM_BG_DARK)
            txt_frame.pack(side='left', fill='x', expand=True)
            
            tk.Label(txt_frame, text=role, bg=Config.TEAM_BG_DARK, fg=Config.TEAM_TEXT_WHITE, font=("Helvetica", 12, "bold"), anchor='w').pack(fill='x')
            
            for n in name.split('\n'):
                tk.Label(txt_frame, text=n, bg=Config.TEAM_BG_DARK, fg="gray85", font=("Helvetica", 11), anchor='w').pack(fill='x')
            
            ttk.Separator(info_content, orient='horizontal', bootstyle="secondary").pack(fill='x', pady=5)

        # Bloques de miembros del equipo
        create_block(Config.ICON_CROWN, "PRODUCT OWNER", "GENDER ALEXANDER CAMACHO GARCIA")
        create_block("⭐", "SCRUM MASTER", "YULY PAOLA FLOREZ LOPEZ")
        create_block("💻", "EQUIPO DE DESARROLLO", "EMMANUEL DIAZ GUTIERREZ\nALFREDO MANUEL RODRIGUEZ LUQUETA")

    # =========================================================================
    # --- VISTA PRINCIPAL ---
    # =========================================================================
    def show_main_view(self):
        """Muestra la vista principal: encabezado, barra de búsqueda y lista de contactos."""
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)
        
        # 1. ENCABEZADO
        header_frame = ttk.Frame(self.master, style='Header.TFrame', height=80, padding=15)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text=Config.ICON_CROWN, bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_DORADO, font=("Arial", 24)).pack(side='left', padx=10)
        ttk.Label(header_frame, text="AGENDA NORMA INGENS ROBUR", style='Header.TLabel').pack(side='left', padx=5)

        # 2. BARRA DE BÚSQUEDA
        search_container = ttk.Frame(self.master, style='Main.TFrame', padding=(175, 30, 20, 10))
        search_container.pack(fill='x')
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_container, textvariable=search_var, font=('Helvetica', 12), width=50, bootstyle="primary")
        search_entry.pack(side='left', padx=(0, 10), ipady=6)
        
        def on_search(*args):
            """Ejecuta la búsqueda de contactos y actualiza la lista al teclear."""
            self._populate_list(scrolled_frame, search_var.get())
        
        search_entry.bind("<KeyRelease>", on_search)
        ttk.Button(search_container, text=Config.ICON_BUSCAR, command=on_search, bootstyle="primary").pack(side='left', ipady=2)

        # 3. LISTA DE CONTACTOS
        list_area = ttk.Frame(self.master, style='Main.TFrame', padding=(40, 10, 40, 0))
        list_area.pack(fill='both', expand=True)

        scrolled_frame = ScrolledFrame(list_area, autohide=True, bootstyle="round")
        scrolled_frame.pack(fill='both', expand=True, pady=(0, 80)) 
        
        scrolled_frame.container.configure(style='Main.TFrame')
        
        self._populate_list(scrolled_frame)

        # 4. BOTONES FLOTANTES
        tk.Button(self.master, text="+", bg=Config.COLOR_DORADO, fg=Config.COLOR_NAVY_PROFUNDO, 
                  font=('Arial', 24, 'bold'), width=3, height=1, bd=0, relief='raised', cursor="hand2",
                  activebackground="#b08d55",
                  command=lambda: self.show_contact_form(is_new=True)).place(relx=0.96, rely=0.96, anchor='se')

        tk.Button(self.master, text=Config.ICON_INFO, bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_DORADO,
                  font=('Arial', 24, 'bold'), width=3, height=1, bd=0, relief='raised', cursor="hand2",
                  activebackground="#2B3D5F",
                  command=self._show_team_modal).place(relx=0.04, rely=0.96, anchor='sw')

    def _populate_list(self, scroll_widget, query=None):
        """Pobla el ScrolledFrame con las tarjetas de contacto, con soporte para búsqueda.

        Args:
            scroll_widget: El widget ScrolledFrame (o su contenedor).
            query: El texto de búsqueda para filtrar la lista (opcional).
        """
        for widget in scroll_widget.container.winfo_children():
            widget.destroy()

        contacts = db.obtener_contactos(query) if query else db.obtener_contactos()

        if not contacts:
            tk.Label(scroll_widget.container, text="No se encontraron contactos.", 
                      bg=Config.COLOR_CREMA_FONDO, fg="gray", font=('Helvetica', 14)).pack(pady=50)
            return

        for contact in contacts:
            self._create_contact_card(scroll_widget.container, contact)

    def _create_contact_card(self, parent, data):
        """Crea y configura una tarjeta individual de contacto.

        Args:
            parent: El widget contenedor donde se insertará la tarjeta.
            data: Tupla con los datos del contacto (id, nombre, telefono, email).
        """
        c_id, c_name, c_tel, c_email = data
        
        # Tarjeta (Frame)
        card = tk.Frame(parent, bg=Config.COLOR_BLANCO, padx=20, pady=15)
        card.config(highlightbackground=Config.COLOR_DORADO, highlightthickness=1)
        card.pack(fill='x', pady=8, padx=5)

        card.bind("<Button-1>", lambda e: self.show_contact_detail(data))

        # Avatar (Iniciales)
        lbl_avatar = tk.Label(card, text=get_initials(c_name), bg=Config.COLOR_DORADO, fg=Config.COLOR_NAVY_PROFUNDO,
                              font=('Helvetica', 14, 'bold'), width=5, height=2)
        lbl_avatar.pack(side='left', padx=(0, 20))
        lbl_avatar.bind("<Button-1>", lambda e: self.show_contact_detail(data))

        # Info
        info_frame = tk.Frame(card, bg=Config.COLOR_BLANCO)
        info_frame.pack(side='left', fill='both', expand=True)
        
        lbl_name = tk.Label(info_frame, text=c_name, font=('Helvetica', 14, 'bold'), 
                             bg=Config.COLOR_BLANCO, fg=Config.COLOR_NAVY_PROFUNDO)
        lbl_name.pack(anchor='w')
        
        lbl_sub = tk.Label(info_frame, text=c_email, font=('Helvetica', 10), 
                            bg=Config.COLOR_BLANCO, fg="gray")
        lbl_sub.pack(anchor='w')

        # Bindings para sub-widgets
        for w in [info_frame, lbl_name, lbl_sub]:
            w.bind("<Button-1>", lambda e: self.show_contact_detail(data))

        # Botones Acción (Eliminar y Editar)
        ttk.Button(card, text=Config.ICON_ELIMINAR, bootstyle="outline-danger", style='Action.TButton', width=4,
                    command=lambda: self.handle_delete_contact(c_id, c_name)).pack(side='right', padx=5)
        
        ttk.Button(card, text=Config.ICON_EDITAR, bootstyle="outline-primary", style='Action.TButton', width=4,
                    command=lambda: self.show_contact_form(False, data)).pack(side='right', padx=5)

    # =========================================================================
    # --- VISTA DETALLE Y FORMULARIO ---
    # =========================================================================
    def show_contact_detail(self, data):
        """Muestra la vista de detalle de un contacto.

        Args:
            data: Tupla con los datos del contacto (id, nombre, telefono, email).
        """
        c_id, c_name, c_tel, c_email = data
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)

        # Encabezado
        header = ttk.Frame(self.master, style='Header.TFrame', height=70, padding=10)
        header.pack(fill='x')
        tk.Button(header, text=f"{Config.ICON_ATRAS} Volver", command=self.show_main_view,
                  bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_BLANCO, bd=0, font=('Helvetica', 12, 'bold'), cursor="hand2").pack(side='left', padx=15)
        ttk.Label(header, text="DETALLE DE CONTACTO", style='Header.TLabel').pack(side='left', padx=30)

        # Panel de Perfil
        profile_panel = tk.Frame(self.master, bg=Config.COLOR_BLANCO, padx=40, pady=30, relief='raised', bd=1)
        profile_panel.pack(pady=30, padx=50, fill='x')

        # Avatar grande y Nombre
        tk.Label(profile_panel, text=get_initials(c_name), bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_DORADO,
                  font=('Helvetica', 35, 'bold'), width=4, height=2).pack(pady=10)
        
        tk.Label(profile_panel, text=c_name, font=('Helvetica', 22, 'bold'), 
                  bg=Config.COLOR_BLANCO, fg=Config.COLOR_NAVY_PROFUNDO).pack(pady=5)

        # Barra de Acciones (Editar/Eliminar)
        action_bar = tk.Frame(profile_panel, bg=Config.COLOR_BLANCO)
        action_bar.pack(pady=15)
        
        ttk.Button(action_bar, text=f"{Config.ICON_EDITAR} Editar", style='Gold.TButton', width=15,
                    command=lambda: self.show_contact_form(False, data)).pack(side='left', padx=10)
        
        ttk.Button(action_bar, text=f"{Config.ICON_ELIMINAR} Eliminar", bootstyle="danger", width=15,
                    command=lambda: self.handle_delete_contact(c_id, c_name)).pack(side='left', padx=10)

        # Sección de Detalles
        details_frame = ttk.Frame(self.master, style='Main.TFrame', padding=(60, 10))
        details_frame.pack(fill='both', expand=True)

        def add_row(label, value):
            """Crea una fila de etiqueta y valor para la vista de detalle."""
            row = ttk.Frame(details_frame, style='Main.TFrame')
            row.pack(fill='x', pady=8)
            ttk.Label(row, text=label, font=('Helvetica', 10, 'bold'), foreground=Config.COLOR_NAVY_PROFUNDO, background=Config.COLOR_CREMA_FONDO).pack(anchor='w')
            ttk.Label(row, text=value, font=('Helvetica', 14), background=Config.COLOR_CREMA_FONDO).pack(anchor='w')
            ttk.Separator(row, orient='horizontal').pack(fill='x', pady=5)

        # Muestra los datos
        add_row("Teléfono Móvil", c_tel)
        add_row("Correo Electrónico", c_email)
        add_row("ID Sistema", str(c_id))

    def show_contact_form(self, is_new=False, contact_data=None):
        """Muestra el formulario para crear o editar un contacto.

        Args:
            is_new: True para un nuevo contacto, False para edición.
            contact_data: Datos del contacto si es edición (opcional).
        """
        c_id, c_name, c_tel, c_email = (None, "", "", "")
        if contact_data:
            c_id, c_name, c_tel, c_email = contact_data
            
        title = "NUEVO CONTACTO" if is_new else "EDITAR CONTACTO"
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)

        # Encabezado
        header = ttk.Frame(self.master, style='Header.TFrame', height=70, padding=10)
        header.pack(fill='x')
        tk.Button(header, text=f"{Config.ICON_ATRAS} Volver", command=self.show_main_view,
                  bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_BLANCO, bd=0, font=('Helvetica', 12, 'bold')).pack(side='left', padx=15)
        ttk.Label(header, text=title, style='Header.TLabel').pack(side='left', padx=30)

        form_frame = ttk.Frame(self.master, style='Main.TFrame', padding=50)
        form_frame.pack(fill='both', expand=True)

        # Variables de control para los campos
        vars = {
            "nombre": tk.StringVar(value=c_name),
            "telefono": tk.StringVar(value=c_tel),
            "email": tk.StringVar(value=c_email)
        }

        def create_input(lbl, var):
            """Crea una etiqueta y un campo de entrada (Entry)."""
            c = ttk.Frame(form_frame, style='Main.TFrame')
            c.pack(fill='x', pady=12)
            ttk.Label(c, text=lbl, font=('Helvetica', 11, 'bold'), foreground=Config.COLOR_NAVY_PROFUNDO, background=Config.COLOR_CREMA_FONDO).pack(anchor='w')
            ttk.Entry(c, textvariable=var, font=('Helvetica', 12), bootstyle="primary").pack(fill='x', pady=(5,0), ipady=3)

        # Creación de campos del formulario
        create_input("Nombre Completo *", vars["nombre"])
        create_input("Teléfono *", vars["telefono"])
        create_input("Correo Electrónico", vars["email"])

        def save():
            """Función de callback para guardar/actualizar el contacto, incluyendo validación."""
            n = vars["nombre"].get().strip()
            t = vars["telefono"].get().strip()
            e = vars["email"].get().strip()
            
            # 1. Validación de campos obligatorios
            if not n or not t:
                self._show_modal("Error", "Nombre y Teléfono son obligatorios.")
                return
            
            # 2. Validación de formato de teléfono usando la utilidad
            if not validar_telefono(t):
                self._show_modal("Error", "Teléfono inválido.")
                return

            # 3. Ejecución de la operación CRUD
            if is_new:
                db.insertar_contacto(n, t, e)
                self._show_modal("Éxito", "Contacto guardado.")
            else:
                db.actualizar_contacto(c_id, n, t, e)
                self._show_modal("Éxito", "Contacto actualizado.")
            
            # 4. Regreso a la vista principal
            self.show_main_view()

        ttk.Button(form_frame, text=f"{Config.ICON_GUARDAR} GUARDAR", style='Gold.TButton', width=20, command=save).pack(pady=40)

    # --- MODALES ---
    def _show_modal(self, title, msg):
        """Muestra una ventana de información estándar de Tkinter."""
        messagebox.showinfo(title, msg)

    def handle_delete_contact(self, c_id, c_name):
        """Maneja la solicitud de eliminación pidiendo confirmación al usuario.

        Args:
            c_id: ID del contacto a eliminar.
            c_name: Nombre del contacto para el mensaje de confirmación.
        """
        if messagebox.askyesno("Eliminar", f"¿Eliminar a {c_name}?"):
            db.eliminar_contacto(c_id)
            self.show_main_view()