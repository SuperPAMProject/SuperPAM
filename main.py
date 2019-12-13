#Authored by Steven Quast and Michael Tanner
#Refactored by Michael Tanner


# =============================================================================
#-----MAIN MODULE-----
# =============================================================================

# This module will initally run all SuperPAM code on startup.
# It will intialize the main menu and run the update loop every time the user
# presses a button. The update loop will affect all active widgets in the menu,
# updating their color, font, size, and highlight/selection status.

#GUI FRAMEWORK IMPORTS
import kivy
kivy.require("1.9.0")
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.base import EventLoop
from kivy.core.audio import SoundLoader

#GENERAL LIBRARIES
import sys, os, platform, threading
from datetime import datetime
from win32 import win32gui
import functools

#PAM SYSTEM COMPONENTS
from menuDivisions import *
import mainMenu
import display

#RESOURCES
from colors import getColor, getColorOfScheme
from sounds import getSound
from controls import *
from playsound import playsound

#PAM FUNCTIONS
from pamFunctions import playGame
from pamFunctions import getFunction
from pamFunctions import sortByTitle
from pamFunctions import get_hwnds_for_pid
from pamFunctions import get_window_pid


# Resize function so that we can ensure the game carousel animates properly, regardless of window size
def onResize(one, two, three):
    if pam.selected_y is not 0 and pam.selected_y is not None:
        pam.selected_y = pam.layout.ids["games"].children[3].y


#Initial time and buffer. Will be used to track time between inputs.
currenttime = datetime.now()
BUFFER = 150000

# This class serves as the entirety of the program. It will be the
# container for all the necessary data as well as how to interact with and interpret
# said data
class PAM:
    def __init__(self):
        #Initialize layout
        self.current_state = MAIN_MENU_STATE 
        self.Display = display.SetupDisplay()
        self.Display.load_kv("HomeMenu.kv")
        self.layout = self.Display.build()
        self.Display.built = True
        self.Display.root = self.layout
        self.MM = mainMenu.mainMenu(self.layout.ids["sidebar"], self.layout.ids["games"], self.layout.ids["actionbtns"])
        
        #Animation IDs for game carousel items
        self.comp_anims = [False, False, False, False, False, False, False]
        self.anim0 = None
        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        self.anim5 = None
        self.anim6 = None
        self.current_anim_event = None
        self.selected_y = None

        sortByTitle(self.MM.game_list) #Initialize game library sorted by title

        #No update yet, wait for user input
        self.updateState(None)
        self.running_game = None
        self.last_selected_game = None
        self.setGames()
        self.window = EventLoop.window
        self.window.bind(on_resize=onResize)
        self.event_dict = {
            BUTTON_1: currenttime,
            BUTTON_2: currenttime, 
            BUTTON_3: currenttime,
            BUTTON_4: currenttime,
            BUTTON_5: currenttime,
            BUTTON_6: currenttime,
            HOME_BUTTON:currenttime,
            COIN_BUTTON: currenttime,
            DI_UP: currenttime,
            DI_DOWN: currenttime,
            DI_LEFT:currenttime,
            DI_RIGHT: currenttime
        }
        
        #Begin listening for user input
        self.kListener  = self.layout.ids['kListener']
        self.kListener.keyboard = Window.request_keyboard(self._keyboardClosed, self.kListener)
        self.kListener.keyboard.bind(on_key_down=self.readInputs)
        self.system = platform.system()

        #LOADING SCREEN ANIMATIONS
        self.is_loading = True
        self.logo_anim = Animation(
            opacity=1, t='in_out_cubic', duration=1
            ) + Animation(
            opacity=1, t='in_out_cubic', duration=3
            ) + Animation(
            opacity=0, t='in_out_cubic', duration=1)

        self.wiggle = Animation(
            y=self.layout.ids['logo'].y - 10, t='in_out_cubic', duration=0.3
        ) + Animation(
            y=self.layout.ids['logo'].y + 10, t='in_out_cubic', duration=0.2
        ) + Animation(
            y=self.layout.ids['logo'].y - 10, t='in_out_cubic', duration=0.3
        )

            #FOR BACKGROUND
        self.load_anim = Animation(
            opacity=1, t='in_out_cubic', duration=2
        )+ Animation(
            opacity=0, t='in_out_cubic', duration=0.7
            )

        self.load_anim.start(self.layout.ids['load'])
        self.logo_anim.start(self.layout.ids['logo'])
        self.wiggle.start(self.layout.ids['logo'])
        load_sound = getSound('enter_menu')
        if self.system == 'Windows':
            Clock.schedule_once(functools.partial(self.playMenuSound, load_sound), 2)
        self.is_loading = False
        
    # check current_state and if program is loading
    # displays window based on the current state    
    def displayState(self):
        if not self.is_loading:
            print("Check current_state and display the appropriate window")
        else:
            pass # There's nothing for you to do right now

    # Reads all current button inputs. Because keyboard can't suppress inputs in Linux,
    # editing of the emulator's input reading may be necessary.
    def readInputs(self, keyboard, keycode, text, modifiers):

        if keycode[1] not in self.event_dict:
            return

        #Record time between inputs
        new_time = datetime.now()
        old_time = self.event_dict[keycode[1]]

        if new_time.second == old_time.second:
            if (new_time.microsecond - old_time.microsecond) < BUFFER:
                return
        elif new_time.second - old_time.second == 1:
            if (1000000 + new_time.microsecond - old_time.microsecond) < BUFFER:
                return

        self.event_dict[keycode[1]] = new_time

        if not self.is_loading:
            if keycode[1] == BUTTON_1:
                # Accept button
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        self.selectTab()
                                
                    elif self.MM.currentSection == Section.GAMES:
                        pass # For now
                                                
                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        self.selectActionButton()
                
            elif keycode[1] == BUTTON_2:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        carousel = self.layout.ids['car']
                        if carousel.current_slide is not carousel.slides[0]:
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            self.MM.CurrentSubTab(subTabs).highlighted = False
                            carousel.moveToRootSideBar()
                            self.switchToSidebar(carousel.slides[0])
                    elif self.MM.currentSection == Section.GAMES:
                        self.running_game = None
                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        self.MM.currentSection = Section.TABS

            elif keycode[1] == BUTTON_3:
                if self.MM.currentSection == Section.ACTION_BUTTONS:
                    self.MM.currentSection = Section.GAMES
                elif self.MM.currentSection == Section.TABS:
                    self.MM.currentSection = Section.ACTION_BUTTONS

            elif keycode[1] == BUTTON_4:
                # Accept button
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        self.selectTab()
                                
                    elif self.MM.currentSection == Section.GAMES:
                        pass # For now
                                                
                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        self.selectActionButton()
                        
            elif keycode[1] == BUTTON_5:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        carousel = self.layout.ids['car']
                        if carousel.current_slide is not carousel.slides[0]:
                            carousel.moveToRootSideBar()
                            self.switchToSidebar(carousel.slides[0])
                    elif self.MM.currentSection == Section.GAMES:
                        self.running_game = None
                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        self.MM.currentSection = Section.TABS

            elif keycode[1] == BUTTON_6:
                if self.MM.currentSection == Section.ACTION_BUTTONS:
                    self.MM.currentSection = Section.GAMES
                elif self.MM.currentSection == Section.TABS:
                    self.MM.currentSection = Section.ACTION_BUTTONS

            elif keycode[1] == HOME_BUTTON:
                if self.current_state == MAIN_MENU_STATE:
                    if self.running_game is not None:
                        self.resumeGame()
                        self.current_state = GAME_STATE

                elif self.current_state == GAME_STATE:
                    self.pauseGame() #GO BACK TO HOME MENU
                    self.current_state = MAIN_MENU_STATE

            elif keycode[1] == COIN_BUTTON:
                pass

            elif keycode[1] == DI_DOWN:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        #If tab is closed
                        if self.MM.CurrentTab().collapse:
                            self.MM.CurrentTab().highlighted = False

                            #Progress downward in major tabs until at end
                            self.MM.t_i -= 1
                            if self.MM.t_i <= 0:
                                self.MM.t_i = 0

                            self.MM.CurrentTab().highlighted = True
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            self.MM.s_t_i = len(subTabs) - 1
                            if self.MM.CurrentTab().title is not 'POWER':
                                subTabs[len(subTabs)-1].highlighted = True

                        #If tab is open
                        else:
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            
                            if self.MM.CurrentTab().title is not 'POWER':
                                self.MM.CurrentSubTab(subTabs).highlighted = False
                            
                            self.MM.s_t_i -= 1

                            #Progress downward in sub tabs until at end. Close current major tab
                            if self.MM.s_t_i < 0:
                                self.MM.s_t_i = len(subTabs) - 1
                                if self.MM.t_i > 0:
                                    self.MM.CurrentTab().collapse = True

                            if self.MM.CurrentTab().title is not 'POWER':
                                self.MM.CurrentSubTab(subTabs).highlighted = True                              

                    elif self.MM.currentSection == Section.GAMES:
                        if not self.MM.sfx_is_mute:
                            self.playMenuSound(getSound("down_carousel"))
                        
                        self.MM.g_i += 1
                        if self.MM.g_i >= len(self.MM.game_list):
                            self.MM.g_i = 0
                        self.MM.f_i += 1
                        if self.MM.f_i >= len(self.MM.favorite_list):
                            self.MM.f_i = 0
                        # Cycle through games
                    
                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        if not self.MM.sfx_is_mute:
                            self.playMenuSound(getSound("down_carousel"))

                        self.MM.g_i += 1
                        if self.MM.g_i >= len(self.MM.game_list):
                            self.MM.g_i = 0
                        self.MM.f_i += 1
                        if self.MM.f_i >= len(self.MM.favorite_list):
                            self.MM.f_i = 0

                    else:
                        pass # being in the game options doesn't matter


                elif self.current_state == GAME_STATE:
                    # Transfer input to emulator
                    print("Transfer Input")
                    
                else:
                    print("DEBUG: The current state is incorrect")

            elif keycode[1] == DI_UP:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.TABS:
                        #Tab is closed
                        if self.MM.CurrentTab().collapse:
                            self.MM.CurrentTab().highlighted = False
                            
                            #Progress upward in major tabs until at end
                            self.MM.t_i += 1
                            if self.MM.t_i >= len(self.MM.tabs_list) - 1:
                                self.MM.t_i = len(self.MM.tabs_list) - 1

                            self.MM.CurrentTab().highlighted = True
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            self.MM.s_t_i = len(subTabs) - 1

                        #Tab is open
                        else:    
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            #break free of bottom tabs
                            if self.MM.t_i == 0 and self.MM.s_t_i == len(subTabs) - 1: 
                                self.MM.t_i += 1
                                if self.MM.t_i > len(self.MM.tabs_list) - 1:
                                    self.MM.t_i = len(self.MM.tabs_list) - 1
                                self.MM.CurrentTab().highlighted = True
                                subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                                self.MM.s_t_i = len(subTabs) - 1
                            if self.MM.CurrentTab().title is not 'POWER':
                                self.MM.CurrentSubTab(subTabs).highlighted = False
                            
                            #Progress upward in sub tabs until at top. If at top, close current major tab.
                            self.MM.s_t_i += 1
                            if self.MM.s_t_i > len(subTabs) - 1:
                                self.MM.s_t_i = len(subTabs) - 1
                                if self.MM.t_i > 0:
                                    self.MM.CurrentTab().collapse = True

                            if self.MM.CurrentTab().title is not 'POWER':
                                self.MM.CurrentSubTab(subTabs).highlighted = True



                    elif self.MM.currentSection == Section.GAMES:
                        if not self.MM.sfx_is_mute:
                            self.playMenuSound(getSound("up_carousel"))
                        self.MM.g_i -= 1
                        if self.MM.g_i < 0:
                            self.MM.g_i =  len(self.MM.game_list) - 1
                        self.MM.f_i -= 1
                        if self.MM.f_i < 0:
                            self.MM.f_i =  len(self.MM.favorite_list) - 1
                        # Cycle through games

                    elif self.MM.currentSection == Section.ACTION_BUTTONS:
                        if not self.MM.sfx_is_mute:
                            self.playMenuSound(getSound("down_carousel"))

                        self.MM.g_i += 1
                        if self.MM.g_i >= len(self.MM.game_list):
                            self.MM.g_i = 0
                        self.MM.f_i += 1
                        if self.MM.f_i >= len(self.MM.favorite_list):
                            self.MM.f_i = 0

                    else:
                        pass # being in the game options doesn't matter


                elif self.current_state == GAME_STATE:
                    # Transfer input to emulator
                    print("Transfer Input")
                    
                else:
                    print("DEBUG: The current state is incorrect")
                
            elif keycode[1] == DI_LEFT:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.ACTION_BUTTONS and  (len(self.MM.action_button_list) - 1) - self.MM.a_b_i > ActionButtons.PLAY:
                        self.MM.a_b_i += 1 
                    elif self.MM.currentSection > Section.TABS:
                        self.MM.currentSection -= 1 
                    elif self.MM.currentSection == Section.TABS:
                        carousel = self.layout.ids['car']
                        if carousel.current_slide is not carousel.slides[0]:
                            carousel.moveToRootSideBar()
                            self.switchToSidebar(carousel.slides[0])
                    else:
                        pass # eat the input

                elif self.current_state == GAME_STATE:
                    # Transfer input to emulator
                    print("Transfer Input")
                    
                else:
                    print("DEBUG: The current state is incorrect")
                
            elif keycode[1] == DI_RIGHT:
                if self.current_state == MAIN_MENU_STATE:
                    if self.MM.currentSection == Section.ACTION_BUTTONS and (len(self.MM.action_button_list) - 1) - self.MM.a_b_i < ActionButtons.FAVORITE:
                        self.MM.a_b_i -= 1
                    elif self.MM.currentSection < Section.ACTION_BUTTONS:
                        self.MM.currentSection += 1
                        self.MM.a_b_i = len(self.MM.action_button_list) - 1
                    else:
                        pass # eat the input

                elif self.current_state == GAME_STATE:
                    # Transfer input to emulator
                    print("Transfer Input")
                    
                else:
                    print("DEBUG: The current state is incorrect")
                
        else:
            pass # There's nothing to do right now

        self.updateState(keycode)

    # This function gets called when a game carousel animation completes
    def completeAnim(self, anim, wid):
        self.comp_anims[wid.index] = True
        all_true = True
        for isComplete in self.comp_anims:
            if isComplete == False:
                all_true = False
                break
        
        # all animations done
        if all_true:
            # Grab the carousel as  well as widget height
            games = self.layout.ids["games"].children
            height = games[0].height

            # reset widget locations starting with the current game widget's known base location
            games[3].y = self.selected_y

            # from here, every other game carousel item's y position can be set
            # (0,0) is at the bottom left of the window
            games[6].y = games[3].y + height * 3
            games[5].y = games[3].y + height * 2
            games[4].y = games[3].y + height * 1
            games[2].y = games[3].y - height * 1
            games[1].y = games[3].y - height * 2
            games[0].y = games[3].y - height * 3

            # reset the game list
            self.setGames()

            #reset values so that animations can begin again
            self.comp_anims = [False, False, False, False, False, False, False]
            self.anim0 = None

    # This function gets called on startup to initialize the game to our desired settings
    # and also whenever a new input is received from the player
    def updateState(self, keycode):
        """based on the current state, inputs will alter the state:
        if current state is menu state, the stick will iterate through
        the various menus/sections and call functions as needed.
        If current state is game state, inputs will be determined based on
        control scheme and then transmitted as the appropriate inputs
        If current state is paused state, inputs will be read as appropriate
        (P2 inputs only, etc.)"""

        if self.current_state == MAIN_MENU_STATE:
            # DEBUG SETTING
            if keycode is None:
                self.MM.currentSection = Section.GAMES
                print("DEBUG: The PAM is starting in: " + str(self.MM.currentSection))
            ############################

            if keycode is None or True:
                title = win32gui.GetWindowText (win32gui.GetForegroundWindow())
                pid = get_window_pid(title)
                self.running_game = pid

                # Undo all selections in the Tabs Section
                for tab in self.MM.tabs_list:
                    #ensure tabs use the current color scheme
                    tab.h_color = getColorOfScheme('primary', self.MM.current_color_scheme)
                    tab.s_color = getColorOfScheme('secondary', self.MM.current_color_scheme)
                    tab.background_color = get_color_from_hex(tab.d_color)
                    tab.background_normal = 'img/no_alpha.png'
                    tab.background_selected = 'img/no_alpha.png'
                    tab.sound_mute = self.MM.sfx_is_mute
                    tab.font_name = self.MM.current_font
                    tab.setFontSize(self.MM.current_font_size)

                    subTabs = tab.children[0].children[0].children[0].children[0].children
                    for subtab in subTabs:
                        subtab.h_color = getColorOfScheme('primary', self.MM.current_color_scheme)
                        subtab.s_color = getColorOfScheme('secondary', self.MM.current_color_scheme)
                        subtab.bold = False
                        subtab.setFontSize(self.MM.current_font_size)
                        subtab.font_name = self.MM.current_font
                        subtab.background_color = get_color_from_hex(subtab.d_color)

                        subtab.sound_mute = self.MM.sfx_is_mute

                        if subtab.is_toggled:
                            subtab.bold = True
                            subtab.background_color = get_color_from_hex(subtab.s_color)
                    

                    #set tab fonts
                    tab.font_name = self.MM.current_font #REWORK FOR NEW ACCORDION
 
                for child in self.layout.ids['gameDescArea'].children:
                    child.font_name = self.MM.current_font
                    child.setFontSize(self.MM.current_font_size)

                for child in self.layout.ids['actionbtns'].children:
                    child.sound_mute = self.MM.sfx_is_mute
                
                for child in self.layout.ids['games'].children:
                    child.font_name = self.MM.current_font
                    child.setFontSize(self.MM.current_font_size)

                #Update colors of control bar
                self.layout.ids['controlbar'].bg_color = get_color_from_hex(getColorOfScheme('primary', self.MM.current_color_scheme))
                
                # Stop all animations in the Games Section
                if keycode is None or self.selected_y is None or self.selected_y is 0:
                    self.selected_y = self.layout.ids["games"].children[3].y

                if keycode is not None:
                    if True:#event.event_type is keyboard.KEY_DOWN:
                        # stop previous animations
                        if self.anim0 is not None:
                            # due to how we end animations the game iterator will be 
                            # temporarily changed in order to avoid an issue where the
                            # desired game will already be set and will get animated away
                            # before being reset to the proper position
                            if keycode[1] == DI_UP:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.game_list):
                                    self.MM.g_i = 0
                                self.MM.f_i += 1
                                if self.MM.f_i >= len(self.MM.favorite_list):
                                    self.MM.f_i = 0

                            elif keycode[1] == DI_DOWN:
                                self.MM.g_i -= 1
                                if self.MM.g_i < 0:
                                    self.MM.g_i =  len(self.MM.game_list) - 1
                                self.MM.f_i -= 1
                                if self.MM.f_i < 0:
                                    self.MM.f_i =  len(self.MM.favorite_list) - 1

                            carousel = self.layout.ids["games"]
                            games = carousel.children
                            self.anim0.stop(games[6])
                            self.anim1.stop(games[5])
                            self.anim2.stop(games[4])
                            self.anim3.stop(games[3])
                            self.anim4.stop(games[2])
                            self.anim5.stop(games[1])
                            self.anim6.stop(games[0])

                            # return game iterator to where it is supposed to be
                            if keycode[1] == DI_UP:
                                self.MM.g_i -= 1
                                if self.MM.g_i < 0:
                                    self.MM.g_i =  len(self.MM.game_list) - 1
                                self.MM.f_i -= 1
                                if self.MM.f_i < 0:
                                    self.MM.f_i =  len(self.MM.favorite_list) - 1

                            elif keycode[1] == DI_DOWN:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.game_list):
                                    self.MM.g_i = 0
                                self.MM.f_i += 1
                                if self.MM.f_i >= len(self.MM.favorite_list):
                                    self.MM.f_i = 0

                # Undo all selections in the Game Options Section
                for option in self.MM.action_button_list:
                    option.highlighted = False
                    #ensure buttons use the current color scheme
                    self.layout.ids['play'].d_action = getColorOfScheme('play-d', self.MM.current_color_scheme)
                    self.layout.ids['play'].h_action = getColorOfScheme('play-h', self.MM.current_color_scheme)
                    self.layout.ids['play'].s_action = getColorOfScheme('play-s', self.MM.current_color_scheme)
                    self.layout.ids['play'].action_image = self.layout.ids['play'].d_action

                    self.layout.ids['fav'].d_action = getColorOfScheme('fav-d', self.MM.current_color_scheme)
                    self.layout.ids['fav'].h_action = getColorOfScheme('fav-h', self.MM.current_color_scheme)
                    self.layout.ids['fav'].s_action = getColorOfScheme('fav-s', self.MM.current_color_scheme)
                    self.layout.ids['fav'].action_image = self.layout.ids['fav'].d_action

                    #option.background_color = get_color_from_hex(option.d_color)

                # Then set new selection
                if self.MM.currentSection == Section.TABS:
                    self.transitionToSection('sidebarSection')
                    self.layout.ids['controlbar'].context_switch('sidebarSection')
                    self.setGames()
                    subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                    if self.MM.CurrentTab().highlighted:
                        self.MM.CurrentTab().background_normal = getColorOfScheme('tab-d', self.MM.current_color_scheme)
                        self.MM.CurrentTab().background_selected = getColorOfScheme('tab-d', self.MM.current_color_scheme)
                        self.MM.CurrentTab().background_color = get_color_from_hex(self.MM.CurrentTab().h_color)
                    
                    for subTab in subTabs:
                        if subTab.highlighted:
                            subTab.h_color = getColorOfScheme('primary', self.MM.current_color_scheme)
                            subTab.background_color = get_color_from_hex(subTab.h_color)
                                                                    
                elif self.MM.currentSection == Section.GAMES:
                    if self.MM.GetGame().is_favorite:
                        self.layout.ids['fav'].action_image = self.layout.ids['fav'].s_action

                    self.transitionToSection('games')
                    self.layout.ids['controlbar'].context_switch('games')
                    # the game section doesn't need to be updated at the start of the program
                    if keycode is not None:
                        # Edge case
                        if keycode[1] == DI_LEFT or keycode[1] == DI_RIGHT:
                            self.setGames()

                        # Initialization
                        
                        carousel = self.layout.ids["games"]
                        games = carousel.children
                        anim_x = carousel.x
                        anim_height = games[0].height
                        
                        y0 = games[6].y
                        y1 = games[5].y
                        y2 = games[4].y
                        y3 = games[3].y
                        y4 = games[2].y
                        y5 = games[1].y
                        y6 = games[0].y

                        
                        # animate carousel downwards
                        if keycode[1] == DI_UP:

                            # set new animation event
                            self.current_anim_event = keycode[1]

                            # set animations
                            self.anim0 = Animation(x=anim_x, y=y0 - anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim1 = Animation(x=anim_x, y=y1 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim2 = Animation(x=anim_x, y=y2 - anim_height, color = (1,1,1,1.00), t='in_out_cubic')
                            self.anim3 = Animation(x=anim_x, y=y3 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim4 = Animation(x=anim_x, y=y4 - anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim5 = Animation(x=anim_x, y=y5 - anim_height, color = (1,1,1,0.00), t='in_out_cubic')
                            self.anim6 = Animation(x=anim_x, y=y6 - anim_height, color = (1,1,1,0.00), t='in_out_cubic')

                            # bind the completion function
                            self.anim0.bind(on_complete=self.completeAnim)
                            self.anim1.bind(on_complete=self.completeAnim)
                            self.anim2.bind(on_complete=self.completeAnim)
                            self.anim3.bind(on_complete=self.completeAnim)
                            self.anim4.bind(on_complete=self.completeAnim)
                            self.anim5.bind(on_complete=self.completeAnim)
                            self.anim6.bind(on_complete=self.completeAnim)

                            # start animations
                            self.anim0.start(games[6])
                            self.anim1.start(games[5])
                            self.anim2.start(games[4])
                            self.anim3.start(games[3])
                            self.anim4.start(games[2])
                            self.anim5.start(games[1])
                            self.anim6.start(games[0])

                        # animate carousel upwards
                        elif keycode[1] == DI_DOWN:

                            # set new animation event
                            self.current_anim_event = keycode[1]

                            # set animations
                            self.anim0 = Animation(x=anim_x, y=y0 + anim_height, color = (1,1,1,0), t='in_out_cubic')
                            self.anim1 = Animation(x=anim_x, y=y1 + anim_height, color = (1,1,1,0), t='in_out_cubic')
                            self.anim2 = Animation(x=anim_x, y=y2 + anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim3 = Animation(x=anim_x, y=y3 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim4 = Animation(x=anim_x, y=y4 + anim_height, color = (1,1,1,1), t='in_out_cubic')
                            self.anim5 = Animation(x=anim_x, y=y5 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim6 = Animation(x=anim_x, y=y6 + anim_height, color = (1,1,1,0.33), t='in_out_cubic')

                            # bind the completion function
                            self.anim0.bind(on_complete=self.completeAnim)
                            self.anim1.bind(on_complete=self.completeAnim)
                            self.anim2.bind(on_complete=self.completeAnim)
                            self.anim3.bind(on_complete=self.completeAnim)
                            self.anim4.bind(on_complete=self.completeAnim)
                            self.anim5.bind(on_complete=self.completeAnim)
                            self.anim6.bind(on_complete=self.completeAnim)

                            # start animations
                            self.anim0.start(games[6])
                            self.anim1.start(games[5])
                            self.anim2.start(games[4])
                            self.anim3.start(games[3])
                            self.anim4.start(games[2])
                            self.anim5.start(games[1])
                            self.anim6.start(games[0])

                        elif keycode[1] == BUTTON_1:
                            games[3].select_anim(getColorOfScheme('accent', self.MM.current_color_scheme))
                            Clock.schedule_once(self.startGame, 0.8)

                elif self.MM.currentSection == Section.ACTION_BUTTONS:
                    self.transitionToSection('actionbtns')
                    self.layout.ids['controlbar'].context_switch('actionbtns')
                    self.setGames()
                    self.MM.CurrentOption().highlighted = True
                    if self.MM.GetGame().is_favorite:
                        self.layout.ids['fav'].action_image = self.layout.ids['fav'].s_action
              
        elif self.current_state == GAME_STATE:
                title = win32gui.GetWindowText (win32gui.GetForegroundWindow())
                pid = get_window_pid(title)
                self.running_game = pid

        else:
                print("STATE ERROR!")

    # This function sets the positons of the games in the carousel based on where the user is in the list of games
    def setGames(self):
        
        # Grab the carousel
        games = self.layout.ids["games"].children

        # set A values
        games[6].color[3] = 0.00
        games[5].color[3] = 0.33
        games[4].color[3] = 0.66
        games[3].color[3] = 1
        if self.MM.currentSection != Section.GAMES:
            games[3].color[3] = 0.75
        games[2].color[3] = 0.66
        games[1].color[3] = 0.33
        games[0].color[3] = 0.00

        # DEBUG VALUES
        self.layout.ids['gameImage'].bg_image = "./img/no_alpha.png"
        self.layout.ids['year'].text = 'Year: ' + "ERROR"
        self.layout.ids['dev'].text = 'Developer: ' + "Error"
        self.layout.ids['pub'].text = 'Publisher: ' + "ErRoR"
        
        # Normal
        if not self.MM.favorite_sort:
            #set extra data
            self.layout.ids['gameImage'].bg_image = self.MM.GetGame().game_image
            self.layout.ids['year'].text = 'Year: ' + self.MM.GetGame().game_info[0]
            self.layout.ids['dev'].text = 'Developer: ' + self.MM.GetGame().game_info[1]
            self.layout.ids['pub'].text = 'Publisher: ' + self.MM.GetGame().game_info[2]
            games[3].game_name = self.MM.GetGame().game_name

            # set names
            games[6].text = self.MM.GetGame(-3).text
            games[5].text = self.MM.GetGame(-2).text
            games[4].text = self.MM.GetGame(-1).text
            games[3].text = self.MM.GetGame().text
            games[2].text = self.MM.GetGame(+1).text
            games[1].text = self.MM.GetGame(+2).text
            games[0].text = self.MM.GetGame(+3).text
        # Favorites
        else:
            #set extra data
            self.layout.ids['gameImage'].bg_image = self.MM.GetFavorite().game_image
            self.layout.ids['year'].text = 'Year: ' + self.MM.GetFavorite().game_info[0]
            self.layout.ids['dev'].text = 'Developer: ' + self.MM.GetFavorite().game_info[1]
            self.layout.ids['pub'].text = 'Publisher: ' + self.MM.GetFavorite().game_info[2]
            games[3].game_name = self.MM.GetFavorite().game_name
            # set names
            games[6].text = self.MM.GetFavorite(-3).text
            games[5].text = self.MM.GetFavorite(-2).text
            games[4].text = self.MM.GetFavorite(-1).text
            games[3].text = self.MM.GetFavorite().text
            games[2].text = self.MM.GetFavorite(+1).text
            games[1].text = self.MM.GetFavorite(+2).text
            games[0].text = self.MM.GetFavorite(+3).text

    # Switches the sidebar to one of its sub-menus
    def switchToSidebar(self, sidebar):
        self.MM.tabs_list = []
        self.MM.populateMenus(sidebar)
        self.MM.CurrentTab().highlighted = True
        subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
        self.MM.s_t_i = len(subTabs) - 1
        self.MM.CurrentSubTab(subTabs).highlighted = True
        
    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0)
        
    def _keyboardClosed(self):
        self.kListener.keyboard.unbind(on_key_down=self.readInputs)
        self.kListener.keyboard = None

    #Call the playGame function if the selected game is not currently running
    def startGame(self, *largs):
        currentGame = self.layout.ids["games"].children[3]
        if self.running_game is None:
            playGame(currentGame.game_name)
            title = win32gui.GetWindowText (win32gui.GetForegroundWindow())
            pid = get_window_pid(title)
            self.running_game = pid
            if self.running_game is not None:
                self.last_selected_game = currentGame
        else:
            if currentGame == self.last_selected_game:
                pass 

                for hwnd in get_hwnds_for_pid (self.running_game):
                    win32gui.SetForegroundWindow(hwnd)
                    FRONT = win32gui.GetWindowRect(hwnd)                 
                
            else: 
                self.running_game = playGame(currentGame.game_name)
        if self.system == 'Windows':
            playsound(getSound("exit_menu"), False)
        elif self.system == 'Linux':
            SoundLoader.load(sound)
        if self.running_game is not None:
            self.current_state = GAME_STATE

    #Go back to home menu
    def pauseGame(self):
        playsound(getSound("enter_menu"), False)
        HWND = win32gui.FindWindow(None, 'HomeMenu') 
        win32gui.SetForegroundWindow(HWND)
        FRONT = win32gui.GetWindowRect(HWND)

    #leave home menu, back to game state
    def resumeGame(self):
        for hwnd in get_hwnds_for_pid (self.running_game):
            win32gui.SetForegroundWindow(hwnd)
            FRONT = win32gui.GetWindowRect(hwnd) 

    # Set the Select property of the current tab, which will activate that tab's function
    # Does the same for sub-tabs
    def selectTab(self):
        currentTab = self.MM.CurrentTab()
        if currentTab.collapse:
            currentTab.selected = True
            currentTab.selected = False
        else:
            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
            currentSubTab = self.MM.CurrentSubTab(subTabs)
            currentSubTab.selected = True
            currentSubTab.command(self.MM)
            getFunction(currentSubTab, self.MM)
            if currentSubTab.func_id == 'remap':
                self.layout.ids['controlbar'].context_switch('remap')
            currentSubTab.selected = False
            if currentSubTab.sidebar is not None:
                #self.MM.CurrentTab().collapse = True
                currentSubTab.highlighted = False
                self.switchToSidebar(currentSubTab.sidebar)

    #Schedule an Action Button's function to take place after its animation
    def selectActionButton(self):
        currentOption = self.MM.CurrentOption()
        currentOption.selected = True
        currentOption.select_anim.start(currentOption)
        currentOption.selected = False

        if currentOption.func_id == 'play':
            Clock.schedule_once(self.startGame, 0.8)
        if currentOption.func_id == 'fav':
            getFunction(currentOption, self.MM)
            self.setGames()

    #Alternate sound functions for Windows and Linux
    def playMenuSound(self, sound, *largs):
        if self.system == 'Windows':
            playsound(sound, False)
        elif self.system == 'Linux':
            SoundLoader.load(sound)

    # Increase opacity of current section, reduce opacity of others
    def transitionToSection(self, current_section):
        #Reduce opacity of other sections
        sections = ['sidebarSection', 'games', 'actionbtns']
        sections.remove(current_section)
        for section in sections: self.layout.ids[section].opacity = 0.5

        #Increase opacity of current section
        opacity_anim = Animation(opacity=1, t='in_out_cubic', duration=0.3)
        opacity_anim.start(self.layout.ids[current_section])
        self.layout.ids[current_section].opacity = 1

pam = PAM()

pam.Display.run()