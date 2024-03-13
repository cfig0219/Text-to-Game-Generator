import pygame
import random
import numpy as np

# initializes image loader class
from Images import ImageLoader
images = ImageLoader()


class PlanetBuilder:
    def __init__(self):
        
        # planet attributes
        self.planet_mass = random.randint(50000000000000, 200000000000000)  # mass of planet
        self.planet_radius = random.randint(100, 300)
        self.planet_x = random.randint(600, 800)
        self.planet_y = random.randint(200, 550)
        self.current_planet = images.get_planet_image()
        self.planet = pygame.transform.scale(self.current_planet, (self.planet_radius*2, self.planet_radius*2))
        
        self.planet_rect = self.planet.get_rect()  # Get the rectangle of the planet image
        self.planet_rect.center = (self.planet_x+(60/2), self.planet_y+(60/2))  # Set the planet position

        
    # returns planet
    def get_planet(self):
        return self.planet
        
    # gets planet's rectangle
    def get_rectangle(self):
        return self.planet_rect
        
    # gets planet's x coordinate
    def get_x(self):
        return self.planet_x
    
    # gets planet's y coordinate
    def get_y(self):
        return self.planet_y
        
    # sets planet's x coordinate
    def set_x(self, newx):
        self.planet_x = newx
    
    # sets planet's y coordinate
    def set_y(self, newy):
        self.planet_y = newy
        
    # gets planet's mass
    def get_mass(self):
        return self.planet_mass
        
    # gets planet's radius
    def get_radius(self):
        return self.planet_radius
        
    # sets planet's radius
    def set_radius(self, newrad):
        self.planet_radius = newrad
        self.planet = pygame.transform.scale(self.current_planet, (self.planet_radius*2, self.planet_radius*2))
        self.planet_rect = self.planet.get_rect()  # Get the rectangle of the planet image
        self.planet_rect.center = (self.planet_x+(60/2), self.planet_y+(60/2))  # Set the planet position
        

    # moves planet
    def move_planet(self):
        pass
