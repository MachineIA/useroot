import os
import subprocess
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

SCRIPTS = {
    "1": ("backuphome.py", "ejemplo1.py"),
    "2": ("bachuppaqued.py", "ejemplo2.py"),
    "3": ("ejemplo3", "ejemplo3.py"),
}

SCRIPTS_DIR = Path.home() / "scripts"

# =====================================================
# COLORES ANSI
# =====================================================

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# =====================================================
# ASCII ART
# =====================================================

BANNER = f"""
{MAGENTA}
██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
███████╗██║     ██████╔╝██║██████╔╝   ██║
╚════██║██║     ██╔══██╗██║██╔═══╝    ██║
███████║╚██████╗██║  ██║██║██║        ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
{RESET}
"""

# =====================================================
# FUNCIONES
# =====================================================


def clear():
    os.system("clear")



def show_menu():
    clear()
    print(BANNER)

    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{GREEN}        SCRIPT MANAGER - CYBERPUNK MODE{RESET}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

    for key, (name, _) in SCRIPTS.items():
        print(f"{YELLOW}[{key}]{RESET} {WHITE}{name}{RESET}")

    print(f"\n{RED}[0]{RESET} Salir\n")



def run_script(script_name):
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        print(f"\n{RED}[!] Script no encontrado:{RESET} {script_path}\n")
        input(f"{CYAN}Presiona ENTER para continuar...{RESET}")
        return

    print(f"\n{GREEN}[+] Ejecutando:{RESET} {script_name}\n")

    try:
        subprocess.run(["python", str(script_path)])
    except Exception as e:
        print(f"\n{RED}[!] Error:{RESET} {e}\n")

    input(f"\n{CYAN}Presiona ENTER para volver al menú...{RESET}")


# =====================================================
# MAIN LOOP
# =====================================================

while True:
    show_menu()

    option = input(f"{MAGENTA}Selecciona una opción > {RESET}")

    if option == "0":
        clear()
        print(f"{GREEN}Hasta luego, hacker 😎{RESET}\n")
        break

    elif option in SCRIPTS:
        _, script_file = SCRIPTS[option]
        run_script(script_file)

    else:
        print(f"\n{RED}[!] Opción inválida{RESET}\n")
        input(f"{CYAN}Presiona ENTER para continuar...{RESET}")
