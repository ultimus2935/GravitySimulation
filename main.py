import sys
import os

import pyglet
from pyglet import app, window

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *

import bodies
import physics

win = window.Window(
    width = SCREEN_WIDTH, height = SCREEN_HEIGHT,
    caption = 'Pyglet Test',
    vsync = False
)

if DEBUG: fps = window.FPSDisplay(win)

bodies.init()

@win.event
def on_draw():
    win.clear()
    
    if DEBUG: fps.draw()
    bodies.draw()

def update(dt):
    physics.update(SPEED * dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    app.run()