import comandos as cmd
from pathlib import Path
import importlib.util
import getpass
import os
import plugins.history_jump as hj
import subprocess

THEME_FUNC = None
ETERNORC = None
#colores
def color_cmd(nombre):
    if nombre in shell.commands:
        return f"\033[92m{nombre}\033[0m"  # verde (interno)
    return f"\033[91m{nombre}\033[0m"      # rojo (externo)
# ---------------------------
# CARGA .eternorc (alias + config simple)
# ---------------------------
def cargar_eternorc():
    archivo = Path.home() / ".eternorc"

    alias = {}

    if archivo.exists():
        for linea in archivo.read_text().splitlines():
            linea = linea.strip()

            # ignorar vacíos y comentarios
            if not linea or linea.startswith("#"):
                continue

            # formato simple: alias t=tmux
            if linea.startswith("alias "):
                try:
                    _, rest = linea.split(" ", 1)
                    k, v = rest.split("=", 1)
                    alias[k.strip()] = v.strip()
                except ValueError:
                    pass

    return alias

# ---------------------------
# clases
# ---------------------------
class Eternorc:
    def __init__(self):
        self.alias = cargar_eternorc()

class Shell:
    def __init__(self):
        self.commands = {}
        self.state = {"origen": "externo"}

    def register_command(self, name, func):
        self.commands[name] = func

    def run(self, name, *args):
        return self.commands[name](*args)

shell = Shell()
# ---------------------------
# loap-plugins
# ---------------------------
def load_plugins():
    plugin_dir = Path.home() / ".oh-my-eterno" / "plugins"

    for file in plugin_dir.glob("*.py"):
        spec = importlib.util.spec_from_file_location(file.stem, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "load"):
            mod.load(shell)
# ---------------------------
# CARGA SISTEMA DE TEMA
# ---------------------------
def cargar_oh_my_eterno():
    global THEME_FUNC, ETERNORC

    ETERNORC = Eternorc()

    archivo = Path.home() / ".eternorc"
    tema = "promt1"

    if archivo.exists():
        for linea in archivo.read_text().splitlines():
            if linea.startswith("THEME="):
                tema = linea.split("=", 1)[1].strip()

    path = Path.home() / ".oh-my-eterno" / "init.py"

    spec = importlib.util.spec_from_file_location("ome", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mod.cargar()
    THEME_FUNC = mod.get_theme(tema)


# ---------------------------
# PROMPT
# ---------------------------
def obtener_prompt():
    user = getpass.getuser()
    cwd = Path.cwd().name
    user_col = f"\033[32m{user}\033[0m"   # verde
    cwd_col = f"\033[36m{cwd}\033[0m"     # cyan
    if THEME_FUNC:
        return THEME_FUNC(user, cwd)

    return f"{user}@eterno {cwd} >>>"
# ---------------------------
# llamada al system
# ---------------------------
def system(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
# ---------------------------
# EJECUTOR DE COMANDOS
# ---------------------------
def ejecutar(entrada):
    partes = entrada.split()
    if not partes:
        return

    nombre = partes[0]
    print(color_cmd(nombre))
    args = partes[1:]
#plugins
    if nombre in shell.commands:
       shell.state["origen"] = "plugin"
       return shell.commands[nombre](*args)
#comandos.py (externo)
    if hasattr(cmd, nombre):
#       shell.state["origen"] = "comando interno"
        shell.state["origen"] = "comandos.py"
        print(shell.state["origen"])
        func = getattr(cmd, nombre)
        result = func(*args)

        if result:
            if hasattr(result, "stdout") and result.stdout:
                print(result.stdout, end="")
            if hasattr(result, "stderr") and result.stderr:
                print(result.stderr, end="")
        return
#llamada al sistema
    shell.state["origen"] = "comando externo"
    print("🔴 SYSTEM CALL:", entrada)
    result = system(entrada)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return

    # 🔥 ACTUALIZAR HISTORIAL DE DIRECTORIO
    try:
        cwd = os.getcwd()

        if cwd not in hj.STATE["dirs"]:
            hj.STATE["dirs"].append(cwd)

    except Exception:
        pass
    # -----------------------
    # ALIAS (.eternorc)
    # -----------------------
    if ETERNORC and nombre in ETERNORC.alias:
        entrada = ETERNORC.alias[nombre]
        partes = entrada.split()
        nombre = partes[0]
        args = partes[1:]

    # -----------------------
    # COMANDOS NATIVOS
    # -----------------------
    if hasattr(cmd, nombre):
        func = getattr(cmd, nombre)

        try:
            result = func(*args)

            if result:
                if hasattr(result, "stdout") and result.stdout:
                    print(result.stdout, end="")
                if hasattr(result, "stderr") and result.stderr:
                    print(result.stderr, end="")

        except TypeError:
            print("Argumentos inválidos")
        return

    # -----------------------
    # FALLBACK SHELL
    # -----------------------
    import subprocess

    result = subprocess.run(
        entrada,
        shell=True,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")


# ---------------------------
# INIT
# ---------------------------
cargar_oh_my_eterno()
load_plugins()

# ---------------------------
# LOOP PRINCIPAL
# ---------------------------
while True:
    try:
        entrada = input(obtener_prompt() + " ")

        if entrada.strip() == "exit":
            break

        ejecutar(entrada)

    except KeyboardInterrupt:
        print("\n")
    except EOFError:
        break
