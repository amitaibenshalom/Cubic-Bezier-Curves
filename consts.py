import pygame
import os
import platform
from pygame.locals import *

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
cuttingAreaColor = white
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

# logging values
# get the current diractory the code sits in and create the log file there
currentDir = os.path.dirname(os.path.realpath(__file__))
LOG_FILE_PATH = os.path.join(currentDir, "log.txt")

# borderLineHeight = int(142 / const_height_screen * screen_height)
borderLineHeight = int(142 / const_height_screen * screen_height)
# borderLine2Height = int((const_height_screen - 142) / const_height_screen * screen_height)
borderLine2Height = screen_height-int(60/const_height_screen*screen_height)
borderLineX = int(130 / const_width_screen * screen_width)
# borderLine2X = int((const_width_screen - 330) / const_width_screen * screen_width)
borderLine2X = int((const_width_screen - 385) / const_width_screen * screen_width)
centerInsideBorders = (int((borderLineX + borderLine2X) / 2), int((borderLineHeight + borderLine2Height) / 2))
center = (int(screen_width / 2), int(screen_height / 2))

#cuttingAreaColor = white
cuttingAreaWidth = int((const_height_screen - 142) / const_height_screen * screen_height) - int(142 / const_height_screen * screen_height)
cuttingAreaHeight = cuttingAreaWidth
cuttingAreaPos = (centerInsideBorders[0] - cuttingAreaWidth / 2, centerInsideBorders[1] - cuttingAreaHeight / 2)
cuttingAreaSize = (cuttingAreaWidth, cuttingAreaHeight)

# red border values
redBorderWidth = int(10 / const_width_screen * screen_width)
redBorderPos = (borderLineX, borderLineHeight)
redBorderSize = (borderLine2X - borderLineX, borderLine2Height - borderLineHeight)
redBorderColor = red

drawingAreaPos = (borderLineX + redBorderWidth, borderLineHeight + redBorderWidth)
drawingAreaSize = (borderLine2X - borderLineX - 2* redBorderWidth, borderLine2Height - borderLineHeight - 2*redBorderWidth)
drawingAreaColor = white

delta0X = int(35 / const_width_screen * screen_width)
delta0Y = int(0 / const_height_screen * screen_height)
delta0Z = int(-50 / const_height_screen * screen_height)
delta1X = int(30 / const_width_screen * screen_width)
delta1Y = int(0 / const_height_screen * screen_height)
delta1Z = int(-50 / const_height_screen * screen_height)
MAX_LINES_PER_ROW = 7
MAX_LINES_PER_ROW_OUTSIDE_CONTOUR = 4
MAX_LINES_GENERATED_INSIDE_CONTOUR = 1

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

x0 = int(790 / const_width_screen * screen_width) + centerInsideBorders[0] - center[0]
y0 = int(470 / const_height_screen * screen_height) + centerInsideBorders[1] - center[1]
x1 = int(840 / const_width_screen * screen_width) + centerInsideBorders[0] - center[0]
y1 = int(370 / const_height_screen * screen_height) + centerInsideBorders[1] - center[1]
x2 = int(740 / const_width_screen * screen_width) + centerInsideBorders[0] - center[0]
y2 = int(370 / const_height_screen * screen_height) + centerInsideBorders[1] - center[1]
x3 = int(790 / const_width_screen * screen_width) + centerInsideBorders[0] - center[0]
y3 = int(270 / const_height_screen * screen_height) + centerInsideBorders[1] - center[1]

shiftX = int(250 / const_width_screen * screen_width)
shiftY = int(-70 / const_height_screen * screen_height)
x0_outside = x0 + shiftX
y0_outside = y0 + shiftY
x1_outside = x1 + shiftX
y1_outside = y1 + shiftY
x2_outside = x2 + shiftX
y2_outside = y2 + shiftY
x3_outside = x3 + shiftX
y3_outside = y3 + shiftY

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

button_height0 = 1.3
button_contour_height0 = 1.7
button_height = int(button_height0 / 16.5 * screen_height)
# sizes of buttons and images
buttonAddSize = (int(7.2 / 29.5 * screen_width), button_height)
buttonDeleteSize = (int(4.5 / 29.5 * screen_width), button_height)
buttonInfoSize = (int(button_contour_height0 / 16.5 * screen_height), int(button_contour_height0 / 16.5 * screen_height))
buttonPreviewSize = (int(7.2 / 29.5 * screen_width), button_height)
buttonPrintSize = (int(4.5 / 29.5 * screen_width), button_height)
buttonHeartSize = buttonInfoSize
buttonDropSize = buttonInfoSize
buttonSquareSize = buttonInfoSize

infoHebSize = (int(18.5 / 29.5 * screen_width), int(12.2 / 16.5 * screen_height))
# infoEngSize = infoHebSize
# infoArabSize = infoHebSize
textAboveSize = (int(14 / 29.5 * screen_width), int(3 / 16.5 * screen_height))
textFrameSize = buttonHeartSize

button_contour_x = int(0.5 / 29.5 * screen_width)
button_operation_x = int(29 / 29.5 * screen_width)
button_operation_x0 = 5
# positions of the buttons
buttonAddPosition = (button_operation_x - buttonAddSize[0], int(button_operation_x0 / 16.5 * screen_height))
buttonPreviewPosition = (button_operation_x - buttonPreviewSize[0], int((button_operation_x0 + button_height0 + 1) / 16.5 * screen_height))
buttonDeletePosition = (button_operation_x - 1.3*buttonDeleteSize[0], int((button_operation_x0 + 2 * (button_height0 + 1)) / 16.5 * screen_height))
buttonInfoPosition = (button_contour_x, borderLineHeight+int(0.5/16.5 * screen_height))
buttonPrintPosition = (button_operation_x - 1.3*buttonPrintSize[0], int((button_operation_x0 + 3 * (button_height0 + 1)) / 16.5 * screen_height))
buttonHeartPosition = (button_contour_x, int((6 + button_contour_height0 + 0.5) / 16.5 * screen_height))
buttonDropPosition = (button_contour_x, int((6 + 2 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
buttonSquarePosition = (button_contour_x, int((6 + 3 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
textAbovePosition = (centerInsideBorders[0]-textAboveSize[0]/2, borderLineHeight-textAboveSize[1])
textFramePosition = (buttonHeartPosition[0], buttonHeartPosition[1]-textFrameSize[0])

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
pic_infoHeb = pygame.image.load("pictures/infoHeb2.jpg")
# pic_infoEng = pygame.image.load("pictures/infoEng.jpg")
# pic_infoArab = pygame.image.load("pictures/infoArab.jpg")
pic_buttonHeart = pygame.image.load("pictures/buttonHeart.jpg")
pic_buttonPressedHeart = pygame.image.load("pictures/buttonPressedHeart.jpg")
pic_buttonDrop = pygame.image.load("pictures/buttonDrop.jpg")
pic_buttonPressedDrop = pygame.image.load("pictures/buttonPressedDrop.jpg")
pic_buttonSquare = pygame.image.load("pictures/buttonSquare.jpg")
pic_buttonPressedSquare = pygame.image.load("pictures/buttonPressedSquare.jpg")
pic_doubleArrow = pygame.image.load("pictures/double_arrow.png")
pic_textAbove = pygame.image.load("pictures/textAbove2.jpg")
pic_textFrame = pygame.image.load("pictures/frame.jpg")

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
# pic_infoEng = pygame.transform.scale(pic_infoEng, infoEngSize)
# pic_infoArab = pygame.transform.scale(pic_infoArab, infoArabSize)
pic_buttonHeart = pygame.transform.scale(pic_buttonHeart, buttonHeartSize)
pic_buttonPressedHeart = pygame.transform.scale(pic_buttonPressedHeart, buttonHeartSize)
pic_buttonDrop = pygame.transform.scale(pic_buttonDrop, buttonDropSize)
pic_buttonPressedDrop = pygame.transform.scale(pic_buttonPressedDrop, buttonDropSize)
pic_buttonSquare = pygame.transform.scale(pic_buttonSquare, buttonSquareSize)
pic_buttonPressedSquare = pygame.transform.scale(pic_buttonPressedSquare, buttonSquareSize)
pic_doubleArrow = pygame.transform.scale(pic_doubleArrow, doubleArrowSize)
pic_textAbove = pygame.transform.scale(pic_textAbove, textAboveSize)
pic_textFrame = pygame.transform.scale(pic_textFrame, textFrameSize)

x_length = 16
x_height = 15 # height from the top of the heart downwards
contour_heart = [[(screen_width / 2 - int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 - int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2 + int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 + int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2, int(600 / const_height_screen * screen_height)),
                  (int(1145 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)), (
                  screen_width / 2 + (int(120 / const_width_screen * screen_width)),
                  int(80 / const_height_screen * screen_height)),
                  (screen_width / 2, int(250 / const_height_screen * screen_height))],
                 [(screen_width / 2, int(250 / const_height_screen * screen_height)), (
                 screen_width / 2 - int(120 / const_width_screen * screen_width),
                 int(80 / const_height_screen * screen_height)),
                  (int(225 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)),
                  (screen_width / 2, int(600 / const_height_screen * screen_height))]]
square_side = [int(193 / const_width_screen * screen_width),int(193 / const_width_screen * screen_width)]
x_height = int(60/const_width_screen * screen_width)
x_length = int(24/const_width_screen * screen_width)
contour_square = [[[screen_width / 2 - square_side[0] + x_height - x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height + x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height - x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height + x_length, screen_height/2-square_side[1] + x_height]],
                [[screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height - x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height + x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height - x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height + x_length]],
                [[screen_width / 2, screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2]], [
                      [screen_width / 2 + square_side[0],
                       screen_height / 2],
                      [screen_width / 2 + square_side[0],
                       screen_height / 2 - square_side[1]],
                      [screen_width / 2 + square_side[0],
                       screen_height / 2 - square_side[1]],
                      [screen_width / 2, screen_height / 2 - square_side[1]]],
                  [[screen_width / 2, screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height/2]], [
                      [screen_width / 2 - square_side[0],
                       screen_height / 2],
                      [screen_width / 2 - square_side[0],
                       screen_height / 2 + square_side[1]],
                      [screen_width / 2 - square_side[0],
                       screen_height / 2 + square_side[1]],
                      [screen_width / 2, screen_height / 2 + square_side[1]]]]
x_height = 35
x_length = 16
contour_drop = [[(screen_width / 2 - int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 - int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2 + int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 + int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width/2, int(610 / const_height_screen * screen_height)),
                 (screen_width/2 + int(62 / const_width_screen * screen_width), int(610 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(550 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height))],
                [(screen_width/2 + int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(263 / const_height_screen * screen_height)),
                 (screen_width/2 + int(43 / const_width_screen * screen_width), int(170 / const_height_screen * screen_height)),
                 (screen_width/2, int(145 / const_height_screen * screen_height))],
                [(screen_width/2, int(145 / const_height_screen * screen_height)),
                 (screen_width/2 - int(43 / const_width_screen * screen_width), int(170 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(263 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height))],
                [(screen_width/2 - int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(550 / const_height_screen * screen_height)),
                 (screen_width/2 - int(62 / const_width_screen * screen_width), int(610 / const_height_screen * screen_height)),
                 (screen_width/2, int(610 / const_height_screen * screen_height))]]

contours = [contour_heart, contour_square, contour_drop]

# move the conour heart to the center inside the borders
for k in range(len(contours)):
    for i in range(len(contours[k])):
        for j in range(len(contours[k][i])):
            contours[k][i][j] = (
            contours[k][i][j][0] + int(centerInsideBorders[0] - center[0]),
            contours[k][i][j][1] + int(centerInsideBorders[1] - center[1]))


sample0 = [[(int(756/const_width_screen*screen_width),int(359/const_height_screen*screen_height)),
                (int(770/const_width_screen*screen_width),int(481/const_height_screen*screen_height)),
                (int(667/const_width_screen*screen_width),int(537/const_height_screen*screen_height)),
                (int(659/const_width_screen*screen_width),int(384/const_height_screen*screen_height))],
            [(int(671/const_width_screen*screen_width),int(437/const_height_screen*screen_height)),
                (int(705/const_width_screen*screen_width),int(413/const_height_screen*screen_height)),
                (int(722/const_width_screen*screen_width),int(445/const_height_screen*screen_height)),
                (int(714/const_width_screen*screen_width),int(369/const_height_screen*screen_height))],
            [(int(595/const_width_screen*screen_width),int(490/const_height_screen*screen_height)),
                (int(745/const_width_screen*screen_width),int(283/const_height_screen*screen_height)),
                (int(502/const_width_screen*screen_width),int(478/const_height_screen*screen_height)),
                (int(612/const_width_screen*screen_width),int(317/const_height_screen*screen_height))],
            [(int(559/const_width_screen*screen_width),int(489/const_height_screen*screen_height)),
                (int(559/const_width_screen*screen_width),int(402/const_height_screen*screen_height)),
                (int(567/const_width_screen*screen_width),int(368/const_height_screen*screen_height)),
                (int(550/const_width_screen*screen_width),int(369/const_height_screen*screen_height))],
            [(int(437/const_width_screen*screen_width),int(366/const_height_screen*screen_height)),
                (int(511/const_width_screen*screen_width),int(373/const_height_screen*screen_height)),
                (int(529/const_width_screen*screen_width),int(351/const_height_screen*screen_height)),
                (int(520/const_width_screen*screen_width),int(491/const_height_screen*screen_height))],
            [(int(519/const_width_screen*screen_width),int(491/const_height_screen*screen_height)),
                (int(438/const_width_screen*screen_width),int(493/const_height_screen*screen_height)),
                (int(437/const_width_screen*screen_width),int(501/const_height_screen*screen_height)),
                (int(448/const_width_screen*screen_width),int(378/const_height_screen*screen_height))],
            [(int(401/const_width_screen*screen_width),int(451/const_height_screen*screen_height)),
                (int(402/const_width_screen*screen_width),int(378/const_height_screen*screen_height)),
                (int(399/const_width_screen*screen_width),int(400/const_height_screen*screen_height)),
                (int(405/const_width_screen*screen_width),int(341/const_height_screen*screen_height))],
            [(int(396/const_width_screen*screen_width),int(479/const_height_screen*screen_height)),
                (int(416/const_width_screen*screen_width),int(491/const_height_screen*screen_height)),
                (int(409/const_width_screen*screen_width),int(447/const_height_screen*screen_height)),
                (int(396/const_width_screen*screen_width),int(478/const_height_screen*screen_height))]]

sample1 = [[[int(615/const_width_screen*screen_width), int(419/const_height_screen*screen_height)],
            [int(615/const_width_screen*screen_width), int(371/const_height_screen*screen_height)],
            [int(615/const_width_screen*screen_width), int(391/const_height_screen*screen_height)],
            [int(615/const_width_screen*screen_width), int(352/const_height_screen*screen_height)]],
            [[int(495/const_width_screen*screen_width), int(416/const_height_screen*screen_height)],
            [int(494/const_width_screen*screen_width), int(382/const_height_screen*screen_height)],
            [int(497/const_width_screen*screen_width), int(379/const_height_screen*screen_height)],
            [int(496/const_width_screen*screen_width), int(353/const_height_screen*screen_height)]],
            [[int(416/const_width_screen*screen_width), int(447/const_height_screen*screen_height)],
            [int(463/const_width_screen*screen_width), int(554/const_height_screen*screen_height)],
            [int(633/const_width_screen*screen_width), int(554/const_height_screen*screen_height)],
            [int(690/const_width_screen*screen_width), int(449/const_height_screen*screen_height)]],
            [[int(510/const_width_screen*screen_width), int(510/const_height_screen*screen_height)],
            [int(524/const_width_screen*screen_width), int(487/const_height_screen*screen_height)],
            [int(586/const_width_screen*screen_width), int(484/const_height_screen*screen_height)],
            [int(594/const_width_screen*screen_width), int(513/const_height_screen*screen_height)]],
            [[int(414/const_width_screen*screen_width), int(439/const_height_screen*screen_height)],
            [int(461/const_width_screen*screen_width), int(472/const_height_screen*screen_height)],
            [int(628/const_width_screen*screen_width), int(483/const_height_screen*screen_height)],
            [int(691/const_width_screen*screen_width), int(441/const_height_screen*screen_height)]],
            [[int(445/const_width_screen*screen_width), int(334/const_height_screen*screen_height)],
            [int(457/const_width_screen*screen_width), int(307/const_height_screen*screen_height)],
            [int(484/const_width_screen*screen_width), int(296/const_height_screen*screen_height)],
            [int(518/const_width_screen*screen_width), int(301/const_height_screen*screen_height)]],
            [[int(666/const_width_screen*screen_width), int(333/const_height_screen*screen_height)],
            [int(649/const_width_screen*screen_width), int(313/const_height_screen*screen_height)],
            [int(646/const_width_screen*screen_width), int(303/const_height_screen*screen_height)],
            [int(607/const_width_screen*screen_width), int(300/const_height_screen*screen_height)]]]

# sample 2 before scaling
sample2 = [[[int(689/const_width_screen*screen_width), int(307/const_height_screen*screen_height)],
            [int(705/const_width_screen*screen_width), int(533/const_height_screen*screen_height)],
            [int(644/const_width_screen*screen_width), int(174/const_height_screen*screen_height)],
            [int(654/const_width_screen*screen_width), int(377/const_height_screen*screen_height)]],
            [[int(629/const_width_screen*screen_width), int(380/const_height_screen*screen_height)],
             [int(632/const_width_screen*screen_width), int(340/const_height_screen*screen_height)],
             [int(626/const_width_screen*screen_width), int(347/const_height_screen*screen_height)],
             [int(629/const_width_screen*screen_width), int(314/const_height_screen*screen_height)]],
            [[int(596/const_width_screen*screen_width), int(379/const_height_screen*screen_height)],
             [int(645/const_width_screen*screen_width), int(354/const_height_screen*screen_height)],
             [int(583/const_width_screen*screen_width), int(374/const_height_screen*screen_height)],
             [int(597/const_width_screen*screen_width), int(315/const_height_screen*screen_height)]],
            [[int(569/const_width_screen*screen_width), int(355/const_height_screen*screen_height)],
             [int(571/const_width_screen*screen_width), int(334/const_height_screen*screen_height)],
             [int(569/const_width_screen*screen_width), int(343/const_height_screen*screen_height)],
             [int(569/const_width_screen*screen_width), int(324/const_height_screen*screen_height)]],
            [[int(543/const_width_screen*screen_width), int(378/const_height_screen*screen_height)],
             [int(497/const_width_screen*screen_width), int(379/const_height_screen*screen_height)],
             [int(494/const_width_screen*screen_width), int(330/const_height_screen*screen_height)],
             [int(543/const_width_screen*screen_width), int(328/const_height_screen*screen_height)]],
            [[int(499/const_width_screen*screen_width), int(391/const_height_screen*screen_height)],
             [int(499/const_width_screen*screen_width), int(340/const_height_screen*screen_height)],
             [int(496/const_width_screen*screen_width), int(371/const_height_screen*screen_height)],
             [int(498/const_width_screen*screen_width), int(319/const_height_screen*screen_height)]],
            [[int(471/const_width_screen*screen_width), int(391/const_height_screen*screen_height)],
             [int(471/const_width_screen*screen_width), int(332/const_height_screen*screen_height)],
             [int(466/const_width_screen*screen_width), int(372/const_height_screen*screen_height)],
             [int(470/const_width_screen*screen_width), int(316/const_height_screen*screen_height)]],
            [[int(445/const_width_screen*screen_width), int(423/const_height_screen*screen_height)],
             [int(443/const_width_screen*screen_width), int(323/const_height_screen*screen_height)],
             [int(442/const_width_screen*screen_width), int(396/const_height_screen*screen_height)],
             [int(443/const_width_screen*screen_width), int(316/const_height_screen*screen_height)]],
            [[int(687/const_width_screen*screen_width), int(501/const_height_screen*screen_height)],
             [int(700/const_width_screen*screen_width), int(425/const_height_screen*screen_height)],
             [int(674/const_width_screen*screen_width), int(437/const_height_screen*screen_height)],
             [int(642/const_width_screen*screen_width), int(443/const_height_screen*screen_height)]],
            [[int(652/const_width_screen*screen_width), int(499/const_height_screen*screen_height)],
             [int(655/const_width_screen*screen_width), int(484/const_height_screen*screen_height)],
             [int(653/const_width_screen*screen_width), int(484/const_height_screen*screen_height)],
             [int(655/const_width_screen*screen_width), int(463/const_height_screen*screen_height)]],
            [[int(615/const_width_screen*screen_width), int(447/const_height_screen*screen_height)],
             [int(637/const_width_screen*screen_width), int(618/const_height_screen*screen_height)],
             [int(573/const_width_screen*screen_width), int(340/const_height_screen*screen_height)],
             [int(591/const_width_screen*screen_width), int(502/const_height_screen*screen_height)]],
            [[int(553/const_width_screen*screen_width), int(487/const_height_screen*screen_height)],
             [int(576/const_width_screen*screen_width), int(482/const_height_screen*screen_height)],
             [int(573/const_width_screen*screen_width), int(419/const_height_screen*screen_height)],
             [int(531/const_width_screen*screen_width), int(460/const_height_screen*screen_height)]],
            [[int(552/const_width_screen*screen_width), int(514/const_height_screen*screen_height)],
             [int(583/const_width_screen*screen_width), int(488/const_height_screen*screen_height)],
             [int(537/const_width_screen*screen_width), int(440/const_height_screen*screen_height)],
             [int(548/const_width_screen*screen_width), int(484/const_height_screen*screen_height)]],
            [[int(502/const_width_screen*screen_width), int(448/const_height_screen*screen_height)],
             [int(465/const_width_screen*screen_width), int(479/const_height_screen*screen_height)],
             [int(464/const_width_screen*screen_width), int(542/const_height_screen*screen_height)],
             [int(512/const_width_screen*screen_width), int(507/const_height_screen*screen_height)]],
            [[int(514/const_width_screen*screen_width), int(502/const_height_screen*screen_height)],
             [int(517/const_width_screen*screen_width), int(480/const_height_screen*screen_height)],
             [int(497/const_width_screen*screen_width), int(467/const_height_screen*screen_height)],
             [int(472/const_width_screen*screen_width), int(445/const_height_screen*screen_height)]]]


samples = [sample0, sample1, sample2]

buttons_enabled = True
IS_MOVING_ALL_CURVE = True
IDLE_TIME = 100 # seconds
IDLE_TIME_DRAW = 120 # seconds
enable_idle_drawing = False
idle_mode = False
MAX_RUNS = 60

SHOW_RED_BORDER = True

# arduino
MAX_TIME_WAITING_FOR_ARDUINO = 5  # seconds
MAX_DRAWING_TIME_FOR_ARDUINO = 150  # seconds
time_delay_arduino = 0.005  # seconds

LASER_POWER = 255  # (0 <= x <= 255)
CONTOUR_POWER = 255  # (0 <= x <= 255)
LASER_OFF_RATE = 6
LASER_ON_RATE = 6
CONTOUR_RATE = 50 # for green/yellow paper
MAX_DC_MOTOR_TIME = 1.5  # seconds

mm_per_pulse = [2*80.0/800, 2*80.0/800]  # mm per pulse for each motor
board_size = [83.0, 83.0]  # size of the board in mm
screen_scale = [board_size[0]/cuttingAreaWidth, board_size[1]/cuttingAreaHeight]  # scale from the screen to the board on arduino in mm per pixel
pulse_per_pixel = [screen_scale[0]/mm_per_pulse[0], screen_scale[1]/mm_per_pulse[1]]  # pulse per pixel for each motor

starting_key = -2
next_curve_key = -3
end_key = -4

found_arduino = False
send_to_arduino = False
drawing_curve = False
curve_index = 0
waiting = [False,False]  # two flags to indicate if we are waiting for the arduino to send us data: first is reading a curve, second is drawing one
last_time = [0, 0]  # to limit the time we wait for the arduino to send us data
