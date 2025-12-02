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