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
import controls
import fonts
import colors
from kivy.utils import get_color_from_hex
from enum import Enum
import pamFunctions


# player = "player1" # for testing purposes with the 'controls' module
    

#MISC. CLASSES
#These classes don't fit into any of the other categories.

#The video class is for the demo video of the currently highlighted game. Autoplays after 2 seconds.

#The highlighter class is a bit of an experiement. It is a class for a 
# dynamically shaping highlighter that changes depending on which button you are selecting.
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

class Highlighter(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape_rect = False
        self.shape_circ = False
        self.color = ''


#BUTTON CLASSES
#These will be the main interactive widgets. 
#Each button will have the properties of 'highlighted', 'selected', and 'enabled'
#----PAMBUTTON - The base for all other buttons. The button's colors are organized by
#    d for default, h for highlight and s for selected
class PAMButton(Button):
    enabled = BooleanProperty(True)
    btnTxt = StringProperty("NOT SELECTED")
    background_normal = "img/button_bg.png"
    d_color = colors.getColor("primary")
    h_color = colors.getColor("secondary")
    s_color = colors.getColor("accent")
    func_id = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #Called when user navigates onto this button
    def setHighlight(self):
        self.highlighted = not self.highlighted

    #Called when user navigates to a different button
    def unHighlight(self):
        self.highlighted = False

#----PAM ACTION BUTTON - base for the action buttons. Action buttons have their own icons.
#    Their default color is set to the background, so that there is no colored block around the icons.
class PAMActionButton(PAMButton):
    d_color = colors.getColor("background")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#----PLAY BUTTON - Starts currently highlighted game  
class PAMPlayButton(PAMActionButton):
    default_image = 'img/UI_PLAY_ICON.png'
    #func_id = 'play'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def press_action(self, *args):
        print("PLAY") 

#----SAVE BUTTON -  Shows save states of currently highlighted game
class PAMSaveButton(PAMActionButton):
    default_image = 'img/UI_DATA_ICON.png'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def press_action(self, *args):
        print("SAVE") 

#----FAV BUTTON - Adds currently selected game to the Favorites list     
class PAMFavButton(PAMActionButton):
    default_image = 'img/UI_FAVORITE_ICON.png'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def press_action(self, *args):
        print("FAV") 

class PamSlider(PAMButton, Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 100
        self.bar_color = colors.getColor("background")
        self.button_color_default = colors.getColor("primary")
        self.button_color_selected = colors.getColor("accent")

class PamRadioButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = ''
        self.filled = False

    def on_fill(self):
        pass

class PamCheckbox(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked = False

    def on_check(self):
        pass

class PamActionButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selection_size = 1
        self.icon_default = ''
        self.icon_selected = ''

class PopupWindowButton(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option = Label()
        self.window_pos = 0

class PopupWindowItem(PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_default = ''
        self.icon_selected = ''
        self.item_name = Label()
        self.sub_widget = Widget()

class SideBarTabItem(PAMButton):
    opensPopup = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
#----CAROUSEL ITEM - A button that interacts with a label. Selecting it will take the user to the Action Button group.
#    There will only be one button in the carousel, but it will be passed different labels when the users moves
#    up and down over the game library
class GameCarouselItem(PAMButton):
    game = ''
    carousel_pos = 0
    opacity = 1
    d_color = colors.getColor("background")
    background_normal = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_carousel_move(self):
        pass

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


class PAMLabelGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group_font = ''
        self.group_font_size = 20
        self.group_font_color = colors.getColor("font-dark")


class ControlBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = ''

    def on_context_switch(self):
        pass

    def on_remap(self):
        pass


class GameDescriptionArea(PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = ''
        self.title_style = ''
        self.info_style = ''


class GameCarousel(PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_list: GameCarouselItem
    
    def on_move(self, direction):
        pass


class PopUpWindow(PAMButtonGroup, PAMLabelGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open = False
        self.title = Label()
        self.message = Label()
        self.item_list: PopupWindowItem
        self.button_list: PopupWindowButton


class SideBarTab(PAMButtonGroup, PAMButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_item_list: SideBarTabItem
        self.collapsed = True


class SideBar(PAMButtonGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_list: SideBarTab
        self.active = False

    def collapseAll(self):
        pass


class SaveStateGroup(PAMButtonGroup):
    def __init(self):
        super().__init__(self, **kwargs)
    
    def sortByDate(self):
        pass

    def sortByNumber(self):
        pass



#TESTING AREA
if __name__ == "__main__":
    print("SUCCESS")
    
