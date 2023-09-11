from consts import *

pygame.init()

port = 'COM5'
baudrate = 115200
arduino = serial.Serial(port, baudrate)


# fonts for text
font_style2 = pygame.font.SysFont("calibri", 45)
font_style2.bold = True


class Button(object):
    def __init__(self, pos, size, color, coloron, img, imgon, function):
        self.pos = pos
        self.size = size
        self.color = color
        self.coloron = coloron
        self.img = img
        self.imgon = imgon
        self.function = function
        self.done = True

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        on_button = rect.collidepoint(mouse)
        if not on_button:
            pygame.draw.rect(screen, self.color, rect)
            screen.blit(self.img, self.img.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 0:
            pygame.draw.rect(screen, self.color, rect)
            screen.blit(self.img, self.img.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 1 and self.done:
            pygame.draw.rect(screen, self.coloron, rect)
            screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))
            self.done = False
            if self.function is not None:
                self.function()
        else:
            pygame.draw.rect(screen, self.coloron, rect)
            screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))

# object of a curve, defined by 4 points
class BezierCurve(object):
    def __init__(self, p0, p1, p2, p3, moveable, color, width):
        self.vertices = [p0, p1, p2, p3]
        self.moveable = moveable
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
        if show_control_lines and self.moveable:
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

        # Draw bezier curve
        b_points = self.compute_bezier_points()
        pygame.draw.lines(screen, self.color, False, b_points, self.width)


curves = [] # list of all curves
contour = []
selected_curve = None
selected = None # The currently selected point
show_control_lines = True
show_picture = False
delta = [0,0,0]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((screen_width, screen_height))

def check_buttons():
    global buttons
    for button in buttons:
        button.check()


'''
# send the points as ratio between place and screen size
def send_to_laser():
    global curves
    # print the values of the points in the curves
    # for curve in curves:
    #     print(curve.vertices)
    # return

    # fist, send a key that will tell the arduino to start reading
    if not send_one_number(starting_key):
        return False
    print("sent starting key to laser")
    time.sleep(time_delay_arduino)
    # then, send the number of curves
    if not send_one_number(-len(curves)):
        return False
    print("sent number of curves")
    # time.sleep(time_delay_arduino)
    # then, send the points of each curve
    for curve in curves:
        for point in curve.vertices:
            send_one_number(point[1])
            send_one_number(screen_width - point[0])

        # wait for arduino to send a key that will tell us it finished reading the curve
        t0 = time.time()
        while arduino.in_waiting == 0 and time.time() < t0 + MAX_TIME_WAITING_FOR_ARDUINO:
            pass
        if arduino.in_waiting == 0:
            print("arduino didn't send key")
            return False
        # received_data = arduino.readline().decode('utf-8').rstrip()
        print("arduino sent key")
        time.sleep(time_delay_arduino)

        # send a key that will tell the arduino to go to the next curve
        # send_one_number(next_curve_key)
    # send a key that will tell the arduino to stop reading
    print("sent all points")
    send_one_number(end_key)
    print("sent end key")
    return True
'''


# send the points as ratio between place and screen size
def send_to_laser():
    global curves
    # print the values of the points in the curves
    # for curve in curves:
    #     print(curve.vertices)
    # return

    # fist, send a key that will tell the arduino to start reading
    if not send_one_number(starting_key):
        return False
    print("sent starting key to laser")
    # time.sleep(time_delay_arduino)
    # then, send the number of curves
    if not send_one_number(-len(curves)):
        return False
    print("sent number of curves")
    # time.sleep(time_delay_arduino)
    # then, send the points of each curve
    for curve in curves:
        for point in curve.vertices:
            send_one_number(point[1])
            send_one_number(screen_width-point[0])
        # wait for arduino to send a key that will tell us it finished reading the curve
        t0 = time.time()
        while arduino.in_waiting == 0 and time.time() < t0 + MAX_TIME_WAITING_FOR_ARDUINO:
            pass
            # print("waiting for arduino to send key")
        if arduino.in_waiting == 0:
            print("arduino didn't send key")
            return False
        print("arduino done reading curve " + str(curves.index(curve)))
        received_data = arduino.readline().decode('utf-8').rstrip()

        # wait for arduino to send a key that will tell us that it is finished drawing the curve
        t0 = time.time()
        while arduino.in_waiting == 0 and time.time() < t0 + MAX_DRAWING_TIME_FOR_ARDUINO:
            pass
        if arduino.in_waiting == 0:
            print("arduino took to much time drawing the curve")
            return False
        received_data = arduino.readline().decode('utf-8').rstrip()
        print("arduino done drawing curve " + str(curves.index(curve)))
        # time.sleep(time_delay_arduino)

    # send a key that will tell the arduino to stop reading
    print("sent all curves")
    send_one_number(end_key)
    print("sent end key")
    return True


def send_one_number(value):
    try:
        byte_value = bytearray(struct.pack("f", value))  # Convert float to bytes
        arduino.write(byte_value)
        arduino.flush()
    except Exception:
        return False
    print("sent " + str(value))
    return True


def heart():
    global contour
    contour = []
    for i in range(len(contour_heart)):
        add_contour(contour_heart[i][0],contour_heart[i][1],contour_heart[i][2],contour_heart[i][3])

def sqaure():
    global contour
    contour = []
    for i in range(len(contour_square)):
        add_contour(contour_square[i][0],contour_square[i][1],contour_square[i][2],contour_square[i][3])

def drop():
    global contour
    contour = []
    for i in range(len(contour_drop)):
        add_contour(contour_drop[i][0],contour_drop[i][1],contour_drop[i][2],contour_drop[i][3])

def preview():
    global show_control_lines
    show_control_lines = False

def add_curve0():
    global curves
    if len(curves) < maxCurves:
        add_curve()


def msgNumCurves(num):
    if num > 0:
        value = font_style2.render("ורתונ םיווק " + str(num), True, black)
    else:
        value = font_style2.render("תומוקע ורתונ אל", True, red)
    text_rect = value.get_rect(center=(screen_width / 2 - 30, 50+35))
    screen.blit(value, text_rect)

# def msg():
#     global screen
#     value = font_style2.render("!תודוקנה תועצמאב וקה תרוצ תא ונש", True, white)
#     text_rect = value.get_rect(center=(screen_width / 2, 50))
#     screen.blit(value, text_rect)

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
    new_curve = BezierCurve([x0-deltaX, y0-deltaY], [x1-deltaX, y1-deltaY], [x2-deltaX, y2-deltaY], [x3-deltaX, y3-deltaY],True, curveColor, curveWidth)
    # selected_curve = new_curve
    selected = None
    curves.append(new_curve)
    # move the curve by delta0X and delta0Y to the left and up
    delta[0] += delta0X
    delta[1] += delta0Y
    # if deltaX > screen_width-200 or deltaY > screen_height-200:
    if delta[0] > delta0X*MAX_LINES_PER_ROW:
        delta[2] += 1
        delta[0] = 0
        delta[1] = delta[2]*delta0Z


def add_contour(p0,p1,p2,p3):
    global contour
    new_contour = BezierCurve(p0, p1, p2, p3, False, contourColor, contourWidth)
    contour.append(new_contour)

def draw_all():
    global curves
    for curve in curves:
        curve.draw()
    for curve in contour:
        curve.draw()

def show_popup():
    global show_picture
    show_picture = True

#define all the buttons and make an array of them
ButtonAdd = Button(buttonAddPosition, buttonAddSize, buttonInactiveColour, buttonPressedColour, pic_buttonAdd, pic_buttonPressedAdd, add_curve0)
ButtonDelete = Button(buttonDeletePosition, buttonDeleteSize, buttonInactiveColour, buttonPressedColour, pic_buttonDelete, pic_buttonPressedDelete, clear)
ButtonInfo = Button(buttonInfoPosition, buttonInfoSize, buttonInactiveColour, buttonPressedColour, pic_buttonInfo, pic_buttonPressedInfo, show_popup)
ButtonPreview = Button(buttonPreviewPosition, buttonPreviewSize, buttonInactiveColour, buttonPressedColour, pic_buttonPreview, pic_buttonPressedPreview, preview)
ButtonPrint = Button(buttonPrintPosition, buttonPrintSize, buttonInactiveColour, buttonPressedColour, pic_buttonPrint, pic_buttonPressedPrint, send_to_laser)
ButtonHeart = Button(buttonHeartPosition, buttonHeartSize, buttonInactiveColour, buttonPressedColour, pic_buttonHeart, pic_buttonPressedHeart, heart)
ButtonDrop = Button(buttonDropPosition, buttonDropSize, buttonInactiveColour, buttonPressedColour, pic_buttonDrop, pic_buttonPressedDrop, drop)
ButtonCircle = Button(buttonCirclePosition, buttonCircleSize, buttonInactiveColour, buttonPressedColour, pic_buttonCircle, pic_buttonPressedCircle, sqaure)

buttons = [ButtonAdd,ButtonDelete,ButtonInfo,ButtonPreview,ButtonPrint,ButtonHeart,ButtonDrop,ButtonCircle]


def main():
    global curves
    global selected_curve
    global selected
    global show_control_lines
    global show_picture

    clock = pygame.time.Clock()
    sqaure()

    running = True
    while running:

        try:
            if arduino.in_waiting > 0:
                received_data = arduino.readline().decode('utf-8').rstrip()
                print("Received from Arduino:", received_data)
        finally:
            pass

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
                            selected_curve.color = selectedCurveColor
                            selected = p
                            break
                    if selected is not None:
                        break
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                selected = None
                if selected_curve is not None:
                    selected_curve.color = curveColor
                show_control_lines = True
                show_picture = False

        # Draw stuff
        screen.blit(pic_bg0, [0, 0])
        pygame.draw.rect(screen, lightgray, ((screen_width-(borderLine2Height-borderLineHeight))/2,(screen_height-(borderLine2Height-borderLineHeight))/2,borderLine2Height-borderLineHeight,borderLine2Height-borderLineHeight))
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

        msgNumCurves(maxCurves - len(curves))
        if show_picture:
            popup_x = (screen_width - infoHebSize[0]) // 2
            popup_y = (screen_height - infoHebSize[1]) // 2
            screen.blit(pic_infoHeb, (popup_x, popup_y))
        # pygame_widgets.update(events)
        check_buttons()
        pygame.display.update()
        # Flip screen
        pygame.display.flip()
        clock.tick(100)
        # print clock.get_fps()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()