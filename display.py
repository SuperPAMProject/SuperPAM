
#Authored by Steven Quast
#Refactored by Michael Tanner

# =============================================================================
#-----DISPLAY MODULE-----
# =============================================================================

# This module is responsible for constructing the SuperPAM GUI.
# On startup, the module will build the GUI based on the style rules
# in the HomeMenu markup module. The module will also set the default
# background color and fonts.

import kivy
kivy.require("1.9.0")
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.text import LabelBase
from colors import getColor


#This class is further defined in the HomeMenu GUI markup module
class MainMenuLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainMenuLayout, self).__init__(**kwargs)

# Extends the App Kivy Class. Build will be called when run function is called
class HomeMenuApp(App):
    def build(self):
        return MainMenuLayout()

# Sets the basic parameters of the display window. 
# Calls the HomeMenuApp constructor to begin building the GUI.
def SetupDisplay():
    Window.clearcolor = get_color_from_hex(getColor("background"))
    Window.fullscreen = 'auto'  #dont use when debugging

    # Include the standard Super PAM fonts
    LabelBase.register(
        name='Roboto',
        fn_regular='fonts/Roboto-Light.ttf',
        fn_bold='fonts/Roboto-Bold.ttf')
    LabelBase.register(
        name='Arial',
        fn_regular='fonts/ARIAL.ttf',
        fn_bold='fonts/ARIALBD.ttf')
    LabelBase.register(
        name='Verdana',
        fn_regular='fonts/VERDANA.ttf',
        fn_bold='fonts/VERDANAB.ttf')
    LabelBase.register(
        name="OpenDyslexic", 
        fn_regular="fonts/OPENDYSLEXIC-REGULAR.OTF", 
        fn_bold="fonts/OPENDYSLEXIC-BOLD.OTF")
    return HomeMenuApp()

if __name__ == "__main__":
    menu_app = HomeMenuApp()
    menu_app.run()
