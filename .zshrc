# =======================================================================================================
# ============================================</>>>ALIAS ZSHRC<<</>======================================
# =======================================================================================================

# ===== ZSH =====
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias bash='source ~/.bashrc'

# ===== NVIM-LAZY =====
alias confkitty='micro ~/.config/kitty/kitty.conf'


#========herramientas=======
alias audio='pavucontrol'
alias notas='micro ~/.setup/herramientas.txt'
alias navegador='setsid chromium --ozone-platform=x11 >/dev/null 2>&1 &'
alias navegador='setsid firefox--ozone-platform=x11 >/dev/null 2>&1 &'

# ===== QTILE CONFIG =====
alias qtile='qtile cmd-obj -o cmd -f reload_config'
alias config.py='micro ~/.config/qtile/config.py'
alias config1.py='micro ~/.config/qtile/config1.py'
alias config2.py='micro ~/.config/qtile/config2.py'
alias config3.py='micro ~/.config/qtile/config3.py'
alias escritorio1="echo config1 > ~/.config/qtile/.current_config && qtile cmd-obj -o cmd -f reload_config"
alias escritorio2="echo config2 > ~/.config/qtile/.current_config && qtile cmd-obj -o cmd -f reload_config"
alias escritorio3="echo config3 > ~/.config/qtile/.current_config && qtile cmd-obj -o cmd -f reload_config"
alias escritorio="echo config_default > ~/.config/qtile/.current_config && qtile cmd-obj -o cmd -f reload_config"
alias errorqtile='cat ~/.local/share/qtile/qtile.log | tail -n 20'

#=====kitty
alias kitty='kill -SIGUSR1 $(pidof kitty)'
alias configkitty="kitty +kitten themes"
#=====red & configuraciones
alias recargarred='sudo systemctl restart NetworkManager'
alias pip1='ping github.com'
alias pip2='ping -c 3 google.com'
alias pip3='ping -c 3 8.8.8.8'
alias quiensoy='uname -a && whoami && echo $SHELL'
alias pantalla='xrandr'
alias matrix='mpv --loop --no-audio --fullscreen --no-border --ontop=no ~/Descargas/fondos/fondo1.mp4'

#====scripting
alias useroot='python ~/scripts/UseRooy.py'          
alias files='yazi'
if [[ $- == *i* ]]; then
    clear
    python ~/scripts/menu_de_zshrc.py
fi
suspender() {
    pkill mpv
    mpv --loop --no-audio --fullscreen --no-border --ontop=no ~/Descargas/fondos/"$1" &
}
wallpaperqtile() {
    local img

    img=$(find "$HOME/Descargas" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" \) \
        | fzf --preview='feh --bg-fill {}')

    [ -z "$img" ] && echo "Cancelado" && return

    feh --bg-scale "$img"

    echo "✔ Fondo aplicado: $(basename "$img")"
}
wallpaperkitty() {
    local img

    # lista de imágenes
    img=$(find "$HOME/Descargas" -maxdepth 1 \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" \) \
        | fzf --preview='kitty +kitten icat --clear --transfer-mode=file --place=${FZF_PREVIEW_COLUMNS}x${FZF_PREVIEW_LINES}@0x0 {}')

    # cancelar si no eliges nada
    if [[ -z "$img" ]]; then
        echo "Cancelado"
        return
    fi
    kitty +kitten icat "$img"
    echo -n "¿Aplicar como fondo? (s/n): "
    read -r r
    if [[ "$r" == "s" ]]; then
        local config="$HOME/.config/kitty/kitty.conf"
        sed -i "s|^background_image .*|background_image $img|" "$config"
        if grep -q "^background_image_layout" "$config"; then
            sed -i "s|^background_image_layout .*|background_image_layout scaled|" "$config"
        else
            echo "background_image_layout scaled" >> "$config"
        fi

        # recargar kitty
        kill -SIGUSR1 "$(pidof kitty)"

        echo "✔ Fondo aplicado: $(basename "$img")"
    else
        echo "✖ Cancelado"
    fi
}
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='nvim'
else
  export EDITOR='nano'
fi
