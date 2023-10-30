"""This script sets the base configuration for Qtile.

It consists of keybindings, layouts, widgets, rules and hooks.
An in depth documentation can be found at:
https://github.com/david35mm/.files/tree/main/.config/qtile """

import os
import shutil
import socket
import subprocess

import libqtile.hook
from libqtile import bar
from libqtile import hook
from libqtile import layout
from libqtile import qtile
from libqtile import widget
from libqtile.config import EzClick as Click
from libqtile.config import EzDrag as Drag
from libqtile.config import EzKey as Key
from libqtile.config import Group
from libqtile.config import Match
from libqtile.config import Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


mod = "mod4"
my_term = guess_terminal()
wallpaper = "/usr/share/backgrounds/default.png"


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


def status_bar(widget_list):
    return bar.Bar(widget_list, 18, opacity=0.8)


mouse = [
    Drag("M-1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag("M-3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click("M-2",
          lazy.window.bring_to_front()),
]

keys = [
    Key("M-<Return>",
        lazy.spawn(my_term),
        desc="Launch " + my_term),
    Key("M-S-q",
        lazy.window.kill(),
        desc="Close the window"),
    Key("M-d",
        lazy.spawn("rofi -show drun -show-icons"),
        desc="Open the window switcher"),
    Key("M-l",
        lazy.spawn("/home/nfarago/.config/scripts/i3lock.sh"),
        desc="Lock screen"),
    Key("<Print>",
        lazy.spawn("gnome-screenshot -i"),
        desc="Create screenshot"),
    Key("M-<Left>",
        lazy.group.prev_window(),
        desc="Focus previous window"),
    Key("M-<Right>",
        lazy.group.next_window(),
        desc="Focus next window"),
    Key("M-S-<Left>",
        lazy.function(window_to_next_screen, switch_screen=True),
        desc="Move window to next screen"),
    Key("M-S-<Right>",
        lazy.function(window_to_previous_screen, switch_screen=True),
        desc="Move window to previous screen"),
    Key("M-<space>",
        lazy.layout.shuffle_up(),
        desc="Swap with previous window"),
    Key("M-S-k",
        lazy.layout.shuffle_down(),
        desc="Swap with next window"),
    Key("M-f",
        lazy.window.toggle_fullscreen(),
        desc="Fullscreen toogle"),
    Key("M-S-<space>",
        lazy.window.toggle_floating(),
        desc="Floating toggle"),
    Key("M-S-f",
        lazy.layout.flip(),
        desc="Flip master pane side"),
    Key("M-S-h",
        lazy.layout.shrink(),
        desc="Shrink window size"),
    Key("M-S-l",
        lazy.layout.grow(),
        desc="Expand window size"),
    Key("M-S-n",
        lazy.layout.reset(),
        desc="Normalize all windows size"),
    Key("M-<Tab>",
        lazy.next_layout(),
        desc="Cycle through layouts"),
    Key("M-h",
        lazy.layout.shrink_main(),
        desc="Shrink master pane width"),
    #  Key("M-l",
    #    lazy.layout.grow_main(),
    #    desc="Grow master pane width"),
    Key("M-n",
        lazy.layout.normalize(),
        desc="Normalize all slave windows size"),
    Key("M-<comma>",
        lazy.prev_screen(),
        desc="Focus the previous screen"),
    Key("M-<period>",
        lazy.next_screen(),
        desc="Focus the next screen"),
    Key("<XF86AudioLowerVolume>",
        lazy.spawn("pamixer -u -d 5"),
        desc="Decrease the volume"),
    Key("<XF86AudioMute>",
        lazy.spawn("pamixer -t"),
        desc="Mute toggle"),
    Key("<XF86AudioRaiseVolume>",
        lazy.spawn("pamixer -u -i 5"),
        desc="Increase the volume"),
    Key("<XF86MonBrightnessDown>",
        lazy.spawn("brightnessctl set 10%-"),
        desc="Decrease the brightness"),
    Key("<XF86MonBrightnessUp>",
        lazy.spawn("brightnessctl set 10%+"),
        desc="Increase the brightness"),
    Key("M-S-s",
        lazy.spawn("systemctl suspend"),
        desc="Sleep"),
    Key("M-S-r",
        lazy.restart(),
        desc="Restart Qtile"),
    Key("M-S-e",
        lazy.shutdown(),
        desc="Quit Qtile"),
]

group_names = {
    "1.  main": "main",
    "2.  dev": "external",
    "3.  dev_client": "external",
    "4.  other": "main",
    "5.  dev browser": "external",
    "6.  terminals": "main",
    "7. 󰒱 slack": "main",
    "8.  util": "main",
    "9.  any": "main"
}

groups = [
    Group(list(group_names)[0],
          layout="monadtall",
          matches=[
              Match(wm_class=["Min", "Google-chrome"]),
          ]),
    Group(list(group_names)[1],
          layout="monadtall",
          matches=[
              Match(wm_class=["Emacs", "Geany", "jetbrains-idea", "jetbrains-webstorm"]),
          ]),
    Group(list(group_names)[2],
          layout="monadtall",
          matches=[
              Match(wm_class=["Code"]),
          ]),
    Group(list(group_names)[3],
          layout="monadtall",
          matches=[
              Match(wm_class=["Brave-browser", "Lxappearance", "Nitrogen"]),
          ]),
    Group(list(group_names)[4],
          layout="monadtall"),
    Group(list(group_names)[5],
          layout="monadtall",
          matches=[
              Match(wm_class=["Kitty"]),
          ]),
    Group(list(group_names)[6],
          layout="monadtall",
          matches=[
              Match(wm_class=["TelegramDesktop", "Slack"]),
          ]),
    Group(list(group_names)[7],
          layout="max",
          matches=[
              Match(wm_class=["Thunar"]),
              Match(title=["Celluloid"]),
          ]),
    Group(list(group_names)[8],
          layout="floating"),
]


colours = [
    ["#181b20", "#181b20"],  # Background
    ["#e6e6e6", "#e6e6e6"],  # Foreground
    ["#535965", "#535965"],  # Grey Colour
    ["#e55561", "#e55561"],
    ["#8ebd6b", "#8ebd6b"],
    ["#e2b86b", "#e2b86b"],
    ["#4fa6ed", "#4fa6ed"],
    ["#bf68d9", "#bf68d9"],
    ["#48b0bd", "#48b0bd"],
]

layout_theme = {
    "border_focus": colours[6],
    "border_normal": colours[2],
    "margin": 4,
    "border_width": 2,
}

layouts = [
    # layout.Bsp(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Slice(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Stack(stacks=2, **layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
]

prompt = f"{os.environ['USER']}@{socket.gethostname()}: "

widget_defaults = dict(background=colours[0],
                       foreground=colours[1],
                       font="Roboto Nerd Font Regular",
                       fontsize=14,
                       padding=1)

extension_defaults = widget_defaults.copy()

widget_external_monitor = [
    widget.Sep(
        name="sep1",
        foreground=colours[0],
        linewidth=4),
    widget.GroupBox(
        active=colours[8],
        inactive=colours[2],
        other_current_screen_border=colours[2],
        other_screen_border=colours[2],
        this_current_screen_border=colours[4],
        this_screen_border=colours[2],
        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        highlight_method="text",
        borderwidth=5,
        invert_mouse_wheel=True,
        hide_unused=False,
        margin=2,
        padding=2,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(
        name="sep2",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.CurrentLayout(
        foreground=colours[7],
        font="Roboto Nerd Font Bold"),
    widget.Sep(
        name="sep3",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.WindowName(
        max_chars=75),
]

widgets = [
    widget.Sep(
        name="sep1",
        foreground=colours[0],
        linewidth=4),
    widget.Image(
        filename="~/.config/qtile/fedora.png",
        mouse_callbacks=({
            "Button1": lambda: qtile.spawn("rofi -show drun"),
            "Button3": lambda: qtile.spawn("rofi -show run"),
        }),
        scale=True),
    widget.Sep(
        name="sep2",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.GroupBox(
        active=colours[8],
        inactive=colours[2],
        other_current_screen_border=colours[2],
        other_screen_border=colours[2],
        this_current_screen_border=colours[4],
        this_screen_border=colours[2],
        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        highlight_method="text",
        invert_mouse_wheel=True,
        hide_unused=False,
        margin=2,
        padding=0,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(
        name="sep3",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.CurrentLayout(
        foreground=colours[7],
        font="Roboto Nerd Font Bold"),
    widget.Sep(
        name="sep4",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.WindowName(
        max_chars=75),
    # widget.Backlight(
    #     foreground=colours[3],
    #     foreground_alert=colours[3],
    #     format=" {percent:2.0%}",
    #     backlight_name="amdgpu_bl0", # ls /sys/class/backlight/
    #     change_command="brightnessctl set {0}%",
    #     step=10),
    widget.CPU(
        foreground=colours[3],
        format=" {load_percent}%",
        mouse_callbacks={
            "Button1": lambda: qtile.spawn(my_term + " -e htop"),
        },
        update_interval=1.0),
    widget.Sep(
        name="sep5",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Memory(
        foreground=colours[4],
        format=" {MemUsed:.0f} MB",
        mouse_callbacks={
            "Button1": lambda: qtile.spawn(my_term + " -e htop"),
        },
        update_interval=1.0),
    widget.Sep(
        name="sep6",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.CheckUpdates(
        colour_have_updates=colours[5],
        colour_no_updates=colours[5],
        custom_command="dnf updateinfo -q --list",
        display_format=" {updates} Updates",
        no_update_string=" Up to date!",
        mouse_callbacks=({
            "Button1": lambda: qtile.spawn(os.path.expanduser(
                "~/.config/scripts/update_system.sh")),
            "Button3": lambda: qtile.spawn(os.path.expanduser(
                "~/.config/scripts/check_updates.sh")),
        }),
        update_interval=900),
    widget.Sep(
        name="sep7",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    # widget.Net(
    #     foreground = colours[7],
    #     format = "爵 {down}  ",
    #     interface = "enp1s0"),
    widget.Battery(
        foreground=colours[7],
        format="{char} {percent:2.0%}",
        charge_char=" ",
        discharge_char=" ",
        empty_char="- ",
        full_char=" ",
        unknown_char="UNK ",
        low_foreground=colours[3],
        low_percentage=0.15,
        show_short_text=False,
        notify_below=15),
    widget.Sep(
        name="sep8",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Systray(
        foreground=colours[2],
        icon_size=14,
        padding=4),
    widget.Sep(
        name="sep9",
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Clock(
        foreground=colours[8],
        format=" %a %b %d  %I:%M %P    "),
    # widget.StockTicker(
    #     apikey="AESKWL5CJVHHJKR5",
    #     url="https://www.alphavantage.co/query?"),
]

screens = [
    Screen(
        top=status_bar(widgets),
        wallpaper=wallpaper,
        wallpaper_mode="stretch"),
]

connected_monitors = (subprocess.run(
    "xrandr | busybox grep 'connected' | busybox cut -d' ' -f2",
    check=True,
    shell=True,
    stdout=subprocess.PIPE,
).stdout.decode("UTF-8").split("\n")[:-1].count("connected"))

if connected_monitors > 1:
    monitor_ids = range(0, connected_monitors)
    for group in groups:
        if group_names[group.name] == "main":
            group.screen_affinity = monitor_ids[0]
        if group_names[group.name] == "external":
            group.screen_affinity = monitor_ids[1]
    screens.append(
        Screen(
            top=status_bar(widget_external_monitor),
            wallpaper=wallpaper,
            wallpaper_mode="stretch"))
    startup = os.path.expanduser("~/.config/scripts/set_monitor.sh")
    subprocess.Popen(startup)


for k, group in zip(["1", "2", "3", "4", "5", "6", "7", "8", "9"], groups):
    keys.append(Key("M-" + k, lazy.group[group.name].toscreen()))
    keys.append(Key("M-S-" + k, lazy.window.togroup(group.name)))


auto_fullscreen = True
auto_minimize = True
bring_front_click = False
cursor_warp = False
dgroups_app_rules = []
dgroups_key_binder = None
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="Authentication"),
        Match(title="branchdialog"),
        Match(title="Chat"),
        Match(title="pinentry"),
        Match(title="Polls"),
        Match(wm_class="Arandr"),
        Match(wm_class="Blueman-adapters"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="confirm"),
        Match(wm_class="confirmreset"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="Gnome-screenshot"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="notification"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="splash"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="toolbar"),
    ])
focus_on_window_activation = "focus"
follow_mouse_focus = True
reconfigure_screens = True


# pylint: disable=consider-using-with
@libqtile.hook.subscribe.restart
def delete_cache():
    shutil.rmtree(os.path.expanduser("~/.config/qtile/__pycache__"))


@libqtile.hook.subscribe.shutdown
def stop_apps():
    delete_cache()
    qtile.spawn(["killall", "dunst", "lxpolkit", "picom", "udiskie", "pasystray", "nm-applet", "blueman-applet"]) # programs in autostart.sh


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


@libqtile.hook.subscribe.startup
def start_apps():
    qtile.spawn(["~/.config/scripts/set_monitor.sh"])


wmname = "LG3D"
