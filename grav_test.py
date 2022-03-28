from math import cos, sin, atan2, sqrt, pi
from random import randrange, uniform

import pygame as pg

GRAVITATIONAL_FIELD_STRENGTH = 9.81 # N/Kg
NET_FORCE = 9.81 # N - Freefall
M = 10e7

pg.init()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = GRAVITATIONAL_FIELD_STRENGTH // 9
        self.mass = 2 # Kg
        self.x_momentum = 500 # m/s
        self.y_momentum = 500 # m/s
        self.m_slope = self.y_momentum / self.x_momentum # (i) acc
        self.delta = 0.001 # work
    
    def move(self, x_central, y_central):
        x2 = x_central
        y2 = y_central
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = atan2(y2 - self.y, x2 - self.x)
        force = (self.g * self.mass * M) / hyp
        force_x = force * cos(theta)
        force_y = force * sin(theta)
        self.x_momentum += force_x * self.delta
        self.y_momentum += force_y * self.delta
        self.m_slope = self.y_momentum / self.x_momentum
        self.x += self.x_momentum / self.mass * self.delta
        self.y += self.y_momentum / self.mass * self.delta
        return [self.x, self.y]

WIDTH, HEIGHT = 1000, 750
centerX = WIDTH // 2
centerY = HEIGHT // 2
CENTER = WIDTH // 2, HEIGHT // 2

WHITE = (255, 255, 255)
RED = (255, 80, 70)
BLACK = (0, 0, 0)

screen = pg.display.set_mode((WIDTH, HEIGHT))

particles = []
r = 200

def generate_particles(times):
    for i in range(times):
        ang = uniform(0, 1) * 2 * pi
        hyp = sqrt(uniform(0, 1)) * r
        adj = cos(ang) * hyp
        opp = sin(ang) * hyp
        
        x = centerX + adj
        y = centerY + opp
        
        particle = Particle(x, y)
        particles.append(particle)

generate_particles(500)

def draw_particles():
    for i in range(len(particles)):
        pg.draw.circle(screen, WHITE, (particles[i].move(CENTER[0], CENTER[1])), 1)

running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BLACK)

    # Gravity point
    central_mass = pg.draw.circle(screen, RED, CENTER, 2)

    draw_particles()

    pg.display.update()