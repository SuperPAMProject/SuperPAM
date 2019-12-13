#Authored by Steven Quast
#Refactored by Michael Tanner

# =============================================================================
#-----MENU MODULE-----
# =============================================================================

# This module initializes the core features of the Super PAM Menu.
# In particular, it populates the game library, sets the iterator indices for 
# the tabs, sub-tabs, and action buttons, which will be used in the MAIN module
# for user navigation. The module uses these indices to track which menu item the 
# user is currently highlighting. 

from menuDivisions import Section
from pamWidgets import GameCarouselItem
from pamFunctions import getUserSettings

# This class will contain all the data needed to write to all the labels
# in order to display everything
class mainMenu:

    # Set up menu buttons/game carousel/game info
    # Populate lists from files
    def __init__(self, sidebar, games, actionbtns):
        self.tabs_list = []
        self.game_list = []
        self.favorite_list = []
        self.action_button_list = []
        self.currentSection = Section.TABS; # Sections
        self.t_i = 0; # Tabs
        self.s_t_i = 0 # SubTabs
        self.g_i = 0; # Games
        self.a_b_i = 0; # Action Buttons
        self.f_i = 0; # Favorites
        self.populateMenus(sidebar)
        self.populateGameLibrary(games)
        self.populateFavorites()
        self.populateActionButtons(actionbtns)

        #Read from data files on startup
        self.current_color_scheme = getUserSettings('color_scheme:')
        self.current_font = getUserSettings('font_type:')
        self.current_font_size = float(getUserSettings('font_size:'))
        self.turbo_on = bool(int(getUserSettings('turbo_on:')))
        self.video_is_mute = bool(int(getUserSettings('mute_video:')))
        self.sfx_is_mute = bool(int(getUserSettings('mute_sfx:')))

        #Miscellaneous settings
        self.favorite_sort = False
        self.defaults = False
              
    # Sets up the menus labels so that they can be displayed
    def populateMenus(self, sidebar):
        for child in sidebar.children:
            self.tabs_list.append(child)
        
        self.t_i = len(self.tabs_list) - 1

    # Reads from a folder all the game data
    # then stores the data for use at a later time
    def populateGameLibrary(self, games):
        with open("games.txt", 'r') as handle:
            games.add_widget(GameCarouselItem())
            games.add_widget(GameCarouselItem())
            games.add_widget(GameCarouselItem())
            games.add_widget(GameCarouselItem()) # current game 
            games.add_widget(GameCarouselItem())
            games.add_widget(GameCarouselItem())
            games.add_widget(GameCarouselItem())
            for i in range(0, len(games.children)):
                games.children[i].background_color = (0, 0, 0, 0)
                games.children[i].index = i #index will be used later in the animations
            
            index = 0
            for line in handle:
                info = line.split(', ')
                if len(info) < 5:
                    print("ERROR IN READING GAME")
                    continue
                
                newGame = GameCarouselItem()
                newGame.game_name = info[0]
                newGame.game_info.append(info[1])
                newGame.game_info.append(info[2])
                newGame.game_info.append(info[3])
                newGame.game_info.append(info[4])
                newGame.game_image = info[5].strip("\n")
                newGame.game_path = info[0]
                newGame.text = newGame.game_name
                newGame.index = index
                index += 1
                self.game_list.append(newGame);

    # Reads a list of favorites from a file
    # and compares it to the game list. If the game
    # is on the list, then it adds it to the favorite list
    def populateFavorites(self):
        f = open('user/favorites.txt', 'r')
        lines = f.readlines()
        game_titles = []

        for game in self.game_list: game_titles.append(game.game_name + '\n')
        matches = set(lines).intersection(game_titles)

        for game in self.game_list: 
            if (game.game_name + '\n') in matches:
                game.is_favorite = True
                self.favorite_list.append(game)
                
        f.close()

    # Sets up the game options so that they can be displayed
    def populateActionButtons(self, actionbtns):
            
        for child in actionbtns.children:
            self.action_button_list.append(child)

        self.a_b_i = len(self.action_button_list) - 1

    # Tabs
    def CurrentTab(self, offset = 0):
        if len(self.tabs_list) > 0:
            if (self.t_i + offset) < 0 or (self.t_i + offset) >= len(self.tabs_list):
                return self.tabs_list[self.t_i]
            returnMe = self.tabs_list[self.t_i + offset]
            return returnMe
        else:
            return None

    # SubTabs - added by Michael Tanner
    def CurrentSubTab(self, subTabList, offset = 0):
        if len(subTabList) > 0:
            if (self.s_t_i + offset) < 0 or (self.s_t_i + offset) >= len(subTabList):
                return subTabList[self.s_t_i]
            returnMe = subTabList[self.s_t_i + offset]
            return returnMe
        else:
            return None

    # Games
    def GetGame(self, offset = 0):
        gameId = self.g_i + offset
            
        while gameId < 0:
            gameId += len(self.game_list)

        while gameId >= len(self.game_list):
            gameId -= len(self.game_list)

        return self.game_list[gameId]

    # Favorites
    def GetFavorite(self, offset = 0):
        if len(self.favorite_list) is 0:
            emptyGame = GameCarouselItem()
            emptyGame.game_name = "DummyPath"
            emptyGame.game_info.append(" ")
            emptyGame.game_info.append(" ")
            emptyGame.game_info.append(" ")
            emptyGame.game_info.append(" ")
            emptyGame.game_image = "./img/no_alpha.png"
            emptyGame.game_path = "DummyPath"
            emptyGame.text = " "
            emptyGame.index = 0
            return emptyGame
        
        favoriteId = self.f_i + offset
        while favoriteId < 0:
            favoriteId += len(self.favorite_list)

        while favoriteId >= len(self.favorite_list):
            favoriteId -= len(self.favorite_list)

        return self.favorite_list[favoriteId]

    # Game Options
    def CurrentOption(self):
        return self.action_button_list[self.a_b_i]


