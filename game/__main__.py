import arcade

from .constants import *
from .views import MainMenuView


def main():
    main_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = MainMenuView()
    main_window.show_view(view)

    arcade.run()


if __name__ == "__main__":
    main()
