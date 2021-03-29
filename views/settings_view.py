from abc import ABC, abstractmethod

import arcade
import arcade.gui

from config import CONFIG
from functools import partial


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.last_size = (self.width, self.height) = self.window.get_size()
        # use setting_index to grab the currently selected setting
        self.setting_index = 0

        # setting_list will store list of settings to add to the view
        self.setting_list = [
            partial(SettingToggle, text="Turn music off/on", binding="is_music_on"),
            partial(SettingToggle, text="Fullscreen", binding="is_fullscreen"),
            partial(SettingSlider, text="Adjust volume", binding="music_volume"),
            partial(SettingToggle, text="test", binding="is_music_on")
        ]
        self.setting_list = [
            setting(self.width // 4, self.height - i * 60 - self.height // 4)
            for i, setting in enumerate(self.setting_list)
        ]

    def on_draw(self):
        arcade.start_render()
        self.setup()

        arcade.draw_text("Settings", self.width // 2 - 22, self.height * .90, arcade.color.WHITE, 20)

        longest = (self.width // 2)
        for setting in self.setting_list:
            setting.draw(longest)

        setting = self.setting_list[self.setting_index]
        x = setting.x + (longest + 60) // 2
        width = longest + 100

        if type(setting) == SettingToggle:
            arcade.draw_rectangle_outline(
                center_x=x,
                center_y=setting.y + 8,
                width=width,
                height=30,
                color=arcade.color.WHITE,
            )
        else:
            arcade.draw_rectangle_outline(
                center_x=x,
                center_y=setting.y,
                width=width,
                height=60,
                color=arcade.color.WHITE,
                )

    def on_show_view(self):
        ...

    def on_update(self, delta_time: float):
        ...

    def update(self, delta_time: float):
        if self.last_size != (new_size := self.window.get_size()):
            self.width, self.height = new_size
            for i, setting in enumerate(self.setting_list):
                setting.x = self.width // 4
                setting.y = self.height - i * 50 - self.height // 4
        self.last_size = new_size

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.setting_index -= 1
            if self.setting_index < 0:
                self.setting_index = len(self.setting_list) - 1
        elif symbol == arcade.key.DOWN:
            self.setting_index = (self.setting_index + 1) % len(self.setting_list)
        elif symbol == arcade.key.LEFT:
            self.setting_list[self.setting_index].decrease()
        elif symbol == arcade.key.RIGHT:
            self.setting_list[self.setting_index].increase()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        pass


class SettingField(ABC):
    """
    Represents a setting the user can modify, with a text label.
    """

    def __init__(self, x: int, y: int, text: str, binding: str):
        self.x = x
        self.y = y
        self.text = text
        self.binding = binding
        self.length = len(self.text) * 8

    @property
    def value(self):
        return getattr(CONFIG, self.binding)

    @value.setter
    def value(self, value):
        setattr(CONFIG, self.binding, value)

    @value.getter
    def value(self):
        return getattr(CONFIG, self.binding)

    def draw(self, longest):
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            color=arcade.csscolor.WHITE,
            width=self.length,
            font_name="arial.ttf",
        )

    @abstractmethod
    def decrease(self):
        ...

    @abstractmethod
    def increase(self):
        ...


class SettingToggle(SettingField):
    """
    Represents a toggleable setting
    """

    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        self.value = False

    def increase(self):
        self.value = True

    def draw(self, longest):
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            color=arcade.csscolor.WHITE,
            width=self.length,
        )
        arcade.draw_rectangle_outline(
            self.x + longest + 35, self.y + 8, 49, 20, color=arcade.color.AQUA
        )
        if self.value:
            arcade.draw_rectangle_filled(
                self.x + longest + 47,
                self.y + 8,
                23,
                18,
                color=arcade.color.AO,
            )

        else:
            arcade.draw_rectangle_filled(
                self.x + longest + 23,
                self.y + 8,
                23,
                18,
                color=arcade.color.RED,
            )


class SettingSlider(SettingField):
    """
    Represents a setting with a slider, with values ranging from [1, 10]
    """

    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        if 2 <= self.value:
            self.value -= 1

    def increase(self):
        if self.value < 10:
            self.value += 1

    def draw(self, longest):
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            color=arcade.csscolor.WHITE,
            width=self.length,
        )
        arcade.draw_line(self.x, self.y - 15, self.x + longest, self.y - 15, arcade.color.WHITE)
        arcade.draw_text(str(self.value), self.x + longest + 25, self.y - 10, arcade.color.WHITE, 20)

        tick_len = longest // 9
        arcade.draw_circle_filled(self.x + (tick_len * (self.value - 1)), self.y - 15, 8.0, arcade.color.WHITE)
