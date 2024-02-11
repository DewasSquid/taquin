from ursina import *


class Shaders:
    """Une énumération de fonctions pour shaders"""
    def bloom(blur_size: int = .05):
        return Shader(
            "Bloom",
            fragment=open("./assets/shaders/bloom.frag").read(),
            default_input={
                "blur_size": blur_size
            }
        )

class Textures:
    """Une énumération de chemin d'accès vers des textures"""
    MENU_BACKGROUND = "./assets/images/menu_bg.jpg"