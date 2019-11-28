#TO-DO:
#Implement multiplayer
#Add videos (code, vid editing)
#Add control remap
#Add final UI animations
#Add OS checks


import threading
import sys
from datetime import datetime
#import keyboard # This import requires a pip install. It will also require a
                # sudo for Linux machines (i.e. Raspbian)
import includes
import mainMenu
import display
import pamWidgets
import pamFunctions
from kivy.base import EventLoop
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.core.window import Window


# Our own on_resize function so that we can ensure the games animate properly
def on_resize(one, two, three):
    if pam.selectedY is not 0 and pam.selectedY is not None:
        pam.selectedY = pam.layout.ids["games"].children[3].y
    print("RESIZING")

currenttime = datetime.now()
print(currenttime)

# This class serves as the entirety of the program. It will be the
# container for all the necessary data as well as how to interact/interpret
# said data
class PAM:

    # initialization of the PAM
    def __init__(self):
        self.currentState = includes.CurrentState.MAIN_MENU_STATE; 
        self.Display = display.SetupDisplay()
        self.Display.load_kv("HomeMenu.kv")
        self.layout = self.Display.build()
        self.Display.built = True
        self.Display.root = self.layout
        self.MM = mainMenu.mainMenu(self.layout.ids["sidebar"], self.layout.ids["games"], self.layout.ids["actionbtns"])
        #self.layout.ids["games"].children[3].bind(pos=self.on_resize)
        #self.inputHook = keyboard.hook(self.readInputs)
        self.currentInputs = []
        self.comp_anims = [False, False, False, False, False, False, False]
        self.anim0 = None
        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        self.anim5 = None
        self.anim6 = None
        self.currentAnimEvent = None
        self.selectedY = None
        pamFunctions.sortByTitle(self.MM.gameList)
        self.updateState(None)
        self.runningGame = None
        self.lastSelectedGame = None
        self.setGames()
        self.window = EventLoop.window
        self.window.bind(on_resize=on_resize)
        #self.inputClock = Clock()
        self.eventDict = {
            includes.BUTTON_1: currenttime,
            includes.BUTTON_2: currenttime, 
            includes.BUTTON_3: currenttime,
            includes.BUTTON_4: currenttime,
            includes.BUTTON_5: currenttime,
            includes.BUTTON_6: currenttime,
            includes.HOME_BUTTON:currenttime,
            includes.COIN_BUTTON: currenttime,
            includes.DI_UP: currenttime,
            includes.DI_DOWN: currenttime,
            includes.DI_LEFT:currenttime,
            includes.DI_RIGHT: currenttime
        }
        
        self.kListener  = self.layout.ids['kListener']
        self.kListener.keyboard = Window.request_keyboard(self._keyboard_closed, self.kListener)
        self.kListener.keyboard.bind(on_key_down=self.readInputs)
        

        
        #self.Display.bind(on_start=setup)
        
    # check currentState and if program is loading
    # displays window based on the current state    
    def displayState(self):
        if not includes.isLoading:
            print("Check currentState and display the appropriate window");
        else:
            pass # There's nothing for you to do right now

    # TODO: Finish button reading
    # Reads all current button inputs. Because keyboard can't suppress inputs in Linux,
    # editing of the emulator's input reading may be necessary.
    def readInputs(self, keyboard, keycode, text, modifiers):

        if keycode[1] not in self.eventDict:
            return

        newTime = datetime.now()
        oldTime = self.eventDict[keycode[1]]



        if newTime.second == oldTime.second:
            if (newTime.microsecond - oldTime.microsecond) < includes.BUFFER:
                return
        elif newTime.second - oldTime.second == 1:
            if (1000000 + newTime.microsecond - oldTime.microsecond) < includes.BUFFER:
                return

        self.eventDict[keycode[1]] = newTime

        if True: #not isLoading:
            if True:#event.event_type == keyboard.KEY_DOWN:
                
                # Anti Turbo
                #if(event.name in self.currentInputs and 
                #event.name != includes.DI_UP and event.name != includes.DI_DOWN
                #and event.name != includes.DI_LEFT and event.name != includes.DI_RIGHT):
                    #return
                
                #else:
                   #self.currentInputs.append(event.name)

                if keycode[1] == includes.BUTTON_1:
                    # Accept button
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            currentTab = self.MM.CurrentTab()
                            if currentTab.collapse:
                                currentTab.selected = True
                                currentTab.selected = False
                            else:
                                subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                                currentSubTab = self.MM.CurrentSubTab(subTabs)
                                currentSubTab.selected = True
                                pamFunctions.getFunction(currentSubTab, self.MM)
                                currentSubTab.selected = False
                                if currentSubTab.sidebar is not None:
                                    self.MM.CurrentTab().collapse = True
                                    currentSubTab.highlighted = False
                                    self.switchToSidebar(currentSubTab.sidebar)
                                    

                        elif self.MM.currentSection == includes.Section.GAMES:
                            pass # For now
                            
                            
                        elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                            currentOption = self.MM.CurrentOption()
                            currentOption.selected = True
                            pamFunctions.getFunction(currentOption, self.MM)
                            currentOption.selected = False

                            if currentOption.func_id == 'play':
                                self.currentState = includes.CurrentState.GAME_STATE
                               # includes.playsound(includes.sounds.getSound("exit_menu"), False)
                    
                elif keycode[1] == includes.BUTTON_2:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            carousel = self.layout.ids['car']
                            if carousel.current_slide is not carousel.slides[0]:
                                carousel.moveToRootSideBar()
                                self.switchToSidebar(carousel.slides[0])
                        elif self.MM.currentSection == includes.Section.GAMES:
                            pamFunctions.closeGame(self.runningGame)
                            self.runningGame = None
                        elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                            pass

                elif keycode[1] == includes.BUTTON_3:
                    pass

                elif keycode[1] == includes.BUTTON_4:
                    pass

                elif keycode[1] == includes.BUTTON_5:
                    pass

                elif keycode[1] == includes.BUTTON_6:
                    pass

                elif keycode[1] == includes.HOME_BUTTON:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.runningGame is not None:
                            print("PID:")
                            print(self.runningGame.pid)
                            #for hwnd in pamFunctions.get_hwnds_for_pid (self.runningGame.pid):
                             #   print(hwnd, "=>", includes.win32gui.GetWindowText (hwnd))
                              #  includes.win32gui.SetForegroundWindow(hwnd)
                               # FRONT = includes.win32gui.GetWindowRect(hwnd)   
                            self.currentState = includes.CurrentState.GAME_STATE

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        self.currentState = includes.CurrentState.MAIN_MENU_STATE
                        #GO BACK TO HOME MENU. NOT LINUX FRIENDLY. REPLACE LATER.
                        #includes.playsound(includes.sounds.getSound("enter_menu"), False)
                        #HWND = includes.win32gui.FindWindow(None, 'HomeMenu') 
                        #includes.win32gui.SetForegroundWindow(HWND)
                        #FRONT = includes.win32gui.GetWindowRect(HWND)

                elif keycode[1] == includes.COIN_BUTTON:
                    pass

                elif keycode[1] == includes.DI_DOWN:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
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




                        elif self.MM.currentSection == includes.Section.GAMES:
                            #includes.playsound(includes.sounds.getSound("down_carousel"), False)
                            
                            self.MM.g_i += 1
                            if self.MM.g_i >= len(self.MM.gameList):
                                self.MM.g_i = 0
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")

                elif keycode[1] == includes.DI_UP:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            #Tab is closed
                            if self.MM.CurrentTab().collapse:
                                self.MM.CurrentTab().highlighted = False
                                
                                #Progress upward in major tabs until at end
                                self.MM.t_i += 1
                                if self.MM.t_i >= len(self.MM.tabsList) - 1:
                                    self.MM.t_i = len(self.MM.tabsList) - 1

                                self.MM.CurrentTab().highlighted = True
                                subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                                self.MM.s_t_i = len(subTabs) - 1

                            #Tab is open
                            else:    
                                subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                                #break free of bottom tabs
                                if self.MM.t_i == 0 and self.MM.s_t_i == len(subTabs) - 1: 
                                    self.MM.t_i += 1
                                    if self.MM.t_i > len(self.MM.tabsList) - 1:
                                        self.MM.t_i = len(self.MM.tabsList) - 1
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

                                



                        elif self.MM.currentSection == includes.Section.GAMES:
                           # includes.playsound(includes.sounds.getSound("up_carousel"), False)
                            self.MM.g_i -= 1
                            if self.MM.g_i < 0:
                                self.MM.g_i =  len(self.MM.gameList) - 1
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    
                elif keycode[1] == includes.DI_LEFT:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and  (len(self.MM.optionsList) - 1) - self.MM.o_i > includes.GameOptions.PLAY:
                            self.MM.o_i += 1 
                        elif self.MM.currentSection > includes.Section.TABS:
                            self.MM.currentSection -= 1 
                            subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                            self.MM.s_t_i = len(subTabs) - 1
                        else:
                            pass # eat the input

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    
                elif keycode[1] == includes.DI_RIGHT:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and (len(self.MM.optionsList) - 1) - self.MM.o_i < includes.GameOptions.FAVORITE:
                            self.MM.o_i -= 1
                        elif self.MM.currentSection < includes.Section.GAME_OPTIONS:
                            self.MM.currentSection += 1
                            self.MM.o_i = len(self.MM.optionsList) - 1
                        else:
                            pass # eat the input

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    
            #elif event.event_type == keyboard.KEY_UP:
                # Anti Turbo
               # if(event.name in self.currentInputs):
                   # self.currentInputs.remove(event.name);
               # else:
                   # return
                
        else:
            pass # There's nothing to do right now

        self.updateState(keycode)

    # This function gets called when a game carousel animation completes
    def completeAnim(self, anim, wid):
        self.comp_anims[wid.index] = True
        allTrue = True
        for isComplete in self.comp_anims:
            if isComplete == False:
                allTrue = False
                break
        
        # all animations done
        if allTrue:
            # Grab the carousel as  well as widget height
            games = self.layout.ids["games"].children
            height = games[0].height

            # reset widget locations starting with the current game widget's known base location
            games[3].y = self.selectedY

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

        if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
            # DEBUG SETTING
            if keycode is None:
                self.MM.currentSection = includes.Section.GAMES
                print("DEBUG: The PAM is starting in: " + str(self.MM.currentSection))
            ############################

            if keycode is None or True:#event.event_type is keyboard.KEY_DOWN:
                # Undo all selections in the Tabs Section
                for tab in self.MM.tabsList:
                    #ensure tabs use the current color scheme
                    tab.h_color = includes.colors.getColorOfScheme('primary', self.MM.current_color_scheme)
                    tab.s_color = includes.colors.getColorOfScheme('secondary', self.MM.current_color_scheme)
                    tab.background_color = includes.get_color_from_hex(tab.d_color)
                    tab.background_normal = 'img/no_alpha.png'
                    tab.background_selected = 'img/no_alpha.png'

                    subTabs = tab.children[0].children[0].children[0].children[0].children
                    for subtab in subTabs:
                        subtab.h_color = includes.colors.getColorOfScheme('primary', self.MM.current_color_scheme)
                        subtab.s_color = includes.colors.getColorOfScheme('secondary', self.MM.current_color_scheme)
                        subtab.bold = False
                        subtab.setFontSize(self.MM.current_font_size)
                        subtab.font_name = self.MM.current_font
                        subtab.background_color = includes.get_color_from_hex(subtab.d_color)
                        if subtab.isToggled:
                            subtab.bold = True
                            subtab.background_color = includes.get_color_from_hex(subtab.s_color)
                    

                    #set tab fonts
                    tab.font_name = self.MM.current_font #REWORK FOR NEW ACCORDION
 
                for child in self.layout.ids['gameDescArea'].children:
                    child.font_name = self.MM.current_font
                    child.setFontSize(self.MM.current_font_size)

                for child in self.layout.ids['games'].children:
                    child.font_name = self.MM.current_font
                    child.setFontSize(self.MM.current_font_size)

                #Update colors of control bar
                self.layout.ids['controlbar'].bg_color = includes.get_color_from_hex(includes.colors.getColorOfScheme('primary', self.MM.current_color_scheme))
                
                # Stop all animations in the Games Section
                if keycode is None or self.selectedY is None or self.selectedY is 0:
                    self.selectedY = self.layout.ids["games"].children[3].y

                if keycode is not None:
                    if True:#event.event_type is keyboard.KEY_DOWN:
                        # stop previous animations
                        if self.anim0 is not None:
                            # due to how we end animations the game iterator will be 
                            # temporarily changed in order to avoid an issue where the
                            # desired game will already be set and will get animated away
                            # before being reset to the proper position
                            if keycode[1] == includes.DI_UP:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.gameList):
                                    self.MM.g_i = 0

                            elif keycode[1] == includes.DI_DOWN:
                                self.MM.g_i -= 1
                                if self.MM.g_i < 0:
                                    self.MM.g_i =  len(self.MM.gameList) - 1

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
                            if keycode[1] == includes.DI_UP:
                                self.MM.g_i -= 1
                                if self.MM.g_i < 0:
                                    self.MM.g_i =  len(self.MM.gameList) - 1

                            elif keycode[1] == includes.DI_DOWN:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.gameList):
                                    self.MM.g_i = 0

                # Undo all selections in the Game Options Section
                for option in self.MM.optionsList:
                    option.highlighted = False
                    #ensure buttons use the current color scheme
                    self.layout.ids['play'].d_action = includes.colors.getColorOfScheme('play-d', self.MM.current_color_scheme)
                    self.layout.ids['play'].h_action = includes.colors.getColorOfScheme('play-h', self.MM.current_color_scheme)
                    self.layout.ids['play'].s_action = includes.colors.getColorOfScheme('play-s', self.MM.current_color_scheme)
                    self.layout.ids['play'].action_image = self.layout.ids['play'].d_action

                    self.layout.ids['fav'].d_action = includes.colors.getColorOfScheme('fav-d', self.MM.current_color_scheme)
                    self.layout.ids['fav'].h_action = includes.colors.getColorOfScheme('fav-h', self.MM.current_color_scheme)
                    self.layout.ids['fav'].s_action = includes.colors.getColorOfScheme('fav-s', self.MM.current_color_scheme)
                    self.layout.ids['fav'].action_image = self.layout.ids['fav'].d_action

                    #option.background_color = includes.get_color_from_hex(option.d_color)

                # Then set new selection
                if self.MM.currentSection == includes.Section.TABS:
                    self.setGames()
                    subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
                    if self.MM.CurrentTab().highlighted:
                        self.MM.CurrentTab().background_normal = includes.colors.getColorOfScheme('tab-d', self.MM.current_color_scheme)
                        self.MM.CurrentTab().background_selected = includes.colors.getColorOfScheme('tab-d', self.MM.current_color_scheme)
                        self.MM.CurrentTab().background_color = includes.get_color_from_hex(self.MM.CurrentTab().h_color)
                    
                    for subTab in subTabs:
                        if subTab.highlighted:
                            subTab.h_color = includes.colors.getColorOfScheme('primary', self.MM.current_color_scheme)
                            subTab.background_color = includes.get_color_from_hex(subTab.h_color)
                            
                
                elif self.MM.currentSection == includes.Section.GAMES:

                    # the game section doesn't need to be updated at the start of the program
                    if keycode is not None:
                        # Edge case
                        if keycode[1] == includes.DI_LEFT or keycode[1] == includes.DI_RIGHT:
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
                        if keycode[1] == includes.DI_UP:

                            # set new animation event
                            self.currentAnimEvent = keycode[1]

                            # set animations
                            self.anim0 = includes.Animation(x=anim_x, y=y0 - anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim1 = includes.Animation(x=anim_x, y=y1 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim2 = includes.Animation(x=anim_x, y=y2 - anim_height, color = (1,1,1,1.00), t='in_out_cubic')
                            self.anim3 = includes.Animation(x=anim_x, y=y3 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim4 = includes.Animation(x=anim_x, y=y4 - anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim5 = includes.Animation(x=anim_x, y=y5 - anim_height, color = (1,1,1,0.00), t='in_out_cubic')
                            self.anim6 = includes.Animation(x=anim_x, y=y6 - anim_height, color = (1,1,1,0.00), t='in_out_cubic')

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
                        elif keycode[1] == includes.DI_DOWN:

                            # set new animation event
                            self.currentAnimEvent = keycode[1]

                            # set animations
                            self.anim0 = includes.Animation(x=anim_x, y=y0 + anim_height, color = (1,1,1,0), t='in_out_cubic')
                            self.anim1 = includes.Animation(x=anim_x, y=y1 + anim_height, color = (1,1,1,0), t='in_out_cubic')
                            self.anim2 = includes.Animation(x=anim_x, y=y2 + anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                            self.anim3 = includes.Animation(x=anim_x, y=y3 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim4 = includes.Animation(x=anim_x, y=y4 + anim_height, color = (1,1,1,1), t='in_out_cubic')
                            self.anim5 = includes.Animation(x=anim_x, y=y5 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                            self.anim6 = includes.Animation(x=anim_x, y=y6 + anim_height, color = (1,1,1,0.33), t='in_out_cubic')

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

                        elif keycode[1] == includes.BUTTON_1:
                            self.startGame()

                elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                    self.setGames()
                    self.MM.CurrentOption().highlighted = True

        elif self.currentState == includes.CurrentState.GAME_STATE:
                print("You have started a game")

        else:
                print("STATE ERROR!")

    # This function sets the games in the carousel based on where the user is in the list of games
    def setGames(self):

        # Grab the carousel
        games = self.layout.ids["games"].children

        # set A values
        games[6].color[3] = 0.00
        games[5].color[3] = 0.33
        games[4].color[3] = 0.66
        games[3].color[3] = 1
        if self.MM.currentSection != includes.Section.GAMES:
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
        if not self.MM.favoriteSort:
            #set extra data
            self.layout.ids['gameImage'].bg_image = self.MM.GetGame().gameImage
            self.layout.ids['year'].text = 'Year: ' + self.MM.GetGame().gameInfo[0]
            self.layout.ids['dev'].text = 'Developer: ' + self.MM.GetGame().gameInfo[1]
            self.layout.ids['pub'].text = 'Publisher: ' + self.MM.GetGame().gameInfo[2]
            games[3].gameName = self.MM.GetGame().gameName

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
            self.layout.ids['gameImage'].bg_image = self.MM.GetFavorite().gameImage
            self.layout.ids['year'].text = 'Year: ' + self.MM.GetFavorite().gameInfo[0]
            self.layout.ids['dev'].text = 'Developer: ' + self.MM.GetFavorite().gameInfo[1]
            self.layout.ids['pub'].text = 'Publisher: ' + self.MM.GetFavorite().gameInfo[2]
            games[3].gameName = self.MM.GetFavorite().gameName
            
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
        self.MM.tabsList = []
        self.MM.populateMenus(sidebar)
        self.MM.CurrentTab().highlighted = True
        subTabs = self.MM.CurrentTab().children[0].children[0].children[0].children[0].children
        self.MM.s_t_i = len(subTabs) - 1
        self.MM.CurrentSubTab(subTabs).highlighted = True
        
    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0);
        
    def _keyboard_closed(self):
        self.kListener.keyboard.unbind(on_key_down=self.readInputs)
        self.kListener.keyboard = None

    def startGame(self):
        currentGame = self.layout.ids["games"].children[3]
        print("GAME = " + currentGame.gameName)
        if currentGame.gameName is "DummyPath":
            print("There's no game dummy!")
            return
        if self.runningGame is None:
            self.runningGame = pamFunctions.playGame(currentGame.gameName)
            self.lastSelectedGame = currentGame
        else:
            if currentGame == self.lastSelectedGame:
                pass #add in check for if lastSelectedGame is still running
                #GO BACK TO GAME. NOT LINUX FRIENDLY. REPLACE LATER.

                print("PID:")
                print(self.runningGame.pid)
                #for hwnd in pamFunctions.get_hwnds_for_pid (self.runningGame.pid):
                    #   print(hwnd, "=>", includes.win32gui.GetWindowText (hwnd))
                    #  includes.win32gui.SetForegroundWindow(hwnd)
                    # FRONT = includes.win32gui.GetWindowRect(hwnd)                 
                
            else: 
                pamFunctions.closeGame(self.runningGame)
                self.runningGame = pamFunctions.playGame(currentGame.gameName)
        #includes.playsound(includes.sounds.getSound("exit_menu"), False)
        self.currentState = includes.CurrentState.GAME_STATE

pam = PAM();

pam.Display.run();