#!/bin/sh
picom -b &
pasystray &
nm-applet &
blueman-applet &
dunst -conf ~/.config/qtile/dunstrc1 &
udiskie -asn -f thunar &
lxpolkit &
