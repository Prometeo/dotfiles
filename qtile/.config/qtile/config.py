# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from pathlib import Path
import os
import random

from libqtile import bar, layout, widget, extension, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Vars
mod = "mod4"
my_terminal = "alacritty"
home = str(Path.home())
wallpapers_dir = home + "/wallpapers/"
wallpaper = wallpapers_dir + random.choice(os.listdir(wallpapers_dir))

colors = {
    "night": ("#2e3440", "#3b4252", "#434c5e", "#4c566a"),
    "storm": ("#d8dee9", "#e5e9f0", "#eceff4"),
    "frost": ("#8fbcbb", "#88c0d0", "#81a1c1", "#5e81ac"),
    "aurora": ("#bf616a", "#d08770", "#ebcb8b", "#a3be8c", "#b48ead")
}

# End Vars

keys = [
    # Monitors
    # Switch focus to specific monitor
    Key([mod], "w", lazy.to_screen(0), desc='Keyboard focus to monitor 1'),
    Key([mod], "e", lazy.to_screen(1), desc='Keyboard focus to monitor 2'),


    # Launch terminal, kill window, restart and exit Qtile, session
    Key([mod], "Return", lazy.spawn(my_terminal), desc="Launch terminal"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "Escape", lazy.spawn('xkill'), desc="Select and kill a window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "x", lazy.spawn('arcolinux-logout')),

    # Multimedia
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse sset Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse sset Master 5%+")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10-")),

    # Dmenu, rofi
    Key([mod], "r", lazy.spawn('rofi -show run')),

    # Working with windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Make window floating"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(),
        desc="Make window full screen"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Lockscreen
    Key([mod, "shift"], "l", lazy.spawn("betterlockscreen -l dim"),
        desc="Lockscreen with betterlockscreen"),


    # Resize layout
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

]

__groups = {
    1: Group("I"),
    2: Group("II", matches=[Match(wm_class=['emacs'])]),
    3: Group("III", matches=[Match(wm_class=['firefox'])]),
    4: Group("IV"),
    5: Group("V"),
    6: Group("VI"),
    7: Group("VII"),
    8: Group("VIII"),
    9: Group("IX"),
}

groups = [__groups[i] for i in __groups]


def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]


for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(get_group_key(i.name)), lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(get_group_key(i.name)), lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(
        border_width=2,
        border_focus=colors['aurora'][2],
        single_border_width=0,
        margin=4
    ),
]

widget_defaults = dict(
    font='Hack Nerd Font',
    fontsize=14,
    margin=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.Sep(linewidth=0, padding=6),
                widget.GroupBox(
                    hide_unused=True,
                    disable_drag=True,
                    active=colors['storm'][2],
                    block_highlight_text_color=colors['aurora'][3],
                    highlight_method='block',
                ),
                widget.Prompt(),
                widget.WindowName(
                    foreground=colors['frost'][3],
                    padding=0,
                ),
                widget.CPU(
                    foreground=colors['aurora'][4]
                ),
                widget.CheckUpdates(
                    update_interval=600,
                    distro="Arch_checkupdates",
                    display_format="{updates} Updates",
                    foreground=colors['aurora'][0],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                        my_terminal + ' -e sudo pacman -Syu')},
                ),
                widget.Net(
                    interface="enp30s0",
                    format="{down}↓ {up}↑",
                    foreground=colors['frost'][0]
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(format='%d-%m-%Y %a %I:%M %p',
                             foreground=colors['aurora'][0]),
                widget.Volume(padding=5,emoji=True),
                widget.BatteryIcon(),
                widget.QuickExit(),
            ],
            24,
            background="#282c34",
            opacity=0.8,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

cmd = [
    "numlockx on",
    "picom &",
    "feh --bg-fill " + wallpaper,
    # "/usr/bin/emacs --daemon &",
]

for i in cmd:
    os.system(i)

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
