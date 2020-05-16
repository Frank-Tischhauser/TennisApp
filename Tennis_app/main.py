from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineListItem

from Tennis_app.player import Player
from Tennis_app.match import Match

import json

Window.size = 350, 500


class HomeScreen(Screen):
    pass


class InputScreen(Screen):
    pass


class SaveScreen(Screen):
    pass


class ListItem(OneLineListItem):
    pass


class CreateButton(MDRectangleFlatButton):

    def on_press(self):
        player1 = Player(self.player1_name)
        player2 = Player(self.player2_name)
        GameScreen.player1 = player1
        GameScreen.player2 = player2
        GameScreen.match = Match(player1, player2, self.match_name)


class GameScreen(Screen):
    pass


class DataScreen(Screen):
    pass


class TennisApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("main.kv")

    def get_json(self):

        with open('data.json', 'r') as file:
            return json.load(file)

    def on_start(self):

        data = self.get_json()

        for dict in data:
            self.root.ids.save_screen.ids.match_list.add_widget(
                ListItem(text='{} : {} vs {}'.format(
                    dict['match_name'], dict['winner_name'], dict['looser_name'])))

    def change_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    TennisApp().run()
