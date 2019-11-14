#-----PAM WIDGETS MODULE-----
#The purpose of this module is to contain and define all custom widgets for the Super PAM.
#The widgets come in four groups: BUTTON, LABEL, GROUP, and MISC.

#MISC. - No clear category. Typically non-interactive and experimental. 
#BUTTONS - interactive widgets that respond to the user pressing the 'select' input
#LABELS - non-interactive, texttual, responds to input from BUTTONS, GROUPS, or MISC. widgets
#GROUPS - containers of other widgets. Used to iterate over groups and issue commands to them

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import *
from kivy.graphics.vertex_instructions import Rectangle
import controls
import keyboard
import fonts
import colors
import sounds
from kivy.utils import get_color_from_hex
from enum import Enum
import pamFunctions
from kivy.core.audio import SoundLoader
from playsound import playsound

    
#MISC. CLASSES
#----VIDEO-  demo video of the currently highlighted game. Autoplays after 2 seconds. 
class PAMVideo(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_video = ''
        self.playing = False
        self.muted = False
    
    def on_play(self):
        pass

    def on_stop(self):
        pass

class GameCarouselHighlighter(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isFavorite = False #see if you can remove this later

class PAMImage(Image):
    bg_image = StringProperty('img/no_alpha.png')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


#BUTTON CLASSES
#These will be the main interactive widgets. 
#Each button will have the properties of 'highlighted', 'selected', and 'enabled'

#----PAM BUTTON - The base for all other buttons. The button's colors are organized by
#    d for default, h for highlight and s for selected
class PAMButton(Button):
    highlighted = BooleanProperty(False)
    selected = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_id = ''
        self.enabled = BooleanProperty(True)
        self.background_normal = "img/button_bg.png"
        self.d_color = colors.getColor("primary")
        self.h_color = colors.getColor("secondary")
        self.s_color = colors.getColor("accent")
        self.h_sound = sounds.getSound("highlight_btn")
        self.s_sound = sounds.getSound("select_btn")
        self.bind(highlighted=self.on_highlight)
        self.bind(selected=self.on_select)
        
        
    def on_highlight(self, *args):
        if self.highlighted:
            playsound(self.h_sound, False)

    def on_select(self, *args):
        if self.selected:
            print(self.func_id + " Selected")
            playsound(self.s_sound, False)

#----SCALE BUTTON - TODO: This class needs a description
class ScaleButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----PAM ACTION BUTTON - base for the action buttons. Action buttons have their own icons.
#    Their default color is set to the background, so that there is no colored block around the icons.
class PAMActionButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.d_action = ''
        self.h_action = ''
        self.s_action = ''
        self.d_color = colors.getColor("background")

    def on_highlight(self, *args):
        if self.highlighted:
            playsound(self.h_sound, False)
            self.action_image = self.h_action
            print(self.canvas.children[4])
            print(self.canvas.children[4].source)
        else:
            self.action_image=self.d_action
    
    def on_select(self, *args):
        if self.selected:
            print(self.func_id + " Selected")
            playsound(self.s_sound, False)
            #self.action_image=self.s_action
        else:
            self.action_image=self.d_action

#----PAM SLIDER - Slider for volume control
class PamSlider(PAMButton, Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 100
        self.bar_color = colors.getColor("background")
        self.button_color_default = colors.getColor("primary")
        self.button_color_selected = colors.getColor("accent")

#----PAM RADIO BUTTON - Radio button for groups of mutually exclusive options. 
#    Filling one button will unfill the others in the same group.
class PamRadioButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = ''
        self.filled = False

    def on_fill(self):
        pass

#----PAM CHECKBOX - Button for true/false options (SFX muted, dyslexia mode, etc.)
class PamCheckbox(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked = False

    def on_check(self):
        pass

#----WINDOW BUTTON- Button featured at the bottom of a popup. 
#    Will typically be used to either exit the popup and save the user's option changes.
class PopupWindowButton(ScaleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option = Label()
        self.window_pos = 0

#----WINDOW ITEM- A widget inside a popup. The widget contains a name, button, and either a
#    checkbox, radio button, or slider
class PopupWindowItem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_default = ''
        self.icon_selected = ''
        self.item_name = Label()
        self.sub_widget = Widget()

#----TAB ITEM - Button used to open popup windows for options. 
class SideBarTabItem(ScaleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
#----CAROUSEL ITEM - A button that interacts with a label. Selecting it will take the user to the Action Button group.
#   Each CarouselItem will be associated with a unique game and will display that game's title as its text.
class GameCarouselItem(ScaleButton):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameName = "";
        self.gameInfo = [];
        self.gamePath = ""
        self.gameImage = "";
        self.gameVideo = "";
        self.gameDesc = "";
        self.isFavorite = False;
        self.d_color = colors.getColor("background")
        self.index = 0


    def on_carousel_move(self):
        pass

#----SAVE STATE- Button associated with the one of the currently selected game's save states
class SaveState(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = 30
        self.file_path = ''
        self.game = ''
        self.save_date = ''
        self.save_number = 0
        self.game_image = ''

    def changeSize(self):
        self.scale += 30
        self.update()
        print("PRESSED")

    def update(self):
        self.font_size = self.scale

    def on_press(self):
        self.changeSize()


#LABEL CLASSES
# These classes will be used for non-interactive, dynamic textual elements. 
# Each label will only change its text under 

#----SCALE LABEL - TODO: This class needs a description
class ScaleLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----CONTROL BAR ITEM - part of the control bar at the bottom of the screen
#    Each item has both text and an image indicating which control maps to a given command.
class ControlBarItem(ScaleLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.control_icon = ''
        self.control_pos = 0

#----GAME TITLE - features the title of the currenty highlighted game in the carousel. 
#    Only updates when a new game is highlighted
class GameTitle(ScaleLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----GAME INFO - Labels for title, developer, publisher and release year. 
#    The info each label will contain is outlined in the .kv file
class GameInfo(ScaleLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

#GROUP CLASSES
# These classes will act as containers for any of the proceeding classes. 
# Each container will use the 'children' property to iterate over the widgets inside them and perform operations on them.

#----PAM BUTTON GROUP - Base for other button groups, such as the PopUp window and SideBar
class PAMButtonGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----PAM LABEL GROUP - Group for only textual, non-interactive elements
class PAMLabelGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group_font = ''
        self.group_font_size = 20
        self.group_font_color = colors.getColor("font-dark")

#----CONTROL BAR - Displays controls at the bottom of the screen.
class ControlBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = ''

    #Called when the user enters another section (Options, Games, Action buttons) 
    # will display controls relevant to that context
    def on_context_switch(self):
        pass

    def on_remap(self):
        pass

#----GAME DESCRIPTION AREA - Group for widgets that display information about the current game
class GameDescriptionArea(PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = ''
        self.title_style = ''
        self.info_style = ''

#----GAME CAROUSEL - Group for the game library. The carousel will feature one game highlighted at a time. 
#    Non-highlighted games will be de-emphasized through reduced opacity
#    Selecting a game in the carousel will redirect the user to the Action Button Group.
class GameCarousel(PAMButtonGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def updateGameInfo(self, game):
        pamFunctions.current_game = game.gameInfo[3]
        print(pamFunctions.current_game)
    
    def on_move(self, direction):
        pass

#----POPUP WINDOW - Float layout to house buttons for a given options category. 
class PopupWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.open = False
        #self.title = ''
        self.message = Label()
        self.item_list: PopupWindowItem
        self.button_list: PopupWindowButton

#----POPUP WINDOW LAYOUT - TODO: This class needs a description
class PopupWindowLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)    

#----SIDE BAR TAB - Both a group and an item within a group. The tabs are the items within the sidebar.
#    And each tab houses several buttons the user can select to access their options.  
class SideBarTab(PAMButtonGroup, ScaleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_item_list: SideBarTabItem
        self.collapse = True
        self.d_color = colors.getColor("background")

#----SIDE BAR - Group that contains all Sidebar tabs. 
class SideBar(PAMButtonGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_list: SideBarTab
        

    def collapseAll(self):
        pass

#----SAVE STATE GROUP- Group within a popup window. Contains save states for the currently selected game.
class SaveStateGroup(PAMButtonGroup):
    def __init(self, **kwargs):
        super().__init__(self, **kwargs)
    
    def sortByDate(self):
        pass

    def sortByNumber(self):
        pass

#TESTING AREA
#if __name__ == "__main__":
#   Put code to test here
#   print("SUCCESS")