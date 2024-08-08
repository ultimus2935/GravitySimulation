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

def createBodies(n: int, radius: float = 10, position: tuple[float, float] = None, velocity: tuple[float, float] = None, massDensity: float = 1e+3, chargeDensity: float = 0):    
    for i in range(n):
        body = shapes.Circle(
            x = 0, y = 0, radius = 20, 
            color = (255, 255, 255),
            batch = kineticBodies
        )
        
        body.mass = massDensity * (4/3) * math.pi * body.radius**2
        body.charge = chargeDensity * (4/3) * math.pi * body.radius**2
        
        body.acceleration = (0, 0)
        
        if velocity is None:
            body.velocity = (
                randint(-body.radius, body.radius),
                randint(-body.radius, body.radius)
            )
        else: body.velocity = velocity
        
        if position is None:
            body.position = (
                randint(body.radius, SCREEN_WIDTH - body.radius), 
                randint(body.radius, SCREEN_HEIGHT - body.radius)
            )
        else: body.position = position
        
        kineticBodies.list.append(body)

def init():
    createBodies(2, massDensity = 7.85e+3)

def draw():
    kineticBodies.draw()