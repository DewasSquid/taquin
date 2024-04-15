from ursina import Entity, Tooltip, camera, color, Button


class GameFrame(Entity):
    def __init__(self, *args, **kwargs):
        """Entitée "root", il est recommendé de l'utiliser en tant que parent"""
        super().__init__(
            parent=camera.ui,
            y=.15,
            *args,
            **kwargs
        )

class MenuButton(Button):
    def __init__(self, text: str, tooltip: Tooltip = None, *arg, **kwargs) -> None:
        """Boutton personalisé avec style préfait

        Args:
            text (str): le texte à afficher
            tooltip (Tooltip): Une boite d'informations supplémentaires qui s's'affiche au passage de la souris
        """
        super().__init__(
            text=text,
            tooltip=tooltip,
            scale=(.25, .075),
            highlight_color=color.azure,
            *arg,
            **kwargs
        )