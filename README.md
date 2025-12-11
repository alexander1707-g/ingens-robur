
# 📚 Agenda Norma Ingens Robur

## 🌟 Descripción General del Proyecto

Este proyecto implementa una **aplicación de escritorio de agenda de contactos** utilizando Python, `tkinter` y la librería `ttkbootstrap` para un diseño moderno. El objetivo principal es ofrecer una herramienta eficiente para la gestión **CRUD (Crear, Leer, Actualizar, Eliminar)** de contactos, manteniendo la persistencia de los datos en una base de datos **SQLite** llamada `agenda.db`.

El proyecto final genera un ejecutable (`.exe`) para su uso directo en entornos de escritorio sin necesidad de instalar Python.

## 📁 Estructura del Proyecto

```
.
├── build/                 # Directorio generado por PyInstaller
├── database/
│   ├── agenda_database.py # Módulo CRUD de SQLite
│   └── agenda.db          # Archivo de la base de datos (se genera al inicio)
├── ejecutable/            # Contiene el producto final de despliegue
│   └── main.exe           # Archivo ejecutable de la aplicación (creado con PyInstaller)
├── models/
│   ├── Contacto.py        # Clase Contacto (entidad)
│   └── Agenda.py          # Clase Agenda (colección y lógica de negocio)
├── ui/
│   ├── interfaz_grafica.py# Clase AgendaApp (Lógica de la UI y navegación)
│   └── logo_empresa.png   # Imagen utilizada en el modal 'Acerca de'
├── utils/
│   └── validaciones.py    # Funciones de validación (nombre, teléfono, email)
├── .gitignore
├── main.py                # Punto de entrada de la aplicación
└── README.md              # Este archivo
```

## 🗃️ Estructura de la Base de Datos (SQLite)

La tabla principal para almacenar los contactos se llama `contactos` en el archivo `agenda.db`.

| Campo | Tipo de Dato | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Identificador único del contacto. |
| `nombre` | `TEXT` | `NOT NULL` | Nombre completo del contacto. |
| `telefono` | `TEXT` | `NOT NULL` | Número de teléfono del contacto. |
| `email` | `TEXT` | `NULL` | Dirección de correo electrónico (opcional). |

## ⚙️ Módulos y Clases Principales

### 1\. Módulo: `database.agenda_database` (Capa de Persistencia)

Este módulo contiene las funciones de bajo nivel para la conectividad y las operaciones CRUD directas sobre la tabla `contactos`.

| Función | Descripción |
| :--- | :--- |
| `get_db_connection()` | Establece y devuelve la conexión a `agenda.db`. Configura las filas para ser accesibles por nombre (`sqlite3.Row`). |
| `crear_tabla()` | Crea la tabla `contactos`. Incluye lógica de migración para actualizar estructuras de tablas antiguas (con campo `notas`) a la nueva estructura de 4 campos. |
| `insertar_contacto(...)` | **CRUD: Create** Inserta un nuevo contacto. |
| `obtener_contactos(...)` | **CRUD: Read** Recupera todos los contactos, permitiendo filtrar por coincidencia parcial en nombre, teléfono o email. |
| `actualizar_contacto(...)` | **CRUD: Update** Modifica los datos de un contacto por su ID. |
| `eliminar_contacto(...)` | **CRUD: Delete** Elimina un contacto por su ID. |
| `obtener_contacto_por_id(...)` | Recupera un único contacto por su ID. |

### 2\. Clase: `Contacto` y `Agenda` (Módulo `models/`)

Clases que modelan las entidades del sistema y su lógica de colección.

| Clase | Atributos Clave | Métodos Clave |
| :--- | :--- | :--- |
| **`Contacto`** | `id`, `nombre`, `telefono`, `email` | `mostrar_info_contacto()` |
| **`Agenda`** | `contactos` (lista de objetos) | `cargar_contactos()`, `buscar_exacta()`, `buscar_parcial()` |

### 3\. Módulo: `utils.validaciones`

Funciones para validar el formato de los datos de entrada.

| Función | Propósito |
| :--- | :--- |
| `validar_nombre(nombre)` | Asegura formato alfabético y longitud mínima. |
| `validar_telefono(telefono)` | Asegura formato numérico (`+` opcional) con longitud entre 7 y 15 dígitos. |
| `validar_email(email)` | Asegura el formato estándar de correo electrónico. |

### 4\. Clase: `AgendaApp` (Módulo `ui.interfaz_grafica.py`)

Clase principal de la aplicación GUI. Gestiona la navegación y la interacción del usuario.

| Funcionalidad | Vistas/Métodos Principales |
| :--- | :--- |
| **Navegación** | `show_main_view()`, `show_contact_detail()`, `show_contact_form()` |
| **Estilos** | Uso de `Config` y `_configure_styles()` para el tema **Navy Profundo** y **Dorado**. |
| **Formulario** | `show_contact_form() -> save()`: Recoge datos, **valida** (`validar_telefono`), y ejecuta CRUD. |
| **Eliminación** | `handle_delete_contact()`: Pide confirmación antes de eliminar el contacto. |

## 🚀 Instrucciones de Ejecución

Existen dos formas de ejecutar la aplicación:

### A. Ejecución Directa (Modo Desarrollo)

Este método requiere tener Python y las dependencias instaladas.

#### Prerrequisitos

  * Python 3.14.0 o superior
  * Bibliotecas: `ttkbootstrap`, `Pillow (PIL)`.

#### Pasos:

1.  Instala las dependencias:
    ```bash
    pip install ttkbootstrap Pillow
    ```
2.  Ejecuta el script principal:
    ```bash
    python main.py
    ```

### B. Ejecución del Binario (Producto Final)

La aplicación está precompilada en un archivo ejecutable utilizando PyInstaller para su fácil distribución.

#### Pasos:

1.  Navega al directorio del ejecutable:
    ```bash
    cd ejecutable/
    ```
2.  Ejecuta directamente el archivo binario:
    ```bash
    ./main.exe
    ```

> **Nota:** Al iniciar por primera vez, la aplicación llama automáticamente a la función `crear_tabla()` para inicializar la base de datos `agenda.db` si esta no existe.