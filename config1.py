# ~/.config/qtile/config3.py
import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.config import ScratchPad, DropDown

# ----------------------------------------------------------------------
# PALETA DE COLORES (Cyberpunk Megacity)
# ----------------------------------------------------------------------
colors = {
    "bg":          "#0c0f12",  # Negro tecnológico profundo
    "panel_bg":    "#14191f",  # Gris oscuro industrial
    "fg":          "#e2e8f0",  # Blanco frío
    "cyber_yellow":"#ffee00",  # Amarillo Radiactivo / Cyberpunk 2077
    "neon_pink":   "#ff0055",  # Rosa Neón / Trauma Team
    "neon_cyan":   "#00f0ff",  # Azul hielo / Netrunner
    "matrix_green":"#00ff66",  # Verde de consola / Toxina
    "dark_purple": "#24123a",  # Púrpura de contraste nocturno
    "grey":        "#3f4e5a",  # Gris de ranura
}
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([
        "mpv",
        "--loop",
        "--no-audio",
        "--fullscreen",
        "--no-border",
        "/home/useroot/Descargas/fondos/fondo1.mp4"
    ])

@hook.subscribe.client_new
def chromium_rules(window):
    if window.get_wm_class() and "chromium" in window.get_wm_class():
        window.opacity = 0.85
        
mod = "mod4"  # Tecla Super
terminal = "kitty"

keys = [
    # Navegación avanzada de ventanas
    # Cambiar de ventana
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
#    Key([mod], "h", lazy.layout.left(), desc="Focus left"),
#    Key([mod], "l", lazy.layout.right(), desc="Focus right"),
#    Key([mod], "j", lazy.layout.down(), desc="Focus down"),
#    Key([mod], "k", lazy.layout.up(), desc="Focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to next"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Pantalla completa"),
    Key([mod], "m", lazy.window.toggle_maximize(), desc="Maximizar ventana"),
    # Super + Control + m despliega/esconde la barra horizontal de recursos
    Key([mod, "control"], "h", lazy.group['scratchpad'].dropdown_toggle('monitor')),
    # Intercambio de posición de ventanas
    # Mover ventanas de posición
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Mover ventana a la izquierda"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Mover ventana a la derecha"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Mover ventana abajo"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Mover ventana arriba"),
    # Mueve la ventana e intercambia el tamaño/espacio con la de esa dirección
    Key([mod, "shift", "control"], "Left", lazy.layout.swap_left(), desc="Intercambiar espacio a la izquierda"),
    Key([mod, "shift", "control"], "Right", lazy.layout.swap_right(), desc="Intercambiar espacio a la derecha"),
    # Nota: Si Columns no responde a swap arriba/abajo, se usa shuffle para moverla dentro de la columna
    Key([mod, "shift", "control"], "Up", lazy.layout.shuffle_up(), desc="Mover arriba"),
    Key([mod, "shift", "control"], "Down", lazy.layout.shuffle_down(), desc="Mover abajo"),
#    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
#    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
#    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
#    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Redimensionamiento agresivo
# Redimensionar ventanas
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Agrandar a la izquierda"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Agrandar a la derecha"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Agrandar abajo"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Agrandar arriba"),

#    Key([mod, "control"], "h", lazy.layout.grow_left()),
#    Key([mod, "control"], "l", lazy.layout.grow_right()),
#    Key([mod, "control"], "j", lazy.layout.grow_down()),
#    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Controles del Sistema
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
#    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill window"),
    Key([mod], "End", lazy.window.kill(), desc="Cerrar ventana enfocada"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# ----------------------------------------------------------------------
# WORKSPACES / DISTRITOS DE LA CIUDAD (Iconos Netbrain / Cyber-Glitched)
# ----------------------------------------------------------------------
groups = [
    Group("1", label=" 󰣇 NET "),
    Group("2", label=" 󰆍 DEV "),
    Group("3", label=" 󰭹 SYS "),
    Group("4", label=" 󱔗 OPS "),
    Group("5", label=" 󰎆 MED "),
    Group("6", label=" 󰌢 DIR "),
]
# AÑADE ESTO JUSTO AQUÍ ABAJO:
    ScratchPad("scratchpad", [
        DropDown(
            "monitor", 
            "kitty --name=barra_htop htop --only-meters", # Solo barras de CPU/RAM
            x=0.01,         # Centrado horizontal ligeramente despegado del borde
            y=0.035,        # Se despliega justo debajo de tu barra de 26px
            width=0.98,     # Ocupa casi todo el ancho de la pantalla de forma horizontal
            height=0.08,    # Una barra delgada (8% de la pantalla)
            opacity=0.95,   # Un toque de transparencia cyberpunk
            on_focus_lost_hide=False # No se cierra si haces clic en otra ventana
        ),
    ]),
]
for i in groups:
    if i.name == "scratchpad":
        continue
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

# ----------------------------------------------------------------------
# LAYOUTS (Geometría Cortante y Estructurada)
# ----------------------------------------------------------------------
layout_theme = {
    "border_width": 3,
    "margin": 10,  # Separación ideal para fondos detallados
    "border_focus": colors["cyber_yellow"], # El foco brilla en amarillo chillón
    "border_normal": colors["dark_purple"],
}

layouts = [
    layout.Columns(
        border_focus="#ff00ff",      # El color de la ventana activa
        border_normal="#333333",     # El color de la ventana inactiva
        border_width=2,              # Grosor del borde
        margin=2,                    # Distancia entre ventanas (bájalo para que estén más cerca)
    ),
    # ... tus otros layouts
    layout.Columns(**layout_theme, border_focus_stack=colors["neon_pink"], num_columns=2),
    layout.Max(margin=6),
    layout.Floating(**layout_theme),
]
# ----------------------------------------------------------------------
# BARRA DE ESTADO (Diseño Industrial Angular "Cyber-Grid")
# ----------------------------------------------------------------------
def init_widgets_list():
    widgets_list = [
        # Indicador de Modo / Logo de Entrada
        widget.TextBox(
            text=" 󱗗 UseRoot ",
            font="MesloLGS NF Bold",
            fontsize=15,
            foreground=colors["bg"],
            background=colors["cyber_yellow"],
            padding=10,
        ),
        widget.TextBox(
            text="",
            fontsize=24,
            padding=0,
            foreground=colors["cyber_yellow"],
            background=colors["panel_bg"],
        ),
        
        # Selector de Escritorios / Grupos
        widget.GroupBox(
            font="MesloLGS NF Bold",
            fontsize=12,
            margin_y=3,
            margin_x=0,
            padding_y=4,
            padding_x=8,
            active=colors["neon_cyan"],
            inactive=colors["grey"],
            rounded=False,
            highlight_color=colors["bg"],
            highlight_method="line",
            this_current_screen_border=colors["neon_pink"],
            block_highlight_text_color=colors["cyber_yellow"],
            background=colors["panel_bg"],
        ),
        # ... dentro de tu lista de widgets = [ ... ]
        
        widget.TextBox(
            text=" ⚙ ", # Icono de tuerca (asegúrate de que tu terminal/fuente lo renderice)
            fontsize=16,
            foreground="#ff00ff", # El color que te guste
            background=colors["panel_bg"],
            mouse_callbacks={
                'Button1': lazy.group['scratchpad'].dropdown_toggle('monitor')
            },
        ),
        
        widget.TextBox(
            text="",
            fontsize=24,
            padding=0,
            foreground=colors["panel_bg"],
            background=colors["bg"],
        ),
        
        widget.Prompt(foreground=colors["cyber_yellow"], font="MesloLGS NF"),
        
        # Título de Ventana Activa (Centrado y limpio)
        widget.WindowName(
            foreground=colors["fg"],
            font="MesloLGS NF",
            fontsize=12,
            padding=15,
        ),
        
        # --- BLOQUES ANGULARES DE DATOS (Derecha) ---
        
        # Red / Tráfico de Datos
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["dark_purple"], background=colors["bg"]),
        widget.TextBox(text=" 󰖩 ", fontsize=14, foreground=colors["neon_cyan"], background=colors["dark_purple"], padding=0),
        widget.Net(
            interface="wlan0", 
            format='{down:.0f}↓ {up:.0f}↑', 
            background=colors["dark_purple"], 
            foreground=colors["fg"],
            font="MesloLGS NF Bold",
            fontsize=11
        ),
        
        # Carga del Procesador (CPU)
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["panel_bg"], background=colors["dark_purple"]),
        widget.TextBox(text=" 󰍛 ", fontsize=14, foreground=colors["cyber_yellow"], background=colors["panel_bg"], padding=0),
        widget.CPU(
            format='CPU {load_percent}%', 
            background=colors["panel_bg"], 
            foreground=colors["fg"],
            font="MesloLGS NF Bold",
            fontsize=11
        ),
        
        # Memoria RAM
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["dark_purple"], background=colors["panel_bg"]),
        widget.TextBox(text=" 󰘚 ", fontsize=14, foreground=colors["neon_pink"], background=colors["dark_purple"], padding=0),
        widget.Memory(
            format='RAM {MemUsed:.0f}M', 
            background=colors["dark_purple"], 
            foreground=colors["fg"],
            font="MesloLGS NF Bold",
            fontsize=11
        ),
        
        # Reloj / Cronómetro de Hackeo
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["cyber_yellow"], background=colors["dark_purple"]),
        widget.TextBox(text=" 󰥔 ", fontsize=14, foreground=colors["bg"], background=colors["cyber_yellow"], padding=0),
        widget.Clock(
            format='%H:%M:%S', 
            background=colors["cyber_yellow"], 
            foreground=colors["bg"],
            font="MesloLGS NF Bold",
            fontsize=12
        ),
        
        # Espacio para el Systray (Iconos de aplicaciones de terceros)
        widget.TextBox(text=" ", background=colors["cyber_yellow"], padding=2),
        widget.Systray(background=colors["bg"], padding=6),
        widget.Spacer(length=4, background=colors["bg"]),
    ]
    return widgets_list

screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            26,  # Altura exacta y estilizada
            background=colors["bg"],
            opacity=0.93,
            margin=[8, 10, 2, 10]  # Flotando con el espacio del layout
        ),
    ),
]

# ----------------------------------------------------------------------
# REGLAS Y COMPORTAMIENTO MOUSE
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
wmname = "LG3D"
