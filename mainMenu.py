import includes
import os

# This class will contain all the data needed to write to all the labels
# in order to display everything
class mainMenu:

    # Set up menu buttons/game carousel/game info
    # Populate lists from files
    def __init__(self, display):
        print(display)
        self.tabsList = [];
        self.gameList = [];
        self.favoriteList = [];
        self.optionsList = [];
        self.currentSection = includes.Section.TABS; # Sections
        self.t_i = 0; # Tabs
        self.g_i = 0; # Games
        self.o_i = 0; # Game Options
        self.f_i = 0; # Favorites
        self.populateMenus(display);
        #self.populateGameLibrary();
        #self.populateFavorites();
        self.populateGameOptions(display);
        

    # sets up the menus labels so that they can be displayed
    def populateMenus(self, display):

        def populateMenu(self, widget):

            # if we come across a MenuTab, add it to the list
            if 'MenuTab' in widget.name:
                self.tabsList.append(widget);
                return;
                
            for child in widget.children:
                populateMenu(self, child);
                #newTab.subTabList.append(child);
            
        for child in display.children:
            populateMenu(self, child);
            
        print("populated tabs list");


    # reads from a folder all the game data
    # then stores the data for use at a later time
    def populateGameLibrary(self, display):
        with open(display.game_titles, 'r') as handle:
            for line in handle:
                newGame = config.Game()
                newGame.gameName = line
                #self.game_lib.add_widget(myLabel)
                self.gameList.append(newGame);
                
    # sets up the game options so that they can be displayed
    def populateGameOptions(self, display):

        def populateOption(self, widget):

            # if we come across an ActionButton, add it to the list
            if 'ActionButton' in widget.name:
                self.optionsList.append(widget);
                return;
                
            for child in widget.children:
                populateOption(self, child);
                #newTab.subTabList.append(child);
            
        for child in display.children:
            populateOption(self, child);
            
        print("populated options list");


    # Tabs
    def CurrentTab(self, offset = 0):
        if len(self.tabsList) > 0:
            if (self.t_i + offset) < 0 or (self.t_i + offset) >= len(self.tabsList):
                return self.tabsList[self.t_i]
            returnMe = self.tabsList[self.t_i + offset]
            return returnMe
        else:
            return -1

    # Games
    def GetGame(self, gameId = -1):
        if gameId == -1:
            gameId = self.g_i
            
        while gameId < 0:
            gameId += len(self.gameList)

        while gameId >= len(self.gameList):
            gameId -= len(self.gameList)
            
        return self.gameList[gameId];

    def GetFavorite(self, favoriteId):
        while favoriteId < 0:
            favoriteId += len(self.favoriteList)

        while favoriteId >= len(self.favoriteList):
            favoriteId -= len(self.favoriteList)

        return self.favoriteList[favoriteId]

    # Game Options
    def CurrentOption(self):
        return self.optionsList[self.o_i]

    # Sorting
    def SortByGenre(self):
        print("test")

    def SortByYear(self):
        print("test")

    def SortByDeveloper(self):
        print("test")
