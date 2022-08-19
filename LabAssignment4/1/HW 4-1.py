import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

key_input=['']

def drawTriangle():
    # p1=(0,.5,0), p2=(0,0,0), p3=(.5,0,0)
    glBegin(GL_TRIANGLES)
    glVertex3fv(np.array([.0,.5,0.]))
    glVertex3fv(np.array([.0,.0,0.]))
    glVertex3fv(np.array([.5,.0,0.]))
    glEnd()

def render():
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

    glColor3ub(255, 255, 255)
    for i in reversed(key_input):
        if i=='Q':
            glTranslatef(-.1,0,0)
        if i=='E':
            glTranslatef(.1,0,0)
        if i=='A':
            glRotate(10,0,0,1)
        if i=='D':
            glRotate(-10,0,0,1)
        if i=='1':
            key_input.clear()
            

    drawTriangle()

def key_callback(window, key, scancode, action, mods):
    global key_input
    if key==glfw.KEY_Q:
        if action==glfw.PRESS or action==glfw.REPEAT:
            key_input.append('Q')
    if key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            key_input.append('E')
    if key==glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            key_input.append('A')
    if key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            key_input.append('D')
    if key==glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            key_input.append('1')
            

def main():
    
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029470", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
if __name__ == "__main__":
  main()

