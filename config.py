import os
import sys

# 1. Aseguramos que Qtile encuentre los archivos locales en su ruta
qtile_path = os.path.expanduser("~/.config/qtile")
if qtile_path not in sys.path:
    sys.path.insert(0, qtile_path)

# 2. Archivo oculto que guarda la elección del tema
THEME_FILE = os.path.join(qtile_path, ".current_config")

# 3. Configuración por defecto de respaldo
config_a_cargar = "config_default"

# 4. Leemos el archivo selector y validamos dinámicamente
if os.path.exists(THEME_FILE):
    try:
        with open(THEME_FILE, "r") as f:
            contenido = f.read().strip()
            
            # Verificamos si existe el archivo físico (ej: config1.py) antes de importarlo
            archivo_py = os.path.join(qtile_path, f"{contenido}.py")
            if os.path.exists(archivo_py):
                config_a_cargar = contenido
            else:
                print(f"⚠️ [Qtile] {contenido}.py no existe. Usando respaldo.")
    except Exception:
        config_a_cargar = "config_default"

# 5. Importación dinámica del entorno elegido
print(f"=== [Qtile] Cargando Entorno Activo: {config_a_cargar} ===")

if config_a_cargar == "config1":
    from config1 import *
elif config_a_cargar == "config2":
    from config2 import *
elif config_a_cargar == "config3":
    from config3 import *
else:
    from config_default import *
