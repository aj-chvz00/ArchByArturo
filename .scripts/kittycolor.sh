#!/bin/bash

# Array de colores de fondo (puedes añadir más si quieres)
colors=("red" "blue" "green" "yellow" "cyan" "magenta")

# Elegir un color aleatorio
random_color=${colors[$RANDOM % ${#colors[@]}]}

# Cambiar el color de fondo en el archivo de configuración
sed -i "s/background\s*=.*/background = $random_color/" ~/.config/kitty/kitty.conf

# Mensaje opcional para indicar el cambio
#echo "Color de fondo cambiado a $random_color"
