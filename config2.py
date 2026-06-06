import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# ----------------------------------------------------------------------
# PALETA DE COLORES (Estilo Cyberpunk / Neon Hacker / Hyprland)
# ----------------------------------------------------------------------
colors = {
    "bg":      "#1e1e2e",  # Fondo oscuro (Catppuccin Mocha)
    "fg":      "#cdd6f4",  # Texto claro
    "active":  "#00f5d4",  # Neon Cyan/Turquesa
    "inactive":"#585b70",  # Gris apagado
    "accent":  "#7b2cbf",  # Morado Hacker
    "magenta": "#ff007f",  # Rosa/Neon Magenta
    "yellow":  "#ffee55",  # Amarillo Cyber
    "green":   "#00ff66",  # Verde Matrix/Hacker
    "blue":    "#00b4d8",  # Azul eléctrico
}

mod = "mod4"  # Tecla Super / Windows
terminal = "kitty"

keys = [
    # Atajos básicos de movimiento
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Mover ventanas
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Shuffle window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Shuffle window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Shuffle window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Shuffle window up"),
    
    # Cambiar tamaño (Estilo Hyprland)
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Control del entorno
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# ----------------------------------------------------------------------
# GRUPOS / WORKSPACES (Iconos coloridos estilo Netbrain)
# ----------------------------------------------------------------------
groups = [
    Group("1", label=" 󰈹 ", matches=[Match(wm_class="firefox")]),
    Group("2", label=" 󰆍 "),
    Group("3", label=" 󰅨 "),
    Group("4", label=" 󱓞 "),
    Group("5", label=" 󰓇 "),
    Group("6", label=" 󰍡 "),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Move window to group {i.name}"),
    ])

# ----------------------------------------------------------------------
# LAYOUTS (Bordes gruesos, Gaps amplios y esquinas tipo Hyprland)
# ----------------------------------------------------------------------
layout_theme = {
    "border_width": 3,
    "margin": 12,  # El truco para que parezca Hyprland son los Gaps grandes
    "border_focus": colors["active"],
    "border_normal": colors["bg"],
}

layouts = [
    layout.Columns(**layout_theme, border_focus_stack=colors["magenta"], num_columns=2),
    layout.Max(margin=8),
    layout.Floating(**layout_theme),
]

# ----------------------------------------------------------------------
# BARRA DE ESTADO (Ultra colorida con "Pills/Cápsulas")
# ----------------------------------------------------------------------
def init_widgets_list():
    widgets_list = [
        # Icono de inicio / Logo Hacker
        widget.TextBox(
            text=" 󰣇 ",
            font="MesloLGS NF",
            fontsize=22,
            foreground=colors["active"],
            background=colors["bg"],
            mouse_callbacks={'Button1': lazy.spawn("rofi -show drun")},
        ),
        widget.Spacer(length=5),
        
        # Workspaces / Grupos
        widget.GroupBox(
            font="MesloLGS NF",
            fontsize=16,
            margin_y=3,
            margin_x=4,
            padding_y=5,
            padding_x=5,
            active=colors["active"],
            inactive=colors["inactive"],
            rounded=True,
            highlight_color=colors["accent"],
            highlight_method="line",
            this_current_screen_border=colors["magenta"],
            block_highlight_text_color=colors["fg"],
        ),
        widget.Prompt(foreground=colors["yellow"]),
        widget.WindowName(foreground=colors["fg"], fontsize=12, padding=10),
        
        # --- BLOQUES COLORIDOS (Estilo Píldoras) ---
        
        # Bloque CPU
        widget.TextBox(text="", fontsize=24, foreground=colors["accent"], padding=0),
        widget.TextBox(text="󰍛 ", fontsize=14, foreground=colors["bg"], background=colors["accent"], padding=0),
        widget.CPU(format='{load_percent}%', background=colors["accent"], foreground=colors["bg"], font="MesloLGS NF"),
        widget.TextBox(text="", fontsize=24, foreground=colors["accent"], padding=0),
        widget.Spacer(length=8),

        # Bloque Memoria RAM
        widget.TextBox(text="", fontsize=24, foreground=colors["blue"], padding=0),
        widget.TextBox(text="󰘚 ", fontsize=14, foreground=colors["bg"], background=colors["blue"], padding=0),
        widget.Memory(format='{MemUsed:.0f}{mm}', background=colors["blue"], foreground=colors["bg"]),
        widget.TextBox(text="", fontsize=24, foreground=colors["blue"], padding=0),
        widget.Spacer(length=8),

        # Bloque Red / Internet
        widget.TextBox(text="", fontsize=24, foreground=colors["magenta"], padding=0),
        widget.TextBox(text="󰖩 ", fontsize=14, foreground=colors["bg"], background=colors["magenta"], padding=0),
        widget.Net(interface="wlan0", format='{down:.0f}↓↑{up:.0f}', background=colors["magenta"], foreground=colors["bg"]),
        widget.TextBox(text="", fontsize=24, foreground=colors["magenta"], padding=0),
        widget.Spacer(length=8),

        # Bloque Reloj / Hora
        widget.TextBox(text="", fontsize=24, foreground=colors["green"], padding=0),
        widget.TextBox(text=" ", fontsize=14, foreground=colors["bg"], background=colors["green"], padding=0),
        widget.Clock(format='%I:%M %p', background=colors["green"], foreground=colors["bg"]),
        widget.TextBox(text="", fontsize=24, foreground=colors["green"], padding=0),
        widget.Spacer(length=5),
        
        # System Tray (Iconos de apps de fondo)
        widget.Systray(padding=5),
        widget.Spacer(length=5),
    ]
    return widgets_list

screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            28,  # Altura de la barra
            background=colors["bg"],
            opacity=0.90,  # Transparencia genial tipo Hyprland
            margin=[8, 12, 0, 12]  # Margen externo [arriba, derecha, abajo, izquierda] para que flote
        ),
    ),
]

# ----------------------------------------------------------------------
# CONFIGURACIONES EXTRAS & COMPORTAMIENTO
# ----------------------------------------------------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
    ],
    **layout_theme
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"

# ----------------------------------------------------------------------
# AUTOSTART (Para activar las esquinas redondeadas y sombras en Debian/Termux)
# ----------------------------------------------------------------------
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    # Si estás usando un servidor X de entorno gráfico completo o vnc, picom te dará el toque Hyprland.
    # Descomenta la línea de abajo si tienes picom instalado para ver bordes redondeados verdaderos y sombras.
    # subprocess.Popen(['picom', '--experimental-backends', '-b'])
