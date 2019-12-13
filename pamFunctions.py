#Authored and refactored by Michael Tanner

# =============================================================================
#-----PAM FUNCTIONS MODULE-----
# =============================================================================

# This module outlines a range of helpful functions for other Super PAM modules.
# These functions are primarily used by the Button components in the menu,
# but they are available for use in all other modules. 

# The functions are separated by category: ACTION BUTTON, SORTING, SOUND, VISUALS, 
# USER, CONTROLS, AND MISCELLANEOUS. At the end of the module is a function identifier,
# which helps pair certain functions with the Home Menu's Action Buttons.

import os, sys
from subprocess import check_output, CalledProcessError
from pamWidgets import GameCarouselItem
import win32gui
import win32process


# =============================================================================
# ACTION BUTTON FUNCTIONS
# =============================================================================

# Start the game designated by the given path
def playGame(game_path):
    if game_path is "DummyPath":
        print("There's no game, dummy!")
        return None
    try:
        current_directory = os.getcwd().replace('\\', '/')
        os.chdir(current_directory + '/emulators')
        process = check_output(current_directory + '/emulators/mame64.exe ' + game_path , shell=True)
        os.chdir(current_directory)
        title = win32gui.GetWindowText (win32gui.GetForegroundWindow())
        pid = get_window_pid(title)
        print("GAME: " + title)
        print(pid)
        return pid  
    except CalledProcessError as e:
        output = e.output
        print(output)

# Add/remove the currently selected game to the Favorites list
def favGame(game, menu):
    if game.game_name is "DummyPath":
        return

    game.is_favorite = not game.is_favorite
    
    game_title = game.game_name + '\n'

    f = open('user/favorites.txt', 'r')
    lines = f.readlines()
    if (game_title) in lines:
        lines.remove(game_title)
        menu.favorite_list.remove(game)
    else:
        lines.append(game_title)
        menu.favorite_list.append(game)
    f.close()

    f = open('user/favorites.txt', 'w')
    for line in lines:
        f.write(line)
    f.close()

    print("Favorites Data:")
    print(lines)
    

# =============================================================================
# SORTING
# =============================================================================
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
    return game.game_info[1]


def sortByPub(lib):
    lib.sort(key=getPub)
    for game in lib:
        print(getPub(game))

def getPub(game):
    return game.game_info[2]


def sortByGenre(lib):
    lib.sort(key=getGenre)

def getGenre(game):
    return game.genre


def sortByYear(lib):
    lib.sort(key=getYear)
    for game in lib:
        print(getYear(game))

def getYear(game):
    return game.game_info[0]


def sortByFavorite(lib, menu):
    menu.favorite_sort = not menu.favorite_sort
    lib.sort(key=getFavorite)
    for game in lib:
        if getFavorite(game):
            print(game.game_name)

def getFavorite(game):
    return game.is_favorite


# =============================================================================
# SOUND
# =============================================================================

# Mute either the sound effects or the Game Video, depending on which
# button is selected.
def muteSound(menu, btn):
   
    if 'Video' in btn.text:
        menu.video_is_mute = not menu.video_is_mute
        btn.text = 'Unmute Video' if menu.video_is_mute else 'Mute Video'

    if 'SFX' in btn.text:
        menu.sfx_is_mute = not menu.sfx_is_mute
        btn.text = 'Unmute SFX' if menu.sfx_is_mute else 'Mute SFX'

    editUserSettings('mute_sfx:', str(int(menu.sfx_is_mute)))
    editUserSettings('mute_video:', str(int(menu.video_is_mute)))


# =============================================================================
# VISUALS
# =============================================================================

def setColorScheme(menu, scheme):
    menu.current_color_scheme = scheme.lower()
    editUserSettings('color_scheme:', scheme.lower())


def setFontType(menu, font):
    menu.current_font = font
    editUserSettings('font_type:', font)


def setFontSize(menu, size):
    if size.lower() == 'small':
        menu.current_font_size = 0.5
    elif size.lower() == 'medium':
        menu.current_font_size = 0.8
    elif size.lower() == 'large':
        menu.current_font_size = 1.2
    editUserSettings('font_size:', str(menu.current_font_size))


# =============================================================================
# USER
# =============================================================================
def editUserSettings(field, value):
    f = open('user/settings.txt', 'r')
    lines = f.readlines()
    for i in range(len(lines)):
        if field in lines[i]:
            lines[i] = field + value + '\n'
    f.close()

    f = open('user/settings.txt', 'w')
    for line in lines:
        f.write(line)
    f.close()

def getUserSettings(field):
    f = open('user/settings.txt', 'r')
    lines = f.readlines()
    for line in lines:
        if field in line:
            return line.replace(field, '').strip('\n')
    f.close()
    return 'n/a'

def emptyFavorites(menu):
    open('user/favorites.txt', 'w').close()
    menu.favorite_list = []

def revertToDefaults(menu):
    f = open('user/default_settings.txt', 'r')
    lines = f.readlines()
    f.close()

    f = open('user/settings.txt', 'w')
    for line in lines:
        f.write(line)

    menu.defaults = True
    menu.current_color_scheme = 'waves'
    menu.current_font = 'Roboto'
    menu.current_font_size = 0.8
    menu.video_is_mute = False
    menu.sfx_is_mute = False
    menu.turbo_on = False



# =============================================================================
# CONTROLS
# =============================================================================

def setTurbo(menu):
    menu.turbo_on = not menu.turbo_on
    editUserSettings('turbo_on:', str(int(menu.turbo_on)))

# =============================================================================
# MISC.
# =============================================================================

# Used to make a widget visible/invisible
def setVisibility(wid):
    wid.disabled = not wid.disabled
    if wid.opacity == 1:
        wid.opacity = 0
    else:
        wid.opacity = 1

# Obtain the process id of a window, given its title
def get_window_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

# Obtain window handle for a given process id
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

def populateGameLibrary(self):
    self.setLayout()
    with open("games.txt", 'r') as handle:
        for line in handle:
            info = line.split(', ')
            newGame = GameCarouselItem()
            newGame.game_name = info[0]
            newGame.game_info.append(info[1])
            newGame.game_info.append(info[2])
            newGame.game_info.append(info[3])
            newGame.game_info.append(info[4])
            newGame.text = newGame.game_name
            self.add_widget(newGame)
            self.game_list.append(newGame)

# =============================================================================
# FUNCTON IDENTIFIER
# =============================================================================

#Activated on press of action buttons. Gets the assigned function to the selected button
def getFunction(btn, menu, *largs):
    if btn.func_id == 'play':
        if menu.favorite_sort:
            return playGame(menu.GetFavorite())    
        return playGame(menu.GetGame())
    elif btn.func_id == 'fav':
        if menu.favorite_sort:
            return favGame(menu.GetFavorite(), menu)    
        return favGame(menu.GetGame(), menu)



if __name__ == "__main__":
    pass
