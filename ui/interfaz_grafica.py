import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame
import os # Importado para verificar si existe la imagen

# --- 1. DEFINICIÓN DE CONSTANTES Y COLORES ---
class Config:
    COLOR_NAVY_PROFUNDO = "#1A2B4C"  # Azul Dominante App Principal
    COLOR_DORADO = "#C59D5F"         # Dorado/Acento
    COLOR_CREMA_FONDO = "#F5F5F0"    # Fondo Suave
    COLOR_BLANCO = "#FFFFFF"
    
    # --- PALETA EXACTA DE LA IMAGEN "EQUIPO DE TRABAJO" ---
    TEAM_BG_DARK = "#0C1524"         # Azul muy oscuro (fondo derecha)
    TEAM_BG_CREAM = "#F2F0E4"        # Crema (fondo logo izquierda)
    TEAM_TEXT_GOLD = "#D4AF37"       # Dorado brillante para textos
    TEAM_TEXT_WHITE = "#FFFFFF"
    
    # Iconos Aplicación
    ICON_ATRAS = "⬅"
    ICON_GUARDAR = "💾"
    ICON_LLAMAR = "📞"
    ICON_MENSAJE = "✉"
    ICON_EDITAR = "✏"
    ICON_BUSCAR = "🔍"
    ICON_ELIMINAR = "🗑"
    ICON_INFO = "ℹ" # Icono para el botón del equipo

# --- 2. CLASE DE MOCKUP PARA LA INTERFAZ ---
class MockContact:
    def __init__(self, id, nombre, telefono, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def get_initials(self):
        parts = self.nombre.split()
        if not parts: return "NN"
        return "".join([p[0].upper() for p in parts[:2]])

# --- 3. DATOS DE EJEMPLO ---
MOCK_CONTACTS = [
    MockContact(1, "Juan Pérez (Mockup)", "555-1234", "juan.perez@ejemplo.com"),
    MockContact(2, "María González (Mockup)", "555-5678", "maria.g@ejemplo.com"),
    MockContact(3, "Carlos Ruiz (Mockup)", "555-9012", "carlos.ruiz@ejemplo.com")
]

class AgendaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AGENDA NORMA INGENS ROBUR - Escritorio")
        self.master.geometry("1000x700")
        
        # Inicialización de variables y estilos
        self.selected_contact = None
        self._configure_styles()
        self.show_main_view()
        
    def _configure_styles(self):
        """Configura los estilos personalizados de ttkbootstrap."""
        self.style = ttk.Style()
        self.style.configure('Main.TFrame', background=Config.COLOR_CREMA_FONDO)
        self.style.configure('Header.TFrame', background=Config.COLOR_NAVY_PROFUNDO)
        self.style.configure('Header.TLabel', background=Config.COLOR_NAVY_PROFUNDO, foreground=Config.COLOR_BLANCO, font=('Helvetica', 18, 'bold'))
        self.style.configure('Gold.TButton', background=Config.COLOR_DORADO, foreground=Config.COLOR_NAVY_PROFUNDO, font=('Helvetica', 12, 'bold'))
        self.style.map('Gold.TButton', background=[('active', '#b08d55')]) 
        self.style.configure('Navy.TButton', background=Config.COLOR_NAVY_PROFUNDO, foreground=Config.COLOR_DORADO, font=('Helvetica', 12, 'bold'))
        
    def _clear_view(self):
        """Limpia todos los widgets del frame principal."""
        for widget in self.master.winfo_children():
            widget.destroy()
            
    # --- LÓGICA DE MODAL GENERAL (APP) ---
    def _show_custom_modal(self, title, message, is_confirmation=False, confirm_callback=None):
        self.overlay = tk.Frame(self.master, bg=Config.COLOR_NAVY_PROFUNDO)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()
        
        modal_width = 400
        modal_frame = ttk.Frame(self.overlay, bootstyle='light', padding=30)
        modal_frame.place(relx=0.5, rely=0.5, anchor='center', width=modal_width)
        
        ttk.Label(modal_frame, text=title, font=('Helvetica', 14, 'bold'), 
                  foreground=Config.COLOR_NAVY_PROFUNDO, bootstyle="primary").pack(pady=(0, 10))
        ttk.Separator(modal_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(modal_frame, text=message, font=('Helvetica', 10), wraplength=modal_width-60, 
                  justify=tk.CENTER).pack(pady=(10, 20), expand=True)

        def close_modal():
            self.overlay.destroy()
            
        button_frame = ttk.Frame(modal_frame)
        button_frame.pack(pady=10)
        
        if is_confirmation:
            def confirmed():
                close_modal()
                if confirm_callback:
                    confirm_callback()
            ttk.Button(button_frame, text="Confirmar", command=confirmed, 
                       bootstyle="danger" if "Eliminar" in title else "success").pack(side='left', padx=10, ipadx=10)
            ttk.Button(button_frame, text="Cancelar", command=close_modal, bootstyle="secondary").pack(side='left', padx=10, ipadx=10)
        else:
            ttk.Button(button_frame, text="Aceptar", command=close_modal, bootstyle="primary").pack(padx=10, ipadx=20)

    def _show_info_modal(self, title, message):
        self._show_custom_modal(title, message, is_confirmation=False)
        
    def _show_confirmation_modal(self, title, message, callback_on_confirm):
        self._show_custom_modal(title, message, is_confirmation=True, confirm_callback=callback_on_confirm)


# ##################################################################################
    # ### SECCIÓN NUEVA: LÓGICA DE LA VENTANA DE EQUIPO (SOLICITUD DE IMAGEN)       ###
    # ##################################################################################
    
    def _show_team_modal(self):
        """
        Muestra la ventana informativa del equipo de trabajo
        """
        # 1. Overlay (Fondo oscuro total)
        team_overlay = tk.Frame(self.master, bg=Config.TEAM_BG_DARK)
        team_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        team_overlay.lift()

        # Botón para cerrar (X en la esquina superior derecha)
        close_btn = tk.Button(team_overlay, text="✕", bg=Config.TEAM_BG_DARK, fg=Config.COLOR_BLANCO,
                              font=("Arial", 16, "bold"), bd=0, cursor="hand2",
                              command=team_overlay.destroy)
        close_btn.place(relx=0.97, rely=0.02, anchor='ne')

        # 2. Contenedor Principal (Centrado)
        # Usamos un Frame que contendrá las dos mitades (Izquierda y Derecha)
        container = tk.Frame(team_overlay, bg=Config.TEAM_BG_DARK)
        container.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)

        # --- COLUMNA IZQUIERDA (Logo y Fondo Crema) ---
        left_frame = tk.Frame(container, bg=Config.TEAM_BG_CREAM)
        left_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        # Intentar cargar la imagen "logo_empresa.png"
        try:
            # NOTA: Asegúrate de tener 'logo_empresa.png' en la misma carpeta del script
            if os.path.exists("logo_empresa.png"):
                self.logo_img = tk.PhotoImage(file="logo_empresa.png")
                # Redimensionar si es muy grande (opcional, ajusta subsample según tamaño real)
                # self.logo_img = self.logo_img.subsample(2, 2) 
                logo_label = tk.Label(left_frame, image=self.logo_img, bg=Config.TEAM_BG_CREAM)
                logo_label.pack(expand=True)
            else:
                # Placeholder si no hay imagen
                tk.Label(left_frame, text="[AQUÍ VA EL LOGO]\nGuarda tu imagen como\n'logo_empresa.png'", 
                         bg=Config.TEAM_BG_CREAM, fg=Config.COLOR_NAVY_PROFUNDO, font=("Helvetica", 12)).pack(expand=True)
        except Exception as e:
             tk.Label(left_frame, text=f"Error cargando imagen:\n{e}", bg=Config.TEAM_BG_CREAM).pack(expand=True)

        tk.Label(left_frame, text="NORMA INGENS ROBUR", font=("Times New Roman", 16, "bold"), 
                 bg=Config.TEAM_BG_CREAM, fg=Config.COLOR_NAVY_PROFUNDO).place(relx=0.5, rely=0.85, anchor='center')


        # --- COLUMNA DERECHA (Información del Equipo - Fondo Azul Oscuro) ---
        right_frame = tk.Frame(container, bg=Config.TEAM_BG_DARK)
        right_frame.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)
        
        # Título superior "EQUIPO DE TRABAJO" con la barra
        title_box = tk.Frame(right_frame, bg=Config.TEAM_BG_DARK, highlightbackground=Config.COLOR_DORADO, highlightthickness=1)
        title_box.pack(fill='x', padx=40, pady=(40, 20))
        
        # Icono corona pequeño y texto
        tk.Label(title_box, text="👑", bg=Config.TEAM_BG_DARK, fg=Config.COLOR_DORADO, font=("Arial", 14)).pack(side='left', padx=10, pady=10)
        tk.Label(title_box, text="EQUIPO DE TRABAJO", bg=Config.TEAM_BG_DARK, fg=Config.COLOR_BLANCO, font=("Helvetica", 14)).pack(side='left', pady=10)

        # Función helper para crear los bloques de texto del equipo
        def create_role_block(parent, icon_char, role_title, names_list):
            block = tk.Frame(parent, bg=Config.TEAM_BG_DARK)
            block.pack(pady=15)
            
            # Icono circular simulado
            tk.Label(block, text=icon_char, font=("Segoe UI Emoji", 24), bg=Config.TEAM_BG_DARK, fg=Config.TEAM_TEXT_GOLD).pack()
            
            # Título del Rol
            tk.Label(block, text=role_title, font=("Helvetica", 12, "bold"), bg=Config.TEAM_BG_DARK, fg=Config.COLOR_BLANCO).pack(pady=(5, 5))
            
            # Nombres
            for name in names_list:
                tk.Label(block, text=name, font=("Helvetica", 11, "bold"), bg=Config.TEAM_BG_DARK, fg=Config.COLOR_BLANCO).pack()

        # Bloque 1: Product Owner
        create_role_block(right_frame, "👤", "PRODUCT OWNER", ["GENDER ALEXANDER CAMACHO GARCIA"])
        
        # Bloque 2: Scrum Master
        create_role_block(right_frame, "🌱", "SCRUM MASTER", ["YULY PAOLA FLOREZ LOPEZ"])
        
        # Bloque 3: Equipo de Desarrollo
        create_role_block(right_frame, "🚀", "EQUIPO DE DESARROLLO", ["EMMANUEL DIAZ GUTIERREZ", "ALFREDO MANUEL RODRIGUEZ LUQUETA"])

    # ##################################################################################
    # ### FIN SECCIÓN NUEVA                                                         ###
    # ##################################################################################
    def _get_current_contacts(self, search_text=None):
        if search_text and search_text != "Buscar contacto...":
            return [c for c in MOCK_CONTACTS if search_text.lower() in c.nombre.lower()]
        return MOCK_CONTACTS

    # --- VISTA 1: LISTA PRINCIPAL ---
    def show_main_view(self):
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)
        
        # 1. ENCABEZADO SUPERIOR
        header_frame = ttk.Frame(self.master, style='Header.TFrame', height=70, padding=10)
        header_frame.pack(fill='x')
        
        ttk.Label(header_frame, text="👑", style='Header.TLabel', foreground=Config.COLOR_DORADO).pack(side='left', padx=15)
        ttk.Label(header_frame, text="AGENDA NORMA INGENS ROBUR", style='Header.TLabel').pack(side='left', padx=20)
        
        # 2. BARRA DE BÚSQUEDA
        search_frame = ttk.Frame(self.master, style='Main.TFrame', padding=20)
        search_frame.pack(fill='x')
        
        search_var = tk.StringVar(value="Buscar contacto...")
        search_entry = ttk.Entry(search_frame, textvariable=search_var, font=('Helvetica', 12), width=50, bootstyle="primary")
        
        def on_search(event=None):
            self._refresh_list_container(scrolled_frame, self._get_current_contacts(search_var.get()))
            
        def clear_placeholder(event):
            if search_entry.get() == "Buscar contacto...":
                search_entry.delete(0, END)
                search_entry.config(foreground='black')
            
        def reset_placeholder(event):
            if not search_entry.get():
                search_entry.insert(0, "Buscar contacto...")
                search_entry.config(foreground='gray')
            
        search_entry.bind("<FocusIn>", clear_placeholder)
        search_entry.bind("<FocusOut>", reset_placeholder)
        search_entry.bind("<Return>", on_search)
        search_entry.pack(pady=5, ipady=5, side='left', expand=True, padx=(0, 10))
        search_entry.config(foreground='gray')
        
        ttk.Button(search_frame, text=Config.ICON_BUSCAR, command=on_search, bootstyle="primary").pack(side='left')

        # 3. CONTENEDOR DE LA LISTA
        list_container = ttk.Frame(self.master, style='Main.TFrame', padding=(50, 0, 50, 0))
        list_container.pack(fill='both', expand=True)

        scrolled_frame = ScrolledFrame(list_container, autohide=True, bootstyle="light")
        scrolled_frame.pack(fill='both', expand=True)
        scrolled_frame.container.configure(style='Main.TFrame')
        
        # 4. ITERAR Y CREAR TARJETAS
        self._refresh_list_container(scrolled_frame, self._get_current_contacts())
            
        # 5. BOTÓN FLOTANTE (AGREGAR)
        add_button = tk.Button(self.master, text="+", bg=Config.COLOR_DORADO, fg=Config.COLOR_NAVY_PROFUNDO, 
                               font=('Arial', 24, 'bold'), width=3, height=1, bd=0, relief='raised',
                               cursor="hand2", command=self.show_new_contact_form)
        add_button.place(relx=0.95, rely=0.95, anchor='se')

        # ### NUEVO CODIGO: BOTÓN FLOTANTE INFO EQUIPO (Inferior Izquierda) ###
        info_button = tk.Button(self.master, text=Config.ICON_INFO, bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_DORADO,
                                font=('Arial', 20, 'bold'), width=3, height=1, bd=0, relief='raised',
                                cursor="hand2", command=self._show_team_modal)
        info_button.place(relx=0.03, rely=0.95, anchor='sw')
        # ### FIN NUEVO CODIGO ###

    def _refresh_list_container(self, list_container, contacts_list):
            for widget in list_container.container.winfo_children():
                widget.destroy()

            if not contacts_list:
                ttk.Label(list_container.container, text="No se encontraron contactos.", style='Main.TFrame', font=('Helvetica', 14)).pack(pady=50)
            else:
                for contact in contacts_list:
                    self.create_contact_card(list_container, contact)

    def create_contact_card(self, parent_widget, contact):
        card = tk.Frame(parent_widget.container, bg=Config.COLOR_BLANCO, padx=20, pady=15, 
                        relief='flat', borderwidth=1, 
                        highlightbackground=Config.COLOR_DORADO, highlightthickness=1)
        card.pack(fill='x', padx=10, pady=8)
        
        card.bind("<Button-1>", lambda e: self.show_contact_detail(contact))
        
        lbl_initials = tk.Label(card, text=contact.get_initials(), bg=Config.COLOR_DORADO, fg=Config.COLOR_NAVY_PROFUNDO, 
                                font=('Helvetica', 14, 'bold'), width=5, height=2)
        lbl_initials.pack(side='left', padx=(0, 20))
        lbl_initials.bind("<Button-1>", lambda e: self.show_contact_detail(contact))

        info_frame = tk.Frame(card, bg=Config.COLOR_BLANCO) 
        info_frame.pack(side='left', fill='both', expand=True)
        
        lbl_name = ttk.Label(info_frame, text=contact.nombre, font=('Helvetica', 14, 'bold'), foreground=Config.COLOR_NAVY_PROFUNDO, background=Config.COLOR_BLANCO)
        lbl_name.pack(anchor='w')
        
        lbl_detail = ttk.Label(info_frame, text=contact.email, font=('Helvetica', 10), foreground='gray', background=Config.COLOR_BLANCO)
        lbl_detail.pack(anchor='w')

        for w in [info_frame, lbl_name, lbl_detail]:
            w.bind("<Button-1>", lambda e: self.show_contact_detail(contact))

        ttk.Button(card, text=Config.ICON_LLAMAR, bootstyle="outline-primary", width=3, 
                   command=lambda: self._show_info_modal("Acción", f"Simulando llamada a {contact.telefono}")).pack(side='right', padx=5)
        ttk.Button(card, text=Config.ICON_MENSAJE, bootstyle="outline-warning", width=3,
                   command=lambda: self._show_info_modal("Acción", f"Abriendo correo para {contact.email}")).pack(side='right', padx=5)

    def show_new_contact_form(self):
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)
        self._create_contact_form_view(title="NUEVO CONTACTO")

    def show_contact_detail(self, contact):
        self._clear_view()
        self.selected_contact = contact
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)

        header_frame = ttk.Frame(self.master, style='Header.TFrame', height=70, padding=10)
        header_frame.pack(fill='x')
        tk.Button(header_frame, text=f"{Config.ICON_ATRAS} Volver", command=self.show_main_view, bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_BLANCO, bd=0, font=('Helvetica', 12)).pack(side='left', padx=15)
        ttk.Label(header_frame, text="DETALLE", style='Header.TLabel').pack(side='left', padx=50)
        ttk.Button(header_frame, text=f"{Config.ICON_EDITAR} Editar", style='Gold.TButton', command=lambda: self.show_edit_contact_form(contact)).pack(side='right', padx=15)

        profile_frame = tk.Frame(self.master, bg=Config.COLOR_BLANCO, padx=50, pady=30, relief='raised')
        profile_frame.pack(pady=30, padx=50, fill='x')
        tk.Label(profile_frame, text=contact.get_initials(), bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_DORADO, font=('Helvetica', 35, 'bold'), width=4, height=2).pack(pady=10)
        ttk.Label(profile_frame, text=contact.nombre, font=('Helvetica', 22, 'bold'), background=Config.COLOR_BLANCO, foreground=Config.COLOR_NAVY_PROFUNDO).pack(pady=5)
        
        action_frame = tk.Frame(profile_frame, bg=Config.COLOR_BLANCO, pady=20)
        action_frame.pack()
        ttk.Button(action_frame, text=f"{Config.ICON_LLAMAR} Llamar", style='Gold.TButton', width=15, 
                   command=lambda: self._show_info_modal("Acción", f"Simulando llamada a {contact.telefono}")).pack(side='left', padx=10)
        ttk.Button(action_frame, text=f"{Config.ICON_MENSAJE} Correo", style='Gold.TButton', width=15,
                   command=lambda: self._show_info_modal("Acción", f"Abriendo correo para {contact.email}")).pack(side='left', padx=10)

        info_frame = ttk.Frame(self.master, style='Main.TFrame', padding=(50, 20, 50, 20))
        info_frame.pack(fill='both', expand=True)

        def create_detail_row(label, value):
            f = ttk.Frame(info_frame, style='Main.TFrame')
            f.pack(fill='x', pady=8)
            ttk.Label(f, text=label, font=('Helvetica', 10, 'bold'), foreground=Config.COLOR_NAVY_PROFUNDO, background=Config.COLOR_CREMA_FONDO).pack(anchor='w')
            ttk.Label(f, text=value, font=('Helvetica', 16), background=Config.COLOR_CREMA_FONDO).pack(anchor='w')
            ttk.Separator(f, orient='horizontal').pack(fill='x', pady=5)

        create_detail_row("ID de Contacto", str(contact.id))
        create_detail_row("Teléfono Móvil", contact.telefono)
        create_detail_row("Correo Electrónico", contact.email)

        ttk.Button(self.master, text=f"{Config.ICON_ELIMINAR} Eliminar Contacto", bootstyle="danger", width=30, 
                   command=lambda: self.handle_delete_contact(contact)).pack(pady=20)
                   
    def show_edit_contact_form(self, contact):
        self._clear_view()
        self.master.configure(bg=Config.COLOR_CREMA_FONDO)
        self._create_contact_form_view(title="EDITAR CONTACTO", contact_to_edit=contact)

    def _create_contact_form_view(self, title, contact_to_edit=None):
        header_frame = ttk.Frame(self.master, style='Header.TFrame', height=70, padding=10)
        header_frame.pack(fill='x')
        tk.Button(header_frame, text=f"{Config.ICON_ATRAS} Volver", command=self.show_main_view, bg=Config.COLOR_NAVY_PROFUNDO, fg=Config.COLOR_BLANCO, bd=0, font=('Helvetica', 12)).pack(side='left', padx=15)
        ttk.Label(header_frame, text=title, style='Header.TLabel').pack(side='left', padx=50)

        form_container = ttk.Frame(self.master, style='Main.TFrame', padding=40)
        form_container.pack(fill='both', expand=True)
        
        self.form_vars = {
            "nombre": tk.StringVar(value=contact_to_edit.nombre if contact_to_edit else ""), 
            "telefono": tk.StringVar(value=contact_to_edit.telefono if contact_to_edit else ""), 
            "email": tk.StringVar(value=contact_to_edit.email if contact_to_edit else "")
        }
        
        def create_bootstrap_input(parent, label_text, var):
            container = ttk.Frame(parent, style='Main.TFrame')
            container.pack(fill='x', pady=10)
            ttk.Label(container, text=label_text, font=('Helvetica', 11, 'bold'), background=Config.COLOR_CREMA_FONDO, foreground=Config.COLOR_NAVY_PROFUNDO).pack(anchor='w')
            entry = ttk.Entry(container, textvariable=var, font=('Helvetica', 12), bootstyle="primary")
            entry.pack(fill='x', pady=(5, 0))
            return entry

        create_bootstrap_input(form_container, "Nombre Completo", self.form_vars["nombre"])
        create_bootstrap_input(form_container, "Teléfono", self.form_vars["telefono"])
        create_bootstrap_input(form_container, "Correo Electrónico", self.form_vars["email"])

        save_command = lambda: self.handle_save_contact(contact_to_edit)
        ttk.Button(form_container, text=f"{Config.ICON_GUARDAR} GUARDAR CONTACTO", style='Gold.TButton', width=30, 
                   command=save_command).pack(pady=30)
                   
        if contact_to_edit:
             ttk.Label(form_container, text=f"ID de Contacto: {contact_to_edit.id}", font=('Helvetica', 9), background=Config.COLOR_CREMA_FONDO, foreground='gray').pack(pady=5)

    def handle_save_contact(self, contact_to_edit=None):
        name = self.form_vars["nombre"].get().strip()
        phone = self.form_vars["telefono"].get().strip()
        email = self.form_vars["email"].get().strip()

        if not name or not phone:
            self._show_info_modal("Error de Validación", "Nombre y Teléfono son obligatorios.")
            return

        if contact_to_edit:
            self._show_info_modal("CONEXIÓN PENDIENTE", f"MODIFICAR Contacto (ID: {contact_to_edit.id}) listo para implementar.")
        else:
            self._show_info_modal("CONEXIÓN PENDIENTE", f"INSERTAR Nuevo Contacto ({name}) listo para implementar.")
        
        self.show_main_view() 

    def handle_delete_contact(self, contact):
        def perform_deletion():
            self._show_info_modal("CONEXIÓN PENDIENTE", f"ELIMINAR Contacto con ID: {contact.id} listo para implementar.")
            self.show_main_view()

        self._show_confirmation_modal(
            "Eliminar Contacto", 
            f"¿Está seguro de que desea eliminar a {contact.nombre} (ID: {contact.id})? Esta acción es irreversible.",
            perform_deletion)


if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = AgendaApp(root)
    root.mainloop()