import pygame
# consts
gray = (100, 100, 100)
lightgray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
X, Y, Z = 0, 1, 2
# NO_TOUCH_MSG = 0
# EDGE_TOUCH_MSG = 1
# SLOPE_TOUCH_MSG = 2

# screen_width = 1200
# screen_height = 650
pygame.init()
infoObject = pygame.display.Info()
print(infoObject)
screen_width = infoObject.current_w
screen_height = infoObject.current_h

borderLineHeight = 110
borderLine2Height = screen_height-90

delta0X = 70
delta0Y = 0

# control points values
circleColor0 = purple
circleColor1 = blue
circleColor2 = yellow
circleRadius0 = 8
circleRadius1 = 8
circleRadius2 = 8
x0 = screen_width/2+400
y0 = screen_height/2+200

x1 = screen_width/2+350
y1 = screen_height/2+100

x2 = screen_width/2+450
y2 = screen_height/2-100

x3 = screen_width/2+400
y3 = screen_height/2-200

# bezier curve values
curveColor = red
curveWidth = 5
maxCurves = 15

# button values
buttonInactiveColour=(250, 50, 10)
buttonHoverColour=(150, 0, 0)
buttonPressedColour=(0, 200, 20)

# get the image from the diratory "pictures"
image = pygame.image.load("INFO1.gif")
