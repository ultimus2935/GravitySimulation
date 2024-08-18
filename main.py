import sys
import os
import math

from random import randint

import pyglet
from pyglet import app, window, shapes, graphics

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *
from util.constants import *

win = window.Window(
    width = SCREEN_WIDTH, height = SCREEN_HEIGHT,
    caption = 'Pyglet Test',
    vsync = False
)

if DEBUG: fps = window.FPSDisplay(win)

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

def gravity(body, bodies):
    if body.mass == 0: return (0, 0)
    
    acceleration = (0, 0)
    
    for other in bodies.list:
        if body != other:
            distance = math.sqrt((body.position[0] - other.position[0])**2 + (body.position[1] - other.position[1])**2)
            magnitude = G * other.mass / (distance**2)
            
            acceleration = (
                acceleration[0] + magnitude * (other.position[0] - body.position[0]) / distance,
                acceleration[1] + magnitude * (other.position[1] - body.position[1]) / distance
            )
    
    return acceleration

def electrostatic(body, bodies):
    if body.charge == 0: return (0, 0)
    
    acceleration = (0, 0)
    
    for other in bodies.list:
        if body != other:
            distance = math.sqrt((body.position[0] - other.position[0])**2 + (body.position[1] - other.position[1])**2)
            magnitude = (k * other.charge * body.charge) / (body.mass * distance**2)
            
            acceleration = (
                acceleration[0] + magnitude * (other.position[0] - body.position[0]) / distance,
                acceleration[1] + magnitude * (other.position[1] - body.position[1]) / distance
            )
    
    return acceleration

@win.event
def on_draw():
    win.clear()
    
    if DEBUG: fps.draw()
    kineticBodies.draw()

def update(dt):
    for body in kineticBodies.list:
        body.acceleration = (0, 0)
        body.acceleration += gravity(body, kineticBodies)
        body.acceleration += electrostatic(body, kineticBodies)
        
        body.velocity = (
            body.velocity[0] + body.acceleration[0] * dt,
            body.velocity[1] + body.acceleration[1] * dt)
        
        body.position = (
            body.position[0] + body.velocity[0] * dt,
            body.position[1] + body.velocity[1] * dt)

if __name__ == '__main__':
    createBodies(2, massDensity = 7.85e+3)
    pyglet.clock.schedule_interval(update, SPEED/60)
    app.run()