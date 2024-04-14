import numpy as np
import glfw
from OpenGL.GL import *

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()
    
def key_callback(window, key, scancode, action, mods):
    # print('key:', key, 'scancode:', scancode, 'action:', action, 'mods:', mods)
    # if key is Q, then translate the triangle by -0.1 in x direction
    if action == 0:
        return
    
    global T, M, O
    M = np.identity(3)
    if key == glfw.KEY_Q:
        M = np.array([[1, 0, -.1],
                      [0, 1, 0.],
                      [0, 0, 1]])
        T = M @ T
    # if key is E, then translate the triangle by 0.1 in x direction
    if key == glfw.KEY_E:
        M = np.array([[1, 0, .1],
                      [0, 1, 0.],
                      [0, 0, 1]])
        T = M @ T
    # if key is A, then rotate the triangle by 10 degrees counter-clockwise in local coordinate
    if key == glfw.KEY_A:
        # rotate
        t = np.radians(10)
        M = np.array([[np.cos(t), -np.sin(t), 0.],
                      [np.sin(t), np.cos(t), 0.],
                      [0., 0., 1.]])
        
        T = T @ M @ np.linalg.inv(T) @ T
        
    # if key is D, then rotate the triangle by 10 degrees clockwise in local coordinate
    if key == glfw.KEY_D:
        t = np.radians(-10)
        M = np.array([[np.cos(t), -np.sin(t), 0.],
                      [np.sin(t), np.cos(t), 0.],
                      [0., 0., 1.]])
        
        T = T @ M @ np.linalg.inv(T) @ T

    # if key is 1, reset the triangle with identity matrix
    if key == glfw.KEY_1:
        T = O.copy()
        M = np.identity(3)
    

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "Hello World", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    global T, M, O

    T = np.array([[1, 0, 0],
                    [0, 1, 0.],
                    [0, 0, 1]])
    
    # save T copy
    O = T.copy()
    
    M = np.identity(3)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(T)        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
    