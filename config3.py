import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# COLORES RETRO-WAVE / CYBERPUNK 1980
colors = {
    "bg":      "#1a102f",  # Violeta muy profundo y oscuro
    "fg":      "#f0e6ff",  # Blanco con tinte lavanda
    "neon_p":  "#ff0055",  # Rosa Neón
    "neon_o":  "#ff7300",  # Naranja Eléctrico
    "neon_y":  "#ffee00",  # Amarillo Cyber
    "neon_b":  "#00f0ff",  # Cian Neón
    "inactive":"#4d3b66",  # Violeta apagado para inactivos
}

mod = "mod4"
terminal = "kitty"

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "c", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
]

# Grupos con iconos Retro-gaming / Tech
groups = [
    Group("1", label=" 󰊖 "),
    Group("2", label=" 󰄛 "),
    Group("3", label=" 󰗀 "),
    Group("4", label=" 󰭹 "),
    Group("5", label=" 󱓷 "),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

# Layout con Gaps medianos y bordes Rosa Neón
layout_theme = {
    "border_width": 3,
    "margin": 8,
    "border_focus": colors["neon_p"],
    "border_normal": colors["inactive"],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(margin=4),
]

# Barra compacta con separadores diagonales (estilo "Slash")
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(text=" 󰀨 RetroWM ", background=colors["neon_p"], foreground=colors["bg"], font="MesloLGS NF Bold"),
                widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["neon_p"], background=colors["bg"]),
                
                widget.Spacer(length=10),
                widget.GroupBox(
                    font="MesloLGS NF",
                    fontsize=14,
                    active=colors["neon_b"],
                    inactive=colors["inactive"],
                    highlight_method="block",
                    this_current_screen_border=colors["inactive"],
                ),
                
                widget.WindowName(foreground=colors["fg"], fontsize=11, padding=15),
                
                # Stats con formato clásico y limpio
                widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["neon_o"]),
                widget.TextBox(text="  ", background=colors["neon_o"], foreground=colors["bg"]),
                widget.CPU(format='{load_percent}%', background=colors["neon_o"], foreground=colors["bg"]),
                
                widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["neon_y"], background=colors["neon_o"]),
                widget.TextBox(text="  ", background=colors["neon_y"], foreground=colors["bg"]),
                widget.Memory(format='{MemUsed:.0f}M', background=colors["neon_y"], foreground=colors["bg"]),
                
                widget.TextBox(text="", fontsize=24, padding=0, foreground=colors["neon_b"], background=colors["neon_y"]),
                widget.TextBox(text="  ", background=colors["neon_b"], foreground=colors["bg"]),
                widget.Clock(format='%H:%M', background=colors["neon_b"], foreground=colors["bg"]),
            ],
            24,
            background=colors["bg"],
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
floating_layout = layout.Floating(float_rules=[*layout.Floating.default_float_rules], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"
