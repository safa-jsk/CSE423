# Task 01
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

w_width, w_height = 1200, 675
rain_count = 25
rain_speed = 10
rain_drops_blue = [(random.randint(-w_width//2, w_width//2), random.randint(-w_height, w_height-50)) for i in range(rain_count)]
rain_drops_white = [(random.randint(-w_width//2, w_width//2), random.randint(-w_height, w_height-50)) for i in range(rain_count)]
rain_length = 50
wind = 0.0
day = True
day_time = 1

def rain(): # with GL_LINES
    global rain_drops_blue, rain_drops_white, rain_count, rain_speed, wind, rain_length
    
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(49/255, 79/255, 255/255)
    for i in range(rain_count):
        x, y = rain_drops_blue[i]
        glVertex2f(x, y)
        glVertex2f(x + wind, y - rain_length)
    glColor3f(1, 1, 1)
    for i in range(rain_count):
        x, y = rain_drops_white[i]
        glVertex2f(x, y)
        glVertex2f(x + wind, y - rain_length)
    glEnd()

def animate():
    global rain_drops_blue, rain_drops_white, rain_count, rain_speed, wind, rain_length, day_time, day
    
    for i in range(rain_count):
        x, y = rain_drops_blue[i]
        y -= rain_speed
        if y < -(w_height):
            x = random.randint(-w_width//2, w_width//2)
            y = random.randint(-w_height, w_height-50)
        rain_drops_blue[i] = (x, y)
    for i in range(rain_count):
        x, y = rain_drops_white[i]
        y -= rain_speed
        if y < -(w_height):
            x = random.randint(-w_width//2, w_width//2)
            y = random.randint(-w_height, w_height-50)
        rain_drops_white[i] = (x, y)
    glutPostRedisplay()

def animate_day():
    global day_time, day
    
    if day:
        if day_time < 1:
            day_time += 0.05
        else:
            day_time = 1
    else:
        if day_time > 0:
            day_time -= 0.05
        else:
            day_time = 0
    glutPostRedisplay()
    glutTimerFunc(50, lambda _: animate_day(), 0)

def draw_background():
    global day, day_time
    
    # Sky
    glBegin(GL_TRIANGLES)
    
    sky_r = 1 * day_time
    sky_g = 1 * day_time
    sky_b = 1 * day_time
    glColor3f(sky_r, sky_g, sky_b)
    
    glVertex2f(-w_width//2, w_height)
    glVertex2f(-w_width//2, -w_height)
    glVertex2f(w_width//2, -w_height)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(sky_r, sky_g, sky_b)
    glVertex2f(w_width//2, -w_height)
    glVertex2f(w_width//2, w_height)
    glVertex2f(-w_width//2, w_height)
    glEnd()
    
    # Ground
    glBegin(GL_TRIANGLES)
    glColor3f(128/255, 89/255, 14/255)
    glVertex2f(-w_width//2, -w_height)
    glVertex2f(-w_width//2, 250)
    glVertex2f(w_width//2, 250)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(128/255, 89/255, 14/255)
    glVertex2f(w_width//2, 250)
    glVertex2f(w_width//2, -w_height)
    glVertex2f(-w_width//2, -w_height)
    glEnd()
    
    # hills
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    x = -w_width//2
    while x < w_width//2:
        glVertex2f(x+25, 200)
        glVertex2f(x, 75)
        glVertex2f(x+50, 75)
        x += 50
    glEnd()

def draw_house():
    # House
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)
    glVertex2f(-150, -150)      # left bottom
    glVertex2f(-150, 100)       # left top
    glVertex2f(150, 100)        # right top
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)
    glVertex2f(150, 100)        # right top
    glVertex2f(150, -150)       # right bottom
    glVertex2f(-150, -150)      # left bottom
    glEnd()
    
    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(78/255, 23/255, 176/255)
    glVertex2f(0, 300)            # top
    glVertex2f(-200, 100)         # left
    glVertex2f(200, 100)          # right
    glEnd()

    # Door
    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(-40, -150)
    glVertex2f(-40, 50)
    glVertex2f(40, 50)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(40, 50)
    glVertex2f(40, -150)
    glVertex2f(-40, -150)
    glEnd()

    # Window
    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(-120, -50)           # left bottom
    glVertex2f(-120, 50)            # left top
    glVertex2f(-70, 50)             # right top
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(-70, -50)            # right bottom
    glVertex2f(-70, 50)             # right top
    glVertex2f(-120, -50)           # left bottom
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(70, -50)
    glVertex2f(70, 50)
    glVertex2f(120, 50)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(120, 50)
    glVertex2f(120, -50)
    glVertex2f(70, -50)
    glEnd()
    
    # Window Grills
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)
    glVertex2f(-120, 0)
    glVertex2f(-70, 0)
    glVertex2f(-95, 50)
    glVertex2f(-95, -50)
    glVertex2f(70, 0)
    glVertex2f(120, 0)
    glVertex2f(95, 50)
    glVertex2f(95, -50)
    glEnd()
    
    # Door Knob
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)
    glVertex2f(20, -50)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,500, 0,0,0, 0,1,0)
    glMatrixMode(GL_MODELVIEW)
    
    draw_background()
    draw_house()
    rain()
    glutSwapBuffers()

def special_keyboard_listener(key, x, y):
    global rain_speed, wind, rain_length
    
    if key == GLUT_KEY_UP:
        rain_speed += 1
        print(f"Speed increased to {rain_speed}")
    elif key == GLUT_KEY_DOWN:
        if rain_speed > 1:
            rain_speed -= 1
            print(f"Speed decreased to {rain_speed}")
        else:
            print("Minimum speed reached")
    elif key == GLUT_KEY_RIGHT:
        if wind < rain_length:
            wind += 1
            print("Wind to the Right")
        else:
            print("Maximum wind reached")
    elif key == GLUT_KEY_LEFT:
        if wind > -rain_length:
            wind -= 1
            print("Wind to the Left")
        else:
            print("Maximum wind reached")
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global day
    if key == b"d":
        day = not day
        if day:
            print("Day Time")
        else:
            print("Night Time")
    glutPostRedisplay()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100, 1, 1, 1000)
    
glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

glutCreateWindow(b"Rainy House")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)
glutSpecialFunc(special_keyboard_listener)
glutKeyboardFunc(keyboard_listener)
animate_day()
glutMainLoop()


# =============================================================================
# |                                                                            |
# |                                                                            |
# |                                                                            |
# =============================================================================

# Task 02
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *

# import math
# import random

# global  balls, w_width, w_height, ball_size, ball_speed, pause, blink, boundary_x, boundary_y
# w_width, w_height = 1200, 675   # 16:9
# boundary_x = w_width // 2
# boundary_y = w_height // 2
# balls = []
# ball_size = 10
# ball_speed = 0.1
# pause = False
# blink = False

# class Ball:
#     global boundary_x, boundary_y, ball_size, ball_speed, pause, blink
#     def __init__(self, x = 0, y = 0):
#         self.x = x
#         self.y = y
#         self.color = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
#         self.direction = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
#         self.visible = True

#     def draw(self):
#         if self.visible:
#             glPointSize(ball_size)
#             glBegin(GL_POINTS)
#             glColor3f(self.color[0]/255, self.color[1]/255, self.color[2]/255)
#             glVertex2f(self.x, self.y)
#             glEnd()
    
#     def move(self):
#         if not pause:
#             self.x += self.direction[0] * ball_speed
#             self.y += self.direction[1] * ball_speed
            
#             if abs(self.x) + (ball_size // 2) >= (boundary_x):
#                 self.direction = (-self.direction[0], self.direction[1])
#             if abs(self.y) + (ball_size // 2) >= (boundary_y):
#                 self.direction = (self.direction[0], -self.direction[1])

# def draw_boundary():
#     glLineWidth(5)
#     glBegin(GL_LINES)
#     glColor3f(1, 0, 0)
#     glVertex2f(-boundary_x, -boundary_y)
#     glVertex2f(boundary_x, -boundary_y)
#     glVertex2f(boundary_x, -boundary_y)
#     glVertex2f(boundary_x, boundary_y)
#     glVertex2f(boundary_x, boundary_y)
#     glVertex2f(-boundary_x, boundary_y)
#     glVertex2f(-boundary_x, boundary_y)
#     glVertex2f(-boundary_x, -boundary_y)
#     glEnd()

# def convert_coordinate(x, y):
#     global w_width, w_height
#     a = x - (w_width // 2)
#     b = (w_height // 2) - y 
#     return a, b

# def keyboard_listener(key, x, y):
#     global ball_size, pause, blink
#     if key == b'w':
#         if not pause:
#             ball_size += 1
#             print("Size Increased")
#     elif key == b's':
#         if not pause:
#             if ball_size > 1:
#                 ball_size -= 1
#                 print("Size Decreased")
#             else:
#                 print("Minimum Size Reached")
#     elif key == b' ':
#         pause = not pause
#         if pause:
#             blink = False
#             print("Paused")
#         else:
#             print("Resumed")
#     glutPostRedisplay()

# def special_keyboard_listener(key, x, y):
#     global ball_speed, pause
#     if key == GLUT_KEY_UP:
#         if not pause:
#             ball_speed *= 2
#             print("Speed Increased")
#     elif key == GLUT_KEY_DOWN:
#         if not pause:
#             ball_speed /= 2
#             print("Speed Decreased")
#     glutPostRedisplay()

# def mouse_listener(button, state, x, y):
    
#     # State means if the button is pressed or released
    
#     global balls, blink, pause
    
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         if not pause:
#             print(x, y)
#             x, y = convert_coordinate(x, y)
#             print(x, y)
#             new_ball = Ball(x, y)
#             balls.append(new_ball)
    
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         if not pause:
#             blink = not blink
#             if blink:
#                 blinking()
#                 # glutTimerFunc(100, lambda _: blinking(), 0)
    
#     glutPostRedisplay()
    
# def display():
#     global balls
    
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0,0,0,0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     # gluLookAt(0,0,1000, 0,0,0, 0,1,0)
    
#     for i in balls:
#         i.draw()
#     draw_boundary()
    
#     glutSwapBuffers()
    
# def animate():
#     global balls
    
#     for i in balls:
#         i.move()
#     glutPostRedisplay()

# def blinking():
#     if blink:
#         print("Blinking")
#         for i in balls:
#             i.visible = not i.visible
#         glutTimerFunc(500, lambda _: blinking(), 0)
#     glutPostRedisplay()

# def init():
#     global boundary_x, boundary_y
#     #//clear the screen
#     glClearColor(0,0,0,0)
#     #//load the PROJECTION matrix
#     glMatrixMode(GL_PROJECTION)
#     #//initialize the matrix
#     glLoadIdentity()
#     glOrtho(-boundary_x, boundary_x, -boundary_y, boundary_y, 0, 1)
#     # gluPerspective(100, 1, 1, 1000)

# ball1 = Ball()
# balls.append(ball1)

# glutInit()
# glutInitWindowSize(w_width, w_height)
# glutInitWindowPosition(0, 0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
# glutCreateWindow(b"Ball Game")

# init()
# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutKeyboardFunc(keyboard_listener)
# glutSpecialFunc(special_keyboard_listener)
# glutMouseFunc(mouse_listener)
# glutMainLoop()

# =============================================================================
# |                                  THE END                                    |
# =============================================================================     