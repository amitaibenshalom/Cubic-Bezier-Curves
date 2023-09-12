import pygame
from pygame.locals import *
import serial
import struct
import time

# consts
gray = (100, 100, 100)
lightgray = (180, 180, 180)
verylightgray = (220, 220, 220)
red = (255, 0, 0)
pink = (255, 0, 255)
light_red = (255, 100, 100)
green = (0, 255, 0)
purple = (255, 0, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
orange = (255, 165, 0)
X, Y, Z = 0, 1, 2


# screen_width = 1000
# screen_height = 600
pygame.init()
infoObject = pygame.display.Info()
print(infoObject)
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screenColor = gray
cuttingAreaColor = verylightgray

borderLineHeight = 142
borderLine2Height = screen_height-142
tolerance = 3

delta0X = 30
delta0Y = 0
delta0Z = -50
MAX_LINES_PER_ROW = 8

# control points values
circleColor0 = purple
circleColor1 = blue
circleColor2 = yellow
circleRadius0 = 8
circleRadius1 = 8
circleRadius2 = 8

x0 = 800
y0 = 450
x1 = 850
y1 = 350
x2 = 750
y2 = 350
x3 = 800
y3 = 250

mm_per_pixel_x = 295/1366
mm_per_pixel_y = 165/768
pixel_per_cm_screen = 90/1.9

# bezier curve values
curveColor = red
selectedCurveColor = green
control_lines_color = lightgray
curveWidth = 6
maxCurves = 15

# contour values
contourColor = black
contourWidth = 8
contour0radius = 100
# contour0 = [(screen_width/2+contour0radius, screen_height/2)]

# button values
buttonInactiveColour=yellow
buttonHoverColour=red
buttonPressedColour=green
buttonOfflineColour=gray

button_height = int(1.6/16.5 * screen_height)

#sizes of buttons and images
buttonAddSize = (int(8.1/29.5 * screen_width),button_height)
buttonDeleteSize = (int(4.7/29.5 * screen_width), button_height)
buttonInfoSize = (button_height, button_height)
buttonPreviewSize = (int(8.9/29.5 * screen_width), button_height)
buttonPrintSize = (int(4.7/29.5 * screen_width), button_height)
buttonHeartSize = buttonInfoSize
buttonDropSize = buttonInfoSize
buttonCircleSize = buttonInfoSize

infoHebSize = (int(11.7/29.5 * screen_width), int(9/16.5 * screen_height))
infoEngSize = (int(11.7/29.5 * screen_width), int(9/16.5 * screen_height))
infoArabSize = (int(11.7/29.5 * screen_width), int(9/16.5 * screen_height))

#positions of the buttons
buttonAddPosition = (int(15.3/29.5 * screen_width), int(14.2/16.5 * screen_height))
buttonDeletePosition = (int(0.5/29.5 * screen_width), int(14.2/16.5 * screen_height))
buttonInfoPosition = (int(0.5/29.5 * screen_width), int(0.5/16.5 * screen_height))
buttonPreviewPosition = (int(5.8/29.5 * screen_width), int(14.2/16.5 * screen_height))
buttonPrintPosition = (int(24/29.5 * screen_width), int(14.2/16.5 * screen_height))
buttonHeartPosition = (int((0.5+buttonInfoSize[0]/pixel_per_cm_screen+0.5)/29.5 * screen_width), int(0.5/16.5 * screen_height))
buttonDropPosition = (int((0.5+buttonInfoSize[0]/pixel_per_cm_screen+0.5+buttonHeartSize[0]/pixel_per_cm_screen+0.5)/29.5 * screen_width), int(0.5/16.5 * screen_height))
buttonCirclePosition = (int((0.5+buttonInfoSize[0]/pixel_per_cm_screen+0.5+buttonHeartSize[0]/pixel_per_cm_screen+0.5+buttonDropSize[0]/pixel_per_cm_screen+0.5)/29.5 * screen_width), int(0.5/16.5 * screen_height))

# get the image from the diratory "pictures"
pic_buttonDelete = pygame.image.load("pictures/buttonDelete.jpg")
pic_buttonPressedDelete = pygame.image.load("pictures/buttonPressedDelete.jpg")
pic_buttonInfo = pygame.image.load("pictures/buttonInfo.jpg")
pic_buttonPressedInfo = pygame.image.load("pictures/buttonPressedInfo.jpg")
pic_buttonAdd = pygame.image.load("pictures/buttonAdd.jpg")
pic_buttonPressedAdd = pygame.image.load("pictures/buttonPressedAdd.jpg")
pic_buttonPreview = pygame.image.load("pictures/buttonPreview.jpg")
pic_buttonPressedPreview = pygame.image.load("pictures/buttonPressedPreview.jpg")
pic_buttonPrint = pygame.image.load("pictures/buttonPrint.jpg")
pic_buttonPressedPrint = pygame.image.load("pictures/buttonPressedPrint.jpg")
pic_buttonOffPrint = pygame.image.load("pictures/buttonOffPrint.jpg")
pic_bg0 = pygame.image.load("pictures/bg0.jpg")
pic_bg1 = pygame.image.load("pictures/bgWithButtons.jpg")
pic_infoHeb = pygame.image.load("pictures/infoHeb.jpg")
pic_infoEng = pygame.image.load("pictures/infoEng.jpg")
pic_infoArab = pygame.image.load("pictures/infoArab.jpg")
pic_buttonHeart = pygame.image.load("pictures/buttonHeart.jpg")
pic_buttonPressedHeart = pygame.image.load("pictures/buttonPressedHeart.jpg")
pic_buttonDrop = pygame.image.load("pictures/buttonDrop.jpg")
pic_buttonPressedDrop = pygame.image.load("pictures/buttonPressedDrop.jpg")
pic_buttonCircle = pygame.image.load("pictures/buttonCircle.jpg")
pic_buttonPressedCircle = pygame.image.load("pictures/buttonPressedCircle.jpg")

# resize the images
pic_buttonDelete = pygame.transform.scale(pic_buttonDelete, buttonDeleteSize)
pic_buttonPressedDelete = pygame.transform.scale(pic_buttonPressedDelete, buttonDeleteSize)
pic_buttonInfo = pygame.transform.scale(pic_buttonInfo, buttonInfoSize)
pic_buttonPressedInfo = pygame.transform.scale(pic_buttonPressedInfo, buttonInfoSize)
pic_buttonAdd = pygame.transform.scale(pic_buttonAdd, buttonAddSize)
pic_buttonPressedAdd = pygame.transform.scale(pic_buttonPressedAdd, buttonAddSize)
pic_buttonPreview = pygame.transform.scale(pic_buttonPreview, buttonPreviewSize)
pic_buttonPressedPreview = pygame.transform.scale(pic_buttonPressedPreview, buttonPreviewSize)
pic_buttonPrint = pygame.transform.scale(pic_buttonPrint, buttonPrintSize)
pic_buttonPressedPrint = pygame.transform.scale(pic_buttonPressedPrint, buttonPrintSize)
pic_buttonOffPrint = pygame.transform.scale(pic_buttonOffPrint, buttonPrintSize)
pic_bg0 = pygame.transform.scale(pic_bg0, (screen_width, screen_height))
pic_bg1 = pygame.transform.scale(pic_bg1, (screen_width, screen_height))
pic_infoHeb = pygame.transform.scale(pic_infoHeb, infoHebSize)
pic_infoEng = pygame.transform.scale(pic_infoEng, infoEngSize)
pic_infoArab = pygame.transform.scale(pic_infoArab, infoArabSize)
pic_buttonHeart = pygame.transform.scale(pic_buttonHeart, buttonHeartSize)
pic_buttonPressedHeart = pygame.transform.scale(pic_buttonPressedHeart, buttonHeartSize)
pic_buttonDrop = pygame.transform.scale(pic_buttonDrop, buttonDropSize)
pic_buttonPressedDrop = pygame.transform.scale(pic_buttonPressedDrop, buttonDropSize)
pic_buttonCircle = pygame.transform.scale(pic_buttonCircle, buttonCircleSize)
pic_buttonPressedCircle = pygame.transform.scale(pic_buttonPressedCircle, buttonCircleSize)

contour_heart = [[(screen_width/2, 600),(1145,345),(screen_width/2+120,80),(screen_width/2, 250)],[(screen_width/2,600),(225,345),(screen_width/2-120,80),(screen_width/2,250)]]
contour_square = [[[screen_width/2+230, 400], [screen_width/2+230, 170], [screen_width/2+230, 170], [screen_width/2, 170]],[[screen_width/2, 600], [screen_width/2+230, 600], [screen_width/2+230, 600], [screen_width/2+230, 400]],[[screen_width/2, 600], [screen_width/2-230, 600], [screen_width/2-230, 600], [screen_width/2-230, 400]],[[screen_width/2-230, 400], [screen_width/2-230, 170], [screen_width/2-230, 170], [screen_width/2, 170]]]
contour_drop = [[(screen_width/2,600),(900,600),(900,500),(900,450)],[(900,450),(850,250),(750,250),(screen_width/2,150)],[(screen_width/2,600),(550,600),(470,500),(470,450)],[(470,450),(500,250),(600,200),(screen_width/2,150)]]

MAX_TIME_WAITING_FOR_ARDUINO = 5 # seconds
MAX_DRAWING_TIME_FOR_ARDUINO = 20 # seconds
time_delay_arduino = 0.005 # seconds
starting_key = -2
next_curve_key = -3
end_key = -4

found_arduino = False
send_to_arduino = False
drawing_curve = False
curve_index = 0
waiting = [False,False] # two flags to indicate if we are waiting for the arduino to send us data: first is reading a curve, second is drawing one
last_time = [0,0] # to limit the time we wait for the arduino to send us data


