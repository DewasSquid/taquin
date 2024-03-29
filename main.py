import os
from importlib import import_module

from ursina import *

from modules import *


app = Ursina()

button_spacing = .075 * 1.25
menu_parent = GameFrame()
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
    level.main()

LEVEL_PATH = "assets/levels"
for i, level_dir in enumerate(os.listdir(LEVEL_PATH)):
    level_path = os.path.join(LEVEL_PATH, level_dir)
    
    if not "__init__.py" in os.listdir(level_path) or not os.path.isdir(level_path):
        continue
    
    level_absolute = level_path.replace("/", ".")
    level_absolute = level_absolute.replace("\\", ".")
    level_module = import_module(level_absolute)
    
    MenuButton(
        parent=load_menu,
        text=level_dir,
        tooltip=Tooltip(
            text=f"<scale:1.5><yellow>{level_module.config['difficulty']} étoile(s)\n<scale:1><default>{level_module.config['description']}",
            background_color=color.black,
            wordwrap=25
        ),
        y=(-i * button_spacing),
        on_click=Func(start_game, level_module)
    )

load_menu.back_button = MenuButton(parent=load_menu, text="Retour", y=((-i-2) * button_spacing), on_click=Func(setattr, state_handler, "state", "main_menu"))

# Petite animation stylé quand on change de menu
for menu in (main_menu, load_menu):
    def animate_in_menu(menu=menu):
        for i, entity in enumerate(menu.children):
            entity.original_x = entity.x
            entity.x += .1
            entity.animate_x(entity.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

            if isinstance(entity, Text):
                entity.alpha = 0
                entity.animate("alpha", 1, delay=i*.05, duration=.1)
            else:
                entity.alpha = 0
                entity.animate("alpha", .7, delay=i*.05, duration=.1, curve=curve.out_quad)
    menu.on_enable = animate_in_menu

BackgroundImage(parent=menu_parent, texture=Textures.MENU_BACKGROUND, scale=(window.aspect_ratio, 1), y=-.15)

app.run()