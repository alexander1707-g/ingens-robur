from ui.interfaz_grafica import AgendaApp
import ttkbootstrap as ttk

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = AgendaApp(root)
    root.mainloop()