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
import os
import subprocess

from libqtile import hook
from typing import Optional
from libqtile.widget.textbox import TextBox


from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()
bordercolor = "#a3a3a3"
borderinactive = "#595959"
bordersize = 1

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),   
    Key([mod, "shift"], "m", lazy.window.toggle_maximize(), desc="Toggle maximize"),  
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "BackSpace", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
   
    #launch
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="toggle rofi"),
    Key([mod], "p", lazy.spawn("alacritty"), desc="launch alacritty"),
    Key([mod], "o", lazy.spawn("konsole"), desc="launch konsole"),

    #teclas de volumen
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"), desc="subir volumen"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"), desc="bajar volumen"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="mute"),

    #teclas de brillo
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="aumentar brillo"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="disminuir brillo"),

    #captura de pantalla
    Key([], "F5", lazy.spawn("scrot"), desc="screenshot"),
    Key([mod], "F5", lazy.spawn("scrot -s"), desc="screenshot recortada"),
    
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in[
     "  ", "  ", " 󰇩 ", "  ", "  ", "  ", "  ", " 󰊤 ","  ",
]]


for i, group in enumerate(groups):
    numeroEscritorio =str(i+1)
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                numeroEscritorio,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                numeroEscritorio,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=bordersize,
        margin=30,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,
    ),

    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=bordersize,
        margin=1,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,
    ),

    layout.Max(
        border_width=bordersize,
        margin=0,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,

    ),
    
    layout.Spiral(
        main_pane_ratio = 0.48,
        margin=30,
        border_width=bordersize,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,
        new_client_position = "after_current",
    ),

    layout.Spiral(
        main_pane_ratio = 0.48,
        margin=1,
        border_width=bordersize,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,
        new_client_position = "after_current",
    ),
    
    layout.Max(
        border_width=bordersize,
        border_focus=bordercolor,
        border_on_single=True,
        border_normal=borderinactive,
        margin=1,
    ),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()



screens = [
    Screen(
        top=bar.Bar(
            [                
                widget.TextBox(
                    text="  ",
                    foreground="#d9d9d9",
                    background="#000000",
                    fontsize=23,
                ),

                widget.TextBox(
                    text='\uE0B0',
                    padding=0,
                    fontsize=30,
                    background="#21002b",
                    foreground="#000000",
                    ),
                
                widget.GroupBox(
                    background="#21002b",
                    inactive="#612a91",
                    active="#ffe6ee",
                    fontsize= 18,
                    highlight_method="line",
                    margin=0,
                    borderwidth= 0,
                    center_aligned=False,
                    highlight_color= ["#000000", "#0c1a1c"],
                    this_current_screen_border="#14000f",
                    block_highlight_text_color="#dbfcff",
                    ),

                widget.TextBox(
                    text='\uE0B0',
                    padding=0,
                    fontsize=30,
                    background="#0c0012",
                    foreground="#21002b",
                    ),

                #widget.NetGraph(
                #    frequency=0.1,
                #    type="line",
                #    border_color="#0c0012",
                #    start_pos="bottom",
                #    border_width=0,
                #    margin_y=1,
                #    samples=100,
                #    line_width=1,
                #    background="#0c0012",
                #    graph_color="#5ac7c7",
                #    padding=0,
                #),
#
                #widget.CPUGraph(
                #    frequency=0.1,
                #    type="line",
                #    border_color="#0c0012",
                #    start_pos="bottom",
                #    border_width=0,
                #    margin_y=0,
                #    samples=100,
                #    line_width=1,
                #    background="#0c0012",
                #    graph_color="#61ff86",
                #    padding=0,
                #),
#
                #widget.HDDBusyGraph(
                #    frequency=0.1,
                #    type="line",
                #    border_color="#0c0012",
                #    start_pos="bottom",
                #    border_width=0,
                #    margin=0,
                #    samples=100,
                #    line_width=1,
                #    background="#0c0012",
                #    graph_color="#db3d3d",
                #    padding=0,
                #),
                
                widget.Prompt(
                    prompt='',
                    foreground="#834391",
                    font="MesloLGS NF",
                    cursor=True,
                ),
                
                widget.Spacer(),

                widget.CurrentLayoutIcon(
                background="#0C0012",
                scale=0.7,
                ),

                widget.Sep(
                background="#0C0012",
                foreground="#0C0012",
                padding=2,
                ),
                              
                widget.TextBox(
                    text='\uE0B2',
                    padding=0,
                    fontsize=30,
                    background="#0C0012",
                    foreground="#071E22",
                ),
                widget.Systray(
                    fontsize=22,
                    background="#071E22",
                    foreground="#000000",
                    
                ),
                
                widget.TextBox(
                    text='\uE0B2',
                    padding=0,
                    fontsize=30,
                    background="#071E22",
                    foreground="#1D7874",
                ),
                                
                widget.TextBox(
                    text="󰋜",
                    background="#1D7874",
                    fontsize="20",
                    foreground="#ffbeab", 
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("nemo")}
                ),
                widget.Sep(
                    background="#1D7874",
                    foreground="#1D7874",
                    linewidth=1,
                ),
                widget.TextBox(
                    text="",
                    background="#1D7874",
                    fontsize="20",
                    foreground="#fffead",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("brave")}
                ),
                widget.Sep(
                    background="#1D7874",
                    foreground="#1D7874",
                    linewidth=1,
                ),
                widget.TextBox(
                    text="󱃖",
                    background="#1D7874",
                    fontsize="20",
                    foreground="#c4ffcc",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("code")}
                ),
                widget.Sep(
                    background="#1D7874",
                    foreground="#1D7874",
                    linewidth=1,
                ),
                widget.TextBox(
                    text="",
                    background="#1D7874",
                    fontsize="20",
                    foreground="#d1d1d1",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("lxappearance ")}
                    ),
                widget.Sep(
                    background="#1D7874",
                    foreground="#1D7874",
                    linewidth=1,
                ), 
                
                

                widget.TextBox(
                    text='\uE0B2',
                    padding=0,
                    fontsize=30,
                    background="#1D7874",
                    foreground="#679289",
                    ),

                widget.Wttr(
                    font="noto-fonts-emoji",
                    fontsize= 16,
                    format= "%m %f %c%w",
                    background="#679289",
                    foreground="#dae3e3",
                ),
               
               
                
                widget.TextBox(
                    text='\uE0B2',
                    padding=0,
                    fontsize=30,
                    background="#679289",
                    foreground="#F4C095",
                    ),
                 
                widget.Clock(
                    format="%d-%m-%Y %H:%M ",
                    timezone="America/Los_Angeles",
                    font="JetBrains Mono Bold",
                    fontsize=15,
                    background="#F4C095",
                    foreground="#786146",
                ),
                                
                widget.TextBox(
                    text='\uE0B2',
                    padding=0,
                    fontsize=30,
                    background="#F4C095",
                    foreground="#EE2E31",
                    ),

                #widget.CPU(
                #    format="{freq_current}Ghz  ",
                #    update_interval=2.0,
                #    font="JetBrains Mono Bold",
                #    fontsize=15,
                #    background="#EE2E31",
                #    foreground="#ffdbc7",
                #    padding=0,
                #),🥴

            ],
            24,
            background="#0c0012",
            margin=0,
            #border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        #You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        #x11_drag_polling_rate = 60,
    ),
    #Screen(
    #    top=bar.Bar(
    #        [                
    #            widget.TextBox(
    #                text="  ",
    #                foreground="#d9d9d9",
    #                background="#000000",
    #                fontsize=23,
    #            ),
#
    #            widget.TextBox(
    #                text='\uE0B0',
    #                padding=0,
    #                fontsize=30,
    #                background="#21002b",
    #                foreground="#000000",
    #                ),
    #            
    #            #widget.GroupBox(
    #            #    background="#21002b",
    #            #    inactive="#612a91",
    #            #    active="#ffe6ee",
    #            #    fontsize= 18,
    #            #    highlight_method="line",
    #            #    margin=0,
    #            #    borderwidth= 0,
    #            #    center_aligned=False,
    #            #    highlight_color= ["#000000", "#0c1a1c"],
    #            #    this_current_screen_border="#14000f",
    #            #    block_highlight_text_color="#dbfcff",
    #            #    ),
#
    #            widget.TextBox(
    #                text='\uE0B0',
    #                padding=0,
    #                fontsize=30,
    #                background="#0c0012",
    #                foreground="#21002b",
    #                ),
#
    #            #widget.NetGraph(
    #            #    frequency=0.1,
    #            #    type="line",
    #            #    border_color="#0c0012",
    #            #    start_pos="bottom",
    #            #    border_width=0,
    #            #    margin_y=1,
    #            #    samples=100,
    #            #    line_width=1,
    #            #    background="#0c0012",
    #            #    graph_color="#5ac7c7",
    #            #    padding=0,
    #            #),
##
    #            #widget.CPUGraph(
    #            #    frequency=0.1,
    #            #    type="line",
    #            #    border_color="#0c0012",
    #            #    start_pos="bottom",
    #            #    border_width=0,
    #            #    margin_y=0,
    #            #    samples=100,
    #            #    line_width=1,
    #            #    background="#0c0012",
    #            #    graph_color="#61ff86",
    #            #    padding=0,
    #            #),
##
    #            #widget.HDDBusyGraph(
    #            #    frequency=0.1,
    #            #    type="line",
    #            #    border_color="#0c0012",
    #            #    start_pos="bottom",
    #            #    border_width=0,
    #            #    margin=0,
    #            #    samples=100,
    #            #    line_width=1,
    #            #    background="#0c0012",
    #            #    graph_color="#db3d3d",
    #            #    padding=0,
    #            #),
    #            
    #            widget.Prompt(
    #                prompt='',
    #                foreground="#834391",
    #                font="MesloLGS NF",
    #                cursor=True,
    #            ),
    #            
    #            widget.Spacer(),
#
    #            widget.CurrentLayoutIcon(
    #            background="#0C0012",
    #            scale=0.7,
    #            ),
#
    #            widget.Sep(
    #            background="#0C0012",
    #            foreground="#0C0012",
    #            padding=2,
    #            ),
    #                          
    #            widget.TextBox(
    #                text='\uE0B2',
    #                padding=0,
    #                fontsize=30,
    #                background="#0C0012",
    #                foreground="#071E22",
    #            ),
    #            #widget.Systray(
    #            #    fontsize=22,
    #            #    background="#071E22",
    #            #    foreground="#000000",
    #            #    
    #            #),
    #            
    #            widget.TextBox(
    #                text='\uE0B2',
    #                padding=0,
    #                fontsize=30,
    #                background="#071E22",
    #                foreground="#1D7874",
    #            ),
    #                            
    #            widget.TextBox(
    #                text="󰋜",
    #                background="#1D7874",
    #                fontsize="20",
    #                foreground="#ffbeab", 
    #                mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("nemo")}
    #            ),
    #            widget.Sep(
    #                background="#1D7874",
    #                foreground="#1D7874",
    #                linewidth=1,
    #            ),
    #            widget.TextBox(
    #                text="",
    #                background="#1D7874",
    #                fontsize="20",
    #                foreground="#fffead",
    #                mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("brave")}
    #            ),
    #            widget.Sep(
    #                background="#1D7874",
    #                foreground="#1D7874",
    #                linewidth=1,
    #            ),
    #            widget.TextBox(
    #                text="󱃖",
    #                background="#1D7874",
    #                fontsize="20",
    #                foreground="#c4ffcc",
    #                mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("code")}
    #            ),
    #            widget.Sep(
    #                background="#1D7874",
    #                foreground="#1D7874",
    #                linewidth=1,
    #            ),
    #            widget.TextBox(
    #                text="",
    #                background="#1D7874",
    #                fontsize="20",
    #                foreground="#d1d1d1",
    #                mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("lxappearance ")}
    #                ),
    #            widget.Sep(
    #                background="#1D7874",
    #                foreground="#1D7874",
    #                linewidth=1,
    #            ), 
    #            
    #            
#
    #            widget.TextBox(
    #                text='\uE0B2',
    #                padding=0,
    #                fontsize=30,
    #                background="#1D7874",
    #                foreground="#679289",
    #                ),
#
    #            widget.Wttr(
    #                font="JetBrains Mono",
    #                fontsize= 16,
    #                format= "%m %f%c",
    #                background="#679289",
    #                foreground="#dae3e3",
    #            ),
    #           
    #           
    #            
    #            widget.TextBox(
    #                text='\uE0B2',
    #                padding=0,
    #                fontsize=30,
    #                background="#679289",
    #                foreground="#F4C095",
    #                ),
    #             
    #            widget.Clock(
    #                format="%d-%m-%Y %H:%M ",
    #                timezone="America/Los_Angeles",
    #                font="JetBrains Mono Bold",
    #                fontsize=15,
    #                background="#F4C095",
    #                foreground="#786146",
    #            ),
    #                            
    #            widget.TextBox(
    #                text='\uE0B2',
    #                padding=0,
    #                fontsize=30,
    #                background="#F4C095",
    #                foreground="#EE2E31",
    #                ),
#
    #            widget.CPU(
    #                format="{freq_current}Ghz  ",
    #                update_interval=2.0,
    #                font="JetBrains Mono Bold",
    #                fontsize=15,
    #                background="#EE2E31",
    #                foreground="#ffdbc7",
    #                padding=0,
    #            ),
#
    #        ],
    #        24,
    #        background="#0c0012",
    #        margin=0,
    #        #border_width=[2, 0, 2, 0],  # Draw top and bottom borders
    #        #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    #    ),
    #    #You can uncomment this variable if you see that on X11 floating resize/moving is laggy
    #    # By default we handle these events delayed to already improve performance, however your system might still be struggling
    #    # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
    #    #x11_drag_polling_rate = 60,
    #),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width = 2,
    border_focus=bordercolor,
    border_normal="#000000",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]

)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])

#espacio para definir funciones



