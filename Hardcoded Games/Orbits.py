import pygame
import random
import numpy as np

# global variable
ship_distances = [155, 150]

class OrbitPath:
    def __init__(self, screen):
        # saves screen from input
        self.screen = screen
    
        # Create a list to store the spaceship's positions for the path
        self.ship_path = []

    # Limit the path length to avoid consuming too much memory
    def store_path(self, coordinates):
        # Store the current position of the spaceship for the path
        self.ship_path.append(coordinates)

        if len(self.ship_path) > 2:
            pygame.draw.lines(self.screen, (0, 255, 0), False, self.ship_path, 2)
            
            # removes oldest paths
            if len(self.ship_path) > 400:
                self.ship_path.pop(0)
            if len(ship_distances) > 400:
                ship_distances.pop(0)

    # store distance
    def store_distance(self, distance):
        ship_distances.append(distance)
        
    # resets the orbit distances
    def reset_distances(self):
        ship_distances = [155,150]
        
    # gets ship distances
    def get_distances(self):
        # converts ship path into numpy array
        path_array = np.array(ship_distances)
        
        return path_array
