from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.window import WindowBase
from kivy.properties import *
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
import kivy.graphics.instructions
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.animation import Animation
import kivy
kivy.require("1.9.0")
from kivy.properties import ObjectProperty
from enum import IntEnum
import colors
import fonts
import controls
import sounds
from win32 import win32gui  
from kivy.core.audio import SoundLoader
from playsound import playsound



#constants
HIGHLIGHTER_Y = 0.576
BUFFER = 150000

BUTTON_1 = 'z'
BUTTON_2 = 'x'
BUTTON_3 = 'c'
BUTTON_4 = 'a'
BUTTON_5 = 's'
BUTTON_6 = 'd'
HOME_BUTTON = 'q'
COIN_BUTTON = 'w'
DI_UP = 'numpad8'
DI_LEFT = 'numpad4'
DI_RIGHT = 'numpad6'
DI_DOWN = 'numpad2'


# Global Variables
isLoading = False; # may not need this
game_titles = "games.txt"


# See about putting these enums and class definitions into a separate file.
# A list of enums that will make it easier to "human-readably" know where
# the program is currently when traversing the main menu
class CurrentState(IntEnum):
    MAIN_MENU_STATE = 0;
    GAME_STATE = 1;
    LOADING_STATE = 2;

class Section(IntEnum):
    TABS = 0;
    GAMES = 1;
    GAME_OPTIONS = 2;

class Tabs(IntEnum):
    MULTIPLAYER = 0;
    OPTIONS = 1;
    USER = 2;
    POWER = 3;

class GameOptions(IntEnum):
    PLAY = 0;
    SAVES = 1;
    FAVORITE = 2;

# This class contains all the data needed to successfully navigate through
# the main menu options. I MAY ADD A BOOLEAN FOR CHECKING IF THE CURRENT TAB
# HAS A SUBLIST
class Tab:
    def __init__(self):
        self.tabName = "";
        self.isOpen = False;
        self.isSelected = False;
        self.hasFunction = False;
        self.subTabList = [];
        self.subTabIterator = -1;
        

# This class contains all the data needed for fully displaying a game to
# the main menu screen
class Game:
    def __init__(self):
        self.gameName = "";
        self.gameInfo = [];
        self.gameImage = "";
        self.gameVideo = "";
        self.gameDesc = "";
        self.isFavorite = False;

# A small class that holds the name of the game options buttons as well as
# a pointer to what function to call when the option is selected
class Options:
    def __init__(self):
        self.optionName = "";
        self.optionImage = "";
