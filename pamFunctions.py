#import pamWidgets
import os
import subprocess
from subprocess import check_output
import includes
import pamWidgets
import win32con
import win32gui
import win32process
from kivy.app import App

#PLACEHOLDER VARIABLES
player = ''
session = ''
current_game = ''
emulator = 'emulators/mame64.exe'
client = ''
library = ''
menu = ''

def populateGameLibrary(self):
    self.setLayout()
    with open(includes.game_titles, 'r') as handle:
        for line in handle:
            info = line.split(', ')
            newGame = pamWidgets.GameCarouselItem()
            newGame.gameName = info[0]
            newGame.gameInfo.append(info[1])
            newGame.gameInfo.append(info[2])
            newGame.gameInfo.append(info[3])
            newGame.gameInfo.append(info[4])
            newGame.text = newGame.gameName
            self.add_widget(newGame)
            self.gameList.append(newGame)
            #Just printing for testing. Can be removed anytime
            print("Title: " + newGame.gameName)
            print("Year: " + newGame.gameInfo[0])
            print("Publisher: " + newGame.gameInfo[1])
            print("Developer: " + newGame.gameInfo[2])
            print("Path: " + newGame.gameInfo[3])


#ACTON BUTTON FUNCTIONS
def playGame(game_path):
    try:
        os.chdir('C:/Users/Michael/Documents/Hobbies/Coding/Bob/SuperPAM/emulators')
        process = check_output('C:/Users/Michael/Documents/Hobbies/Coding/Bob/SuperPAM/emulators/mame64.exe ' + game_path , shell=True)
        print(process)
        os.chdir('C:/Users/Michael/Documents/Hobbies/Coding/Bob/SuperPAM')
        return process
    except subprocess.CalledProcessError as e:
        output = e.output
        print(output)
   
def closeGame(game):
    game.terminate()

def saveGame(game):
    #get file path to current game's save states
    #load files into a list of Save State buttons, one for each state (max of 8)
    #deactivate the current group
    #spawn save state group popup
    #activate popup group
    pass

def favGame(game, menu):
    game.isFavorite = not game.isFavorite

    if game.isFavorite:
        menu.favoriteList.append(game)
        with open('user/favorites.txt', 'a') as favTxt:
            favTxt.write(game.gameName + "\n")
        favTxt.close()
    else:
        menu.favoriteList.remove(game)
        with open("user/favorites.txt", "r") as favTxt:
            lines = favTxt.readlines()
        with open("user/favorites.txt", "w") as favTxt:
            for line in lines:
                if line.strip("\n") != game.gameName:
                    favTxt.write(line)
        favTxt.close()

    for g in menu.favoriteList:
        print(g.gameName)
    

    

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

def remapButton(player):
    pass

def confirmRemap(player):
    pass


#MISC. FUNCTIONS
def get_hwnds_for_pid (pid):
  def callback (hwnd, hwnds):
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
      _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
      if found_pid == pid:
        hwnds.append (hwnd)
    return True

  hwnds = []
  win32gui.EnumWindows (callback, hwnds)
  return hwnds

def setVisibility(wid):
    wid.disabled = not wid.disabled
    if wid.opacity == 1:
        wid.opacity = 0
    else:
        wid.opacity = 1

def multiplayerPopup(btn, menu):

    #con = pamWidgets.PopupWindowLayout(size=(75, 75), pos=(50, 50)) #pamWidgets.PopupWindowButton(text='hi')#
    #App.get_running_app().root.add_widget(con)
    dark = App.get_running_app().root.ids.dark
    dark.size_hint = (1, 1)
    dark.opacity = 1
    dark.disabled = False

    pop = App.get_running_app().root.ids.multiplayerPop
    pop.ids.header.ids.title.text = 'MULTIPLAYER'
    pop.size_hint = (0.6, 0.74)
    pop.opacity = 1
    pop.disabled = False
    
    for child in pop.ids.content.children:
        setVisibility(child)

    return True

def sortPopup(btn, menu):
    dark = App.get_running_app().root.ids.dark
    dark.size_hint = (1, 1)
    dark.opacity = 1
    dark.disabled = False

    pop = App.get_running_app().root.ids.sortPop
    pop.ids.header.ids.title.text = 'SORT GAMES'
    pop.size_hint = (0.6, 0.74)
    pop.opacity = 1
    pop.disabled = False

    setVisibility(pop.ids.content.children[0])
    return True

def optionsPopup(btn, menu):
    dark = App.get_running_app().root.ids.dark
    dark.size_hint = (1, 1)
    dark.opacity = 1
    dark.disabled = False

    pop = App.get_running_app().root.ids.multiplayerPop
    pop.ids.header.ids.title.text = 'OPTIONS'
    pop.size_hint = (0.6, 0.74)
    pop.opacity = 1
    pop.disabled = False
    return True


#ACTIVATED ON BUTTON SELECTION, TAKES ID OF BUTTON TO DETERMINE FUNCTION
def getFunction(btn, menu):
    if btn.func_id == 'play':
        return playGame(menu.GetGame().gameName)
    elif btn.func_id == 'save':
        return saveGame(current_game)
    elif btn.func_id == 'fav':
        return favGame(menu.GetGame(), menu)
    elif btn.func_id == 'host':
        return startSession(player)
    elif btn.func_id == 'multiplayer':
        return multiplayerPopup(btn, menu)
    elif btn.func_id == 'sort':
        return sortPopup(btn, menu)
    elif btn.func_id == 'options':
        return optionsPopup(btn, menu)
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
    pass