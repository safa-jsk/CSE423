from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width = 500
W_Height = 700
score = 0

catcher_x = 0
catcher_height = -250  # Position of the catcher
catcher_width = 60
catcher_speed=0.1
diamond_radius = 17
diamond_speed = 0.1
diamond = []  # List to hold the falling diamond
missed_count = 0
game_over_flag = False
pause_flag = False
catcher_color = (1.0, 1.0, 1.0)  # Default catcher color is white


def midpointLine(x1, y1, x2, y2):
    zone = determineZone(x1, y1, x2, y2)
    s_x1, s_y1 = convertZone(zone, x1, y1)
    e_x2, e_y2 = convertZone(zone, x2, y2)
    dx = e_x2 - s_x1
    dy = e_y2 - s_y1
    d = 2 * dy - dx
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    x = s_x1
    y = s_y1
    while x < e_x2:
        ori_x, ori_y = convertZone(zone, x, y)
        glBegin(GL_POINTS)
        glVertex2f(ori_x, ori_y)
        glEnd()
        if d <= 0:
            d += de
            x += 1
        else:
            d += dne
            y += 1
            x += 1


def diamondShape(center_x, center_y, size):
    half_size = size / 2
    glBegin(GL_POINTS)
    glVertex2f(center_x, center_y + half_size)  # top
    glVertex2f(center_x - half_size, center_y)  # left
    glVertex2f(center_x + half_size, center_y)  # right
    glVertex2f(center_x, center_y - half_size)  # bottom
    for i in range(int(half_size)):
        glVertex2f(center_x - i, center_y + half_size - i)
    for i in range(int(half_size)):
        glVertex2f(center_x + i, center_y + half_size - i)
    for i in range(int(half_size)):
        glVertex2f(center_x - i, center_y - half_size + i)
    for i in range(int(half_size)):
        glVertex2f(center_x + i, center_y - half_size + i)
    glEnd()


def determineZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx >= 0 and dy >= 0:
        return 0 if abs(dx) > abs(dy) else 1
    elif dx < 0 and dy >= 0:
        return 3 if abs(dx) > abs(dy) else 2
    elif dx < 0 and dy < 0:
        return 4 if abs(dx) > abs(dy) else 5
    elif dx >= 0 and dy < 0:
        return 7 if abs(dx) > abs(dy) else 6


def convertZone(givenZone, x, y):
    if givenZone == 0:
        return x, y
    elif givenZone == 1:
        return y, x
    elif givenZone == 2:
        return -y, x
    elif givenZone == 3:
        return -x, y
    elif givenZone == 4:
        return -x, -y
    elif givenZone == 5:
        return -y, -x
    elif givenZone == 6:
        return y, -x
    elif givenZone == 7:
        return x, -y


def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    # Axis-Aligned Bounding Box (AABB) collision detection
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def spaceship():
     global catcher_x, catcher_width, catcher_height
     midpointLine(catcher_x, catcher_height, catcher_x + catcher_width, catcher_height)
    
     midpointLine(catcher_x + catcher_width+20, catcher_height+20, catcher_x + catcher_width, catcher_height )
     midpointLine(catcher_x-20, catcher_height+20 , catcher_x + catcher_width+20, catcher_height+20 )
     midpointLine(catcher_x, catcher_height+1.7 , catcher_x-20, catcher_height+20 )

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)  # Clear the screen to black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)  # Camera position
    glMatrixMode(GL_MODELVIEW)
    
    global score, missed_count, game_over_flag, diamond, diamond_speed, catcher_color
    glColor3f(1, 0.75, 0)
    play_pause()

    # Restart button
    glColor3f(0.0, 0.7, 0.8)
    left_arrow()

    # Cross button
    glColor3f(1, 0, 0)
    cross()
    
    # If game over, change catcher color to red
    if game_over_flag:
        catcher_color = (1.0, 0.0, 0.0)  # Red color for the catcher when game is over
    else:
        catcher_color = (1.0, 1.0, 1.0)  # White color when game is ongoing
    
    # Apply the current catcher color before drawing
    glColor3f(*catcher_color)
    spaceship()  # Draw the spaceship (catcher)

    if diamond and not game_over_flag:
        diamond[1] -= diamond_speed  # Move the diamond down
        glColor3f(*diamond[2])  # Set the diamond's random color
        diamondShape(diamond[0], diamond[1], diamond_radius * 2)  # Draw the diamond

        # Check if the diamond is caught by the catcher
        if aabb(diamond[0] - diamond_radius, diamond[1] - diamond_radius, diamond_radius * 2, diamond_radius * 2,
                catcher_x, catcher_height, catcher_width, 10):
            score += 1
            print(f"Score: {score}")
            diamond = []  # Reset the diamond
            # No need to change the catcher color here, as it will be white when diamond is caught

        # Check if the diamond is missed
        elif diamond[1] < -300:
            game_over_flag = True  # Set the game over flag
            print(f"Game Over! Score: {score}")
            diamond = []  # Remove the missed diamond
            

    # If no diamond is falling and game over is not active, start a new diamond
    if not diamond and not game_over_flag:
        diamond = [random.uniform(-200, 200), 250, (random.random(), random.random(), random.random())]

    # Gradually increase the diamond speed as the game goes on
    if not game_over_flag:
        diamond_speed *= 1.001  # Increase speed slightly (e.g., 0.1% per frame)


    # Swap buffers to render the updated frame
    glutSwapBuffers()
    glutPostRedisplay()


def play_pause():
    if pause_flag:
        midpointLine(5, 195, 4, 170)
        midpointLine(5, 195, 15, 185.5)
        midpointLine(5, 170, 15, 185)
    else:
        midpointLine(-5, 195, -5.5, 170)
        midpointLine(5, 195, 4, 170)

def left_arrow():
    midpointLine(-175, 190, -195, 190)
    midpointLine(-185, 195, -195, 190)
    midpointLine(-195, 190, -185, 185)


def cross():
    midpointLine(175, 180, 195, 195)
    midpointLine(195, 180, 175, 195)


def SpecialkeyboardListener(key, x, y):
    global catcher_x, catcher_width, pause_flag, game_over_flag
    if key == b'\x1b':
        glutLeaveMainLoop()

    if key == GLUT_KEY_LEFT:
        if catcher_x-20 > -W_Width / 2:
            catcher_x -= catcher_speed+5

    if key == GLUT_KEY_RIGHT:
        if catcher_x + catcher_width +20< W_Width / 2:
            catcher_x += catcher_speed+5

    if key == b' ' and game_over_flag:
        restart_game() 



def restart_game():
    # Restart game logic
    global score, missed_count, diamond_speed, catcher_color, game_over_flag
    diamond.clear()
    score = 0
    missed_count = 0
    diamond_speed = 0.1
    catcher_color = (1.0, 1.0, 1.0)  # Reset catcher color to white
    game_over_flag = False
    print("Starting Over")


def mouseListener(button, state, x, y):
    global pause_flag, game_over_flag
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x, y = mouseConverter(x, y)

        # Handle Pause/Play button click
        if -4 <= x <= 7 and 170 <= y < 198:
            if not pause_flag:
                pause_flag = True
                print(f"Paused. Current score: {score}")
            else:
                pause_flag = False

        # Handle restart button click
        if -160 <= x <= -130 and 190 <= y <= 200:
            restart_game()

        # Handle exit button click
        if 140 <= x <= 195 and 180 <= y <= 200:
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()

    glutPostRedisplay()


def mouseConverter(x, y):
    # Convert mouse coordinates to OpenGL coordinates
    a = x - (400 / 2)
    b = (500 / 2) - y
    return a, b


def animate():
    if not pause_flag and not game_over_flag:
        glutPostRedisplay()


def init():
    # Initialize OpenGL settings
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)
    glutSpecialFunc(SpecialkeyboardListener)  # Handle special keys like arrows


glutInit()
glutInitWindowSize(400,400)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth, Double buffer, RGB color
wind = glutCreateWindow(b"Shooting the circles")
init()
glutDisplayFunc(display)  # Display callback function
glutIdleFunc(animate)  # What you want to do in the idle time (when no drawing is occurring)
glutMouseFunc(mouseListener)
glutMainLoop()