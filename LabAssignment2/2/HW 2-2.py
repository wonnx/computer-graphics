import glfw
from OpenGL.GL import *
import numpy as np

user_Input=ord('W')
b=np.zeros(100,dtype=int)
for i in range(100):
    b[i]=-1
b[51]=0; b[50]=1; b[49]=2; b[87]=3;
b[81]=4; b[48]=5; b[57]=6; b[56]=7;
b[55]=8; b[54]=9; b[53]=10; b[52]=11; 

def render():
    global user_Input
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    a = np.linspace(0,2*np.pi,13) 
    for i in range(12):
        glVertex2f(np.cos(a[i]),np.sin(a[i]))
    glEnd()
    
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(np.cos(a[b[user_Input]]),np.sin(a[b[user_Input]]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global user_Input
    if b[key]==-1:
        print("User input is out of range! \n")
        return
    user_Input=key

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

