
#-----COLOR SCHEME MODULE-----
#This module is a simple color scheme dictionary. The user will select a color scheme name through the 'current_scheme'
#variable. Based on that chosen scheme, the getColor function will retrieve a color fitting the category given by
#the user. The categories are: background, primary, secondary, accent, warning, font-light, and font-dark.

#Primary will be used as default for most button widgets, with secondary used as their highlight color, 
#and accent as a selection color. Warning is used only in critical decisions for the user.
#Font-light is the font-color for lighter backgrounds, and font-dark is for darker ones. 
#Each action button (Play, Save, Favorite) all have their default, highlight, and selection images for every color scheme.

with open('user/color_scheme.txt', 'r') as cs:
    for line in cs:
        current_scheme = line

color_schemes = {
    "waves" : {
        "background": "#101216",
        "primary": "#3D518C",
        "secondary": "#7899D4",
        "accent": "#96CDFF",
        "warning": "#C33C54",
        "font_light": "#FFFFFF",
        "font-dark": "#FFFFFF",
        "play-d":'img/Play_Waves_Default.png',
        "play-h":'img/Play_Waves_Highlight.png',
        "play-s":'img/Play_Waves_Select.png',
        "save-d":'img/Save_Waves_Default.png',
        "save-h":'img/Save_Waves_Highlight.png',
        "save-s":'img/Save_Waves_Select.png',
        'fav-d':'img/Fav_Waves_Default.png',
        'fav-h':'img/Fav_Waves_Highlight.png',
        'fav-s':'img/Fav_Waves_Select.png',
        'tab-d': 'img/button_waves.png'
    },
    "watermelon" : {
        "background": "#101216",
        "primary": "#23967F",
        "secondary": "#FC6471",
        "accent": "#ED6A5E",
        "warning": "#ED6A5E",
        "font_light": "#FFFFFF",
        "font_dark": "#101216",
        "play-d":'img/Play_Watermelon_Default.png',
        "play-h":'img/Play_Watermelon_Highlight.png',
        "play-s":'img/Play_Watermelon_Select.png',
        "save-d":'img/Save_Watermelon_Default.png',
        "save-h":'img/Save_Watermelon_Highlight.png',
        "save-s":'img/Save_Watermelon_Select.png',
        'fav-d':'img/Fav_Watermelon_Default.png',
        'fav-h':'img/Fav_Watermelon_Highlight.png',
        'fav-s':'img/Fav_Watermelon_Select.png',
        'tab-d': 'img/button_watermelon.png'
    }, 
    "burn" : {
        "background": "#101216",
        "primary": "#E16036",
        "secondary": "#E13700",
        "accent": "#D6CBC1",
        "warning": "#FF3300",
        "font_light": "#FFFFFF",
        "font_dark": "#101216",
        "play-d":'img/Play_Burn_Default.png',
        "play-h":'img/Play_Burn_Highlight.png',
        "play-s":'img/Play_Burn_Select.png',
        "save-d":'img/Save_Burn_Default.png',
        "save-h":'img/Save_Burn_Highlight.png',
        "save-s":'img/Save_Burn_Select.png',
        'fav-d':'img/Fav_Burn_Default.png',
        'fav-h':'img/Fav_Burn_Highlight.png',
        'fav-s':'img/Fav_Burn_Select.png',
        'tab-d': 'img/button_burn.png'
    },
    "blossom": {
        "background": "#101216",
        "primary": "#f03524",
        "secondary": "#E2AFDE",
        "accent": "#7E5A9B",
        "warning": "#FF3300",
        "font_light": "#63458A",
        "font_dark": "#63458A",
        "play-d":'img/Play_Waves_Default.png',
        "play-h":'img/Play_Waves_Highlight.png',
        "play-s":'img/Play_Waves_Select.png',
        "save-d":'img/Save_Waves_Default.png',
        "save-h":'img/Save_Waves_Highlight.png',
        "save-s":'img/Save_Waves_Select.png',
        'fav-d':'img/Fav_Waves_Default.png',
        'fav-h':'img/Fav_Waves_Highlight.png',
        'fav-s':'img/Fav_Waves_Select.png',
        'tab-d': 'img/button_blossom.png'
    }
}

def getColor(color):
    return color_schemes[current_scheme].get(color)

def getColorOfScheme(color, scheme):
    return color_schemes[scheme].get(color)

if __name__ == "__main__":
    print(getColor("accent"))