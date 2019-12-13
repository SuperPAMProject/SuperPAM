#Authored and refactored by Michael Tanner

# =============================================================================
#-----SOUND EFFECTS MODULE-----
# =============================================================================

#This module serves as dictionary to map sound effect files to a given identifier.
#The user must call the getSound function and pass it an identifer to retrive 
#the sound effect file that they require. 

sounds = {
    "highlight_btn":"sounds/select_1.wav",
    "select_btn":"sounds/select_3.wav",
    "end_of_list": "sounds/eol_1.wav",
    "up_carousel": "sounds/up_carousel_2.wav",
    "down_carousel": "sounds/down_carousel_2.wav",
    "enter_menu": 'sounds/enter_menu.wav',
    "exit_menu": "sounds/exit_menu.wav"
}


def getSound(sound):
    return sounds[sound]