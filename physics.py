import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.constants import *

import bodies
from bodies import kineticBodies

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