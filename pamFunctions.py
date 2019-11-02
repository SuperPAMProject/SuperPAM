#import pamWidgets
import os
import subprocess
import includes

#PLACEHOLDER VARIABLES
player = ''
session = ''
current_game = 'games/Legend of Zelda, The - Link_s Awakening (V1.2) (U) [!].gb'
emulator = 'emulators/VisualBoyAdvance.exe'
client = ''
library = ''
menu = ''

def populateGamesLibrary(file):
    with open(file, 'r') as handle:
        for line in handle:
            info = line.split(', ')
            newGame = includes.Game()
            newGame.gameName = info[0]
            newGame.gameInfo.append(info[1])
            newGame.gameInfo.append(info[2])
            newGame.gameInfo.append(info[3])
            newGame.gameInfo.append(info[4])
            print("Title: " + newGame.gameName)
            print("Year: " + newGame.gameInfo[0])
            print("Publisher: " + newGame.gameInfo[1])
            print("Developer: " + newGame.gameInfo[2])
            print("Path: " + newGame.gameInfo[3])
            #self.game_lib.add_widget(myLabel)
            #self.gameList.append(newGame);


#ACTON BUTTON FUNCTIONS
def playGame(emulator_path, game_path):
     return subprocess.Popen([emulator_path, game_path])

def closeGame(game):
    game.terminate()

def saveGame(game):
    #get file path to current game's save states
    #load files into a list of Save State buttons, one for each state (max of 8)
    #deactivate the current group
    #spawn save state group popup
    #activate popup group
    print("SAVE")

def favGame(game, menu):
    print("FAVORITE")
    #game.favorite = not game.favorite

   # if game.favorite:
    #    menu.favoriteList.append(game)
    #else:
     #   menu.favoriteList.remove(game)


#MULTIPLAYER FUNCTIONS
def startSession(player):
    #Listen for client signal
    pass

def endSession(player):
    #Stop listening for client
    pass

def acceptClient(client):
    pass

def kickClient(client):
    pass


#SORTING FUNCTIONS
def sortByTitle(lib):
    lib.sort(key=getTitle)

def getTitle(game):
    return game.text 


def sortByDev(lib):
    lib.sort(key=getDev)

def getDev(game):
    return game.developer


def sortByPub(lib):
    lib.sort(key=getPub)

def getPub(game):
    return game.publisher


def sortByGenre(lib):
    lib.sort(key=getGenre)

def getGenre(game):
    return game.genre


def sortByYear(lib):
    lib.sort(key=getYear)
    pass

def getYear(game):
    return game.year


#SOUND FUNCTIONS
def soundPopup(player):
    pass


#VISUALS FUNCTIONS
def visualsPopup(player):
    pass


#USER FUNCTIONS
def userPopup(player):
    pass

def setUsername(player):
    pass

def viewStats(player):
    pass

def reformatSystem(player):
    pass


#CONTROLS FUNCTIONS
def controlsPopup(player):
    pass


#ACTIVATED ON BUTTON SELECTION, TAKES ID OF BUTTON TO DETERMINE FUNCTION
def getFunction(btn):
    if btn.func_id == 'play':
        return playGame(emulator, current_game)
    elif btn.func_id == 'save':
        return saveGame(current_game)
    elif btn.func_id == 'fav':
        return favGame(current_game, menu)
    elif btn.func_id == 'host':
        return startSession(player)
    elif btn.func_id == 'accept':
        return acceptClient(client)
    elif btn.func_id == 'kick':
        return kickClient(client)
    elif btn.func_id == 'terminate':
        return endSession(session)
    elif btn.func_id == 'dev':
        return sortByDev(library)
    elif btn.func_id == 'pub':
        return sortByPub(library)
    elif btn.func_id == 'genre':
        return sortByGenre(library)
    elif btn.func_id == 'year':
        return sortByYear(library)
    elif btn.func_id == 'sound':
        return soundPopup(player)
    elif btn.func_id == 'visuals':
        return visualsPopup(player)
    elif btn.func_id == 'user':
        return userPopup(player)
    elif btn.func_id == 'controls':
        return controlsPopup(player)


if __name__ == "__main__":
    populateGamesLibrary("games.txt")