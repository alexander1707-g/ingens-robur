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
    def _init_(self, id, nombre, telefono, email):
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
    def _init_(self, master):
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
        Muestra la ventana informativa del equipo con el diseño exacto de la imagen.
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