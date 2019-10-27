#-----CONTROL SCHEME MODULE-----
#This module is a control scheme dictionary that assigns keys to each players' inputs. 
#The purpose of this module is to help the user check a user's input against the currently assigned keys. 
#The user can check this association by calling the getInput function. The function requires the player'a id and the 
#input to be checked. The function will then return the key name as a string.
import keyboard

player = "player1"

inputs = {
    "player1": {
        "up": 'up',
        "down": 'down',
        "left": 'left',
        "right": 'right',
        "select": 'enter',
        "reject": 'backspace',
        "home": 'spacebar',
        "coin": 'shift',
        "btn1": 'w',
        "btn2": 'a',
        "btn3": 's',
        "btn4": 'd',
        "btn5": 'q',
        "btn6": 'e'
    },

    "player2": {
        "up": '8',
        "down": '2',
        "left": '4',
        "right": '6',
        "select": 'z',
        "reject": 'x',
        "home": 'spacebar',
        "coin": '/',
        "btn1": 'r',
        "btn2": 't',
        "btn3": 'y',
        "btn4": 'f',
        "btn5": 'g',
        "btn6": 'h'
    },

    "player3": {
        "up": 'up',
        "down": 'down',
        "left": 'left',
        "right": 'right',
        "select": 'enter',
        "reject": 'backspace',
        "home": 'spacebar',
        "coin": 'shift',
        "btn1": 'w',
        "btn2": 'a',
        "btn3": 's',
        "btn4": 'd',
        "btn5": 'q',
        "btn6": 'e'
    },

    "player4": {
        "up": 'up',
        "down": 'down',
        "left": 'left',
        "right": 'right',
        "select": 'enter',
        "reject": 'backspace',
        "home": 'spacebar',
        "coin": 'shift',
        "btn1": 'w',
        "btn2": 'a',
        "btn3": 's',
        "btn4": 'd',
        "btn5": 'q',
        "btn6": 'e'
    } 
}

def getInput(player, input):
    return inputs[player].get(input)

def getPlayer():
    return player

if __name__ == "__main__":
    print(getInput(player, "select"))