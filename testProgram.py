import threading
import sys
import keyboard # This import requires a pip install. It will also require a
                # sudo for Linux machines (i.e. Raspbian)
import includes
import mainMenu
import display
from kivy.uix.boxlayout import BoxLayout




# This class serves as the entirety of the program. It will be the
# container for all the necessary data as well as how to interact/interpret
# said data
class PAM:

    # initialization of the PAM
    def __init__(self):      
        self.currentState = includes.CurrentState.MAIN_MENU_STATE; 
        self.Display = display.SetupDisplay();
        self.Display.load_kv("menu.kv")
        self.layout = self.Display.build()
        print("hello")
        print(self.layout.children)
        print("hello")
        self.mainMenuLayout = display.MainMenuLayout()
        self.MM = mainMenu.mainMenu(self.layout);
        self.inputHook = keyboard.hook(self.readInputs)
        self.currentInputs = [];
        self.updateState();
        


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
        if not isLoading:
            if event.event_type == KEY_DOWN:

                # Anti Turbo
                if(event.name in self.currentInputs and event.name != DI_UP and event.name != DI_DOWN and event.name != DI_LEFT and event.name != DI_RIGHT):
                    return;
                else:
                    self.currentInputs.append(event.name);


                if event.name == BUTTON_1:
                    # Accept button
                    if self.currentState == CurrentState.MAIN_MENU_STATE:
                        if self.MM.CurrentSection() == TABS:
                            currentTab = self.MM.CurrentTab()
                            # do stuff with the current tab
                        elif self.MM.CurrrentSection() == CurrentState.GAMES:
                            currentGame = self.MM.GetGame()
                            # do stuff with the current game
                        elif self.MM.CurrentSection() == CurrentState.GAME_OPTIONS:
                            currentOption = self.MM.CurrentOption()
                            # do stuff with the current option
                    print(event.name)
                    
                elif event.name == BUTTON_2:
                    print(event.name)

                elif event.name == BUTTON_3:
                    print(event.name)

                elif event.name == BUTTON_4:
                    print(event.name)

                elif event.name == BUTTON_5:
                    print(event.name)

                elif event.name == BUTTON_6:
                    print(event.name)

                elif event.name == BUTTON_7:
                    print(event.name)

                elif event.name == BUTTON_8:
                    print(event.name)

                elif event.name == HOME_BUTTON:
                    print(event.name)

                elif event.name == COIN_BUTTON:
                    print(event.name)

                elif event.name == DI_UP:
                    if self.currentState == CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == Section.TABS:
                            
                            # if not at the beginning of the list and not inside a tab
                            if self.MM.t_i > 0 and self.MM.currentTab().collapse:
                                self.MM.CurrentTab().is_selected = False
                                self.MM.t_i -= 1
                                if self.MM.CurrentTab().collapse:
                                    self.MM.CurrentTab().is_selected = True
                                else:
                                    currentTab = self.MM.CurrentTab()
                                    currentTab.children[len(currentTab.children) - 1].is_selected = True

                            # if not at the beginning and tab not collapsed
                            elif self.MM.t_i > 0 and not self.MM.CurrentTab().collapse:
                                if self.MM.CurrentTab().is_selected:
                                    self.MM.CurrentTab().is_selected = False
                                    self.MM.t_i -= 1
                                    if self.MM.CurrentTab().collapse:
                                        self.MM.CurrentTab().is_selected = True
                                    else:
                                        currentTab = self.MM.CurrentTab()
                                        currentTab.children[len(currentTab.children) - 1].is_selected = True

                                else:
                                    for i in range(len(self.MM.CurrentTab().children)):
                                        if self.MM.CurrentTab().children[i].is_selected:
                                            self.MM.CurrentTab().children[i].is_selected = False;

                                            if i == 0:
                                                self.MM.CurrentTab().is_selected = True;
                                            else:
                                                currentTab.children[i - 1].is_selected = True;

                                            break;
                            else:
                                print("DEBUG: Potentially unaccounted-for case in the Tabs section")

                        elif self.MM.currentSection == Section.GAMES:
                            print("Cycle through games")
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)


                elif event.name == DI_DOWN:
                    if self.currentState == CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == Section.TABS:
                            # if not on the last tab and the current tab is collapsed
                            if self.MM.t_i < len(self.MM.tabsList) - 1 and self.MM.currentTab().collapse:
                                self.MM.CurrentTab().is_selected = False
                                self.MM.t_i += 1
                                self.MM.CurrentTab().is_selected = True


                            # if on any tab and the tab is not collapsed
                            elif not self.MM.CurrentTab().collapse:
                                if self.MM.CurrentTab().is_selected:
                                    self.MM.CurrentTab().is_selected = False                                    
                                    self.MM.CurrentTab().children[0].is_selected = True
                                
                                else: # find the child that is selected 
                                    for i in range(len(self.MM.CurrentTab().children)):
                                        if self.MM.CurrentTab().children[i].is_selected: # once you find it
                                            

                                            if (i == (len(self.MM.CurrentTab().children) - 1)) and self.MM.t_i < (len(self.MM.tabsList) - 1): # if it's the last item in a sub tab and there is a next tab
                                                self.MM.CurrentTab().children[i].is_selected = False;
                                                self.MM.t_i += 1
                                                self.MM.CurrentTab().is_selected = True;
                                            else:
                                                self.MM.CurrentTab().children[i].is_selected = False;
                                                currentTab.children[i + 1].is_selected = True;

                                            break;
                            else:
                                print("DEBUG: Potentially unaccounted-for case in the Tabs section")


                        elif self.MM.currentSection == Section.GAMES:
                            print("Cycle through games")
                            # Cycle through games

                        else:
                            pass # being in the game options doesn't matter


                    elif self.currentState == CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

                # move towards the left side of the screen
                elif event.name == DI_LEFT:
                    if self.currentState == CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == Section.GAME_OPTIONS and self.MM.o_i > PLAY:
                            self.MM.CurrentOption().is_selected = False
                            self.MM.o_i -= 1 
                            self.MM.CurrentOption().is_selected = True
                        elif self.MM.currentSection > Section.TABS:
                            self.MM.currentSection -= 1
                            
                        else:
                            pass # eat the input
                        print(event.name)

                    elif self.currentState == CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

                # move towards the right side of the screen
                elif event.name == DI_RIGHT:
                    if self.currentState == CurrentState.MAIN_MENU_STATE:
                        if self.MM.currentSection == Section.GAME_OPTIONS and self.MM.o_i < FAVORITE:
                            self.MM.CurrentOption().is_selected = False
                            self.MM.o_i += 1
                            self.MM.CurrentOption().is_selected = True
                            
                        elif self.MM.currentSection < Section.GAME_OPTIONS:
                            self.MM.currentSection += 1

                        else:
                            pass # eat the input
                        print(event.name)

                    elif self.currentState == CurrentState.GAME_STATE:
                        # Transfer input to emulator
                        print("Transfer Input")
                        
                    else:
                        print("DEBUG: The current state is incorrect")
                    print(event.name)
                    

            elif event.event_type == KEY_UP:
                # Anti Turbo
                if(event.name in self.currentInputs):
                    self.currentInputs.remove(event.name);
                else:
                    # print("Somehow, there was a key up event for something that didn't have a key down input")
                    print(event.name)
                    return
                
            
        else:
            pass # There's nothing to do right now

        self.updateState();

      
    def updateState(self):
        """based on the current state, inputs will alter the state:
        if current state is menu state, the stick will iterate through
        the various menus/sections and call functions as needed.
        If current state is game state, inputs will be determined based on
        control scheme and then transmitted as the appropriate inputs
        If current state is paused state, inputs will be read as appropriate
        (P2 inputs only, etc.)"""
        if self.currentState == CurrentState.MAIN_MENU_STATE:
            # Undo all selections
            # Tabs Section
            for tab in self.MM.tabsList:
                for subTab in tab.children:
                    subTab.color = subTab.default_color

                tab.color = tab.default_color

            # Games Section
            # Game Options Section
            for option in self.MM.optionsList:
                option.backgroud_normal = option.default

            # Then set new selection
            if self.MM.currentSection == Section.TABS:
                if self.MM.CurrentTab().is_selected:
                    self.MM.CurrentTab().color = self.MM.CurrentTab().selected_color
                else:
                    for subTab in self.MM.CurrentTab().children:
                        if subTab.is_selected:
                            subTab.color = subTab.selected_color
            elif self.MM.currentSection == Section.GAMES:
                # Show the active game as well as the surrounding games
                # Also, update any animations needed to fully transtition between games
                print("Games Section")
            elif self.MM.currentSection == Section.GAME_OPTIONS:
                for option in self.MM.optionsList:
                    if option.is_selected:
                        option.background_normal = option.selected
                
        elif self.currentState == CurrentState.GAME_STATE:
            print("you shouldn't be here yet")
        else:
            print("STATE ERROR!")

    
    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0);
        
        
# This was just me testing code. Can be deleted at any time.
def endProgram():
    print("hello")
    sys.exit()
    print("bye")

pam = PAM();
pam.Display.run();
# main loop
# displays current state
# updates current state

