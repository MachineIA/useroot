#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

# Menú visual solamente
# Aquí luego puedes agregar lo que quieras mostrar

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
██╗   ██╗██████╗ 
██║   ██║██╔══██╗
██║   ██║██████╔╝
██║   ██║██╔══██╗
╚██████╔╝██║  ██║
 ╚═════╝ ╚═╝  ╚═╝
{RESET}
"""

# =====================================================
# FUNCIONES
# =====================================================


def clear():
    os.system("clear")



def pause():
    """
    Evita errores en entornos sin stdin.
    """

    if sys.stdin.isatty():
        try:
            input(f"\n{CYAN}Presiona ENTER para continuar...{RESET}")
        except OSError:
            pass



def safe_input(text):
    """
    Input seguro para evitar OSError: [Errno 29] I/O error
    """

    if not sys.stdin.isatty():
        print(f"\n{RED}[!] No hay terminal interactiva disponible.{RESET}")
        return "0"

    try:
        return input(text)
    except OSError:
        print(f"\n{RED}[!] Error leyendo entrada del usuario.{RESET}")
        return "0"



def show_menu():
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{GREEN}              UR TERMINAL{RESET}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    print(f"{YELLOW}⚡ Sistema listo{RESET}")
    print(f"{YELLOW}⚡ Qtile cargado{RESET}")
    print(f"{YELLOW}⚡ Zsh activo{RESET}")
    print(f"{YELLOW}⚡ Alias personalizados cargados{RESET}")



# =====================================================
# TESTS BÁSICOS
# =====================================================


def test_python_version():
    assert isinstance(get_python_version(), str)



def test_kernel():
    assert isinstance(get_kernel(), str)


# =====================================================
# FASTFETCH
# =====================================================


def get_uptime():
    try:
        with open("/proc/uptime") as f:
            seconds = float(f.readline().split()[0])

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)

        return f"{hours}h {minutes}m"
    except:
        return "Unknown"



def get_memory():
    try:
        meminfo = {}

        with open("/proc/meminfo") as f:
            for line in f:
                key, value = line.split(":")
                meminfo[key] = int(value.strip().split()[0])

        total = meminfo["MemTotal"] / 1024 / 1024
        available = meminfo["MemAvailable"] / 1024 / 1024
        used = total - available

        return f"{used:.2f} GiB / {total:.2f} GiB"
    except:
        return "Unknown"



def get_kernel():
    return os.uname().release



def get_shell():
    return os.environ.get("SHELL", "Unknown")



def get_user_host():
    return f"{os.environ.get('USER', 'user')}@{os.uname().nodename}"



def get_python_version():
    return sys.version.split()[0]



def get_packages():
    try:
        result = subprocess.check_output(
            ["pacman", "-Q"],
            text=True
        )

        return str(len(result.splitlines()))
    except:
        return "Unknown"



def show_system_info():
    print(BANNER)

    left = [
        f"{MAGENTA}╭──────────────────────────────╮{RESET}",
        f"{MAGENTA}│{RESET} User     : {GREEN}{get_user_host()}{RESET}",
        f"{MAGENTA}│{RESET} OS       : {CYAN}Arch Linux{RESET}",
        f"{MAGENTA}│{RESET} Kernel   : {YELLOW}{get_kernel()}{RESET}",
        f"{MAGENTA}│{RESET} Shell    : {WHITE}{get_shell()}{RESET}",
        f"{MAGENTA}│{RESET} Python   : {GREEN}{get_python_version()}{RESET}",
        f"{MAGENTA}│{RESET} Packages : {BLUE}{get_packages()}{RESET}",
        f"{MAGENTA}│{RESET} Uptime   : {CYAN}{get_uptime()}{RESET}",
        f"{MAGENTA}│{RESET} Memory   : {RED}{get_memory()}{RESET}",
        f"{MAGENTA}╰──────────────────────────────╯{RESET}",
    ]

    for line in left:
        print(line)


# =====================================================
# MAIN LOOP
# =====================================================

clear()
show_system_info()
show_menu()
