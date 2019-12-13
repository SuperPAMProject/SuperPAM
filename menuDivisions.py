#Authored by Steven Quast
#Refactored by Michael Tannner

# =============================================================================
#-----MENU DIVISIONS MODULE-----
# =============================================================================

# This module defines divisions between the States, Sections, and  
# Action Buttons of the Super PAM Menu. Each division is written as 
# an integer enum for easy readability in other modules.

from enum import IntEnum

MAIN_MENU_STATE = 0
GAME_STATE = 1
LOADING_STATE = 2


class CurrentState(IntEnum):
    MAIN_MENU_STATE = 0
    GAME_STATE = 1
    LOADING_STATE = 2

class Section(IntEnum):
    TABS = 0
    GAMES = 1
    ACTION_BUTTONS = 2

class ActionButtons(IntEnum):
    PLAY = 0
    FAVORITE = 1
