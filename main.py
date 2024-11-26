import sys
import os
import math
import csv

import numpy as np
from numpy import array, zeros, pi
from numpy.linalg import norm

import pyglet
from pyglet import shapes, graphics, canvas
from pyglet.window import key, Window

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *
from util.constants import *

win = Window(
    *SCREEN_SIZE, 
    caption = 'Gravity Simulator', 
    vsync = False, resizable = False
)

if FULLSCREEN:
    screen = canvas.get_display().get_screens()[0]
    win.set_size(screen.width, screen.height)
    win.set_fullscreen(True)
    
ORIGIN = array([win.width // 2, win.height // 2])
    
win.view = win.view.translate((*ORIGIN, 1))
win.view = win.view.scale((*ZOOM_FACTOR, 1))

kineticBodies = graphics.Batch()
kineticBodies.list = []

class Body():
    def __init__(
        self, name = '',
        mass_density = 0, charge_density = 0, radius = 0, 
        position = zeros(2), velocity = zeros(2),
        color =  (255, 255, 255), batch = None
        ):
        
        self.name = name
        
        self.position = position
        self.velocity = velocity
        
        self.mass = mass_density * pi * radius**2
        self.charge = charge_density * pi * radius**2
        
        self.sprite = shapes.Circle(
            *position, radius = radius,
            batch = batch, color = color + (255,)
        )
        
    def gravity(self, bodies):
        acceleration = zeros(2)
        if self.mass == 0: return acceleration
        
        for body in bodies:
            if body == self or body.mass == 0: continue
            
            r = body.position - self.position
            acceleration += G * body.mass * (r / norm(r)**3)
        
        return acceleration

    def electrostatic(self, bodies):
        acceleration = zeros(2)
        if self.mass == 0: return acceleration
        
        for body in bodies:
            if body == self or body.charge == 0: continue
            
            r = body.position - self.position
            acceleration += (k * body.charge * self.charge / self.mass) * (r / norm(r)**3)
                
        return acceleration
            
    def update(self, bodies, dt):
        acceleration = self.gravity(bodies)
        # acceleration += self.electrostatic(bodies) # Uncomment to enable electrostaic forces
        
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        
        self.sprite.position = self.position

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
    
    kineticBodies.draw()

@win.event
def on_key_press(symbol, modifiers):
    global RUNNING
    
    if symbol == key.P: RUNNING = not RUNNING

def update(dt):
    if RUNNING:
        for body in kineticBodies.list: 
            body.update(kineticBodies.list, dt)

if __name__ == '__main__':
    loadBodies(SYSTEM_FILE_PATH)
    pyglet.clock.schedule_interval(update, dt)
    pyglet.app.run()