import sys
import os
import math

from random import randint

import pyglet
from pyglet import shapes, graphics

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *
    
kineticBodies = graphics.Batch()
kineticBodies.list = []

def state1(): 
    n = 2
    
    for i in range(n):
        body = shapes.Circle(
            x = 0, y = 0, radius = 20, 
            color = (255, 255, 255),
            batch = kineticBodies
        )
        
        body.mass_density = 7.85e+3
        body.mass = body.mass_density * (4/3) * math.pi * body.radius**2
        
        body.charge_density = 0
        body.charge = body.charge_density * (4/3) * math.pi * body.radius**2
        
        body.acceleration = (0, 0)
        
        body.velocity = (
            randint(-body.radius, body.radius),
            randint(-body.radius, body.radius)
        )
        
        body.position = (
            randint(body.radius, SCREEN_WIDTH - body.radius), 
            randint(body.radius, SCREEN_HEIGHT - body.radius)
        )
        
        kineticBodies.list.append(body)

def state2():
    n = 2
    
    state_variables = [
        [[0, 20], [CENTER_X - 150, CENTER_Y]],
        [[0, -20], [CENTER_X + 150, CENTER_Y]]
    ]
    
    for i in range(n):
        body = shapes.Circle(
            x = 0, y = 0, radius = 20, 
            color = (255, 255, 255),
            batch = kineticBodies
        )
        
        body.density = 7.85e+3
        body.mass = body.density * (4/3) * math.pi * body.radius**2
        
        body.acceleration = (0, 0)
        
        body.velocity = state_variables[i][0]
        body.position = state_variables[i][1]
        
        kineticBodies.list.append(body)

def init():
    # state1()
    state2()

def draw():
    kineticBodies.draw()