import threading
import sys
import keyboard # This import requires a pip install. It will also require a
                # sudo for Linux machines (i.e. Raspbian)
import includes
import mainMenu
import display
import pamWidgets
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
        self.updateState();
        for tab in self.MM.tabsList:
            print(tab.text)
        


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
                            # do stuff with the current tab
                        elif self.MM.currrentSection == includes.Section.GAMES:
                            currentGame = self.MM.GetGame()
                            # do stuff with the current game
                        elif self.MM.currentSection == includes.Section.GAME_OPTIONS:
                            currentOption = self.MM.CurrentOption()
                            # do stuff with the current option
                    print(event.name)
                    
                elif event.name == includes.BUTTON_2:
                    print(event.name)

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
                    print(event.name)

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

                        elif self.MM.currentSection == includes.Section.GAMES:
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


                        elif self.MM.currentSection == includes.Section.GAMES:
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
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and self.MM.o_i > includes.GameOptions.PLAY:
                            self.MM.CurrentOption().highlighted = False
                            self.MM.o_i -= 1 
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
                        if self.MM.currentSection == includes.Section.GAME_OPTIONS and self.MM.o_i < includes.GameOptions.FAVORITE:
                            self.MM.CurrentOption().highlighted = False
                            self.MM.o_i += 1
                            self.MM.CurrentOption().highlighted = True
                            
                        elif self.MM.currentSection < includes.Section.GAME_OPTIONS:
                            self.MM.currentSection += 1

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

        self.updateState();

      
    def updateState(self):
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
                    print(self.MM.CurrentTab().background_color)
                    self.MM.CurrentTab().background_color = includes.get_color_from_hex(self.MM.CurrentTab().h_color)
                    print(self.MM.CurrentTab().background_color)
                else:
                    for subTab in self.MM.CurrentTab().children:
                        if subTab.highlighted:
                            subTab.background_color = includes.get_color_from_hex(subTab.h_color)
            elif self.MM.currentSection == includes.Section.GAMES:
                # Show the active game as well as the surrounding games
                # Also, update any animations needed to fully transtition between games
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

    
    # a function to close out of the PAM
    def closePAM(self):
        sys.exit(0);
        

pam = PAM();

pam.Display.run();

# main loop
# displays current state
# updates current state

