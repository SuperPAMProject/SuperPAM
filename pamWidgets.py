#-----PAM WIDGETS MODULE-----
#The purpose of this module is to contain and define all custom widgets for the Super PAM.
#The widgets come in four groups: BUTTON, LABEL, GROUP, and MISC.

#BUTTONS - interactive widgets that respond to the user pressing the 'select' input
#LABELS - non-interactive, texttual, responds to input from BUTTONS, GROUPS, or MISC. widgets
#GROUPS - containers of other widgets. Used to iterate over groups and issue commands to them
#MISC. - No clear category. Typically non-interactive and experimental. 

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.graphics.vertex_instructions import Rectangle
import controls
import keyboard
import fonts
import colors
from kivy.utils import get_color_from_hex
from enum import Enum
import pamFunctions


#player = "player1" # for testing purposes with the 'controls' module
    

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


#BUTTON CLASSES
#These will be the main interactive widgets. 
#Each button will have the properties of 'highlighted', 'selected', and 'enabled'
#----PAMBUTTON - The base for all other buttons. The button's colors are organized by
#    d for default, h for highlight and s for selected
class PAMButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled = BooleanProperty(True)
        self.btnTxt = StringProperty("")
        self.background_normal = "img/button_bg.png"
        self.d_color = colors.getColor("primary")
        self.h_color = colors.getColor("secondary")
        self.s_color = colors.getColor("accent")
        self.func_id = ''

    #Called when user moves to the next button
    def setHighlight(self):
        self.highlighted = not self.highlighted

    #Called when user is no longer viewing this button
    def unHighlight(self):
        self.highlighted = False


#----PAM ACTION BUTTON - base for the action buttons. Action buttons have their own icons.
#    Their default color is set to the background, so that there is no colored block around the icons.
class PAMActionButton(PAMButton):
    d_color = colors.getColor("background")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.properties)
        self.d_action = ''
        self.h_action = ''
        self.s_action = ''


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
class PopupWindowButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option = Label()
        self.window_pos = 0


#----WINDOW ITEM- A widget inside a popup. The widget contains a name, button, and either a
#    checkbox, radio button, or slider
class PopupWindowItem(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_default = ''
        self.icon_selected = ''
        self.item_name = Label()
        self.sub_widget = Widget()


#----TAB ITEM - Button used to open popup windows for options. 
class SideBarTabItem(PAMButton):
    opensPopup = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 

#----CAROUSEL ITEM - A button that interacts with a label. Selecting it will take the user to the Action Button group.
#   Each CarouselItem will be associated with a unique game and will display that game's title as its text.
class GameCarouselItem(PAMButton):
    game = ''
    opacity = 1 #opacity will change with the item's position on-screen
    d_color = colors.getColor("background")
    background_normal = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameName = "";
        self.gameInfo = [];
        self.gameImage = "";
        self.gameVideo = "";
        self.gameDesc = "";
        self.isFavorite = False;


    def on_carousel_move(self):
        pass


#----SAVE STATE- Button associated with the one of the currently selected game's save states
class SaveState(PAMButton):
    scale = 30
    file_path = ''
    game = ''
    save_date = ''
    save_number = 0
    game_image = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

#----CONTROL BAR ITEM - part of the control bar at the bottom of the screen
#    Each item has both text and an image indicating which control maps to a given command.
class ControlBarItem(Label):
    control_icon = ''
    control_pos = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----GAME TITLE - features the title of the currenty highlighted game in the carousel. 
#    Only updates when a new game is highlighted
class GameTitle(Label):
    alignment = 'center'
    scale = 30
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----GAME INFO - Labels for title, developer, publisher and release year. 
#    The info each label will contain is outlined in the .kv file
class GameInfo(Label):
    alignment = 'left'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        


#GROUP CLASSES
# These classes will act as containers for any of the proceeding classes. 
# Each container will use the 'children' property to iterate over the widgets inside them and perform operations on them.


#----BUTTON GROUP - Base for other button groups, such as the PopUp window and SideBar
class PAMButtonGroup(BoxLayout):
    active = BooleanProperty(False)
    currentIndex = NumericProperty(0)
    forward = 'up'
    backward = 'down'
    leftGroup = ObjectProperty(None)
    rightGroup = ObjectProperty(None)
    leftGroupPos = StringProperty('')
    rightGroupPos = StringProperty('')
    gSpacing = NumericProperty(10)
    gPadding = NumericProperty(10)
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       # keyboard.on_press(self.on_press)


    def setLayout(self):
        if self.orientation == 'vertical':
            self.forward = controls.getInput(player, 'up')
            self.backward = controls.getInput(player, 'down')
            self.leftGroupPos = controls.getInput(player, 'left')
            self.rightGroupPos = controls.getInput(player, 'right')
        else:
            self.forward = controls.getInput(player, 'left')
            self.backward = controls.getInput(player, 'right')
            self.leftGroupPos = controls.getInput(player, 'left')
            self.rightGroupPos = controls.getInput(player, 'right')

        
    def nextIndex(self):
        self.currentIndex += 1
        if self.currentIndex > len(self.children) - 1:
            self.currentIndex = len(self.children) - 1
 

    def prevIndex(self):
        self.currentIndex -= 1
        if self.currentIndex < 0:
            self.currentIndex = 0


    def checkForGroup(self, group):
        return group is not None


    def switchGroup(self, group):
        last_child = len(group.children)-1
        self.active = False
        group.active = True
        self.children[self.currentIndex].unHighlight()
        group.children[last_child].highlighted = True
        group.currentIndex = last_child


    def on_press(self, event):
        if self.active and event.event_type == keyboard.KEY_DOWN:
            print(event.name + " " + event.event_type)
            #This shit is a mess. Just don't bother with it right now.
            if event.name == self.leftGroupPos and self.checkForGroup(self.leftGroup):
                if self.orientation == 'vertical':
                    self.switchGroup(self.leftGroup)
                else:
                    if self.children[len(self.children)-1].highlighted:
                        self.currentIndex -= 1
                        self.switchGroup(self.leftGroup)
            elif event.name == self.rightGroupPos and self.checkForGroup(self.rightGroup):
                if self.orientation == 'vertical':
                    self.switchGroup(self.rightGroup)

            if event.name == self.forward:
                self.children[self.currentIndex].unHighlight()
                self.nextIndex()
                self.children[self.currentIndex].setHighlight()
            elif event.name == self.backward:
                self.children[self.currentIndex].unHighlight()
                self.prevIndex()
                self.children[self.currentIndex].setHighlight()
            
            if event.name == controls.getInput(player, "select"):
                #self.children[self.currentIndex].selected = BooleanProperty(True)
                self.children[self.currentIndex].btnTxt = "SELECTED"
                #self.children[self.currentIndex].press_action()
                pamFunctions.current_game = "games/Castlevania Adventure, The (U) [!].gb"
                f = pamFunctions.getFunction(self.children[self.currentIndex])

#----LABEL GROUP - Group for only textual, non-interactive elements
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

#----DESCRIPTION AREA - Group for widgets that display information about the current game
class GameDescriptionArea(PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = ''
        self.title_style = ''
        self.info_style = ''

#----CAROUSEL- Group for the game library. The carousel will feature one game highlighted at a time. 
#    Non-highlighted games will be de-emphasized through reduced opacity
#    Selecting a game in the carousel will redirect the user to the Action Button Group.
class GameCarousel(PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_list: GameCarouselItem
    
    def on_move(self, direction):
        pass

#----POPUP- Float layout to house buttons for a given options category. 
class PopUpWindow(PAMButtonGroup, PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open = False
        self.title = Label()
        self.message = Label()
        self.item_list: PopupWindowItem
        self.button_list: PopupWindowButton

#----TAB - Both a group and an item within a group. The tabs are the items within the sidebar.
#    And each tab houses several buttons the user can select to access their options.  
class SideBarTab(PAMButtonGroup, PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_item_list: SideBarTabItem
        self.collapse = True

#----SIDEBAR - Group that contains all Sidebar tabs. 
class SideBar(PAMButtonGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_list: SideBarTab
        self.active = False
        

    def collapseAll(self):
        pass

#----SAVE STATE GROUP- Group within a popup window. Contains save states for the currently selected game.
class SaveStateGroup(PAMButtonGroup):
    def __init(self):
        super().__init__(self, **kwargs)
    
    def sortByDate(self):
        pass

    def sortByNumber(self):
        pass



#TESTING AREA
if __name__ == "__main__":
    #Put code to test here
    print("SUCCESS")
    
