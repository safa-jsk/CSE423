from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

global  balls, w_width, w_height, ball_size, ball_speed, pause, blink, boundary_x, boundary_y
w_width, w_height = 1200, 675   # 16:9
boundary_x = w_width // 2
boundary_y = w_height // 2
balls = []
ball_size = 10
ball_speed = 0.1
pause = False
blink = False

class Ball:
    global boundary_x, boundary_y, ball_size, ball_speed, pause, blink
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.color = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        self.direction = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        self.visible = True

    def draw(self):
        if self.visible:
            glPointSize(ball_size)
            glBegin(GL_POINTS)
            glColor3f(self.color[0]/255, self.color[1]/255, self.color[2]/255)
            glVertex2f(self.x, self.y)
            glEnd()
    
    def move(self):
        if not pause:
            self.x += self.direction[0] * ball_speed
            self.y += self.direction[1] * ball_speed
            
            if abs(self.x) + (ball_size // 2) >= (boundary_x):
                self.direction = (-self.direction[0], self.direction[1])
            if abs(self.y) + (ball_size // 2) >= (boundary_y):
                self.direction = (self.direction[0], -self.direction[1])

def draw_boundary():
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex2f(-boundary_x, -boundary_y)
    glVertex2f(boundary_x, -boundary_y)
    glVertex2f(boundary_x, -boundary_y)
    glVertex2f(boundary_x, boundary_y)
    glVertex2f(boundary_x, boundary_y)
    glVertex2f(-boundary_x, boundary_y)
    glVertex2f(-boundary_x, boundary_y)
    glVertex2f(-boundary_x, -boundary_y)
    glEnd()

def convert_coordinate(x, y):
    global w_width, w_height
    a = x - (w_width // 2)
    b = (w_height // 2) - y 
    return a, b

def keyboard_listener(key, x, y):
    global ball_size, pause, blink
    if key == b'w':
        if not pause:
            ball_size += 1
            print("Size Increased")
    elif key == b's':
        if not pause:
            if ball_size > 1:
                ball_size -= 1
                print("Size Decreased")
            else:
                print("Minimum Size Reached")
    elif key == b' ':
        pause = not pause
        if pause:
            blink = False
            print("Paused")
        else:
            print("Resumed")
    glutPostRedisplay()

def special_keyboard_listener(key, x, y):
    global ball_speed, pause
    if key == GLUT_KEY_UP:
        if not pause:
            ball_speed *= 2
            print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        if not pause:
            ball_speed /= 2
            print("Speed Decreased")
    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    
    # State means if the button is pressed or released
    
    global balls, blink, pause
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not pause:
            print(x, y)
            x, y = convert_coordinate(x, y)
            print(x, y)
            new_ball = Ball(x, y)
            balls.append(new_ball)
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not pause:
            blink = not blink
            if blink:
                blinking()
                # glutTimerFunc(100, lambda _: blinking(), 0)
    
    glutPostRedisplay()
    
def display():
    global balls
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # gluLookAt(0,0,1000, 0,0,0, 0,1,0)
    
    for i in balls:
        i.draw()
    draw_boundary()
    
    glutSwapBuffers()
    
def animate():
    global balls
    
    for i in balls:
        i.move()
    glutPostRedisplay()

def blinking():
    if blink:
        print("Blinking")
        for i in balls:
            i.visible = not i.visible
        glutTimerFunc(500, lambda _: blinking(), 0)
    glutPostRedisplay()

def init():
    global boundary_x, boundary_y
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    glOrtho(-boundary_x, boundary_x, -boundary_y, boundary_y, 0, 1)
    # gluPerspective(100, 1, 1, 1000)

ball1 = Ball()
balls.append(ball1)

glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Ball Game")

init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_keyboard_listener)
glutMouseFunc(mouse_listener)
glutMainLoop()