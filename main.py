import threading
import sys
import keyboard # This import requires a pip install. It will also require a
                # sudo for Linux machines (i.e. Raspbian)
import includes
import mainMenu
import display
import pamWidgets
import pamFunctions
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.graphics.vertex_instructions import Rectangle





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
        self.inputHook = keyboard.hook(self.readInputs)
        self.currentInputs = [];
        self.comp_anims = [False, False, False, False, False];
        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        self.anim5 = None
        self.updateState(None);
        self.runningGame = None
        self.lastSelectedGame = None
        self.setGames();
        


    # check currentState and if program is loading
    # displays window based on the current state    
    def displayState(self):
        if not isLoading:
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
                if(event.name in self.currentInputs and event.name != includes.DI_UP and event.name != includes.DI_DOWN and event.name != includes.DI_LEFT and event.name != includes.DI_RIGHT):
                    return;
                else:
                    self.currentInputs.append(event.name);


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
                                self.runningGame = pamFunctions.playGame(pamFunctions.emulator, currentGame.gamePath)
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
                                    self.runningGame = pamFunctions.playGame(pamFunctions.emulator, currentGame.gamePath)
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
                            
                    print(event.name)
                    
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
                    print(event.name)

                elif event.name == includes.BUTTON_4:
                    print(event.name)

                elif event.name == includes.BUTTON_5:
                    print(event.name)

                elif event.name == includes.BUTTON_6:
                    print(event.name)

                elif event.name == includes.BUTTON_7:
                    print(event.name)

                elif event.name == includes.BUTTON_8:
                    print(event.name)

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
                    print(event.name)

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
                            print("Cycle through games")
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)


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
                            print("Cycle through games")
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

                # move towards the left side of the screen
                elif event.name == includes.DI_LEFT:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and  (len(self.MM.optionsList) - 1) - self.MM.o_i > includes.GameOptions.PLAY:
                            self.MM.CurrentOption().highlighted = False
                            self.MM.o_i += 1 
                            self.MM.CurrentOption().highlighted = True
                        elif self.MM.currentSection > includes.Section.TABS:
                            self.MM.currentSection -= 1
                            
                        else:
                            pass # eat the input
                        print(event.name)

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

                # move towards the right side of the screen
                elif event.name == includes.DI_RIGHT:
                    if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and (len(self.MM.optionsList) - 1) - self.MM.o_i < includes.GameOptions.FAVORITE:
                            self.MM.CurrentOption().highlighted = False
                            self.MM.o_i -= 1
                            self.MM.CurrentOption().highlighted = True
                            
                        elif self.MM.currentSection < includes.Section.GAME_OPTIONS:
                            self.MM.currentSection += 1
                            self.MM.o_i = len(self.MM.optionsList) - 1

                        else:
                            pass # eat the input
                        print(event.name)

                    elif self.currentState == includes.CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

            elif event.event_type == keyboard.KEY_UP:
                # Anti Turbo
                if(event.name in self.currentInputs):
                    self.currentInputs.remove(event.name);
                else:
                    # print("Somehow, there was a key up event for something that didn't have a key down input")
                    print(event.name)
                    return
                
            
        else:
            pass # There's nothing to do right now

        self.updateState(event);

      
    def completeAnim(self, anim, wid):
        self.comp_anims[wid.index] = True
        allTrue = True
        for comptest in self.comp_anims:
            if comptest == False:
                allTrue = False
                break
        
        # all animations done
        if allTrue:
            self.setGames()
            games = self.layout.ids["games"].children
            height = games[0].height
            # reset height
            games[6].y = games[7].y - height
            games[5].y = games[7].y - height * 2
            games[4].y = games[7].y - height * 3
            games[3].y = games[7].y - height * 4
            games[2].y = games[7].y - height * 5

            # reset A values
            games[6].color[3] = 0.33
            games[5].color[3] = 0.66
            games[4].color[3] = 1
            games[3].color[3] = 0.66
            games[2].color[3] = 0.33
            # reset names
            games[6].text = self.MM.GetGame(-2).text
            games[5].text = self.MM.GetGame(-1).text
            games[4].text = self.MM.GetGame().text
            games[3].text = self.MM.GetGame(+1).text
            games[2].text = self.MM.GetGame(+2).text

            #reset booleans
            self.comp_anims = [False, False, False, False, False];

            print("ANIM DONE")


    def updateState(self, event):
        """based on the current state, inputs will alter the state:
        if current state is menu state, the stick will iterate through
        the various menus/sections and call functions as needed.
        If current state is game state, inputs will be determined based on
        control scheme and then transmitted as the appropriate inputs
        If current state is paused state, inputs will be read as appropriate
        (P2 inputs only, etc.)"""
        if self.currentState == includes.CurrentState.MAIN_MENU_STATE:
            # Undo all selections
            # Tabs Section
            for tab in self.MM.tabsList:
                for subTab in tab.children:
                    subTab.background_color = includes.get_color_from_hex(subTab.d_color)

                tab.background_color = includes.get_color_from_hex(tab.d_color)

            # Games Section
            # Game Options Section
            for option in self.MM.optionsList:
                option.background_color = includes.get_color_from_hex(option.d_color)

            # Then set new selection
            if self.MM.currentSection == includes.Section.TABS:
                if self.MM.CurrentTab().highlighted:
                    self.MM.CurrentTab().background_color = includes.get_color_from_hex(self.MM.CurrentTab().h_color)
                else:
                    for subTab in self.MM.CurrentTab().children:
                        if subTab.highlighted:
                            subTab.background_color = includes.get_color_from_hex(subTab.h_color)
            elif self.MM.currentSection == includes.Section.GAMES:
                
                # update y coordinates of GameCarouselItems as well as alpha value of GameName Text
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == includes.DI_UP:
                        carousel = self.layout.ids["games"]
                        games = carousel.children
                        anim_x = carousel.x
                        anim_height = games[0].height
                        y1 = games[1].y
                        y2 = games[2].y
                        y3 = games[3].y
                        y4 = games[4].y
                        y5 = games[5].y
                        self.anim1 = includes.Animation(x=anim_x, y=y1 + anim_height, color = (1,1,1,0), t='in_out_cubic')
                        self.anim2 = includes.Animation(x=anim_x, y=y2 + anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                        self.anim3 = includes.Animation(x=anim_x, y=y3 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                        self.anim4 = includes.Animation(x=anim_x, y=y4 + anim_height, color = (1,1,1,1), t='in_out_cubic')
                        self.anim5 = includes.Animation(x=anim_x, y=y5 + anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                        self.anim1.bind(on_complete=self.completeAnim)
                        self.anim2.bind(on_complete=self.completeAnim)
                        self.anim3.bind(on_complete=self.completeAnim)
                        self.anim4.bind(on_complete=self.completeAnim)
                        self.anim5.bind(on_complete=self.completeAnim)
                        self.anim1.start(games[1])
                        self.anim2.start(games[2])
                        self.anim3.start(games[3])
                        self.anim4.start(games[4])
                        self.anim5.start(games[5])
                    elif event.name == includes.DI_DOWN:
                        carousel = self.layout.ids["games"]
                        games = carousel.children
                        anim_x = carousel.x
                        anim_height = games[0].height
                        y1 = games[1].y
                        y2 = games[2].y
                        y3 = games[3].y
                        y4 = games[4].y
                        y5 = games[5].y
                        self.anim1 = includes.Animation(x=anim_x, y=y1 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                        self.anim2 = includes.Animation(x=anim_x, y=y2 - anim_height, color = (1,1,1,1), t='in_out_cubic')
                        self.anim3 = includes.Animation(x=anim_x, y=y3 - anim_height, color = (1,1,1,0.66), t='in_out_cubic')
                        self.anim4 = includes.Animation(x=anim_x, y=y4 - anim_height, color = (1,1,1,0.33), t='in_out_cubic')
                        self.anim5 = includes.Animation(x=anim_x, y=y5 - anim_height, color = (1,1,1,0), t='in_out_cubic')
                        self.anim1.bind(on_complete=self.completeAnim)
                        self.anim2.bind(on_complete=self.completeAnim)
                        self.anim3.bind(on_complete=self.completeAnim)
                        self.anim4.bind(on_complete=self.completeAnim)
                        self.anim5.bind(on_complete=self.completeAnim)
                        self.anim1.start(games[1])
                        self.anim2.start(games[2])
                        self.anim3.start(games[3])
                        self.anim4.start(games[4])
                        self.anim5.start(games[5])
                # when position of animating GameCarouselItems reaches new 'location',
                # reset the y values to their starting positions and move the "games" data to the new GCI slot
                print("Games Section")
            elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                for option in self.MM.optionsList:
                    if option.highlighted:
                        #option.canvas.rect.source=option.h_action
                        pass

                
        elif self.currentState == includes.CurrentState.GAME_STATE:
            print("you shouldn't be here yet")
        else:
            print("STATE ERROR!")

    def setGames(self):
        # Show the active game as well as the surrounding games
        games = self.layout.ids["games"].children
        print(games)

        
        # Get the current game plus the 4 surrounding it
        
        game0 = self.MM.GetGame(-2)
        game1 = self.MM.GetGame(-1)
        print(game1.gameName)
        currentGame = self.MM.GetGame()
        print(currentGame.gameName)
        game3 = self.MM.GetGame(+1)
        print(game3.gameName)
        game4 = self.MM.GetGame(+2)

        # place current game in game slot 2
        
        #games[2].gameName = currentGame.gameName
        #games[2] = currentGame
        games[3].text = currentGame.gameName
        games[3].color[3] = 1

        # place surrounding games in slots 0,1,3,4

        games[5].text = game0.gameName
        games[5].color[3] = 0.33
        games[4].text = game1.gameName
        games[4].color[3] = 0.66
        games[2].text = game3.gameName
        games[2].color[3] = 0.66
        games[1].text = game4.gameName
        games[1].color[3] = 0.33

        #Set a game as a favorite if its name is in the favorite.txt
        print("Favorites:")
        with open('user/favorites.txt', 'r') as favTxt:
            for game in games:
                for line in favTxt:
                    if game.gameName == line:
                        game.isFavorite = True
                        print(game.gameName)

    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0);
        

pam = PAM();

pam.Display.run();

# main loop
# displays current state
# updates current state

