import threading
import sys
import keyboard # This import requires a pip install. It will also require a
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

<<<<<<< HEAD
=======
# Our own on_resize function so that we can ensure the games animate properly
def on_resize(one, two, three):
    pam.selectedY = pam.layout.ids["games"].children[3].y
>>>>>>> b0a88509c50e70cba8a68649d7acdcc0c10858b7

# This class serves as the entirety of the program. It will be the
# container for all the necessary data as well as how to interact/interpret
# said data
class PAM:

    # initialization of the PAM
    def __init__(self):
        self.currentState = includes.CurrentState.MAIN_MENU_STATE; 
        self.Display = display.SetupDisplay();
        self.Display.load_kv("HomeMenu.kv")
        self.layout = self.Display.build()
        self.Display.built = True
        self.Display.root = self.layout
        self.MM = mainMenu.mainMenu(self.layout.ids["sidebar"], self.layout.ids["games"], self.layout.ids["actionbtns"]);
        #self.layout.ids["games"].children[3].bind(pos=self.on_resize)
        self.inputHook = keyboard.hook(self.readInputs)
        self.currentInputs = [];
        self.comp_anims = [False, False, False, False, False, False, False];
        self.anim0 = None
        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        self.anim5 = None
        self.anim6 = None
        self.currentAnimEvent = None
        self.selectedY = None
        self.updateState(None);
        self.runningGame = None
        self.lastSelectedGame = None
        self.setGames();
        self.window = EventLoop.window
        self.window.bind(on_resize=on_resize)
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
    def readInputs(self, event):
        if True: #not isLoading:
            if event.event_type == keyboard.KEY_DOWN:

                # Anti Turbo
                if(event.name in self.currentInputs and 
                event.name != includes.DI_UP and event.name != includes.DI_DOWN
                and event.name != includes.DI_LEFT and event.name != includes.DI_RIGHT):
                    return
                
                else:
                    self.currentInputs.append(event.name)

                if event.name == includes.BUTTON_1:
                    # Accept button
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            currentTab = self.MM.CurrentTab()
                            currentTab.selected = True
                            pamFunctions.getFunction(currentTab, self.MM)
                            currentTab.selected = False                          
                        elif self.MM.currentSection == includes.Section.GAMES:
                            currentGame = self.MM.GetGame()     
                            if self.runningGame is None:
                                self.runningGame = pamFunctions.playGame(currentGame.gameName)
                                self.lastSelectedGame = currentGame
                            else:
                                if currentGame == self.lastSelectedGame: #add in check for if lastSelectedGame is still running
                                    #GO BACK TO GAME. NOT LINUX FRIENDLY. REPLACE LATER.

                                    print("PID:")
                                    print(self.runningGame.pid)
                                    for hwnd in pamFunctions.get_hwnds_for_pid (self.runningGame.pid):
                                        print(hwnd, "=>", includes.win32gui.GetWindowText (hwnd))
                                        includes.win32gui.SetForegroundWindow(hwnd)
                                        FRONT = includes.win32gui.GetWindowRect(hwnd)                 
                                    
                                else: 
                                    pamFunctions.closeGame(self.runningGame)
                                    self.runningGame = pamFunctions.playGame(currentGame.gameName)
                            includes.playsound(includes.sounds.getSound("exit_menu"), False)
                            self.currentState = includes.CurrentState.GAME_STATE
                            
                            #start transition to playing the game
                        elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                            currentOption = self.MM.CurrentOption()
                            currentOption.selected = True
                            pamFunctions.getFunction(currentOption, self.MM)
                            currentOption.selected = False
                            if currentOption.func_id == 'play':
                                self.currentState = includes.CurrentState.GAME_STATE
                                includes.playsound(includes.sounds.getSound("exit_menu"), False)
                    
                elif event.name == includes.BUTTON_2:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            pass
                        elif self.MM.currentSection == includes.Section.GAMES:
                            pamFunctions.closeGame(self.runningGame)
                            self.runningGame = None
                        elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                            pass

                elif event.name == includes.BUTTON_3:
                    pass

                elif event.name == includes.BUTTON_4:
                    pass

                elif event.name == includes.BUTTON_5:
                    pass

                elif event.name == includes.BUTTON_6:
                    pass

                elif event.name == includes.BUTTON_7:
                    pass

                elif event.name == includes.BUTTON_8:
                    pass

                elif event.name == includes.HOME_BUTTON:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.runningGame is not None:
                            print("PID:")
                            print(self.runningGame.pid)
                            for hwnd in pamFunctions.get_hwnds_for_pid (self.runningGame.pid):
                                print(hwnd, "=>", includes.win32gui.GetWindowText (hwnd))
                                includes.win32gui.SetForegroundWindow(hwnd)
                                FRONT = includes.win32gui.GetWindowRect(hwnd)   
                            self.currentState = includes.CurrentState.GAME_STATE

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        self.currentState = includes.CurrentState.MAIN_MENU_STATE
                        #GO BACK TO HOME MENU. NOT LINUX FRIENDLY. REPLACE LATER.
                        includes.playsound(includes.sounds.getSound("enter_menu"), False)
                        HWND = includes.win32gui.FindWindow(None, 'HomeMenu') 
                        includes.win32gui.SetForegroundWindow(HWND)
                        FRONT = includes.win32gui.GetWindowRect(HWND)

                elif event.name == includes.COIN_BUTTON:
                    pass

                elif event.name == includes.DI_DOWN:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            
                            # if not at the beginning of the list and not inside a tab
                            if self.MM.t_i > 0 and self.MM.CurrentTab().collapse:
                                self.MM.CurrentTab().highlighted = False
                                self.MM.t_i -= 1
                                if self.MM.CurrentTab().collapse:
                                    self.MM.CurrentTab().highlighted = True
                                    
                                else:
                                    currentTab = self.MM.CurrentTab()
                                    currentTab.children[len(currentTab.children) - 1].highlighted = True
                                    

                            # if not at the beginning and tab not collapsed
                            elif self.MM.t_i > 0 and not self.MM.CurrentTab().collapse:
                                if self.MM.CurrentTab().highlighted:
                                    self.MM.CurrentTab().highlighted = False
                                    self.MM.t_i -= 1
                                    if self.MM.CurrentTab().collapse:
                                        self.MM.CurrentTab().highlighted = True
                                        
                                    else:
                                        currentTab = self.MM.CurrentTab()
                                        currentTab.children[len(currentTab.children) - 1].highlighted = True
                                        

                                else:
                                    for i in range(len(self.MM.CurrentTab().children)):
                                        if self.MM.CurrentTab().children[i].highlighted:
                                            self.MM.CurrentTab().children[i].highlighted = False;

                                            if i == 0:
                                                self.MM.CurrentTab().highlighted = True;
                                                
                                            else:
                                                currentTab.children[i - 1].highlighted = True;
                                            break;
                            else:
                                print("DEBUG: Potentially unaccounted-for case in the Tabs section")
                                includes.playsound(includes.sounds.getSound("end_of_list"), False)

                        elif self.MM.currentSection == includes.Section.GAMES:
                            includes.playsound(includes.sounds.getSound("down_carousel"), False)
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

                elif event.name == includes.DI_UP:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.TABS:
                            # if not on the last tab and the current tab is collapsed
                            if self.MM.t_i < len(self.MM.tabsList) - 1 and self.MM.CurrentTab().collapse:
                                self.MM.CurrentTab().highlighted = False
                                self.MM.t_i += 1
                                self.MM.CurrentTab().highlighted = True


                            # if on any tab and the tab is not collapsed
                            elif not self.MM.CurrentTab().collapse:
                                if self.MM.CurrentTab().highlighted:
                                    self.MM.CurrentTab().highlighted = False                                    
                                    self.MM.CurrentTab().children[0].highlighted = True
                                
                                else: # find the child that is selected 
                                    for i in range(len(self.MM.CurrentTab().children)):
                                        if self.MM.CurrentTab().children[i].highlighted: # once you find it
                                            

                                            if (i == (len(self.MM.CurrentTab().children) - 1)) and self.MM.t_i < (len(self.MM.tabsList) - 1): # if it's the last item in a sub tab and there is a next tab
                                                self.MM.CurrentTab().children[i].highlighted = False;
                                                self.MM.t_i += 1
                                                self.MM.CurrentTab().highlighted = True;
                                            else:
                                                self.MM.CurrentTab().children[i].highlighted = False;
                                                currentTab.children[i + 1].highlighted = True;

                                            break;
                            else:
                                print("DEBUG: Potentially unaccounted-for case in the Tabs section")
                                includes.playsound(includes.sounds.getSound("end_of_list"), False)


                        elif self.MM.currentSection == includes.Section.GAMES:
                            includes.playsound(includes.sounds.getSound("up_carousel"), False)
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
                    
                elif event.name == includes.DI_LEFT:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and  (len(self.MM.optionsList) - 1) - self.MM.o_i > includes.GameOptions.PLAY:
                            self.MM.o_i += 1 
                        elif self.MM.currentSection > includes.Section.TABS:
                            self.MM.currentSection -= 1 
                        else:
                            pass # eat the input

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    
                elif event.name == includes.DI_RIGHT:
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
                    
            elif event.event_type == keyboard.KEY_UP:
                # Anti Turbo
                if(event.name in self.currentInputs):
                    self.currentInputs.remove(event.name);
                else:
                    return
                
        else:
            pass # There's nothing to do right now

        self.updateState(event)

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
    def updateState(self, event):
        """based on the current state, inputs will alter the state:
        if current state is menu state, the stick will iterate through
        the various menus/sections and call functions as needed.
        If current state is game state, inputs will be determined based on
        control scheme and then transmitted as the appropriate inputs
        If current state is paused state, inputs will be read as appropriate
        (P2 inputs only, etc.)"""

        if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
            # DEBUG SETTING
            if event is None:
                self.MM.currentSection = includes.Section.GAME_OPTIONS
                print("DEBUG: The PAM is starting in: " + str(self.MM.currentSection))
            ############################

            if event is None or event.event_type is keyboard.KEY_DOWN:
                # Undo all selections in the Tabs Section
                for tab in self.MM.tabsList:
                    # tab
                    #tab.highlighted = False
                    tab.background_color = includes.get_color_from_hex(tab.d_color)

                    # inner tab
                    for subTab in tab.children:
                        #subTab.highlighted = False
                        subTab.background_color = includes.get_color_from_hex(subTab.d_color)

                # Stop all animations in the Games Section
                if event is not None:
                    if event.event_type is keyboard.KEY_DOWN:
                        # stop previous animations
                        if self.anim0 is not None:
                            # due to how we end animations the game iterator will be 
                            # temporarily changed in order to avoid an issue where the
                            # desired game will already be set and will get animated away
                            # before being reset to the proper position
                            if event.name == includes.DI_UP:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.gameList):
                                    self.MM.g_i = 0

                            elif event.name == includes.DI_DOWN:
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
                            if event.name == includes.DI_UP:
                                self.MM.g_i -= 1
                                if self.MM.g_i < 0:
                                    self.MM.g_i =  len(self.MM.gameList) - 1

                            elif event.name == includes.DI_DOWN:
                                self.MM.g_i += 1
                                if self.MM.g_i >= len(self.MM.gameList):
                                    self.MM.g_i = 0

                # Undo all selections in the Game Options Section
                for option in self.MM.optionsList:
                    option.highlighted = False
                    #option.background_color = includes.get_color_from_hex(option.d_color)

                # Then set new selection
                if self.MM.currentSection == includes.Section.TABS:
                    
                    if self.MM.CurrentTab().highlighted:
                        self.MM.CurrentTab().background_color = includes.get_color_from_hex(self.MM.CurrentTab().h_color)
                    else:
                        for subTab in self.MM.CurrentTab().children:
                            if subTab.highlighted:
                                subTab.background_color = includes.get_color_from_hex(subTab.h_color)
                
                elif self.MM.currentSection == includes.Section.GAMES:

                    # the game section doesn't need to be updated at the start of the program
                    if event is not None:

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

                        if self.selectedY == None:
                            self.selectedY = games[3].y

                        # animate carousel downwards
                        if event.name == includes.DI_UP:

                            # set new animation event
                            self.currentAnimEvent = event.name

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
                        elif event.name == includes.DI_DOWN:

                            # set new animation event
                            self.currentAnimEvent = event.name

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

                elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
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
        games[2].color[3] = 0.66
        games[1].color[3] = 0.33
        games[0].color[3] = 0.00

        # set names
        games[6].text = self.MM.GetGame(-3).text
        games[5].text = self.MM.GetGame(-2).text
        games[4].text = self.MM.GetGame(-1).text
        games[3].text = self.MM.GetGame().text
        games[2].text = self.MM.GetGame(+1).text
        games[1].text = self.MM.GetGame(+2).text
        games[0].text = self.MM.GetGame(+3).text

        #Set a game as a favorite if its name is in the favorite.txt
        #print("Favorites:")
        #with open('user/favorites.txt', 'r') as favTxt:
        #    for game in games:
        #        for line in favTxt:
        #            if game.gameName == line:
        #                game.isFavorite = True
        #                print(game.gameName)

    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0);
        
pam = PAM();

pam.Display.run();