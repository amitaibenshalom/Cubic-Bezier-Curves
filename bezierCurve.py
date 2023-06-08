from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button
from consts import *

pygame.init()


# fonts for text
font_style1 = pygame.font.SysFont("calibri", 30)
font_style2 = pygame.font.SysFont("calibri", 45)
font_style3 = pygame.font.SysFont("calibri", 25)
font_style2.bold = True
# print(pygame.font.get_fonts())

# object of a curve, defined by 4 points
class BezierCurve(object):
    def __init__(self, p0, p1, p2, p3):
        self.vertices = [p0, p1, p2, p3]

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
        by =  (3 * b0y + -6 * b1y + 3 * b2y)

        cx = (-3 * b0x + 3 * b1x)
        cy = (-3 * b0y + 3 * b1y)

        dx = (b0x)
        dy = (b0y)

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = (ax * (h * h * h) + bx * (h * h) + cx * h)
        firstFDY =(ay * (h * h * h) + by * (h * h) + cy * h)

        secondFDX = (6 * ax * (h * h * h) + 2 * bx * (h * h))
        secondFDY =(6 * ay * (h * h * h) + 2 * by * (h * h))

        thirdFDX = (6 * ax * (h * h * h))
        thirdFDY =(6 * ay * (h * h * h))

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
        # Draw control points
        control_points = self.vertices
        if show_control_lines:
            for p in control_points:
                # draw start and end points of the curve in circleColor1 and slope points in circleColor2
                if control_points.index(p) == 1 or control_points.index(p) == 2:
                    pygame.draw.circle(screen, circleColor2, (int(p[0]), int(p[1])), circleRadius2)
                elif control_points.index(p) == 0:
                    pygame.draw.circle(screen, circleColor0, (int(p[0]), int(p[1])), circleRadius0)
                else:
                    pygame.draw.circle(screen, circleColor1, (int(p[0]), int(p[1])), circleRadius1)

            # Draw control "lines"
            # pygame.draw.lines(screen, lightgray, False, [(x[0], x[1]) for x in control_points])
            pygame.draw.lines(screen, lightgray, False,
                              [(x[0], x[1]) for x in control_points[:2]])
            pygame.draw.lines(screen, lightgray, False,
                              [(x[0], x[1]) for x in control_points[2:]])

        ### Draw bezier curve
        b_points = self.compute_bezier_points()
        pygame.draw.lines(screen, curveColor, False, b_points, curveWidth)



# list of all curves
curves = []
selected_curve = None
# The currently selected point
selected = None
show_control_lines = True
show_picture = False
delta = [0,0,0]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

button_0 = Button(
    screen,
    screen_width-230,
    10,
    120, # Width
    90, # Height
    text='וק ףסוה',
    fontSize=26,
    margin=20,
    font=pygame.font.SysFont("calibri", 26),
    inactiveColour=buttonInactiveColour,
    hoverColour=buttonHoverColour,
    pressedColour=buttonPressedColour,
    radius=20,
    onClick=lambda: add_curve0()
)

button_1 = Button(
    screen,
    110,
    screen_height-80,
    90,  # Width
    70,  # Height
    text='קחמ',
    fontSize=27,
    margin=20,
    font=pygame.font.SysFont("calibri",27),
    inactiveColour=buttonInactiveColour,
    hoverColour=buttonHoverColour,
    pressedColour=buttonPressedColour,
    radius=20,
    onRelease=lambda: clear()
)

button_2 = Button(
    screen,
    screen_width-200,
    screen_height-80,
    90,  # Width
    70,  # Height
    text="ספדה",
    fontSize=20,
    font=pygame.font.SysFont("calibri",20),
    margin=20,
    inactiveColour=buttonInactiveColour,
    hoverColour=buttonHoverColour,
    pressedColour=buttonPressedColour,
    radius=20,
    onClick=lambda: send_to_laser()
)

button_3 = Button(
    screen,
    screen_width-280,
    60,
    40,  # Width
    40,  # Height
    text="?",
    fontSize=30,
    margin=20,
    font=pygame.font.SysFont("calibri",30),
    inactiveColour=buttonInactiveColour,
    hoverColour=buttonHoverColour,
    pressedColour=buttonPressedColour,
    radius=10,
    onClick=lambda: show_popup()
)

button_4 = Button(
    screen,
    210,
    screen_height-80,
    screen_width-(210+210),  # Width
    70,  # Height
    text="המידקמ הגוצת",
    fontSize=20,
    font=pygame.font.SysFont("calibri", 20),
    margin=20,
    inactiveColour=buttonInactiveColour,
    hoverColour=buttonHoverColour,
    pressedColour=buttonPressedColour,
    radius=10,
    onClick=lambda: preview()
)

def send_to_laser():
    return

def preview():
    global show_control_lines
    show_control_lines = False

def add_curve0():
    global curves
    if len(curves) < maxCurves:
        add_curve()


def msgNumCurves(num):
    if num > 0:
        value = font_style1.render("ורתונ םיווק " + str(num), True, white)
    else:
        value = font_style1.render("תומוקע ורתונ אל", True, red)
    text_rect = value.get_rect(center=(screen_width / 2, 50+35))
    screen.blit(value, text_rect)

def msg():
    global screen
    value = font_style2.render("!תודוקנה תועצמאב וקה תרוצ תא ונש", True, white)
    text_rect = value.get_rect(center=(screen_width / 2, 50))
    screen.blit(value, text_rect)

    # screen.blit(value, [screen_width/2-70, 10])

# def msgTouch(msg):
#     global screen
#     if msg == NO_TOUCH_MSG:
#         value = font_style2.render("move the blue points to change the curve's edges", True, white)
#         screen.blit(value, [230, 10])
#         value = font_style2.render("move the yellow points to change the curve's slope", True, white)
#         screen.blit(value, [230, 30])
#     elif msg == EDGE_TOUCH_MSG:
#         value = font_style3.render("You are changing the curve's edges!", True, white)
#         screen.blit(value, [240, 20])
#     elif msg == SLOPE_TOUCH_MSG:
#         value = font_style3.render("You are changing the curve's slope!", True, white)
#         screen.blit(value, [240, 20])

def clear():
    global curves
    global selected_curve
    global selected
    global delta
    curves.clear()
    selected_curve = None
    selected = None
    delta = [0,0,0]


def add_curve():
    global curves
    global selected_curve
    global selected
    global delta
    deltaX= delta[0]
    deltaY= delta[1]

    new_curve = BezierCurve([x0-deltaX, y0-deltaY], [x1-deltaX, y1-deltaY], [x2-deltaX, y2-deltaY], [x3-deltaX, y3-deltaY])
    selected_curve = new_curve
    selected = None
    curves.append(new_curve)
    # move the curve by delta0X and delta0Y to the left and up
    delta[0] += delta0X
    delta[1] += delta0Y
    if deltaX > screen_width-200 or deltaY > screen_height-200:
        delta[2] += 1
        delta[0] = 0
        delta[1] = delta[2]*-20



def draw_all():
    global curves
    for curve in curves:
        curve.draw()

def show_popup():
    global show_picture
    show_picture = True



def main():
    global curves
    global selected_curve
    global selected
    global show_control_lines
    global show_picture

    clock = pygame.time.Clock()
    add_curve0()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_c:
                    clear()
                elif event.key == pygame.K_a:
                    add_curve0()
                # elif event.key == pygame.K_SPACE:
                #     show_popup()
                else:
                    running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for curve in curves:
                    for p in curve.vertices:
                        if abs(p[0] - event.pos[X]) < 10 and abs(p[1] - event.pos[Y]) < 10:
                            selected_curve = curve
                            selected = p
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                selected = None
                show_control_lines = True
                show_picture = False

        # Draw stuff
        screen.fill(gray)
        draw_all()
        if selected is not None:
            if pygame.mouse.get_pos()[1] > borderLineHeight + circleRadius1 and pygame.mouse.get_pos()[1] < borderLine2Height - circleRadius1 and pygame.mouse.get_pos()[0] > circleRadius1 and pygame.mouse.get_pos()[0] < screen_width - circleRadius1:
                pygame.draw.circle(screen, green, (selected[0], selected[1]), 10)
                # if clicked on the purple point, which moves the whole curve
                if selected_curve.vertices.index(selected) == 0:
                    # check if all points are in the screen
                    inScreen = True
                    for i in range(1, 4):
                        if selected_curve.vertices[i][0] <= circleRadius1 or selected_curve.vertices[i][0] >= screen_width - circleRadius1 or selected_curve.vertices[i][1] <= borderLineHeight or selected_curve.vertices[i][1] >= borderLine2Height:
                            inScreen = False
                    # if so, move the curve
                    if inScreen:
                        for i in range(1, 4):
                            selected_curve.vertices[i][0] = selected_curve.vertices[i][0]+(pygame.mouse.get_pos()[0] - selected[0])
                            selected_curve.vertices[i][1] = selected_curve.vertices[i][1] + (pygame.mouse.get_pos()[1] - selected[1])
                        selected[0], selected[1] = pygame.mouse.get_pos()
                else:
                    # move the selected point
                    selected[0], selected[1] = pygame.mouse.get_pos()

            # if selected_curve.vertices.index(selected) == 1 or selected_curve.vertices.index(selected) == 2:
            #     msgTouch(SLOPE_TOUCH_MSG)
            # else:
            #     msgTouch(EDGE_TOUCH_MSG)
        # else:
        #     msgTouch(NO_TOUCH_MSG)
        msg()

        # draw border line
        pygame.draw.line(screen, black, (0, borderLineHeight), (screen_width, borderLineHeight), 5)
        pygame.draw.line(screen, black, (0, borderLine2Height), (screen_width, borderLine2Height), 5)
        msgNumCurves(maxCurves - len(curves))
        if show_picture:
            popup_x = (screen_width - image.get_width()) // 2
            popup_y = (screen_height - image.get_height()) // 2
            screen.blit(image, (popup_x, popup_y))
        pygame_widgets.update(events)
        pygame.display.update()
        # Flip screen
        pygame.display.flip()
        clock.tick(100)
        # print clock.get_fps()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
