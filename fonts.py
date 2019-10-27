#-----FONT MODULE-----
#This module allows users to quickly retrive either the bold or normal version of the currently set font.
#The fonts are in two modes: standard and dydlexia. User's can retieve the fonts through the getFont function.
#The function requires only the font style (normal or bold) and it will return the path to the desired font.

font_mode = "standard"

fonts = {
    "standard": {
        "normal": "fonts/Roboto-Light.ttf",
        "bold": "fonts/Roboto-Bold.ttf"
    },

    "dyslexia": {
        "normal": "N",
        "bold": "B"
    }
}

def getFont(font):
    return fonts[font_mode].get(font)

def setFont(mode):
    font_mode = mode

if __name__ == "__main__":
    print(getFont("bold"))