import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

Azimuth = np.radians(45)
Elevation = np.radians(45)
distance = 2

eye_x = distance*np.cos(Elevation)*np.sin(Azimuth)
eye_y = distance*np.sin(Elevation)
eye_z = distance*np.cos(Elevation)*np.cos(Azimuth)
at_x = 0;   at_y = 0;   at_z = 0
up_x = 0;   up_y = 1;   up_z = 0

x = 0; y = 0; z = 0; v = 0;


def render():
    global eye_x, eye_y, eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLoadIdentity()
    
    if v == 0:
        gluPerspective(90, 1, 0.01, 300)
    else:
        glOrtho(-5,5,-5,5,-5,5)

    eye_x = at_z + distance*np.cos(Elevation)*np.sin(Azimuth)
    eye_y = at_x + distance*np.sin(Elevation)
    eye_z = at_y + distance*np.cos(Elevation)*np.cos(Azimuth)
    
    gluLookAt(eye_x+x, eye_y+y, eye_z+z, at_x+x, at_y+y, at_z+z, up_x, up_y, up_z)

    drawFrame()
    glColor3ub(255,255,255)
    drawCubeArray()

def key_callback(window, key, scancode, action, mod):
    global v
    if key == glfw.KEY_V:
        if action == glfw.PRESS or action == glfw.REPEAT:
            v = (v+1)%2


def cursor_callback(window, xpos, ypos):
    global up_y, Elevation, Azimuth, x, y, z

    dx = (pos[0] - xpos)*0.0001
    dy = (pos[1] - ypos)*0.0001
    
    if flag == 1:
        if up_y == 1:
            Azimuth += dx
            Elevation -= dy
        else:
            Azimuth += -dx
            Elevation -= dy
        if np.cos(Elevation) < 0:
            up_y = -1
        else:
            up_y = 1
            
    elif flag == 2:
        eye = np.array([eye_x, eye_y, eye_z])
        at = np.array([at_x, at_y, at_z])
        up = np.array([up_x, up_y, up_z])
        w = (eye-at)/(np.sqrt(np.dot(eye-at,eye-at)))
        u = (np.cross(up,w))/(np.sqrt(np.dot(np.cross(up,w),np.cross(up,w))))
        v = np.cross(w,u)

        x += dx*u[0] - dy*v[0]
        y += dx*u[1] - dy*v[1]
        z += dx*u[2] - dy*v[2]


def set_cursor_none(window, xpos, ypos):
    return None


def mouse_button_callback(window, button, action, mod):
    global pos, flag
    
    # Orbit
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            flag = 1
            pos = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback)          
        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, set_cursor_none)
            
    # Panning
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            flag = 2
            pos = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback)
        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, set_cursor_none)


def scroll_callback(window, xoffset, yoffset):
    global distance
    
    # Zooming
    if yoffset > 0:
        distance -= .1*distance
    else:
        distance += .1*distance


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    # Draw a rectangular grid with lines on xz plane.
    for i in range(21):
        glBegin(GL_LINES)
        glColor3ub(120, 120, 120)
        glVertex3fv(np.array([-2., 0, -2.+(i*.2)]))
        glVertex3fv(np.array([2., 0, -2.+(i*.2)]))
        glVertex3fv(np.array([-2.+(i*.2), 0., -2.]))
        glVertex3fv(np.array([-2+(i*.2), 0., 2.]))
        glEnd()


def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()


def drawCubeArray():
    for i in range(2):
        for j in range(2):
            for k in range(2):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Class Assignment 1", None, None)

    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render()
        
    glfw.terminate()

if __name__ == "__main__":
    main()
