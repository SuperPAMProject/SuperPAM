#import pamWidgets
import os
import subprocess

#PLACEHOLDER VARIABLES
player = ''
session = ''
current_game = 'games/Legend of Zelda, The - Link_s Awakening (V1.2) (U) [!].gb'
emulator = 'emulators/VisualBoyAdvance.exe'
client = ''
library = ''
menu = ''


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
        playGame(emulator, current_game)
    elif btn.func_id == 'save':
        saveGame(current_game)
    elif btn.func_id == 'fav':
        favGame(current_game, menu)
    elif btn.func_id == 'host':
        startSession(player)
    elif btn.func_id == 'accept':
        acceptClient(client)
    elif btn.func_id == 'kick':
        kickClient(client)
    elif btn.func_id == 'terminate':
        endSession(session)
    elif btn.func_id == 'dev':
        sortByDev(library)
    elif btn.func_id == 'pub':
        sortByPub(library)
    elif btn.func_id == 'genre':
        sortByGenre(library)
    elif btn.func_id == 'year':
        sortByYear(library)
    elif btn.func_id == 'sound':
        soundPopup(player)
    elif btn.func_id == 'visuals':
        visualsPopup(player)
    elif btn.func_id == 'user':
        userPopup(player)
    elif btn.func_id == 'controls':
        controlsPopup(player)

    
if __name__ == "__main__":
    emu = "emulators/VisualBoyAdvance.exe"
    game = "games/Legend of Zelda, The - Link_s Awakening (V1.2) (U) [!].gb"
    g = playGame(emu, game)