"""
Bloque de ejecución principal.

Inicializa la ventana principal de ttkbootstrap (root) y crea una instancia de 
la clase AgendaApp, lo que inicia la interfaz gráfica de usuario y la lógica 
de la aplicación.
"""
from ui.interfaz_grafica import AgendaApp
import ttkbootstrap as ttk

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = AgendaApp(root)
    root.mainloop()