
#-----COLOR SCHEME MODULE-----
#This module is a simple color scheme dictionary. The user will select a color scheme name through the 'current_scheme'
#variable. Based on that chosen scheme, the getColor function will retrieve a color fitting the category given by
#the user. The categories are: background, primary, secondary, accent, warning, font-light, and font-dark.

#Primary will be used as default for most button widgets, with secondary used as their highlight color, 
#and accent as a selection color. Warning is used only in critical decisions for the user.
#Font-light is the font-color for lighter backgrounds, and font-dark is for darker ones. 


current_scheme = "waves" #should read from user's settings on start up

color_schemes = {
    "waves" : {
        "background": "#101216",
        "primary": "#3D518C",
        "secondary": "#7899D4",
        "accent": "#96CDFF",
        "warning": "#C33C54",
        "font_light": "#FFFFFF",
        "font-dark": "#FFFFFF"
    },
    "watermelon" : {
        "background": "#101216",
        "primary": "#23967F",
        "secondary": "#F7BFB4",
        "accent": "#ED6A5E",
        "warning": "#ED6A5E",
        "font_light": "#FFFFFF",
        "font_dark": "#101216"
    }, 
    "burn" : {
        "background": "#101216",
        "primary": "#E16036",
        "secondary": "#E13700",
        "accent": "#D6CBC1",
        "warning": "#FF3300",
        "font_light": "#FFFFFF",
        "font_dark": "#101216"
    },
    "blossom": {
        "background": "#101216",
        "primary": "#F991CC",
        "secondary": "#E2AFDE",
        "accent": "#7E5A9B",
        "warning": "#FF3300",
        "font_light": "#63458A",
        "font_dark": "#63458A"
    }
}

def getColor(color):
    return color_schemes[current_scheme].get(color)

if __name__ == "__main__":
    print(getColor("accent"))