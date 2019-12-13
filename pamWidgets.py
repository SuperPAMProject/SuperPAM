#Authored and refactored by Michael Tanner

# =============================================================================
#-----PAM WIDGETS MODULE-----
# =============================================================================

#The purpose of this module is to contain and define all custom widgets for the Super PAM.
#The widgets come in four groups: BUTTON, LABEL, GROUP, and MISC.

#MISC. - No clear category. Typically non-interactive.
#BUTTONS - Interactive widgets that respond to the user pressing the 'select' input.
#LABELS - Non-interactive, texttual, responds to input from BUTTONS, GROUPS, or MISC. widgets.
#GROUPS - Containers of other widgets. Used to iterate over groups and issue commands to them.

import platform
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from colors import getColor, getColorOfScheme
from sounds import getSound
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from playsound import playsound
    
system = platform.system()
# =============================================================================
# MISC.
# =============================================================================

class PAMVideo(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_video = ''
        self.playing = False
        self.muted = False
        
class PAMImage(Image):
    bg_image = StringProperty('img/no_alpha.png')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class PAMKeyboardListener(Widget):
    def __init__(self, **kwargs):
        super(PAMKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)

    def _keyboard_closed(self, *args):
        self._keyboard = None


# =============================================================================
# Buttons
# =============================================================================
    #These will be the main interactive widgets. 
    #Each button will have the properties of 'highlighted', 'selected', and 'enabled'

#----PAM BUTTON - The base for all other buttons. The button's colors are organized by
#    d for default, h for highlight and s for selected
class PAMButton(Button):
    #kivy requires static properties defined at the class level,
    #so that they can be binded to events in the constructor.
    highlighted = BooleanProperty(False) 
    selected = BooleanProperty(False)
    font_scale = 0.8
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_id = ''
        self.enabled = BooleanProperty(True)
        self.background_normal = "img/button_bg.png"
        self.d_color = getColor("primary")
        self.h_color = getColor("primary")
        self.s_color = getColor("accent")
        self.h_sound = getSound("highlight_btn")
        self.s_sound = getSound("select_btn")
        self.bind(highlighted=self.on_highlight)
        self.bind(selected=self.on_select)
        self.sound_mute = False
        self.command = lambda x, *args: print(x)
                
    def on_highlight(self, *args):
        if self.highlighted:
            if not self.sound_mute:
                self.play_sound(self.h_sound)

    def on_select(self, *args):
        if self.selected:
            if not self.sound_mute:
                self.play_sound(self.s_sound)
    
    def outputTest(self, *args):
        print("SUCCESS")

    def setFontSize(self, scale):
        self.font_scale = scale
        self.font_size = self.height * 0.1 * self.font_scale

    def play_sound(self, sound):
        if system == 'Windows':
            playsound(sound, False)
        elif system == 'Linux':
            SoundLoader.load(sound)

    def color_transition(self, color):
        anim = Animation(background_color=get_color_from_hex(color), t='in_out_cubic')
        anim.start(self)
        return get_color_from_hex(color)

#----SCALE BUTTON - Buttons that can appropriately scale with the window resolution.
#   The text size in these buttons will scale correctly as well.
class ScaleButton(PAMButton):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setFontSize(self, scale):
        self.font_scale = scale
        self.font_size = self.height * 0.5 * self.font_scale
        

#----PAM ACTION BUTTON - base for the action buttons. Action buttons have their own icons.
#    Their default color is set to the background, so that there is no colored block around the icons.
class PAMActionButton(PAMButton):
    scale_factor = NumericProperty(0.2)
    select_scale = NumericProperty(1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.d_action = ''
        self.h_action = ''
        self.s_action = ''
        self.d_color = getColor("background")   
        self.highlight_anim = Animation(scale_factor=0.25, t='in_out_cubic', duration=0.3)
        self.unhighlight_anim = Animation(scale_factor=0.2, t='in_out_cubic', duration=0.3)
        self.select_anim = Animation(
                    select_scale=1.2, t='in_out_cubic', duration=0.1
                    ) + Animation(
                    select_scale=1, t='in_out_cubic', duration=0.1
                    )

    def on_highlight(self, *args):
        if self.highlighted and not self.selected:
            if not self.sound_mute:
                self.play_sound(self.h_sound)
            self.highlight_anim.start(self)
            self.action_image = self.h_action
        elif not self.highlighted:
            self.action_image=self.d_action
            self.unhighlight_anim.start(self)
    
    def on_select(self, *args):
        if self.selected:
            if not self.sound_mute:
                self.play_sound(self.s_sound)
        else:
            self.action_image=self.d_action


#----TAB ITEM - Button used to navigate the sidebar. 
class SideBarTabItem(ScaleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.d_color = getColor('background')
        self.sidebar = None
        self.is_toggled = False
        self.select_anim = Animation(
              pos_hint={'x':0.44}, t='in_out_cubic', duration=0.3
            ) + Animation(
                pos_hint={'x':0.54}, t='in_out_cubic', duration=0.3)

    def on_select(self, *args):
        if self.selected:
            if not self.sound_mute:
                self.play_sound(self.s_sound)
            self.select_anim.start(self)
            carousel = self.parent.parent.parent.parent.parent.parent.parent.parent
            self.sidebar = carousel.moveToSidebar(self.func_id)
    
    def setFontSize(self, scale):
        self.font_scale = scale
        self.font_size = 27 * self.font_scale
        self.text_size = (self.width, self.height)
 

#----CAROUSEL ITEM - A button that interacts with a label.
#   Each CarouselItem will be associated with a unique game and will display that game's title as its text.
class GameCarouselItem(ScaleButton):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_name = ""
        self.game_info = []
        self.game_path = ""
        self.game_image = ""
        self.game_video = ""
        self.game_desc = ""
        self.is_favorite = False
        self.d_color = getColor("background")
        self.index = 0

    def select_anim(self, color):
        anim = Animation(
                    color=(get_color_from_hex(color)), t='in_out_cubic', duration=0.3
                ) + Animation(
                    color=(1, 1, 1, 1), t='in_out_cubic', duration=0.3)
        anim.start(self)


# =============================================================================
# Labels
# =============================================================================
    #These classes will be used for non-interactive, dynamic textual elements. 

#----SCALE LABEL - Label that is capable of dynamic resizing with the window. 
class ScaleLabel(Label):
    font_scale = 0.8
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setFontSize(self, scale):
        self.font_scale = scale
        self.font_size = self.height * 0.5 * self.font_scale


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
        

# =============================================================================
# Groups
# =============================================================================
    # These classes will act as containers for any of the proceeding classes. 
    # Each container will use the 'children' property to iterate over the widgets inside them and perform operations on them.


#----PAM BUTTON GROUP - Base for other button groups, such as the SideBar
class PAMButtonGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


#----PAM LABEL GROUP - Group for only textual, non-interactive elements
class PAMLabelGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group_font = ''
        self.group_font_size = 20
        self.group_font_color = getColor("font-dark")


#----CONTROL BAR - Displays controls at the bottom of the screen.
class ControlBar(BoxLayout):
    bg_color = ListProperty([0, 0, 0])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = ''

    #Called when the user enters another section (Options, Games, Action buttons) 
    # will display controls relevant to that context
    def context_switch(self, context):
        btn3 = self.children[1]
        btn2 = self.children[3]
        btn1 = self.children[5]

        if context == 'sidebarSection':
            btn1.text = 'Select: '
            btn2.text = 'Back: '
            btn3.text = 'To Game Info: '
        elif context == 'games':
            btn1.text = 'Play: '
            btn2.text = 'Close: '
            btn3.text = 'Favorite: '
        elif context == 'actionbtns':
            btn1.text = 'Select: '
            btn2.text = 'To Sidebar: '
            btn3.text = 'To Games: '
        elif context == 'remap':
            btn1.text = 'Confirm: '
            btn2.text = 'Back: '
            btn3.text = ''


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


#----SIDE BAR TAB - Both a group and an item within a group. The tabs are the items within the sidebar.
#    And each tab houses several buttons the user can select to access their options.  
class SideBarTab(AccordionItem):
    highlighted = BooleanProperty(False)
    selected = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_item_list: SideBarTabItem
        self.collapse = True
        self.d_color = '#FFFFFF00'
        self.func_id = ''
        self.enabled = BooleanProperty(True)
        self.background_normal = "img/no_alpha.png"
        self.background_selected = "img/no_alpha.png"
        self.h_color = getColor("secondary")
        self.s_color = getColor("accent")
        self.h_sound = getSound("highlight_btn")
        self.s_sound = getSound("select_btn")
        self.bind(highlighted=self.on_highlight)
        self.bind(selected=self.on_select)
        self.sound_mute = False
             
    def on_highlight(self, *args):
        if self.highlighted:
            if not self.sound_mute:
                self.play_sound(self.h_sound)

    def on_select(self, *args):
        if self.selected:
            self.collapse = not self.collapse
            subTabs = self.children[0].children[0].children[0].children[0].children
            subTabs[len(subTabs) - 1].highlighted = True
            if not self.sound_mute:
                self.play_sound(self.s_sound)

    def play_sound(self, sound):
        if system == 'Windows':
            playsound(sound, False)
        elif system == 'Linux':
            SoundLoader.load(sound)

    def setFontSize(self, scale):
        self.font_scale = scale
        self.font_size = 27 * self.font_scale
        self.text_size = (self.width, self.height)
        

#----SIDE BAR - Group that contains all Sidebar tabs. 
class SideBar(PAMButtonGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_list: SideBarTab


#----SIDEBAR CAROUSEL - Contains all the sidebars that the user can switch to when selecting
#                       a sub-menu option.
class SidebarCarousel(Carousel):
    def __init__(self, **kwargs):
        super(SidebarCarousel, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'a':
            self.moveToRootSideBar()
        return True

    def moveToSidebar(self, id):
        for sidebar in self.slides:
            if sidebar.bar_id == id:
                self.load_slide(sidebar)
                subTabs = sidebar.children[0].children[0].children[0].children[0].children[0].children
                for tab in subTabs:
                    tab.background_color = get_color_from_hex(tab.d_color)
                return sidebar

    def moveToRootSideBar(self):
        self.load_slide(self.slides[0])
        return self.slides[0]


#TESTING AREA
if __name__ == "__main__":
    pass
#   Put code to test here
#   print("SUCCESS")