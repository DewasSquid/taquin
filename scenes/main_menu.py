import os

from ursina import *

from modules.custom_entities import *
from modules.visuals import *

button_spacing = .075 * 1.25
menu_parent = Entity(parent=camera.ui, y=.15)
main_menu = Entity(parent=menu_parent)
load_menu = Entity(parent=menu_parent)
options_menu = Entity(parent=menu_parent)

state_handler = Animator({
    "main_menu" : main_menu,
    "load_menu" : load_menu,
    "options_menu" : options_menu,
    }
)

# Menu principal
main_menu.title = Text(
    parent=main_menu,
    text="Jeu Du Taquin",
    scale=5,
    color=color.rgba(255, 100, 200),
    position=Vec2(-.4, .1)
)

main_menu.buttons = [
    MenuButton("Jouer", on_click=Func(setattr, state_handler, "state", "load_menu")),
    MenuButton("Sortir", on_click=Sequence(Wait(.01), Func(sys.exit))),
]
for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i-2) * button_spacing


def start_game():
    menu_parent.enabled = False

# Selecteur de niveau
for i, level in enumerate(os.listdir("./assets/levels/")):
    MenuButton(parent=load_menu, text=level, y=-i * button_spacing, on_click=start_game)

load_menu.back_button = MenuButton(parent=load_menu, text="back", y=((-i-2) * button_spacing), on_click=Func(setattr, state_handler, "state", "main_menu"))

# Petite animation stylé quand on change de menu
for menu in (main_menu, load_menu, options_menu):
    def animate_in_menu(menu=menu):
        for i, e in enumerate(menu.children):
            e.original_x = e.x
            e.x += .1
            e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

            e.alpha = 0
            e.animate("alpha", .7, delay=i*.05, duration=.1, curve=curve.out_quad)

            if hasattr(e, "text_entity"):
                e.text_entity.alpha = 0
                e.text_entity.animate("alpha", 1, delay=i*.05, duration=.1)

    menu.on_enable = animate_in_menu

BackgroundImage(parent=menu_parent, texture="./assets/images/menu_bg.jpg")