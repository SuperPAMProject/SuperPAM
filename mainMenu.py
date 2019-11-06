import includes
import pamWidgets
import os

# This class will contain all the data needed to write to all the labels
# in order to display everything
class mainMenu:

    # Set up menu buttons/game carousel/game info
    # Populate lists from files
    def __init__(self, sidebar, games, actionbtns):
        self.tabsList = [];
        self.gameList = [];
        self.favoriteList = [];
        self.optionsList = [];
        self.currentSection = includes.Section.TABS; # Sections
        self.t_i = 0; # Tabs
        self.g_i = 0; # Games
        self.o_i = 0; # Game Options
        self.f_i = 0; # Favorites
        self.populateMenus(sidebar);
        self.populateGameLibrary(games)
        #self.populateFavorites();
        self.populateGameOptions(actionbtns);
        

    # sets up the menus labels so that they can be displayed
    def populateMenus(self, sidebar):

        for child in sidebar.children:
            self.tabsList.append(child)


    # reads from a folder all the game data
    # then stores the data for use at a later time
    def populateGameLibrary(self, games):
        with open(includes.game_titles, 'r') as handle:
            games.add_widget(pamWidgets.GameCarouselItem())
            games.add_widget(pamWidgets.GameCarouselItem())
            games.add_widget(pamWidgets.GameCarouselItem())
            games.add_widget(pamWidgets.GameCarouselItem()) # current game 
            games.add_widget(pamWidgets.GameCarouselItem())
            games.add_widget(pamWidgets.GameCarouselItem())
            games.add_widget(pamWidgets.GameCarouselItem())
            for i in range(0, len(games.children)):
                games.children[i].background_color = (0, 0, 0, 0)
                games.children[i].index = i #index will be used later in the animations
                

            
            selected_game = pamWidgets.GameCarouselItem()
            selected_game.text = ""
            games.add_widget(selected_game)
            #highlighter = pamWidgets.GameCarouselHighlighter()
            #games.add_widget(highlighter)
            #games.children[0].x = games.children[3].x
            #games.children[0].y += games.children[3].y
            #games.children[0].background_color = includes.get_color_from_hex(selected_game.h_color)
            
            index = 0
            for line in handle:
                info = line.split(', ')
                newGame = pamWidgets.GameCarouselItem()
                newGame.gameName = info[0]
                newGame.gameInfo.append(info[1])
                newGame.gameInfo.append(info[2])
                newGame.gameInfo.append(info[3])
                newGame.gameInfo.append(info[4])
                newGame.gamePath = info[4]
                newGame.text = newGame.gameName
                newGame.index = index
                index += 1
                self.gameList.append(newGame);

    # sets up the game options so that they can be displayed
    def populateGameOptions(self, actionbtns):
            
        for child in actionbtns.children:
            self.optionsList.append(child)


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
    def GetGame(self, gameId = None):
        if gameId == None:
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
