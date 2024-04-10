import numpy as np
import glfw
from OpenGL.GL import *

ptype = GL_LINE_LOOP

def render_dodecagon(ptype):
    th = np.radians(30)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(ptype)
    glColor3f(255, 255, 255)
    for i in range(12):
        glVertex2fv([np.cos(i*th), np.sin(i*th)])
    
    glEnd()
    
def key_callback(window, key, scancode, action, mods):
    # if key >= 48 and key <= 57:
    #     global ptype
    #     ptype = (key - 49) % 10
    global ptype
    if key == glfw.KEY_1:
        ptype = GL_POINTS
    elif key == glfw.KEY_2:
        ptype = GL_LINES
    elif key == glfw.KEY_3:
        ptype = GL_LINE_STRIP
    elif key == glfw.KEY_4:
        ptype = GL_LINE_LOOP
    elif key == glfw.KEY_5:
        ptype = GL_TRIANGLES
    elif key == glfw.KEY_6:
        ptype = GL_TRIANGLE_STRIP
    elif key == glfw.KEY_7:
        ptype = GL_TRIANGLE_FAN
    elif key == glfw.KEY_8:
        ptype = GL_QUADS
    elif key == glfw.KEY_9:
        ptype = GL_QUAD_STRIP
    elif key == glfw.KEY_0:
        ptype = GL_POLYGON


    print("ptype: ", ptype)
    
def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "Hello World", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render_dodecagon(ptype)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
    