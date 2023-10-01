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
colorOutSideBorder = (226, 233, 241)
bgColor = white

# screen_width = 1000
# screen_height = 600
const_width_screen = 1366  # DO NOT CHANGE - for calculations of proportional sizes
const_height_screen = 768  # DO NOT CHANGE - for calculations of proportional sizes

pygame.init()
infoObject = pygame.display.Info()
print(infoObject)
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screenColor = gray
# cuttingAreaColor = verylightgray
cuttingAreaColor = white

# borderLineHeight = int(142 / const_height_screen * screen_height)
borderLineHeight = int(142 / const_height_screen * screen_height)
# borderLine2Height = int((const_height_screen - 142) / const_height_screen * screen_height)
borderLine2Height = screen_height-int(60/const_height_screen*screen_height)
borderLineX = int(130 / const_width_screen * screen_width)
borderLine2X = int((const_width_screen - 330) / const_width_screen * screen_width)
centerInsideBorders = (int((borderLineX + borderLine2X) / 2), int((borderLineHeight + borderLine2Height) / 2))
center = (int(screen_width / 2), int(screen_height / 2))

cuttingAreaWidth = int((const_height_screen - 142) / const_height_screen * screen_height) - int(142 / const_height_screen * screen_height)
cuttingAreaHeight = cuttingAreaWidth
cuttingAreaPos = (centerInsideBorders[0] - cuttingAreaWidth / 2, centerInsideBorders[1] - cuttingAreaHeight / 2)
cuttingAreaSize = (cuttingAreaWidth, cuttingAreaHeight)

delta0X = int(40 / const_width_screen * screen_width)
delta0Y = int(0 / const_height_screen * screen_height)
delta0Z = int(-50 / const_height_screen * screen_height)
MAX_LINES_PER_ROW = 7

toleranceTouch = 20

# control points values
circleColor0 = purple
circleColor1 = blue
circleColor2 = yellow
circleRadius0 = int(8 / const_width_screen * screen_width)
circleRadius1 = int(8 / const_width_screen * screen_width)
circleRadius2 = int(5 / const_width_screen * screen_width)
circleRadiusClicked = int(10 / const_width_screen * screen_width)
doubleArrowSize = (int(40 / const_width_screen * screen_width), int(40 / const_height_screen * screen_height))

x0 = int((830 + centerInsideBorders[0] - center[0]) / const_width_screen * screen_width)
y0 = int((450 + centerInsideBorders[1] - center[1]) / const_height_screen * screen_height)
x1 = int((880 + centerInsideBorders[0] - center[0]) / const_width_screen * screen_width)
y1 = int((350 + centerInsideBorders[1] - center[1]) / const_height_screen * screen_height)
x2 = int((780 + centerInsideBorders[0] - center[0]) / const_width_screen * screen_width)
y2 = int((350 + centerInsideBorders[1] - center[1]) / const_height_screen * screen_height)
x3 = int((830 + centerInsideBorders[0] - center[0]) / const_width_screen * screen_width)
y3 = int((250 + centerInsideBorders[1] - center[1]) / const_height_screen * screen_height)

# mm_per_pixel_x = 295/1366
# mm_per_pixel_y = 165/768
pixel_per_cm_screen = 90 / 1.9

# bezier curve values
curveColor = red
selectedCurveColor = green
control_lines_color = lightgray
curveWidth = int(6 / const_width_screen * screen_width)
controlLineWidth = int(3 / const_width_screen * screen_width)
maxCurves = 15

# contour values
contourColor = black
contourWidth = int(8 / const_width_screen * screen_width)
# contour0radius = 100

'''
# dialog box values
dialogBoxColor = lightgray
dialogBoxWidth = 400
dialogBoxHeight = 200
dialogBoxX = screen_width/2 - dialogBoxWidth/2
dialogBoxY = screen_height/2 - dialogBoxHeight/2
dialogBoxTextX = dialogBoxX + 20
dialogBoxTextY = dialogBoxY + 20
dialogBoxTextWidth = dialogBoxWidth - 40
dialogBoxTextHeight = dialogBoxHeight - 40
dialogBoxTextSize = 30
dialogBoxTextColour = black
dialogBoxButtonWidth = 100
dialogBoxButtonHeight = 50
dialogBoxButtonX = dialogBoxX + dialogBoxWidth/2 - dialogBoxButtonWidth/2
dialogBoxButtonY = dialogBoxY + dialogBoxHeight - dialogBoxButtonHeight - 20
dialogBoxButtonColour = gray
dialogBoxButtonHoverColour = lightgray
dialogBoxButtonPressedColour = verylightgray
dialogBoxButtonInactiveColour = gray
dialogBoxButtonBorderWidth = 5
dialogBoxButtonBorderColour = black
dialogBoxButtonBorderHoverColour = black
dialogBoxButtonBorderPressedColour = black
dialogBoxButtonBorderInactiveColour = black
'''

# button values
buttonInactiveColour = yellow
buttonHoverColour = red
buttonPressedColour = green
buttonOfflineColour = gray

# button_height0 = 1.6
# button_height = int(button_height0/16.5 * screen_height)
# # sizes of buttons and images
# buttonAddSize = (int(8.1/29.5 * screen_width),button_height)
# buttonDeleteSize = (int(4.7/29.5 * screen_width), button_height)
# buttonInfoSize = (button_height, button_height)
# buttonPreviewSize = (int(8.9/29.5 * screen_width), button_height)
# buttonPrintSize = (int(4.7/29.5 * screen_width), button_height)
# buttonHeartSize = buttonInfoSize
# buttonDropSize = buttonInfoSize
# buttonCircleSize = buttonInfoSize
button_height0 = 1.2
button_contour_height0 = 1.8
button_height = int(button_height0 / 16.5 * screen_height)
# sizes of buttons and images
buttonAddSize = (int(6 / 29.5 * screen_width), button_height)
buttonDeleteSize = (int(6 / 29.5 * screen_width), button_height)
buttonInfoSize = (int(button_contour_height0 / 16.5 * screen_height), int(button_contour_height0 / 16.5 * screen_height))
buttonPreviewSize = (int(6 / 29.5 * screen_width), button_height)
buttonPrintSize = (int(6 / 29.5 * screen_width), button_height)
buttonHeartSize = buttonInfoSize
buttonDropSize = buttonInfoSize
buttonCircleSize = buttonInfoSize

# infoHebSize = (int(11.7/29.5 * screen_width), int(9/16.5 * screen_height))
infoHebSize = (int(15 / 29.5 * screen_width), int(11 / 16.5 * screen_height))
infoEngSize = infoHebSize
infoArabSize = infoHebSize
textAboveSize = (int(10 / 29.5 * screen_width), int(2.5 / 16.5 * screen_height))

button_contour_x = int(0.5 / 29.5 * screen_width)
button_operation_x = int(29 / 29.5 * screen_width)

# positions of the buttons
buttonAddPosition = (button_operation_x - buttonAddSize[0], int(4 / 16.5 * screen_height))
buttonDeletePosition = (button_operation_x - buttonDeleteSize[0], int((4 + button_height0 + 1) / 16.5 * screen_height))
buttonInfoPosition = (button_contour_x, borderLineHeight)
buttonPreviewPosition = (button_operation_x - buttonPreviewSize[0], int((4 + 2 * (button_height0 + 1)) / 16.5 * screen_height))
buttonPrintPosition = (button_operation_x - buttonPrintSize[0], int((4 + 3 * (button_height0 + 1)) / 16.5 * screen_height))
buttonHeartPosition = (button_contour_x, int((4 + button_contour_height0 + 0.5) / 16.5 * screen_height))
buttonDropPosition = (button_contour_x, int((4 + 2 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
buttonCirclePosition = (button_contour_x, int((4 + 3 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
textAbovePosition = (centerInsideBorders[0]-textAboveSize[0]/2, borderLineHeight-textAboveSize[1])

# get the image from the directory "pictures"
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
pic_bg0 = pygame.image.load("pictures/vertical_bg_0.jpg")
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
pic_doubleArrow = pygame.image.load("pictures/double_arrow.png")
pic_textAbove = pygame.image.load("pictures/text_above_blue.jpg")

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
pic_doubleArrow = pygame.transform.scale(pic_doubleArrow, doubleArrowSize)
pic_textAbove = pygame.transform.scale(pic_textAbove, textAboveSize)

# contour_heart = [[(screen_width/2, 600),(1145,345),(screen_width/2+120,80),(screen_width/2, 250)] , [(screen_width/2,250),(screen_width/2-120,80),(225,345),(screen_width/2,600)]]
# contour_square = [[[screen_width/2, 600], [screen_width/2+230, 600], [screen_width/2+230, 600], [screen_width/2+230, 400]] , [[screen_width/2+230, 400], [screen_width/2+230, 170], [screen_width/2+230, 170], [screen_width/2, 170]], [[screen_width/2, 170], [screen_width/2-230, 170], [screen_width/2-230, 170], [screen_width/2-230, 400]], [[screen_width/2-230, 400], [screen_width/2-230, 600], [screen_width/2-230, 600], [screen_width/2, 600]]]
# contour_drop = [[(screen_width/2,600),(900,600),(900,500),(900,450)],[(900,450),(850,250),(750,250),(screen_width/2,150)] , [(screen_width/2,600),(550,600),(470,500),(470,450)],[(470,450),(500,250),(600,200),(screen_width/2,150)]]

contour_heart = [[(screen_width / 2, int(600 / const_height_screen * screen_height)),
                  (int(1145 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)), (
                  screen_width / 2 + (int(120 / const_width_screen * screen_width)),
                  int(80 / const_height_screen * screen_height)),
                  (screen_width / 2, int(250 / const_height_screen * screen_height))],
                 [(screen_width / 2, int(250 / const_height_screen * screen_height)), (
                 screen_width / 2 - int(120 / const_width_screen * screen_width),
                 int(80 / const_height_screen * screen_height)),
                  (int(225 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)),
                  (screen_width / 2, int(600 / const_height_screen * screen_height))]]
contour_square = [[[screen_width / 2, int(600 / const_height_screen * screen_height)],
                   [screen_width / 2 + int(230 / const_width_screen * screen_width),
                    int(600 / const_height_screen * screen_height)],
                   [screen_width / 2 + int(230 / const_width_screen * screen_width),
                    int(600 / const_height_screen * screen_height)],
                   [screen_width / 2 + int(230 / const_width_screen * screen_width),
                    int(400 / const_height_screen * screen_height)]], [
                      [screen_width / 2 + int(230 / const_width_screen * screen_width),
                       int(400 / const_height_screen * screen_height)],
                      [screen_width / 2 + int(230 / const_width_screen * screen_width),
                       int(170 / const_height_screen * screen_height)],
                      [screen_width / 2 + int(230 / const_width_screen * screen_width),
                       int(170 / const_height_screen * screen_height)],
                      [screen_width / 2, int(170 / const_height_screen * screen_height)]],
                  [[screen_width / 2, int(170 / const_height_screen * screen_height)],
                   [screen_width / 2 - int(230 / const_width_screen * screen_width),
                    int(170 / const_height_screen * screen_height)],
                   [screen_width / 2 - int(230 / const_width_screen * screen_width),
                    int(170 / const_height_screen * screen_height)],
                   [screen_width / 2 - int(230 / const_width_screen * screen_width),
                    int(400 / const_height_screen * screen_height)]], [
                      [screen_width / 2 - int(230 / const_width_screen * screen_width),
                       int(400 / const_height_screen * screen_height)],
                      [screen_width / 2 - int(230 / const_width_screen * screen_width),
                       int(600 / const_height_screen * screen_height)],
                      [screen_width / 2 - int(230 / const_width_screen * screen_width),
                       int(600 / const_height_screen * screen_height)],
                      [screen_width / 2, int(600 / const_height_screen * screen_height)]]]
contour_drop = [[(screen_width / 2, int(600 / const_height_screen * screen_height)),
                 (int(900 / const_width_screen * screen_width), int(600 / const_height_screen * screen_height)),
                 (int(900 / const_width_screen * screen_width), int(500 / const_height_screen * screen_height)),
                 (int(900 / const_width_screen * screen_width), int(450 / const_height_screen * screen_height))],
                [(int(900 / const_width_screen * screen_width), int(450 / const_height_screen * screen_height)),
                 (int(850 / const_width_screen * screen_width), int(250 / const_height_screen * screen_height)),
                 (int(750 / const_width_screen * screen_width), int(250 / const_height_screen * screen_height)),
                 (screen_width / 2, int(150 / const_height_screen * screen_height))],
                [(screen_width / 2, int(600 / const_height_screen * screen_height)),
                 (int(550 / const_width_screen * screen_width), int(600 / const_height_screen * screen_height)),
                 (int(470 / const_width_screen * screen_width), int(500 / const_height_screen * screen_height)),
                 (int(470 / const_width_screen * screen_width), int(450 / const_height_screen * screen_height))],
                [(int(470 / const_width_screen * screen_width), int(450 / const_height_screen * screen_height)),
                 (int(500 / const_width_screen * screen_width), int(250 / const_height_screen * screen_height)),
                 (int(600 / const_width_screen * screen_width), int(200 / const_height_screen * screen_height)),
                 (screen_width / 2, int(150 / const_height_screen * screen_height))]]
contours = [contour_heart, contour_square, contour_drop]
# move the conour heart to the center inside the borders
for k in range(len(contours)):
    for i in range(len(contours[k])):
        for j in range(len(contours[k][i])):
            contours[k][i][j] = (
            contours[k][i][j][0] + int((centerInsideBorders[0] - center[0]) / const_width_screen * screen_width),
            contours[k][i][j][1] + int((centerInsideBorders[1] - center[1]) / const_height_screen * screen_height))

buttons_enabled = True
IS_MOVING_ALL_CURVE = True
IDLE_TIME = 60

# arduino
MAX_TIME_WAITING_FOR_ARDUINO = 5  # seconds
MAX_DRAWING_TIME_FOR_ARDUINO = 150  # seconds
time_delay_arduino = 0.005  # seconds

LASER_POWER = 255  # (0 <= x <= 255)
CONTOUR_POWER = 255  # (0 <= x <= 255)
LASER_OFF_RATE = 6
LASER_ON_RATE = 90
CONTOUR_RATE = 100

starting_key = -2
next_curve_key = -3
end_key = -4

found_arduino = False
send_to_arduino = False
drawing_curve = False
curve_index = 0
waiting = [False,
           False]  # two flags to indicate if we are waiting for the arduino to send us data: first is reading a curve, second is drawing one
last_time = [0, 0]  # to limit the time we wait for the arduino to send us data
