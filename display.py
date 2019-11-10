import keyboard
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.carousel import Carousel
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
import kivy
kivy.require("1.9.0")
import includes
import pamWidgets
import pamFunctions
import colors




class GameItem(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 24
        self.color = (1, 1, 1, 1)


class MainMenuLayout(FloatLayout):
    game_select = ObjectProperty(None)
    game_plus_1 = ObjectProperty(None)
    game_plus_2 = ObjectProperty(None)
    game_minus_1 = ObjectProperty(None)
    game_minus_2 = ObjectProperty(None)
    game_titles = "games.txt"


    def __init__(self, **kwargs):
        super(MainMenuLayout, self).__init__(**kwargs)


# Extends the App Kivy Class. Build will be called when run function is called
class HomeMenuApp(App):
    def build(self):
        return MainMenuLayout()

def SetupDisplay():
    Window.clearcolor = get_color_from_hex(colors.getColor("background"))
    #Window.fullscreen = 'auto'  #dont use when debugging
    LabelBase.register(
        name='Roboto',
        fn_regular='fonts/Roboto-Light.ttf',
        fn_bold='fonts/Roboto-Bold.ttf')
    print("Set up")
    return HomeMenuApp()

if __name__ == "__main__":
    menu_app = HomeMenuApp()
    Window.clearcolor = get_color_from_hex(colors.getColor("background"))
    LabelBase.register(
        name='Roboto',
        fn_regular='fonts/Roboto-Light.ttf',
        fn_bold='fonts/Roboto-Bold.ttf')
    menu_app.run()
