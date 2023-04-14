import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

Azimuth = np.radians(45)
Elevation = np.radians(30)
distance = 8

eye_x = distance*np.cos(Elevation)*np.sin(Azimuth)
eye_y = distance*np.sin(Elevation)
eye_z = distance*np.cos(Elevation)*np.cos(Azimuth)
at_x = 0;   at_y = 0;   at_z = 0
up_x = 0;   up_y = 1;   up_z = 0
x = 0; y = 0; z = 0; v = 0;

tmp = 0
fname = ''
scale = 1
offset = []
drawing = 0


def render():
    global eye_x, eye_y, eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if v == 0: gluPerspective(90, 1, 0.01, 1000)
    else: glOrtho(-5,5,-5,5,-5,5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    eye_x = at_z + distance*np.cos(Elevation)*np.sin(Azimuth)
    eye_y = at_x + distance*np.sin(Elevation)
    eye_z = at_y + distance*np.cos(Elevation)*np.cos(Azimuth)
    gluLookAt(eye_x+x, eye_y+y, eye_z+z, at_x+x, at_y+y, at_z+z, up_x, up_y, up_z)
    drawFrame()

    glColor3ub(255,255,255)
    
    if fname == 'sample-walk.bvh':
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glEnable(GL_RESCALE_NORMAL)
        
        # light intensity for each color channel
        glPushMatrix()
        lightPos = (3.,3.,3.,0.)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glPopMatrix()
        
        lightColor = (1.,1.,1.,1.)
        ambientLightColor = (.1,.1,.1,1.)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

        # material reflectance for each color channel
        objectColor = (0.3,0.3,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        glPushMatrix()

    global tmp
    if drawing == 0: drawHierarchy()
    elif drawing == 1:
        drawMotionHierarchy(tmp)
        tmp += 1
        if tmp >= len(frame)/(len(name_joint) + 1):
            tmp = 0
            offset[0][0] = 0
            offset[0][1] = 0
            offset[0][2] = 0
        
    if fname == 'sample-walk.bvh':
        glPopMatrix()
        glDisable(GL_LIGHTING)


def key_callback(window, key, scancode, action, mod):
    global v, drawing
    if key == glfw.KEY_V:
        if action == glfw.PRESS or action == glfw.REPEAT:
            v = (v+1)%2
    if key == glfw.KEY_SPACE:
        if action == glfw.PRESS or action == glfw.REPEAT:
            drawing = (drawing+1)%2

def drop_callback(window, paths):
    global drawing, tmp
    global fname, name_joint, offset, num_channel, channel, check_end, cnt, motion, num_frame, fps, frame
    f = open(paths[0],'rt')
    fname = os.path.basename(paths[0])
    
    name_joint = []     # name of joint
    offset = []
    num_channel = 0     # total number of channels
    channel = []
    check_end = 0
    cnt = 0             # count the number of '}'
    motion = 0          # checking motion frame
    num_frame = 0       # number of frames
    fps = 0             # FPS
    frame = []
    drawing = 0
    tmp = 0
    
    while True:
        line = f.readline()
        if not line: break
        parse(line)
    f.close()

    print('Filename: ' + fname)
    print('Number of frames: ' + num_frame)
    print('FPS: ' + str(1/float(fps)))
    print('Number of joints: ' + str(len(name_joint)))
    print('List of all joint names: ' + str(name_joint) + '\n')
    
    global scale
    scale = max(max(offset))
    if scale > 5:
        for i in range (len(offset)):
            if len(offset[i]) == 3:
                for j in range (3):
                    offset[i][j]/=scale
    else: scale = 1


def parse(line):
    global offset, num_channel, name_joint, num_frame, fps, cnt, check_end, motion, frame
    line = line.split()
    if 'ROOT' in line: name_joint.append(line[1])
    elif 'OFFSET' in line: offset.append(([float(line[1]),float(line[2]),float(line[3])]))
    elif 'CHANNELS' in line:
        num_channel += int(line[1])
        if int(line[1]) == 3:
            for i in range(3): channel.append([line[2],line[3],line[4]])
        elif int(line[1]) == 6:
            for i in range(3): channel.append([line[5],line[6],line[7]])
    elif 'JOINT' in line:
        if check_end == 1:
            offset.append([cnt])
            cnt = 0; check_end = 0
        name_joint.append(line[1])
    elif 'End' in line: check_end = 1
    elif '{' in line: pass
    elif '}' in line: cnt += 1
    elif 'MOTION' in line: motion = 1
    elif 'Frames:' in line: num_frame = line[1]
    elif 'Frame' in line: fps = line[2]
    else:
        if motion == 1:
            for i in range(0, len(line),3):
                frame.append([float(line[i]), float(line[i+1]), float(line[i+2])])


def drawHierarchy():    
    global offset, fname, gVertexArraySeparate
    glColor3ub(80,80,255)
    
    check = 0; popcnt = 0; pushcnt = 0
    
    for i in range(1, len(offset)):
        if len(offset[i]) == 1:
            for j in range(offset[i][0] - 1):
                glPopMatrix()
                i += 1; check = 1; popcnt += 1
        else:
            if check == 0:
                pushcnt += 1
                glPushMatrix()
                glTranslatef(offset[i-1][0], offset[i-1][1], offset[i-1][2])
                glPushMatrix()
                if fname == 'sample-walk.bvh':
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/4, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0: a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0, offset[i][1]/4, 0)
                        b = abs(offset[i][1])/2
                        if b == 0: b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/4)
                        c = abs(offset[i][2])/2
                        if c == 0: c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    glBegin(GL_LINES)
                    glVertex3fv([0,0,0])
                    glVertex3fv(offset[i])
                    glEnd()
                    glPopMatrix()        
            elif check == 1:
                check = 0
                if fname == 'sample-walk.bvh':
                    glPushMatrix()
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/4, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0: a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/4, 0)
                        b = abs(offset[i][1])/2
                        if b == 0: b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/4)
                        c = abs(offset[i][2])/2
                        if c == 0: c = .03
                        a = b = .03
                    gVertexArraySeparate = createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    glBegin(GL_LINES)
                    glVertex3fv([0,0,0])
                    glVertex3fv(offset[i])
                    glEnd()
                    
    for i in range(pushcnt - popcnt):
        glPopMatrix()


def drawMotionHierarchy(k):
    global offset, fname, gVertexArraySeparate
    glColor3ub(80,80,255)
    
    check = 0; popcnt = 0; pushcnt = 0; endcnt = 0
    
    glPushMatrix()
    glTranslatef(frame[k*(len(name_joint)+1)][0]/scale,frame[k*(len(name_joint)+1)][1]/scale,frame[k*(len(name_joint)+1)][2]/scale)
    
    for i in range(1, len(offset)):
        if len(offset[i]) == 1:
            endcnt+=1
            for j in range(offset[i][0] - 1):
                glPopMatrix()
                i += 1; check = 1; popcnt += 1
        else:
            if check == 0:
                pushcnt += 1
                glPushMatrix()
                glTranslatef(offset[i-1][0], offset[i-1][1], offset[i-1][2])    
                Rotation(i,i-endcnt+k*int(len(name_joint)+1))
                glPushMatrix()
                if fname == 'sample-walk.bvh':
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/3, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0: a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/3, 0)
                        b = abs(offset[i][1])/2
                        if b == 0: b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/3)
                        c = abs(offset[i][2])/2
                        if c == 0: c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    glBegin(GL_LINES)
                    glVertex3fv([0,0,0])
                    glVertex3fv(offset[i])
                    glEnd()
                    glPopMatrix()
                    
            elif check == 1:
                check = 0
                endcnt += 1
                if fname == 'sample-walk.bvh':
                    glPushMatrix()
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/3, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0: a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/3, 0)
                        b = abs(offset[i][1])/2
                        if b == 0: b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/3)
                        c = abs(offset[i][2])/2
                        if c == 0: c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    glBegin(GL_LINES)
                    glVertex3fv([0,0,0])
                    glVertex3fv(offset[i])
                    glEnd()
                    
    for i in range(pushcnt - popcnt):
        glPopMatrix()

    glPopMatrix()


def Rotation(i, num):
    global channel, frame
    if 'Z' in channel[i][0] and 'X' in channel[i][1] and 'Y' in channel[i][2]:
        glRotatef(frame[num][0], 0, 0, 1)
        glRotatef(frame[num][1], 1, 0, 0)
        glRotatef(frame[num][2], 0, 1, 0)
    elif 'Z' in channel[i][0] and 'Y' in channel[i][1] and 'X' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 0, 1)
        glRotatef(frame[num][1], 0, 1, 0)
        glRotatef(frame[num][2], 1, 0, 0)
    elif 'Y' in channel[i][0] and 'X' in channel[i][1] and 'Z' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 1, 0)
        glRotatef(frame[num][1], 1, 0, 0)
        glRotatef(frame[num][2], 0, 0, 1)
    elif 'Y' in channel[i][0] and 'Z' in channel[i][1] and 'X' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 1, 0)
        glRotatef(frame[num][1], 0, 0, 1)
        glRotatef(frame[num][2], 1, 0, 0)
    elif 'X' in channel[i][0] and 'Y' in channel[i][1] and 'Z' in channel[i][2]:    
        glRotatef(frame[num][0], 1, 0, 0)
        glRotatef(frame[num][1], 0, 1, 0)
        glRotatef(frame[num][2], 0, 0, 1)
    elif 'X' in channel[i][0] and 'Z' in channel[i][1] and 'Y' in channel[i][2]:    
        glRotatef(frame[num][0], 1, 0, 0)
        glRotatef(frame[num][1], 0, 0, 1)
        glRotatef(frame[num][2], 0, 1, 0)

    
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
        if np.cos(Elevation) < 0: up_y = -1
        else: up_y = 1
            
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
    if yoffset > 0: distance -= .1*distance
    else: distance += .1*distance


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
    for i in range(100):
        glBegin(GL_LINES)
        glColor3ub(120, 120, 120)
        glVertex3fv(np.array([-10., 0, -10.+(i*.2)]))
        glVertex3fv(np.array([10., 0, -10.+(i*.2)]))
        glVertex3fv(np.array([-10.+(i*.2), 0., -10.]))
        glVertex3fv(np.array([-10+(i*.2), 0., 10.]))
        glEnd()


def createVertexArraySeparate(a, b, c):
    varr = np.array([
            (0,0,1),         # v0 normal
            ( -a ,  b ,  c ), # v0 position
            (0,0,1),         # v2 normal
            (  a , -b ,  c ), # v2 position
            (0,0,1),         # v1 normal
            (  a ,  b ,  c ), # v1 position

            (0,0,1),         # v0 normal
            ( -a ,  b ,  c ), # v0 position
            (0,0,1),         # v3 normal
            ( -a , -b ,  c ), # v3 position
            (0,0,1),         # v2 normal
            (  a , -b ,  c ), # v2 position

            (0,0,-1),
            ( -a ,  b , -c ), # v4
            (0,0,-1),
            (  a ,  b , -c ), # v5
            (0,0,-1),
            (  a , -b , -c ), # v6

            (0,0,-1),
            ( -a ,  b , -c ), # v4
            (0,0,-1),
            (  a , -b , -c ), # v6
            (0,0,-1),
            ( -a , -b , -c ), # v7

            (0,1,0),
            ( -a ,  b ,  c ), # v0
            (0,1,0),
            (  a ,  b ,  c ), # v1
            (0,1,0),
            (  a ,  b , -c ), # v5
            
            (0,1,0),
            ( -a ,  b ,  c ), # v0
            (0,1,0),
            (  a ,  b , -c ), # v5
            (0,1,0),
            ( -a ,  b , -c ), # v4

            (0,-1,0),
            ( -a , -b ,  c ), # v3
            (0,-1,0),
            (  a , -b , -c ), # v6
            (0,-1,0),
            (  a , -b ,  c ), # v2

            (0,-1,0),
            ( -a , -b ,  c ), # v3
            (0,-1,0),
            ( -a , -b , -c ), # v7
            (0,-1,0),
            (  a , -b , -c ), # v6

            (1,0,0),
            (  a ,  b ,  c ), # v1
            (1,0,0),
            (  a , -b ,  c ), # v2
            (1,0,0),
            (  a , -b , -c ), # v6

            (1,0,0),
            (  a ,  b ,  c ), # v1
            (1,0,0),
            (  a , -b , -c ), # v6
            (1,0,0),
            (  a ,  b , -c ), # v5

            (-1,0,0),
            ( -a ,  b ,  c ), # v0
            (-1,0,0),
            ( -a , -b , -c ), # v7
            (-1,0,0),
            ( -a , -b ,  c ), # v3

            (-1,0,0),
            ( -a ,  b ,  c ), # v0
            (-1,0,0),
            ( -a ,  b , -c ), # v4
            (-1,0,0),
            ( -a , -b , -c ), # v7
            ], 'float32')
    return varr


def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))


gVertexArraySeparate = None
def main():
    global gVertexArraySeparate
    
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Class Assignment 3", None, None)

    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render()
        
    glfw.terminate()

if __name__ == "__main__":
    main()
