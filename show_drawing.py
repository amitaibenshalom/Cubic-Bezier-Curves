"""
This code will show the drawing made by the user from the log files.
 COPY ALL OF THE BEZIER VERTICIES INTO THE LIST 'drawing' AND RUN.

FOR EXAMPLE:
drawing = [[[1039, 534], [1062, 841], [942, 335], [962, 636]],[[915, 541], [704, 694], [1044, 696], [839, 542]],[[779, 618], [779, 574], [780, 591], [780, 548]],[[718, 614], [718, 570], [719, 587], [719, 544]],[[654, 705], [654, 586], [654, 653], [654, 542]]]

and run the code.
"""
import os
from datetime import datetime

import pygame
import math

# change this to the drawing you want to show (copy from the log file as is)
drawing = \
[[[1071, 567], [981, 570], [980, 476], [1075, 473]],[[993, 577], [993, 515], [993, 541], [993, 459]],[[951, 473], [974, 780], [858, 273], [874, 575]],[[824, 544], [824, 500], [825, 517], [825, 474]],[[758, 564], [774, 498], [746, 446], [678, 467]],[[952, 739], [986, 651], [914, 609], [872, 653]],[[888, 737], [911, 692], [935, 693], [958, 737]],[[835, 807], [835, 688], [835, 755], [835, 644]],[[819, 755], [784, 810], [690, 758], [736, 683]],[[738, 678], [770, 628], [828, 697], [736, 749]],[[656, 684], [742, 696], [627, 544], [722, 548]],[[659, 686], [628, 686], [656, 635], [686, 672]],[[613, 641], [613, 576], [613, 605], [613, 530]],[[497, 587], [497, 324], [690, 614], [508, 575]]]
contour_index = 0   # 0 - heart, 1 - square, 2 - drop

screen_width, screen_height = 720, 480

curveColor = (255, 0, 0)
contourColor = (0, 0, 0)
curveWidth = 5
background = (255, 255, 255)

curves = []
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 1920, 1080  # do not change this - for proportional scaling
const_width_screen = 1366  # DO NOT CHANGE - for calculations of proportional sizes
const_height_screen = 768  # DO NOT CHANGE - for calculations of proportional sizes
borderLineHeight = int(142 / const_height_screen * ORIGINAL_HEIGHT)
borderLine2Height = ORIGINAL_HEIGHT-int(60/const_height_screen*ORIGINAL_HEIGHT)
borderLineX = int(130 / const_width_screen * ORIGINAL_WIDTH)
borderLine2X = int((const_width_screen - 385) / const_width_screen * ORIGINAL_WIDTH)

# object of a curve, defined by 4 points
class BezierCurve(object):
    def __init__(self, p0, p1, p2, p3, color, width):
        self.vertices = [p0, p1, p2, p3]
        self.color = color
        self.width = width

    def compute_bezier_points(self, numPoints=None):
        if numPoints is None:
            numPoints = 30
        if numPoints < 2 or len(self.vertices) != 4:
            return None

        result = []

        b0x = self.vertices[0][0]
        b0y = self.vertices[0][1]
        b1x = self.vertices[1][0]
        b1y = self.vertices[1][1]
        b2x = self.vertices[2][0]
        b2y = self.vertices[2][1]
        b3x = self.vertices[3][0]
        b3y = self.vertices[3][1]

        # Compute polynomial coefficients from Bezier points
        ax = (-b0x + 3 * b1x + -3 * b2x + b3x)
        ay = (-b0y + 3 * b1y + -3 * b2y + b3y)

        bx = (3 * b0x + -6 * b1x + 3 * b2x)
        by = (3 * b0y + -6 * b1y + 3 * b2y)

        cx = (-3 * b0x + 3 * b1x)
        cy = (-3 * b0y + 3 * b1y)

        dx = b0x
        dy = b0y

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = (ax * (h * h * h) + bx * (h * h) + cx * h)
        firstFDY = (ay * (h * h * h) + by * (h * h) + cy * h)

        secondFDX = (6 * ax * (h * h * h) + 2 * bx * (h * h))
        secondFDY = (6 * ay * (h * h * h) + 2 * by * (h * h))

        thirdFDX = (6 * ax * (h * h * h))
        thirdFDY = (6 * ay * (h * h * h))

        # Compute points at each step
        result.append((int(pointX), int(pointY)))

        for i in range(numSteps):
            pointX += firstFDX
            pointY += firstFDY

            firstFDX += secondFDX
            firstFDY += secondFDY

            secondFDX += thirdFDX
            secondFDY += thirdFDY

            result.append((int(pointX), int(pointY)))

        return result

    def draw(self):
        global screen
        b_points = self.compute_bezier_points()
        pygame.draw.lines(screen, self.color, False, b_points, self.width)

# Function to rotate a point around a fixed point
def rotate_point(point, angle, center_p):
    x, y = point
    cx, cy = center_p

    # Translate the point and center to the origin
    translated_x = x - cx
    translated_y = y - cy

    # Perform the rotation
    new_x = translated_x * math.cos(angle) - translated_y * math.sin(angle)
    new_y = translated_x * math.sin(angle) + translated_y * math.cos(angle)

    # Translate the point back to its original position
    rotated_x = new_x + cx
    rotated_y = new_y + cy

    return int(rotated_x), int(rotated_y)

x_length = 16
x_height = 15 # height from the top of the heart downwards
contour_heart = [[(ORIGINAL_WIDTH / 2 - int(x_length / const_width_screen * ORIGINAL_WIDTH), int((250 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 + int(x_length / const_width_screen * ORIGINAL_WIDTH),int((250 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2 - int(x_length / const_width_screen * ORIGINAL_WIDTH), int((250 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 + int(x_length / const_width_screen * ORIGINAL_WIDTH),int((250 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH / 2 + int(x_length / const_width_screen * ORIGINAL_WIDTH), int((250 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 - int(x_length / const_width_screen * ORIGINAL_WIDTH),int((250 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2 + int(x_length / const_width_screen * ORIGINAL_WIDTH), int((250 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 - int(x_length / const_width_screen * ORIGINAL_WIDTH),int((250 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH / 2, int(600 / const_height_screen * ORIGINAL_HEIGHT)),
                  (int(1145 / const_width_screen * ORIGINAL_WIDTH), int(345 / const_height_screen * ORIGINAL_HEIGHT)), (
                  ORIGINAL_WIDTH / 2 + (int(120 / const_width_screen * ORIGINAL_WIDTH)),
                  int(80 / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2, int(250 / const_height_screen * ORIGINAL_HEIGHT))],
                 [(ORIGINAL_WIDTH / 2, int(250 / const_height_screen * ORIGINAL_HEIGHT)), (
                 ORIGINAL_WIDTH / 2 - int(120 / const_width_screen * ORIGINAL_WIDTH),
                 int(80 / const_height_screen * ORIGINAL_HEIGHT)),
                  (int(225 / const_width_screen * ORIGINAL_WIDTH), int(345 / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2, int(600 / const_height_screen * ORIGINAL_HEIGHT))]]
square_side = [int(193 / const_width_screen * ORIGINAL_WIDTH),int(193 / const_width_screen * ORIGINAL_WIDTH)]
x_height = int(60/const_width_screen * ORIGINAL_WIDTH)
x_length = int(24/const_width_screen * ORIGINAL_WIDTH)
contour_square = [[[ORIGINAL_WIDTH / 2 - square_side[0] + x_height - x_length, ORIGINAL_HEIGHT/2-square_side[1] + x_height],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height + x_length, ORIGINAL_HEIGHT/2-square_side[1] + x_height],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height - x_length, ORIGINAL_HEIGHT/2-square_side[1] + x_height],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height + x_length, ORIGINAL_HEIGHT/2-square_side[1] + x_height]],
                [[ORIGINAL_WIDTH / 2 - square_side[0] + x_height, ORIGINAL_HEIGHT/2-square_side[1] + x_height - x_length],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height, ORIGINAL_HEIGHT/2-square_side[1] + x_height + x_length],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height, ORIGINAL_HEIGHT/2-square_side[1] + x_height - x_length],
                   [ORIGINAL_WIDTH / 2 - square_side[0] + x_height, ORIGINAL_HEIGHT/2-square_side[1] + x_height + x_length]],
                [[ORIGINAL_WIDTH / 2, ORIGINAL_HEIGHT / 2 + square_side[1]],
                   [ORIGINAL_WIDTH / 2 + square_side[0],
                    ORIGINAL_HEIGHT / 2 + square_side[1]],
                   [ORIGINAL_WIDTH / 2 + square_side[0],
                    ORIGINAL_HEIGHT / 2 + square_side[1]],
                   [ORIGINAL_WIDTH / 2 + square_side[0],
                    ORIGINAL_HEIGHT / 2]], [
                      [ORIGINAL_WIDTH / 2 + square_side[0],
                       ORIGINAL_HEIGHT / 2],
                      [ORIGINAL_WIDTH / 2 + square_side[0],
                       ORIGINAL_HEIGHT / 2 - square_side[1]],
                      [ORIGINAL_WIDTH / 2 + square_side[0],
                       ORIGINAL_HEIGHT / 2 - square_side[1]],
                      [ORIGINAL_WIDTH / 2, ORIGINAL_HEIGHT / 2 - square_side[1]]],
                  [[ORIGINAL_WIDTH / 2, ORIGINAL_HEIGHT / 2 - square_side[1]],
                   [ORIGINAL_WIDTH / 2 - square_side[0],
                    ORIGINAL_HEIGHT / 2 - square_side[1]],
                   [ORIGINAL_WIDTH / 2 - square_side[0],
                    ORIGINAL_HEIGHT / 2 - square_side[1]],
                   [ORIGINAL_WIDTH / 2 - square_side[0],
                    ORIGINAL_HEIGHT/2]], [
                      [ORIGINAL_WIDTH / 2 - square_side[0],
                       ORIGINAL_HEIGHT / 2],
                      [ORIGINAL_WIDTH / 2 - square_side[0],
                       ORIGINAL_HEIGHT / 2 + square_side[1]],
                      [ORIGINAL_WIDTH / 2 - square_side[0],
                       ORIGINAL_HEIGHT / 2 + square_side[1]],
                      [ORIGINAL_WIDTH / 2, ORIGINAL_HEIGHT / 2 + square_side[1]]]]
x_height = 35
x_length = 16
contour_drop = [[(ORIGINAL_WIDTH / 2 - int(x_length / const_width_screen * ORIGINAL_WIDTH), int((145 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 + int(x_length / const_width_screen * ORIGINAL_WIDTH),int((145 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2 - int(x_length / const_width_screen * ORIGINAL_WIDTH), int((145 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 + int(x_length / const_width_screen * ORIGINAL_WIDTH),int((145 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH / 2 + int(x_length / const_width_screen * ORIGINAL_WIDTH), int((145 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 - int(x_length / const_width_screen * ORIGINAL_WIDTH),int((145 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH / 2 + int(x_length / const_width_screen * ORIGINAL_WIDTH), int((145 + x_height) / const_height_screen * ORIGINAL_HEIGHT)),
                  (ORIGINAL_WIDTH/2 - int(x_length / const_width_screen * ORIGINAL_WIDTH),int((145 + x_height + 2*x_length) / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH/2, int(610 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 + int(62 / const_width_screen * ORIGINAL_WIDTH), int(610 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 + int(184 / const_width_screen * ORIGINAL_WIDTH), int(550 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 + int(184 / const_width_screen * ORIGINAL_WIDTH), int(407 / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH/2 + int(184 / const_width_screen * ORIGINAL_WIDTH), int(407 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 + int(184 / const_width_screen * ORIGINAL_WIDTH), int(263 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 + int(43 / const_width_screen * ORIGINAL_WIDTH), int(170 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2, int(145 / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH/2, int(145 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 - int(43 / const_width_screen * ORIGINAL_WIDTH), int(170 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 - int(184 / const_width_screen * ORIGINAL_WIDTH), int(263 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 - int(184 / const_width_screen * ORIGINAL_WIDTH), int(407 / const_height_screen * ORIGINAL_HEIGHT))],
                [(ORIGINAL_WIDTH/2 - int(184 / const_width_screen * ORIGINAL_WIDTH), int(407 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 - int(184 / const_width_screen * ORIGINAL_WIDTH), int(550 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2 - int(62 / const_width_screen * ORIGINAL_WIDTH), int(610 / const_height_screen * ORIGINAL_HEIGHT)),
                 (ORIGINAL_WIDTH/2, int(610 / const_height_screen * ORIGINAL_HEIGHT))]]

contours = [contour_heart, contour_square, contour_drop]

centerInsideBorders = (int((borderLineX + borderLine2X) / 2), int((borderLineHeight + borderLine2Height) / 2))
center = (int(ORIGINAL_WIDTH / 2), int(ORIGINAL_HEIGHT / 2))
# move the conour heart to the center inside the borders
for k in range(len(contours)):
    for i in range(len(contours[k])):
        for j in range(len(contours[k][i])):
            contours[k][i][j] = (
            contours[k][i][j][0] + int(centerInsideBorders[0] - center[0]),
            contours[k][i][j][1] + int(centerInsideBorders[1] - center[1]))

# rotate the square contour 45 degrees
angle = math.radians(45)
for i in range(len(contour_square)):
    for j in range(len(contour_square[i])):
        contour_square[i][j] = rotate_point(contour_square[i][j], angle, centerInsideBorders)


def insert_drawing():
    global drawing
    global curves
    global contour_index
    global contours
    for i in range(len(contours[contour_index])):
        new_curve = BezierCurve([int((contours[contour_index][i][0][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((contours[contour_index][i][0][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((contours[contour_index][i][1][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((contours[contour_index][i][1][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((contours[contour_index][i][2][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((contours[contour_index][i][2][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((contours[contour_index][i][3][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((contours[contour_index][i][3][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                contourColor, curveWidth)
        curves.append(new_curve)
    for i in range(len(drawing)):
        new_curve = BezierCurve([int((drawing[i][0][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((drawing[i][0][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((drawing[i][1][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((drawing[i][1][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((drawing[i][2][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((drawing[i][2][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                [int((drawing[i][3][0] - borderLineX) / (borderLine2X - borderLineX) * screen_width),
                                 int((drawing[i][3][1] - borderLineHeight) / (
                                             borderLine2Height - borderLineHeight) * screen_height)],
                                curveColor, curveWidth)
        curves.append(new_curve)


pygame.init()
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bezier Curve")

screen.fill(background)
insert_drawing()
for curve in curves:
    curve.draw()
pygame.display.flip()

currentDirectory = os.getcwd()
drawings_dir = os.path.join(currentDirectory, r'drawings')
if not os.path.exists(drawings_dir):
    os.makedirs(drawings_dir)
# save the image with the current date and time in the folder drawings_dir png format
pygame.image.save(screen, os.path.join(drawings_dir, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            if event.type == pygame.KEYDOWN:
                running = False
pygame.quit()