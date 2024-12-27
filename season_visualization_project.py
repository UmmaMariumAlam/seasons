from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from math import cos, sin, pi


W_Width, W_Height = 500,500
season = 0 #0 - winter, 1 - summer, 2 - rainy

#---------winter var--------
snowflakes = []
xsnow = ysnow = 0
snow_speed = 2
snowing = True
lightsize = 5

#--------rainy-------
rain_speed = 7
raindrops = []

#--------summer------
sun_y = -150
rays_enabled = False
cloud_x = 0

#-----------------general functions------------------
def findZone(x1,y1,x2,y2):
   dx = x2 - x1
   dy = y2 - y1
   zone = ''
   if abs(dx) > abs(dy):
       if (dx >= 0) and (dy >= 0):
           zone = '0'
       elif (dx >= 0) and (dy <= 0):
           zone = '7'
       elif (dx <= 0) and (dy >= 0):
           zone = '3'
       else:
           zone = '4'
   else:
       if (dx >= 0) and (dy >= 0):
           zone = '1'
       elif (dx >= 0) and (dy <= 0):
           zone = '6'
       elif (dx <= 0) and (dy >= 0):
           zone = '2'
       else:
           zone = '5'
   return zone

def originalToZero(zone, x,y):
   if zone == '0':
       return x,y
   elif zone == '1':
       return y,x
   elif zone == '2':
       return -y,x
   elif zone == '3':
       return -x,y
   elif zone == '4':
       return -x,-y
   elif zone == '5':
       return -y,-x
   elif zone == '6':
       return -y,x
   else:
       return x,-y

def zeroToOriginal(zone, x,y):
   if zone == '0':
       return x,y
   elif zone == '1':
       return y,x
   elif zone == '2':
      return -y,x
   elif zone == '3':
      return -x,y
   elif zone == '4':
      return -x,-y
   elif zone == '5':
      return -y,-x
   elif zone == '6':
       return y,-x
   else:
       return x,-y

def midpointLine(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    s_x1, s_y1 = originalToZero(zone,x1,y1)
    e_x2, e_y2 = originalToZero(zone,x2,y2)
  
    dx = e_x2 - s_x1
    dy = e_y2 - s_y1

    d = 2*dy - dx
    dne = 2*dy - 2*dx
    de = 2*dy 
       
    x = s_x1
    y = s_y1 
   # glPointSize(3) 
    glBegin(GL_POINTS)
    while (x < e_x2): 
        #glColor3f(1,1,1)
        ori_x,ori_y = zeroToOriginal(zone,x,y) 
    
        glVertex2f(ori_x, ori_y)
        if (d <= 0):             
            d += de 
            x += 1
        else:
            d += dne
            y += 1
            x += 1
    glEnd()


def draw_house_filled():
    try:
        # Fill the base of the house with brown color
        glColor3f(0.6, 0.3, 0.1)  # Brown color
        for y in range(-150, -100):
            midpointLine(-100, y, -50, y)
        for y in range(-150, -20):
            midpointLine(-50, y, 30, y)
        for y in range(-150, -50):
            midpointLine(30, y, 100, y)

        # Fill the roof of the house
        glColor3f(0.6,0.3,0.1)  # Darker brown color
        for y in range(-100, -50):
            x1 = -100+(y + 100)
            x2 = -50+(y + 100)

            midpointLine(x1, y, x2, y)

        for y in range(-80, 0):
            x1 = -100+(y + 100)
            x2 = -100+(y + 100)
            midpointLine(x1, y, x2, y)


        # Fill the door
        glColor3f(0.3, 0.1, 0.05)  # Dark brown color
        for y in range(-150, -110):
            midpointLine(-25, y, -5, y)

        # Draw the door knob
        glColor3f(1, 0, 0)  # Red color for the door knob
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex2f(-10, -130)
        glEnd()

        # Draw the windows
        glColor3f(1, 1, 0)  # Yellow color for the windows
        xd1, xd2 = 40, 74
        x_mid = 57
        yd1, yd2 = -100, -80
        y_mid = -90
        midpointLine(xd1, yd1, xd2, yd1)
        midpointLine(xd1, yd2, xd2, yd2)
        midpointLine(x_mid, yd1, x_mid, yd2)
        midpointLine(xd1, yd1, xd1, yd2)
        midpointLine(xd2, yd1, xd2, yd2)
        midpointLine(xd1, y_mid, xd2, y_mid)

        # Outline the house as before
        glColor3f(0, 0, 1)
        midpointLine(-100, -150, 100, -150)
        glColor3f(0.43, 0.15, 0.05)
        midpointLine(-100, -100, -50, -50)
        midpointLine(-100, -110, -50, -60)
        midpointLine(-100, -100, -100, -110)
        glColor3f(0, 0, 1)
        midpointLine(-100, -150, -100, -110)
        midpointLine(-50, -20, -50, -150)
        glColor3f(0.43, 0.15, 0.05)
        midpointLine(-55, -25, -10, 35)
        midpointLine(-55, -10, -10, 50)
        midpointLine(-55, -25, -55, -10)
        midpointLine(35, -10, 35, -25)
        midpointLine(-10, 35, 35, -25)
        midpointLine(-10, 50, 35, -10)
        midpointLine(30, 0, 90, 0)
        midpointLine(110, -50, 30, -50)
        midpointLine(90, 0, 110, -50)
        glColor3f(0, 0, 1)
        midpointLine(30, -150, 30, -20)
        midpointLine(100, -51, 100, -150)
        glColor3f(1, 0, 0)
        midpointLine(-25, -150, -25, -110)
        midpointLine(-25, -110, -5, -110)
        midpointLine(-5, -110, -5, -150)
    except Exception as e:
        print(f"Error in draw_house_filled: {e}")


def midpointCircle(center_x, center_y, r): #fulfills the octant or zone
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        circle_symmetry(center_x, center_y,x,y)
        if d >= 0:
            d = d + 2*x - 2*y +5
            x += 1
            y -= 1
        else:
            d = d + 2*x + 3
            x += 1

def circle_symmetry(xc, yc, x, y):#for each point in zone 1, it creates points in other 7 zones
    points = [(x+xc,y+yc),
              (y+xc, x+yc),
              (-x+xc,y+yc),
              (-y+xc,x+yc),
              (-y+xc,-x+yc),
              (-x+xc,-y+yc),
              (x+xc,-y+yc),             
              (y+xc,-x+yc)] 
    glBegin(GL_POINTS)          
    for px, py in points:
        glVertex2f(px,py)
    glEnd()

def circleFilled(xc,yc,r):
    glBegin(GL_POINTS)
    for y in range(-r,r+1):
        x_range = int((r**2-y**2)**0.5) #x = sqr.root(r^2 - y^2)
        for x in range(-x_range,x_range+1):
            glVertex(xc+x,xc+y)
    glEnd()
            
def field():
    glPointSize(2)
    glBegin(GL_POINTS)
  
    y = -120
    while y>=-250:   #house left
        for x in range(-250,-101):
            glVertex2f(x,y)
        y -= 1
    y = -150
    while y>=-250: #house down
        for x in range(-100,101):
            glVertex2f(x,y)
        y -= 1
    y = -121
    while y>=-250: #house right
        for x in range(100,250):
            glVertex2f(x,y)
        y -= 1
    glEnd()

def rectangle_filled(x1,y1,x2,y2,x_except = [],y_except = []):
    y = y1
    glColor3f(0,1,0)
    while y<= y2:
        for x in range(x1+1,x2):
            if len(x_except) != 0 and len(y_except) != 0:
               # print(x_except)           
                if (x_except[0] <= x <= x_except[1] and y_except[0] <= y <= y_except[1]):
                    print('last if clause',x,y)
                    continue
            midpointLine(x,y,x2,y)
        y += 1


#-------------winter specific functions--------

def snowman():
    glColor3f(1,1,1)
    #head
    hr = 10
    while hr>=0:
        midpointCircle(180,-80,hr)
        hr -= 1
    #body
    br = 25
    while br>=0:
        midpointCircle(180,-115,br)
        br -= 1
    #eyes
    glColor3f(0,0,0)
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(173,-75)
    glVertex2f(187,-75)
    glEnd()
    #nose
    glColor3f(1,0.6,0)
    midpointLine(180,-80,165,-80)
    #hands
    glColor3f(0.5,0.3,0.1)#right
    midpointLine(200,-110,215,-110)
    midpointLine(160,-110,145,-110)#left

def lightstand():
    global lightsize
    glColor3f(0.8,0.4,0.1)
    glPointSize(1)
    midpointLine(-200,-90,-200,-155)#right
    midpointLine(-120,-90,-120,-155)#left
    midpointLine(-200,-90,-160,-95)#joining
    midpointLine(-160,-95,-120,-90)
    x = -120
    glColor3f(1,0.9,0)
    glPointSize(lightsize)
    glBegin(GL_POINTS)
    for i in range(5):
        if i%2 != 0:
            y = -92
        elif i == 2: 
            y = -94
        else: 
            y = -89
        glVertex2f(x-16,y)
        x -= 13
    glEnd()

def init_snow():
    global snowflakes,snowing
    y = 250
    if snowing:
        for x in range(2):   
            y_random = random.randint(0,10)
            snowflakes.append([random.randint(-250,250),(y - y_random)])

def snow_drawing():
    glColor3f(1, 1, 1) 
    glPointSize(2)
    glBegin(GL_POINTS)
    for snows in snowflakes:
        glVertex2f(snows[0], snows[1])                               
    glEnd()


def snow_fall_updates():
    global xsnow,ysnow,snow_speed,snowflakes,snowing
    if len(snowflakes) >= 1000:
        snowflakes[:] = snowflakes[:999]
 
    for snow in snowflakes:
        snow[1] = (snow[1]-snow_speed)
        if snow[1] <= -120 and snowing:
            snow[1] = 250
        elif snow[1] <= -120 and not snowing:
            snowflakes.remove(snow)
 
    glutPostRedisplay()
    
def init_winter():
    try:
        #glClearColor(0.4,0.4,0.4,1) #gray background
        glClearColor(0,0,0,1) #black backgrd
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(-1, 1, -1, 1, -1, 1)  # Set orthographic projection
        gluOrtho2D(-250, 250, -250, 250)
    except Exception as e:
        print('error in init',e)






#----------rainy seasons code-----------

def generate_raindrops(count):
    """Generate initial raindrops."""
    global raindrops
    raindrops = [(random.randint(-250, 250), random.randint(-250, 250)) for _ in range(count)]


def draw_raindrops():
    """Draw and animate raindrops."""
    global raindrops
    glColor3f(0.5, 0.8, 1)  # Light blue color for raindrops
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        midpointLine(x, y, x, y - 10)  # Short vertical line to represent raindrop
        raindrops[i] = (x, y - rain_speed)  # Move the raindrop down
        if raindrops[i][1] <= -250:  # Reset raindrop to top if it goes off the screen
            raindrops[i] = (random.randint(-250, 250), 250)


def init_rainy():
    try:
        glClearColor(0.5, 0.5, 0.5, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-250, 250, -250, 250)
        generate_raindrops(100)
    except Exception as e:
        print('error in init', e)

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(33, timer, 0)



#------------summer specific codes----------------

def summer_init():
    try:
        glClearColor(0.5,0.8,1,1) #black background
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(-1, 1, -1, 1, -1, 1)  # Set orthographic projection
        gluOrtho2D(-200, 200, -200, 200)
    except Exception as e:
        print('error in init',e)

def draw_sun():
    global sun_y, rays_enabled
   # Draw the sun
    glColor3f(1, 1, 0)  # Yellow sun
    midpointCircle(150, sun_y, 30)  # Use sun_y for vertical position
    sr=30
    while sr>=0:
        midpointCircle(150, sun_y, sr)
        sr-=1
    if rays_enabled:
        # Draw rays
        glColor3f(1, 0.5, 0)  # Orange rays
        for angle in range(0, 360, 30):
            x1 = 150 + 30 * cos(angle * 3.14159 / 180)
            y1 = sun_y + 30 * sin(angle * 3.14159 / 180)
            x2 = 150 + 50 * cos(angle * 3.14159 / 180)
            y2 = sun_y + 50 * sin(angle * 3.14159 / 180)
            midpointLine(int(x1), int(y1), int(x2), int(y2))

def draw_cloud():
    """Draw the cloud at its current position, considering cloud_x."""
    global cloud_x
    glColor3f(1, 1, 1)  # White cloud

    # Adjust cloud position with cloud_x
    midpointCircle(-50 + cloud_x, 120, 20)
    midpointCircle(-70 + cloud_x, 120, 20)
    midpointCircle(-60 + cloud_x, 140, 20)

    midpointCircle(20 + cloud_x, 150, 20)
    midpointCircle(50 + cloud_x, 150, 20)
    midpointCircle(30 + cloud_x, 170, 20)

    # Filled clouds
    hr = 20
    while hr >= 0:
        midpointCircle(-50 + cloud_x, 120, hr)
        midpointCircle(-70 + cloud_x, 120, hr)
        midpointCircle(-60 + cloud_x, 140, hr)
        hr -= 1

    hr2 = 20
    while hr2 >= 0:
        midpointCircle(20 + cloud_x, 150, hr2)
        midpointCircle(50 + cloud_x, 150, hr2)
        midpointCircle(30 + cloud_x, 170, hr2)
        hr2 -= 1

def summer_animate():
    global sun_y, rays_enabled
    if not rays_enabled:
        # Rising Phase: Move the sun up
        if sun_y < 50:  # Stop rising at a certain position
            sun_y += 1  # Adjust speed as needed
        else:
            rays_enabled = True  # Start displaying rays once the sun has risen
    else:
        # Once the sun has risen, the rays will remain static
        pass

    glutPostRedisplay()  # Redraw the scene


def summer_keyboard_input(key, x, y):
    """Handle left and right arrow key input."""
    global cloud_x
    if key == GLUT_KEY_LEFT:
        cloud_x -= 5  # Move cloud left
        print(f"Cloud moved left to {cloud_x}")
    elif key == GLUT_KEY_RIGHT:
        cloud_x += 5  # Move cloud right
        print(f"Cloud moved right to {cloud_x}")
    glutPostRedisplay()  # Request a redraw to reflect changes



#-------------in general driver code-------------

def reinitialize_season():
    global snowflakes, raindrops,sun_y,rays_enabled
    if season == 0:
        init_winter()
        snowflakes = []
    elif season == 2:
        init_rainy()
        raindrops = []
        generate_raindrops(100)
    elif season == 1:
        summer_init()
        sun_y = -150
        rays_enabled = False
    

def display():
    try:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        global snowflakes,season
       # field()
        draw_house_filled()
        if season == 0:
            init_snow()
            snow_drawing()
            glColor3f(1,1,1)
            field()
            snowman()
            lightstand()
        elif season == 1:
            draw_sun()
            draw_cloud()
            glColor3f(0,1,0)
            field()
        elif season == 2:
            draw_raindrops() #extra addition for rain
            glColor3f(0,1,0)
            field()
             
        
        glutSwapBuffers()
    except Exception as e:
        print('error during rendering',e)

def keyboardListener(key, x, y):
    global snowing,season
    if key==b'w':
        season = 0
        reinitialize_season()
        print("It is Winter Season")
        glutIdleFunc(snow_fall_updates)
    if key==b's':
        season = 1
        reinitialize_season()
        print("It is Summer Season")
        glutIdleFunc(summer_animate)
    if key==b'r':
        season = 2
        reinitialize_season()
        print("It is Rainy Season")


    if season == 0:
        if key==b'z':
            snowing = True
            print("start snowfall")
        if key==b'x':
            snowing = False
            print("stop snowfall")

def specialKeyListener(key, x, y):
    global season,lightsize,cloud_x
    if season == 0:
        if key==GLUT_KEY_UP:
            if lightsize < 11:
                lightsize += 1
                print("Brightness Increased")
        if key== GLUT_KEY_DOWN:		#// up arrow key
            if lightsize >1:
                lightsize -= 1 
                print("Brightness Decreased")
    if season == 1:
        """Handle left and right arrow key input."""
        # global cloud_x
        if key == GLUT_KEY_LEFT:
            cloud_x -= 5  # Move cloud left
            print(f"Cloud moved left to {cloud_x}")
        elif key == GLUT_KEY_RIGHT:
            cloud_x += 5  # Move cloud right
            print(f"Cloud moved right to {cloud_x}")

    glutPostRedisplay()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

window = glutCreateWindow(b"season visualization")
reinitialize_season()

glutDisplayFunc(display) 
glutIdleFunc(snow_fall_updates if season == 0 else None)
glutTimerFunc(0, timer, 0) #extra addition for rain
glutSpecialFunc(specialKeyListener)  # Register after creating the window
glutKeyboardFunc(keyboardListener)
glutMainLoop()