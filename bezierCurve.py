import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button
from consts import *

pygame.init()


# fonts for text
font_style1 = pygame.font.SysFont("bahnschrift", 45)
font_style2 = pygame.font.SysFont("bahnschrift", 19)
font_style3 = pygame.font.SysFont("bahnschrift", 25)


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
        ax = -b0x + 3 * b1x + -3 * b2x + b3x
        ay = -b0y + 3 * b1y + -3 * b2y + b3y

        bx = 3 * b0x + -6 * b1x + 3 * b2x
        by = 3 * b0y + -6 * b1y + 3 * b2y

        cx = -3 * b0x + 3 * b1x
        cy = -3 * b0y + 3 * b1y

        dx = b0x
        dy = b0y

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
        firstFDY = ay * (h * h * h) + by * (h * h) + cy * h

        secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
        secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

        thirdFDX = 6 * ax * (h * h * h)
        thirdFDY = 6 * ay * (h * h * h)

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
screen = pygame.display.set_mode((screen_width, screen_height))

button_0 = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    10,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
    90,  # Width
    90,  # Height
    # Optional Parameters
    text='add curve',  # Text to display
    fontSize=26,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=buttonInactiveColour,  # Colour of button when not being interacted with
    hoverColour=buttonHoverColour,  # Colour of button when being hovered over
    pressedColour=buttonPressedColour,  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    # onClick=lambda: print('')  # Function to call when clicked on
    onClick=lambda: add_curve0()
)

button_1 = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    110,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
    90,  # Width
    90,  # Height
    # Optional Parameters
    text='clear',  # Text to display
    fontSize=27,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=buttonInactiveColour,  # Colour of button when not being interacted with
    hoverColour=buttonHoverColour,  # Colour of button when being hovered over
    pressedColour=buttonPressedColour,  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    # onClick=lambda: print('')  # Function to call when clicked on
    onRelease=lambda: clear()
)

button_2 = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    screen_width-100,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
    90,  # Width
    90,  # Height
    # Optional Parameters
    text="send to laser",  # Text to display
    fontSize=20,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=buttonInactiveColour,  # Colour of button when not being interacted with
    hoverColour=buttonHoverColour,  # Colour of button when being hovered over
    pressedColour=buttonPressedColour,  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    # onClick=lambda: print('')  # Function to call when clicked on
    # onClick=lambda: send_to_laser()
)

button_3 = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    screen_width-155,  # X-coordinate of top left corner
    60,  # Y-coordinate of top left corner
    40,  # Width
    40,  # Height
    # Optional Parameters
    text="?",  # Text to display
    fontSize=30,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=buttonInactiveColour,  # Colour of button when not being interacted with
    hoverColour=buttonHoverColour,  # Colour of button when being hovered over
    pressedColour=buttonPressedColour,  # Colour of button when being clicked
    radius=10,  # Radius of border corners (leave empty for not curved)
    # onClick=lambda: print('')  # Function to call when clicked on
    # onClick=lambda: show_explanation()
)

button_4 = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    210,  # X-coordinate of top left corner
    60,  # Y-coordinate of top left corner
    70,  # Width
    40,  # Height
    # Optional Parameters
    text="preview",  # Text to display
    fontSize=20,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=buttonInactiveColour,  # Colour of button when not being interacted with
    hoverColour=buttonHoverColour,  # Colour of button when being hovered over
    pressedColour=buttonPressedColour,  # Colour of button when being clicked
    radius=10,  # Radius of border corners (leave empty for not curved)
    # onClick=lambda: print('')  # Function to call when clicked on
    onClick=lambda: preview()
)


def preview():
    global show_control_lines
    show_control_lines = False

def add_curve0():
    global curves
    if len(curves) < maxCurves:
        add_curve()


def msgNumCurves(num):
    if num > 0:
        value = font_style1.render(str(num) + " curves left", True, white)
    else:
        value = font_style1.render("no curves left", True, red)
    screen.blit(value, [320, 60])


def msgTouch(msg):
    global screen
    if msg == NO_TOUCH_MSG:
        value = font_style2.render("move the blue points to change the curve's edges", True, white)
        screen.blit(value, [230, 10])
        value = font_style2.render("move the yellow points to change the curve's slope", True, white)
        screen.blit(value, [230, 30])
    elif msg == EDGE_TOUCH_MSG:
        value = font_style3.render("You are changing the curve's edges!", True, white)
        screen.blit(value, [240, 20])
    elif msg == SLOPE_TOUCH_MSG:
        value = font_style3.render("You are changing the curve's slope!", True, white)
        screen.blit(value, [240, 20])

def clear():
    global curves
    global selected_curve
    global selected
    curves.clear()
    selected_curve = None
    selected = None


def add_curve():
    global curves
    global selected_curve
    global selected

    new_curve = BezierCurve([x0, y0], [x1, y1], [x2, y2], [x3, y3])
    selected_curve = new_curve
    selected = None
    curves.append(new_curve)


def draw_all():
    global curves
    for curve in curves:
        curve.draw()


def main():
    global curves
    global selected_curve
    global selected
    global show_control_lines

    clock = pygame.time.Clock()

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

        # Draw stuff
        screen.fill(gray)
        draw_all()
        if selected is not None:
            if pygame.mouse.get_pos()[1] > borderLineHeight + circleRadius1 and pygame.mouse.get_pos()[1] < screen_height - circleRadius1 and pygame.mouse.get_pos()[0] > circleRadius1 and pygame.mouse.get_pos()[0] < screen_width - circleRadius1:
                selected[0], selected[1] = pygame.mouse.get_pos()
                pygame.draw.circle(screen, green, (selected[0], selected[1]), 10)
            if selected_curve.vertices.index(selected) == 1 or selected_curve.vertices.index(selected) == 2:
                msgTouch(SLOPE_TOUCH_MSG)
            else:
                msgTouch(EDGE_TOUCH_MSG)
        else:
            msgTouch(NO_TOUCH_MSG)

        # draw border line
        pygame.draw.line(screen, black, (0, borderLineHeight), (screen_width, borderLineHeight), 5)
        msgNumCurves(maxCurves - len(curves))
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
