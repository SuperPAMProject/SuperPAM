import includes
import pamWidgets
import os

# This class will contain all the data needed to write to all the labels
# in order to display everything
class mainMenu:

    # Set up menu buttons/game carousel/game info
    # Populate lists from files
    def __init__(self, sidebar, games, actionbtns):
        self.tabsList = []
        self.gameList = []
        self.favoriteList = []
        self.optionsList = []
        self.currentSection = includes.Section.TABS; # Sections
        self.t_i = 0; # Tabs
        self.s_t_i = 0 # SubTabs
        self.g_i = 0; # Games
        self.o_i = 0; # Game Options
        self.f_i = 0; # Favorites
        self.populateMenus(sidebar)
        self.populateGameLibrary(games)
        self.populateFavorites()
        self.populateGameOptions(actionbtns)
        self.current_color_scheme = includes.colors.current_scheme
        self.current_font = 'Roboto'
        
    # sets up the menus labels so that they can be displayed
    def populateMenus(self, sidebar):
        for child in sidebar.children:
            self.tabsList.append(child)
        
        self.t_i = len(self.tabsList) - 1

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
            
            index = 0
            for line in handle:
                info = line.split(', ')
                if len(info) < 5:
                    print("ERROR IN READING GAME")
                    continue
                info[4] = info[4].strip("\n")
                newGame = pamWidgets.GameCarouselItem()
                newGame.gameName = info[0]
                newGame.gameInfo.append(info[1])
                newGame.gameInfo.append(info[2])
                newGame.gameInfo.append(info[3])
                newGame.gameInfo.append(info[4])
                newGame.gameImage = info[5]
                newGame.gamePath = info[0]
                newGame.text = newGame.gameName
                newGame.index = index
                index += 1
                self.gameList.append(newGame);

    # reads a list of favorites from a file
    # and compares it to the game list. If the game
    # is on the list, then it adds it to the favorite list
    def populateFavorites(self):
        pass

    # sets up the game options so that they can be displayed
    def populateGameOptions(self, actionbtns):
            
        for child in actionbtns.children:
            self.optionsList.append(child)

        self.o_i = len(self.optionsList) - 1

    # Tabs
    def CurrentTab(self, offset = 0):
        if len(self.tabsList) > 0:
            if (self.t_i + offset) < 0 or (self.t_i + offset) >= len(self.tabsList):
                return self.tabsList[self.t_i]
            returnMe = self.tabsList[self.t_i + offset]
            return returnMe
        else:
            return None

    # SubTabs
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
            gameId += len(self.gameList)

        while gameId >= len(self.gameList):
            gameId -= len(self.gameList)
            
        return self.gameList[gameId]

    # Favorites
    def GetFavorite(self, offset = 0):
        if len(self.favoriteList) is 0:
            return None
        
        favoriteId = self.f_i + offset
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
