SCREENS=$(xrandr | grep " connected " | awk '{ print$1 }')

for screen in "${SCREENS[@]}"
do
	echo ";" $screen
done

echo ${SCREENS[1]}
