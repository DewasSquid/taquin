import os
import subprocess
import sys
from importlib import import_module

from ursina import *

from modules import *

MUSIC_VOLUME = 0.5
SOUND_VOLUME = 1

class Game:
    def __init__(self):
        self.menu_parent = GameFrame()
        self.main_menu = Entity(parent=self.menu_parent)
        self.load_menu = Entity(parent=self.menu_parent)
        self.state_handler = Animator({
            "main_menu": self.main_menu,
            "load_menu": self.load_menu,
        })

        self.button_spacing = .075 * 1.25
        self.setup_main_menu()
        self.setup_load_menu()
        self.setup_escape_menu()

    def setup_main_menu(self):
        self.main_menu.title = Text(
            parent=self.main_menu,
            text="Jeu Du Taquin",
            scale=5,
            position=Vec2(-.4, .1)
        )

        self.main_menu.buttons = [
            MenuButton("Jouer", on_click=Func(setattr, self.state_handler, "state", "load_menu")),
            MenuButton("Sortir", on_click=sys.exit),
        ]
        for i, e in enumerate(self.main_menu.buttons):
            e.parent = self.main_menu
            e.y = (-i - 2) * self.button_spacing

    def setup_load_menu(self):
        LEVEL_PATH = "assets/levels"
        for i, level_dir in enumerate(os.listdir(LEVEL_PATH)):
            level_path = os.path.join(LEVEL_PATH, level_dir)

            if "__init__.py" not in os.listdir(level_path):
                continue

            level_absolute = level_path.replace("/", ".")
            level_absolute = level_absolute.replace("\\", ".")
            level_module = import_module(level_absolute)

            MenuButton(
                parent=self.load_menu,
                text=level_dir,
                tooltip=Tooltip(
                    text=f"<scale:1.5><yellow>{level_module.config['difficulty']} étoile(s)<scale:1>\n<default>{level_module.config['description']}",
                    background_color=color.black,
                    wordwrap=25
                ),
                y=(-i * self.button_spacing),
                on_click=Func(self.start_game, level_module, level_path)
            )

        self.load_menu.back_button = MenuButton(
            parent=self.load_menu, text="Retour", y=((-i - 2) * self.button_spacing),
            on_click=Func(setattr, self.state_handler, "state", "main_menu")
        )
    
    def setup_escape_menu(self):
        self.escape_menu = WindowPanel(
            title="Escape (ECHAP pour reprendre)",
            content=[Button(
                text="Quitter",
                on_click=Func(os.execv, sys.executable, ['python'] + sys.argv)
            )],
            enabled=False
        )

    def start_game(self, level, level_path):
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
        
        self.menu_parent.disable()
        load_level()
        level.main()

    def animate_in_menu(self, menu):
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
        
    def run(self):
        for menu in (self.main_menu, self.load_menu):
            menu.on_enable = Func(self.animate_in_menu, menu)
        app.run()

def input(key):
    if key != "escape": return
    if game.menu_parent.enabled: return
    
    game.escape_menu.enabled = not game.escape_menu.enabled

if __name__ == "__main__":
    app = Ursina()
    sky = Sky()
    game = Game()
    game.run()
