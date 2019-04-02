import numpy as np
from matplotlib import pyplot as plt
from vpython import *
import time

g = 9.81    # m/s**2
l_one = 1     # meters
l_two = .5
W = 0.002   # arm radius
R = 0.1     # ball radius
framerate = 100
steps_per_frame = 10

def f(r, l):
        """
        Pendulum calculations
        Parameters:
                r: theta and omega on an NP array
                l: length of the pendulum rod
        """
        theta = r[0]
        omega = r[1]
        ftheta = omega
        fomega = -(g/l)*np.sin(theta) -.7 * omega
        return np.array([ftheta, fomega], float)

def set_scene():
        '''
        Set the scene and descriptions
        '''
        scene.title = "Assignment 6: Pendulums"
        scene.width = 800
        scene.heigth = 600
        scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
        To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
        On a two-button mouse, middle is left + right.
        Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
        scene.forward = vector(0, -.3, -1)
        scene.x = -1


def main():
        """
        Here we are drawing all of our objects, calculating locations, and animating objects
        """
        set_scene()
        #ceilings
        box(pos=vector(1,0.05,0), size=vector(.1,.1,.1), color=color.orange)
        box(pos=vector(-1,0.05,0), size=vector(.1,.1,.1), color=color.orange)
        
        # Set up initial values
        h = 1.0/(framerate * steps_per_frame)
        r = np.array([np.pi*179/180, 0], float)
        z = np.array([np.pi*90/180, 0], float)

        # Initial x and y
        x = [l_one*np.sin(r[0])-1, l_two*np.sin(z[0])+1]
        y = [-l_one*np.cos(r[0]), -l_two*np.cos(z[0])]

        #Track theta values of first pendulum
        theta_points = []
        time_points = []

        rod = cylinder(pos=vector(-1,0,0), radius=W, axis=vector(x[0], y[0], 0))
        pend = sphere(pos=vector(x[0], y[0], 0), radius=R, color=color.yellow)

        rod_two = cylinder(pos=vector(1,0,0), radius=W, axis=vector(x[1], y[1], 0))
        pend_two = sphere(pos=vector(x[1], y[1], 0), radius=R, color=color.yellow)

        # Loop over some time interval
        dt = 0.01
        t = 0
        while t < 10:
                time_points.append(t)
                theta_points.append(r[0]*180/np.pi)
        # Use the 4'th order Runga-Kutta approximation
                for i in range(steps_per_frame):
                
                        k1 = h*f(r, l_one)
                        k2 = h*f(r + 0.5*k1, l_one)
                        k3 = h*f(r + 0.5*k2, l_one)
                        k4 = h*f(r+k3, l_one)
                        r += (k1 + 2*k2 + 2*k3 + k4)/6

                        k1 = h*f(z, l_two)
                        k2 = h*f(z + 0.5*k1, l_two)
                        k3 = h*f(z + 0.5*k2, l_two)
                        k4 = h*f(z+k3, l_two)
                        z += (k1 + 2*k2 + 2*k3 + k4)/6
                        

                t += dt
                # Update positions
                x = [l_one*np.sin(r[0])-1, l_two*np.sin(z[0])+1]
                y = [-l_one*np.cos(r[0]), -l_two*np.cos(z[0])]
                # Update the cylinder axis
                rod.axis=vector(x[0]+1,y[0],0)
                rod_two.axis=vector(x[1]-1,y[1],0)
                # Update the pendulum's bob
                pend.pos=vector(x[0], y[0], 0)
                pend_two.pos=vector(x[1], y[1], 0)
                #Limits how fast the animation runs
                time.sleep(1./100)

        plt.plot(time_points, theta_points)
        plt.xlabel("Time(s)")
        plt.ylabel("Theta(degrees)")
        plt.title("Theta Vs. Time of Left Pendulum")
        plt.show()

if __name__ == "__main__":
         main()
         exit(0)
