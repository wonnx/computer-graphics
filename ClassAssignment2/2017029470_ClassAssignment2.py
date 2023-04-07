import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

Azimuth = np.radians(45)
Elevation = np.radians(45)
distance = 4

eye_x = distance*np.cos(Elevation)*np.sin(Azimuth)
eye_y = distance*np.sin(Elevation)
eye_z = distance*np.cos(Elevation)*np.cos(Azimuth)
at_x = 0;   at_y = 0;   at_z = 0
up_x = 0;   up_y = 1;   up_z = 0
x = 0; y = 0; z = 0; v = 0

solid = 0
smooth = 0
hierachy = 0
f = None
gVertexArray = None
gIndexArray = None

def render():
    global eye_x, eye_y, eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    global gVertexArray, gIndexArray, f
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    if solid == 0: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    elif solid == 1: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if v == 0: gluPerspective(90, 1, 0.01, 300)
    else: glOrtho(-5,5,-5,5,-5,5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    eye_x = at_z + distance*np.cos(Elevation)*np.sin(Azimuth)
    eye_y = at_x + distance*np.sin(Elevation)
    eye_z = at_y + distance*np.cos(Elevation)*np.cos(Azimuth)
    
    gluLookAt(eye_x+x, eye_y+y, eye_z+z, at_x+x, at_y+y, at_z+z, up_x, up_y, up_z)

    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glEnable(GL_NORMALIZE)

    # light intensity for each color channel
    glPushMatrix()
    lightPos0 = (3.,4.,5.,0.)
    lightPos1 = (-3.,-4.,-5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()

    lightColor0 = (1.,0.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    lightColor1 = (1.,1.,1.,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        
    if hierachy == 0:
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        
    else:
        # draw and animate my hierachical model
        t = glfw.get_time()
        th = 30*np.sin(t)
        
        # body
        glPushMatrix()
        glColor3ub(255, 255, 255)
        glRotatef(t*10,0,1,0)
        glTranslatef(0,.2,1.)
        glTranslatef(0,-(1-np.cos(np.radians(th)))*1.4,0)
        glRotatef(90,0,1,0)
        glScalef(.3, .3, .3)
        
        glPushMatrix()
        file = open("body.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        # head
        glPushMatrix()
        file = open("head.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()



        # right upper arm
        glPushMatrix()
        glTranslate(-0.64602, 3.7926, -0.093504)
        glRotate(th, 1,0,0)

        glPushMatrix()
        file = open("right_upper_arm.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()
        
        
        # right lower arm
        glPushMatrix()
        glTranslate(-0.32407, -0.5282, -0.009151)
        glRotate(th,1,0,0)
        
        glPushMatrix()
        file = open("right_lower_arm.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()


        
        # left upper arm
        glPushMatrix()
        glTranslate(0.58935, 3.6902, -0.078766)
        glRotate(-th, 1,0,0)
        
        glPushMatrix()
        file = open("left_upper_arm.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()
        
        # left lower arm
        glPushMatrix()
        glTranslate(0.46025, -0.4819, -0.012963)
        glRotate(-th,1,0,0)
        
        glPushMatrix()
        file = open("left_lower_arm.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()



        # right upper leg
        glPushMatrix()
        glTranslate(0.20353, 2.3647, -0.041216)
        glRotate(-th/2, 1,0,0)
        
        glPushMatrix()
        file = open("right_upper_leg.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        # right lower leg
        glPushMatrix()
        glTranslate(-0.09202, -0.9036, -0.00381)
        glRotate(-th/3,1,0,0)
        
        glPushMatrix()
        file = open("right_lower_leg.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        # right foot
        glPushMatrix()
        glTranslate(-0.06465, -1.22088, -0.045191)
        
        glPushMatrix()
        file = open("right_foot.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        


        # left upper leg
        glPushMatrix()
        glTranslate(-0.19829, 2.3706, -0.017151)
        glRotate(th/2, 1,0,0)
        
        glPushMatrix()
        file = open("left_upper_leg.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        # left lower leg
        glPushMatrix()
        glTranslate(0.09091, -0.9238, -0.032387)
        glRotate(th/3, 1,0,0)
        
        glPushMatrix()
        file = open("left_lower_leg.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()

        # left foot
        glPushMatrix()
        glTranslate(0.07123, -1.20851, -0.061252)
        
        glPushMatrix()
        file = open("left_foot.obj", 'rt')
        gVertexArray, gIndexArray = createArrays(file)
        if smooth==0: drawObject_glDrawArray()
        elif smooth==1: drawObject_glDrawElements()
        glPopMatrix()
        
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

   
        glPopMatrix()
            

    glDisable(GL_LIGHTING)

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def key_callback(window, key, scancode, action, mod):
    global v, smooth, solid, hierachy, gVertexArray, gIndexArray
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V:
            v = (v+1) % 2
        elif key == glfw.KEY_S:
            smooth = (smooth+1) % 2
            gVertexArray, gIndexArray = createArrays(f)
        elif key == glfw.KEY_Z:
            solid = (solid+1) % 2
        elif key == glfw.KEY_H:
            hierachy = (hierachy + 1) % 2
            gVertexArray, gIndexArray = createArrays(f)
            
            


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

def drawObject_glDrawArray():
    global gVertexArray
    varr=gVertexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawObject_glDrawElements():
    global gVertexArray, gIndexArray
    varr=gVertexArray
    iarr=gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


# open an obj file by drag-and-drop to my obj viewer window
three = 0; four = 0; more = 0
def drop_callback(window, paths):
    global f, gVertexArray, gIndexArray
    f = open(paths[0], 'rt')
    gVertexArray, gIndexArray = createArrays(f)
    print('File name: ', paths[0])
    print('Total number of faces: ', three+four+more)
    print('Number of faces with 3 vertices: ', three)
    print('Number of faces with 4 vertices: ', four)
    print('Number of faces with more than 4 vertices: ', more)

def createArrays(f):
    global three, four, more
    varr = np.array([], 'float32')
    vnarr = np.array([], 'float32')
    vniarr = np.array([], 'int32')
    narr = np.array([], 'float32')
    iarr = np.array([], 'int32')
    three = 0; four = 0; more = 0
    
    if f != None:
        f.seek(0)
        while True:
            line = f.readline()
            if not line: break
            if line[0] == 'v':

                # A single vertex's geometric position in space
                if line[1] == ' ':
                    t = (line.split())[1:]
                    for i in range(3):
                        varr = np.append(varr,np.float32(t[i]))

                # vertex normal
                elif line[1] == 'n':
                    t = (line.split())[1:]
                    for i in range(3):
                        vnarr = np.append(vnarr,np.float32(t[i]))

            # vertex & texture & normal
            elif line[0] == 'f':
                t = (line.split())[1:]
                n = (np.array(t)).size
                
                if n == 3: three += 1
                elif n == 4: four += 1
                elif n > 4: more += 1

                for i in range((n-2)*3):
                    if i%3 == 0:
                        k = t[0].find('/')
                        l = t[0][k+1:].find('/')
                        if k != -1:
                            iarr = np.append(iarr,int(t[0][:k])-1)
                            if l != -1:
                                vniarr = np.append(vniarr,int(t[0][k+l+2:])-1)
                    else:
                        k = t[i-2*int(i/3)].find('/')
                        l = t[i-2*int(i/3)][k+1:].find('/')
                        if k != -1:
                            iarr = np.append(iarr,int(t[i-2*int(i/3)][:k])-1)
                            if l != -1:
                                vniarr = np.append(vniarr,int(t[i-2*int(i/3)][k+l+2:])-1)
                        
        varr = varr.reshape(int(varr.size/3),3)
        vnarr = vnarr.reshape(int(vnarr.size/3),3)
        
        if smooth == 0:
            for i in range(iarr.size):
                narr = np.append(narr,vnarr[vniarr[i]])
                narr = np.append(narr,varr[iarr[i]])
        elif smooth == 1:
            vn = np.zeros((int(varr.size/3),3))
            for i in range(vniarr.size): vn[iarr[i]] += vnarr[vniarr[i]]
            for j in vn:
                d = np.sqrt(j[0]**2+j[1]**2+j[2]**2)
                if d == 0: continue
                else: j /= np.sqrt(j[0]**2+j[1]**2+j[2]**2)
            for k in range(int(varr.size/3)):
                narr = np.append(narr,np.float32(vn[k]))
                narr = np.append(narr,varr[k])

    return narr, iarr
        
        

def main():
    global gVertexArray, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Class Assignment 2", None, None)

    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    gVertexArray, gIndexArray = createArrays(f)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render()

    if f != None: f.close()
    glfw.terminate()

if __name__ == "__main__":
    main()
