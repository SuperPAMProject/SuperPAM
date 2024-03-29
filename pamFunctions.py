#import pamWidgets
import os
import subprocess
from subprocess import check_output
import includes
import pamWidgets
#import win32con
#import win32gui
#import win32process
from kivy.app import App
from kivy.core.text import LabelBase
import display

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
    for game in lib:
        print(getTitle(game))

def getTitle(game):
    return game.text 


def sortByDev(lib):
    lib.sort(key=getDev)
    for game in lib:
        print(getDev(game))

def getDev(game):
    return game.gameInfo[1]


def sortByPub(lib):
    lib.sort(key=getPub)
    for game in lib:
        print(getPub(game))

def getPub(game):
    return game.gameInfo[2]


def sortByGenre(lib):
    lib.sort(key=getGenre)

def getGenre(game):
    return game.genre


def sortByYear(lib):
    lib.sort(key=getYear)
    for game in lib:
        print(getYear(game))

def getYear(game):
    return game.gameInfo[0]


def sortByFavorite(lib):
    lib.sort(key=getFavorite)
    for game in lib:
        if getFavorite(game):
            print(game.gameName)

def getFavorite(game):
    return game.isFavorite


#SOUND FUNCTIONS
def soundPopup(player):
    pass

def MuteSound(menu, btn):
    if btn.text == 'Mute Video':
        menu.videoIsMute = True
        btn.text = 'Unmute Video'

    elif btn.text == 'Mute SFX':
        menu.sfxIsMute = True
        btn.text = 'Unmute SFX'

    elif btn.text == 'Unmute Video':
        menu.videoIsMute = False
        btn.text = 'Mute Video'

    elif btn.text == 'Unmute SFX':
        menu.sfxIsMute = False
        btn.text = 'Mute SFX'

    print(menu.sfxIsMute)
    print(menu.videoIsMute)
    #Store preference in user settings


#VISUALS FUNCTIONS
def visualsPopup(player):
    pass

def setColorScheme(menu, scheme):
    menu.current_color_scheme = scheme.lower()
    print(scheme)
    #Store preference in user settings

def setFontType(menu, font):
    menu.current_font = font
    print(font)
    #Store preference in user settings

def setFontSize(menu, size):
    menu.current_font_size = size.lower()
    print(size)
    #Store preference in user settings


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
#def get_hwnds_for_pid (pid):
 # def callback (hwnd, hwnds):
  #  if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
   ##   _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
     # if found_pid == pid:
      #  hwnds.append (hwnd)
    #return True

  #hwnds = []
  #win32gui.EnumWindows (callback, hwnds)
  #return hwnds

def setVisibility(wid):
    wid.disabled = not wid.disabled
    if wid.opacity == 1:
        wid.opacity = 0
    else:
        wid.opacity = 1

def multiplayerPopup(btn, menu):

    #App.get_running_app().root.add_widget(con)
    #dark = App.get_running_app().root.ids.dark
   # dark.size_hint = (1, 1)
    #dark.opacity = 1
    #dark.disabled = False

    #pop = App.get_running_app().root.ids.multiplayerPop
    #pop.ids.header.ids.title.text = 'MULTIPLAYER'
    #pop.size_hint = (0.6, 0.74)
    #pop.opacity = 1
   # pop.disabled = False
    
   # for child in pop.ids.content.children:
      #  setVisibility(child)

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

def sidebarSwitch(btn, menu):
    #carousel = menu.layout.ids['car']
    #carousel.moveToSideBar(btn.func_id)
    pass

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
        pass
    elif btn.func_id == 'sort':
        pass
    elif btn.func_id == 'options':
        pass
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
        return sidebarSwitch(btn, menu)
    elif btn.func_id == 'visuals':
        pass
    elif btn.func_id == 'user':
        pass
    elif btn.func_id == 'controls':
        pass
    elif btn.func_id == 'by_favs':
        return sortByFavorite(menu.gameList)
    elif btn.func_id == 'by_title':
        return sortByTitle(menu.gameList)
    elif btn.func_id == 'by_dev':
        return sortByDev(menu.gameList)
    elif btn.func_id == 'by_yr':
        return sortByYear(menu.gameList)
    elif btn.func_id == 'by_pub':
        return sortByPub(menu.gameList)
    elif btn.func_id == 'color_scheme':
        return setColorScheme(menu, btn.text)
    elif btn.func_id == 'font_type':
        return setFontType(menu, btn.text)
    elif btn.func_id == 'font_size':
        return setFontSize(menu, btn.text)
    elif btn.func_id == 'mute':
        return MuteSound(menu, btn)



if __name__ == "__main__":
    pass
