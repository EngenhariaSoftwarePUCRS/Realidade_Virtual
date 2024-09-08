import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


display = (800, 600)


def init():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5)


def draw_cube(center_pos, color):
    glPushMatrix()
    glTranslatef(*center_pos)
    glColor3fv(color)
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Top face
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Right face
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    # Back face
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    # Left face
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    # Bottom face
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glEnd()
    glPopMatrix()


def draw_sphere(center_pos, color):
    glPushMatrix()
    glTranslatef(*center_pos)
    glColor3fv(color)
    quad = gluNewQuadric()
    gluSphere(quad, 1, 32, 32)
    glPopMatrix()


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube((-2, 0, 0), (1, 0, 0))
        draw_sphere((2, 0, 0), (0, 0, 1))
        glRotatef(1, 3, 1, 1)
        
        pygame.time.wait(10)
        pygame.display.flip()

if __name__ == "__main__":
    main()
