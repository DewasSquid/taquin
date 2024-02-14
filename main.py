import os
from importlib import import_module

from ursina import *

from modules import *


app = Ursina()

button_spacing = .075 * 1.25
menu_parent = Entity(parent=camera.ui, y=.15)
main_menu = Entity(parent=menu_parent)
load_menu = Entity(parent=menu_parent)

state_handler = Animator({
    "main_menu" : main_menu,
    "load_menu" : load_menu,
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


# Selecteur de niveau
def start_game(level):
    menu_parent.enabled = False
    level.draw_board()

LEVEL_PATH = "assets/levels"
for i, level in enumerate(os.listdir(LEVEL_PATH)):
    level_dir = os.path.join(LEVEL_PATH, level)
    
    if not ("__init__.py" in os.listdir(level_dir), os.path.isdir(level_dir)):
        continue
    
    level_absolute = level_dir.replace("/", ".")
    level_absolute = level_absolute.replace("\\", ".")
    level_module = import_module(level_absolute)
    
    MenuButton(parent=load_menu, text=level, y=-i * button_spacing, on_click=Func(start_game, level_module))

load_menu.back_button = MenuButton(parent=load_menu, text="Retour", y=((-i-2) * button_spacing), on_click=Func(setattr, state_handler, "state", "main_menu"))

# Petite animation stylé quand on change de menu
for menu in (main_menu, load_menu):
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

BackgroundImage(parent=menu_parent, texture="assets/images/menu_bg.jpg")

app.run()