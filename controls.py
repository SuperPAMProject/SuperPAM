#-----CONTROL SCHEME MODULE-----
#This module is a control scheme dictionary that assigns keys to each players' inputs. 
#The purpose of this module is to help the user check a user's input against the currently assigned keys. 
#The user can check this association by calling the getInput function. The function requires the player'a id and the 
#input to be checked. The function will then return the key name as a string.



player = "player1"

inputs = {
    "player1": {
        "up": 'up',
        "down": 'down',
        "left": 'left',
        "right": 'right',
        "btn1": 'z',
        "btn2": 'x',
        "btn3": 'c',
        "btn4": 'a',
        "btn5": 's',
        "btn6": 'd',
        "home": 'q',
        "coin": 'w',
    },

    "player2": {
        "up": '8',
        "down": '2',
        "left": '4',
        "right": '6',
        "btn1": 'z',
        "btn2": 'x',
        "btn3": 'y',
        "btn4": 'f',
        "btn5": 'g',
        "btn6": 'h',
        "home": 'spacebar',
        "coin": '/',
    },

    "player3": {
        "up": '8',
        "down": '2',
        "left": '4',
        "right": '6',
        "btn1": 'z',
        "btn2": 'x',
        "btn3": 'y',
        "btn4": 'f',
        "btn5": 'g',
        "btn6": 'h',
        "home": 'spacebar',
        "coin": '/',
    },

    "player4": {
        "up": '8',
        "down": '2',
        "left": '4',
        "right": '6',
        "btn1": 'z',
        "btn2": 'x',
        "btn3": 'y',
        "btn4": 'f',
        "btn5": 'g',
        "btn6": 'h',
        "home": 'spacebar',
        "coin": '/',
    } 
}

def mapControl(player_id, key, value):
    inputs[player_id][key] = value


def getInput(player, input):
    return inputs[player].get(input)

def getPlayer():
    return player

if __name__ == "__main__":
    mapControl('player1', 'up', 'w')

    print(getInput('player2', "up"))