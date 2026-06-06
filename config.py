import os
import sys

# 1. Aseguramos que Qtile encuentre los archivos locales en su ruta
qtile_path = os.path.expanduser("~/.config/qtile")
if qtile_path not in sys.path:
    sys.path.insert(0, qtile_path)

# 2. Definimos el archivo oculto que guardará nuestra elección
THEME_FILE = os.path.join(qtile_path, ".current_config")

# 3. Configuración por defecto si el archivo no existe (Cargará el estilo Hyprland)
config_a_cargar = "config_default"

# 4. Leemos el archivo selector
if os.path.exists(THEME_FILE):
    try:
        with open(THEME_FILE, "r") as f:
            contenido = f.read().strip()
            # Validamos que solo intente cargar lo que existe
            if contenido in ["config1", "config2", "config3","config_default"]:
                config_a_cargar = contenido
    except Exception:
        # Si hay un error leyendo el archivo, se protege usando la configuración por defecto
        config_a_cargar = "config_default"

# 5. ¡EL TRUCO DE MAGIA!
# Dependiendo del resultado, importamos TODO (*) el contenido del archivo elegido
# Esto incluye las teclas, los layouts, la barra y los hooks de autostart de ese diseño.
if config_a_cargar == "config1":
    print("=== Cargando Entorno Cyberpunk Megacity (config1) ===")
    from config1 import *
elif config_a_cargar == "config2":
    print("=== Cargando Nuevo Diseño (config2) ===")
    from config2 import *
elif config_a_cargar == "config3":
    print("=== Cargando Nuevo Diseño (config3) ===")
    from config3 import *
else:
    # Si todo lo demás falla o si eliges "config_default", te salva la vida el original
    print("=== Cargando Configuración de Respaldo Original ===")
    from config_default import *
