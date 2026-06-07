import os
from collections.abc import Callable
import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# ----------------------------------------------------------------------
# PALETA DE COLORES (Cyberpunk Megacity)
# ----------------------------------------------------------------------
colors = {
    "bg":           "#0c0f12",  # Negro tecnológico profundo
    "panel_bg":     "#14191f",  # Gris oscuro industrial
    "fg":           "#e2e8f0",  # Blanco frío
    "cyber_yellow": "#ffee00",  # Amarillo Radiactivo / Cyberpunk 2077
    "neon_pink":    "#ff0055",  # Rosa Neón / Trauma Team
    "neon_cyan":    "#00f0ff",  # Azul hielo / Netrunner
    "matrix_green": "#00ff66",  # Verde de consola / Toxina
    "dark_purple":  "#24123a",  # Púrpura de contraste nocturno
    "grey":         "#3f4e5a",  # Gris de ranura
}

mod = "mod4"  # Tecla Super
terminal = guess_terminal()

keys = [
    # Navegación avanzada de ventanas
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to next"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Pantalla completa"),
    Key([mod], "m", lazy.window.toggle_maximize(), desc="Maximizar ventana"),
    
    # Desplegar/esconde la barra horizontal de recursos (Scratchpad)
    Key([mod, "control"], "h", lazy.group['scratchpad'].dropdown_toggle('monitor')),
    
    # Intercambio de posición de ventanas
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Mover ventana a la izquierda"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Mover ventana a la derecha"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Mover ventana abajo"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Mover ventana arriba"),
    
    # Intercambiar espacios
    Key([mod, "shift", "control"], "Left", lazy.layout.swap_left(), desc="Intercambiar espacio a la izquierda"),
    Key([mod, "shift", "control"], "Right", lazy.layout.swap_right(), desc="Intercambiar espacio a la derecha"),
    Key([mod, "shift", "control"], "Up", lazy.layout.shuffle_up(), desc="Mover arriba"),
    Key([mod, "shift", "control"], "Down", lazy.layout.shuffle_down(), desc="Mover abajo"),

    # Redimensionamiento de ventanas
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Agrandar a la izquierda"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Agrandar a la derecha"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Agrandar abajo"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Agrandar arriba"),
    Key([mod], "n", lazy.layout.normalize(), desc="Resetear tamaños"),

    # Controles del Sistema
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "End", lazy.window.kill(), desc="Cerrar ventana enfocada"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Añadir VTs para compatibilidad nativa con Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# ----------------------------------------------------------------------
# WORKSPACES / DISTRITOS (Iconos Netbrain) + SCRATCHPAD
# ----------------------------------------------------------------------
groups = [
    Group("1", label=" 󰣇 NET "),
    Group("2", label=" 󰆍 DEV "),
    Group("3", label=" 󰭹 SYS "),
    Group("4", label=" 󱔗 OPS "),
    Group("5", label=" 󰎆 MED "),
    Group("6", label=" 󰌢 DIR "),
]

# Definición del ScratchPad integrado limpiamente en la lógica de grupos
scratchpad_group = ScratchPad("scratchpad", [
    DropDown(
        "monitor", 
        f"{terminal} -e htop", # Usa tu terminal nativa de forma limpia ejecutando htop
        x=0.01,
        y=0.04,
        width=0.98,
        height=0.25, # Un 25% de la pantalla para que las métricas de htop sean legibles
        opacity=0.95,
        on_focus_lost_hide=False
    ),
])

# Inyectamos el scratchpad de forma interna en la lista de Qtile
qtile_groups = groups + [scratchpad_group]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

# ----------------------------------------------------------------------
# LAYOUTS (Geometría Estructurada)
# ----------------------------------------------------------------------
layout_theme = {
    "border_width": 3,
    "margin": 8,  
    "border_focus": colors["cyber_yellow"], 
    "border_normal": colors["dark_purple"],
}

layouts = [
    layout.Columns(
        border_focus=colors["neon_pink"],
        border_normal=colors["panel_bg"],
        border_width=2,
        margin=6,
    ),
    layout.Max(margin=6),
    layout.Floating(**layout_theme),
]

# ----------------------------------------------------------------------
# WIDGET DECORATIONS & BAR
# ----------------------------------------------------------------------
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        # Indicador / Logo de Entrada
        widget.TextBox(
            text=" 󱗗 UseRoot ",
            font="sans Bold",
            fontsize=13,
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
            font="sans Bold",
            fontsize=11,
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
        
        # Botón Tuerca para disparar el terminal desplegable
        widget.TextBox(
            text=" ⚙ ", 
            fontsize=15,
            foreground=colors["neon_pink"], 
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
        
        widget.Prompt(foreground=colors["cyber_yellow"]),
        
        # Título de Ventana Activa
        widget.WindowName(
            foreground=colors["fg"],
            fontsize=12,
            padding=15,
        ),
        
        # --- BLOQUES ANGULARES DE DATOS ---
        
        # Red / Tráfico de Datos (Simplificado sin interfaz estática para evitar fallos)
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["dark_purple"], background=colors["bg"]),
        widget.TextBox(text=" 󰖩 ", fontsize=13, foreground=colors["neon_cyan"], background=colors["dark_purple"], padding=0),
        widget.Net(
            format='{down:.0f}↓ {up:.0f}↑', 
            background=colors["dark_purple"], 
            foreground=colors["fg"],
            font="sans Bold",
            fontsize=11
        ),
        
        # Carga del Procesador (CPU)
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["panel_bg"], background=colors["dark_purple"]),
        widget.TextBox(text=" 󰍛 ", fontsize=13, foreground=colors["cyber_yellow"], background=colors["panel_bg"], padding=0),
        widget.CPU(
            format='CPU {load_percent}%', 
            background=colors["panel_bg"], 
            foreground=colors["fg"],
            font="sans Bold",
            fontsize=11
        ),
        
        # Memoria RAM
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["dark_purple"], background=colors["panel_bg"]),
        widget.TextBox(text=" 󰘚 ", fontsize=13, foreground=colors["neon_pink"], background=colors["dark_purple"], padding=0),
        widget.Memory(
            format='RAM {MemUsed:.0f}M', 
            background=colors["dark_purple"], 
            foreground=colors["fg"],
            font="sans Bold",
            fontsize=11
        ),
        
        # Reloj
        widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["cyber_yellow"], background=colors["dark_purple"]),
        widget.TextBox(text=" 󰥔 ", fontsize=13, foreground=colors["bg"], background=colors["cyber_yellow"], padding=0),
        widget.Clock(
            format='%H:%M:%S', 
            background=colors["cyber_yellow"], 
            foreground=colors["bg"],
            font="sans Bold",
            fontsize=12
        ),
        
        # Espacio final y Systray estándar
        widget.TextBox(text=" ", background=colors["cyber_yellow"], padding=2),
        widget.Systray(background=colors["bg"], padding=6),
        widget.Spacer(length=4, background=colors["bg"]),
    ]
    return widgets_list

screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            26,  # Altura de la barra
            background=colors["bg"],
            opacity=0.93,
            margin=[6, 10, 2, 10]  # Margen flotante estilizado
        ),
    ),
]

# ----------------------------------------------------------------------
# REGLAS, MOUSE Y COMPORTAMIENTO
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
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    **layout_theme
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# Forzamos a pasar la validación interna inyectando los qtile_groups limpios
groups = qtile_groups
fake_screens: list[Screen] | None = None
generate_screens: Callable[[list], list[Screen]] | None = None

wmname = "LG3D"
