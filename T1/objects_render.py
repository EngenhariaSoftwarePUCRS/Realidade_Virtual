import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from typing import Tuple

from points import Point3D

# Initial cube and sphere positions
cube_pos = Point3D(-2, 0, 0)
sphere_pos = Point3D(2, 0, 0)


def init(display: Tuple[int, int] = (800, 600)) -> None:
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 100.0) 
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5)


def draw_cube(    
    center_pos: Point3D,
    size: float = 1.0,
    color: Tuple[float, float, float] = (1, 1, 1),
):
    """Draws a cube at the specified center position with a given size and color."""
    half_size = size / 2.0  # To center the cube on center_pos
    center_pos = center_pos.to_list()

    glPushMatrix()
    glTranslatef(*center_pos)
    glColor3fv(color)
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-half_size, -half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    # Top face
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    # Right face
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f( half_size,  half_size,  half_size)
    glVertex3f( half_size, -half_size,  half_size)
    # Back face
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size,  half_size, -half_size)
    glVertex3f(-half_size,  half_size, -half_size)
    # Left face
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size,  half_size, -half_size)
    glVertex3f(-half_size,  half_size,  half_size)
    glVertex3f(-half_size, -half_size,  half_size)
    # Bottom face
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size, -half_size)
    glVertex3f( half_size, -half_size,  half_size)
    glVertex3f(-half_size, -half_size,  half_size)
    glEnd()
    glPopMatrix()


def draw_sphere(
    center_pos: Point3D,
    size: int = 1,
    color: Tuple[float, float, float] = (1, 1, 1),
):
    """Draws a sphere at the specified center position with a given size and color."""
    center_pos = center_pos.to_list()
    
    glPushMatrix()
    glTranslatef(*center_pos)
    glColor3fv(color)
    quad = gluNewQuadric()
    gluSphere(quad, size, 32, 32)
    glPopMatrix()


def move_cube(cube_pos):
    """
    Moves the cube using WASD keys.
    Updates the cube's position in the cube_pos list.
    """
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        cube_pos[1] += 0.1  # Move up
    if keys[K_s]:
        cube_pos[1] -= 0.1  # Move down
    if keys[K_a]:
        cube_pos[0] -= 0.1  # Move left
    if keys[K_d]:
        cube_pos[0] += 0.1  # Move right


def move_sphere(sphere_pos):
    """
    Moves the sphere using arrow keys.
    Updates the sphere's position in the sphere_pos list.
    """
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        sphere_pos[1] += 0.1  # Move up
    if keys[K_DOWN]:
        sphere_pos[1] -= 0.1  # Move down
    if keys[K_LEFT]:
        sphere_pos[0] -= 0.1  # Move left
    if keys[K_RIGHT]:
        sphere_pos[0] += 0.1  # Move right


def main():
    init()
    global cube_pos, sphere_pos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                move_cube(cube_pos)
                move_sphere(sphere_pos)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(cube_pos, 1, (1, 0, 0))
        draw_sphere(sphere_pos, 1, (0, 0, 1))

        glRotatef(1, 3, 1, 1)
        
        pygame.time.wait(10)
        pygame.display.flip()

if __name__ == "__main__":
    main()
