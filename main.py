import sys
import os

import pyglet
from pyglet import app, window

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *

import bodies
import physics

DEBUG = False;

window = window.Window(
    width = SCREEN_WIDTH,
    height = SCREEN_HEIGHT,
    caption='Pyglet Test'
)

if DEBUG: fps = window.FPSDisplay(window)

bodies.init()

@window.event
def on_draw():
    window.clear()
    
    if DEBUG: fps.draw()
    bodies.draw()

def update(dt):
    physics.update(dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    app.run()