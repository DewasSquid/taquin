from importlib import import_module
from ursina import *
from modules import *

# TODO: Pause menu using key function

MUSIC_VOLUME = 0.5
SOUND_VOLUME = 1

app = Ursina()
sky = Sky()

button_spacing = .075 * 1.25
menu_parent = GameFrame()
main_menu = Entity(parent=menu_parent)
load_menu = Entity(parent=menu_parent)

state_handler = Animator({
    "main_menu": main_menu,
    "load_menu": load_menu,
})

# Menu principal
main_menu.title = Text(
    parent=main_menu,
    text="Jeu Du Taquin",
    scale=5,
    color=color.rgb(255, 30, 30),
    position=Vec2(-.4, .1)
)

main_menu.buttons = [
    MenuButton("Jouer", on_click=Func(setattr, state_handler, "state", "load_menu")),
    MenuButton("Sortir", on_click=Sequence(Wait(.01), Func(sys.exit))),
]
for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i - 2) * button_spacing

# Selecteur de niveau
def start_game(level, level_path):
    def load_level():
        skybox_path = os.path.join(level_path, "skybox")
        music_path = os.path.join(level_path, "audio/music.mp3")

        if skybox_path:
            sky.texture = skybox_path
        if music_path:
            Audio(
                music_path,
                volume=MUSIC_VOLUME,
                loop=True
            )
    
    menu_parent.disable()
    load_level()
    level.main()


LEVEL_PATH = "assets/levels"
for i, level_dir in enumerate(os.listdir(LEVEL_PATH)):
    level_path = os.path.join(LEVEL_PATH, level_dir)

    if "__init__.py" not in os.listdir(level_path):
        continue

    level_absolute = level_path.replace("/", ".")
    level_absolute = level_absolute.replace("\\", ".")
    level_module = import_module(level_absolute)

    MenuButton(
        parent=load_menu,
        text=level_dir,
        tooltip=Tooltip(
            text=f"<scale:1.5><yellow>{level_module.config['difficulty']} étoile(s)<scale:1>\n<default>{level_module.config['description']}",
            background_color=color.black,
            wordwrap=25
        ),
        y=(-i * button_spacing),
        on_click=Func(start_game, level_module, level_path)
    )

load_menu.back_button = MenuButton(
    parent=load_menu, text="Retour", y=((-i - 2) * button_spacing),
    on_click=Func(setattr, state_handler, "state", "main_menu")
)

# Petite animation stylé quand on change de menu
for menu in (main_menu, load_menu):
    def animate_in_menu(menu=menu):
        for i, entity in enumerate(menu.children):
            entity.original_x = entity.x
            entity.x += .1
            entity.animate_x(entity.original_x, delay=i * .05, duration=.1, curve=curve.out_quad)

            if isinstance(entity, Text):
                entity.alpha = 0
                entity.animate("alpha", 1, delay=i * .05, duration=.1)
            else:
                entity.alpha = 0
                entity.animate("alpha", .7, delay=i * .05, duration=.1, curve=curve.out_quad)


    menu.on_enable = animate_in_menu

app.run()
