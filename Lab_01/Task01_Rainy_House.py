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
    glBegin(GL_QUADS)
    
    sky_r = 1 * day_time
    sky_g = 1 * day_time
    sky_b = 1 * day_time
    glColor3f(sky_r, sky_g, sky_b)
    
    glVertex2f(-w_width//2, w_height)
    glVertex2f(-w_width//2, -w_height)
    glVertex2f(w_width//2, -w_height)
    glVertex2f(w_width//2, w_height)
    glEnd()
    
    # Ground
    glBegin(GL_QUADS)
    glColor3f(128/255, 89/255, 14/255)
    glVertex2f(-w_width//2, -w_height)
    glVertex2f(-w_width//2, 250)
    glVertex2f(w_width//2, 250)
    glVertex2f(w_width//2, -w_height)
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
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex2f(-150, -150)      # left bottom
    glVertex2f(-150, 100)       # left top
    glVertex2f(150, 100)        # right top
    glVertex2f(150, -150)       # right bottom
    glEnd()

    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(78/255, 23/255, 176/255)
    glVertex2f(0, 300)            # top
    glVertex2f(-200, 100)         # left
    glVertex2f(200, 100)          # right
    glEnd()

    # Door
    glBegin(GL_QUADS)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(-40, -150)
    glVertex2f(-40, 50)
    glVertex2f(40, 50)
    glVertex2f(40, -150)
    glEnd()

    # Window
    glBegin(GL_QUADS)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(-120, -50)
    glVertex2f(-120, 50)
    glVertex2f(-70, 50)
    glVertex2f(-70, -50)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(36/255, 146/255, 255/255)
    glVertex2f(70, -50)
    glVertex2f(70, 50)
    glVertex2f(120, 50)
    glVertex2f(120, -50)
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