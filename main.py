import sys
import os
import math
import csv

import numpy as np
from numpy import *
from numpy.linalg import norm

import pyglet
from pyglet import *

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

class Body():
    def __init__(self, name = '',
                mass_density = 0, charge_density = 0, radius = 0, 
                position = np.zeros(2), velocity = np.zeros(2),
                batch = None
                ):
        self.name = name
        
        self.pos = position
        self.vel = velocity
        self.acc = zeros(2)
        
        self.mass = mass_density * pi * radius**2
        self.charge = charge_density * pi * radius**2
        
        self.sprite = shapes.Circle(
            *(ORIGIN + position), radius = radius,
            batch = batch
        )
        
    def gravity(self, bodies):
        acc = np.zeros(2)
        if self.mass == 0: return acc
        
        for body in bodies:
            if body == self or body.mass == 0: continue
            
            r = body.pos - self.pos
            acc += G * body.mass * (r / np.linalg.norm(r)**3)
        
        return acc

    def electrostatic(self, bodies):
        acc = np.zeros(2)
        if self.mass == 0: return acc
        
        for body in bodies:
            if body == self or body.charge == 0: continue
            
            r = body.pos - self.pos
            acc += (k * body.charge * self.charge / self.mass) * (r / np.linalg.norm(r)**3)
                
        return acc
            
    def update(self, bodies, dt):
        self.acc = self.gravity(bodies)
        self.acc += self.electrostatic(bodies)
        
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        
        self.sprite.position = ORIGIN + self.pos

def loadBodies(path):
    fp = open(SYSTEM_FILE_PATH, 'r')
    
    reader = csv.DictReader(fp, delimiter = ',')
    for row in reader:
        kineticBodies.list.append(
            Body(
                name = row['name'],
                mass_density = float(row['mass_density']),
                charge_density = float(row['charge_density']),
                radius = float(row['radius']),
                position = array([float(row['x']), float(row['y'])]),
                velocity = array([float(row['vx']), float(row['vy'])]),
                batch = kineticBodies
            )
        )

@win.event
def on_draw():
    win.clear()
    
    if DEBUG: fps.draw()
    kineticBodies.draw()

def update(dt):
    for body in kineticBodies.list: 
        body.update(kineticBodies.list, dt)

if __name__ == '__main__':
    loadBodies('systems/two_body.csv')
    pyglet.clock.schedule_interval(update, dt)
    app.run()