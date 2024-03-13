import pygame
import random


class ImageLoader:
    def __init__(self):

        # Collection of possible backgrounds
        space1 = pygame.image.load('Textures/7046.jpg')
        space2 = pygame.image.load('Textures/39607.jpg')
        space3 = pygame.image.load('Textures/39608.jpg')
        space4 = pygame.image.load('Textures/39612.jpg')
        space5 = pygame.image.load('Textures/39613.jpg')
        space6 = pygame.image.load('Textures/39616.jpg')
        space7 = pygame.image.load('Textures/39617.jpg')
        space8 = pygame.image.load('Textures/39619.jpg')
        space9 = pygame.image.load('Textures/39625.jpg')
        space10 = pygame.image.load('Textures/39626.jpg')
        space11 = pygame.image.load('Textures/39630.jpg')
        space12 = pygame.image.load('Textures/39631.jpg')
        space13 = pygame.image.load('Textures/39636.jpg')
        space14 = pygame.image.load('Textures/39639.jpg')
        space15 = pygame.image.load('Textures/39654.jpg')

        self.space_list = [space1, space2, space3, space4, space5, space6, space7, space8, 
                           space9, space10, space11, space12, space13, space14, space15]

        # Collection of possible planets
        mercury = pygame.image.load('Textures/mercury.png')
        venus = pygame.image.load('Textures/venus.png')
        earth = pygame.image.load('Textures/earth.png')
        luna = pygame.image.load('Textures/luna.png')
        mars = pygame.image.load('Textures/mars.png')
        jupiter = pygame.image.load('Textures/jupiter.png')
        uranus = pygame.image.load('Textures/uranus.png')
        neptune = pygame.image.load('Textures/neptune.png')
        saturn = pygame.image.load('Textures/saturn.png')

        self.planet_list = [mercury, venus, earth, luna, mars, jupiter, uranus, neptune]


    def get_space_image(self):
        self.random_space = random.randint(0, 14)
        return self.space_list[self.random_space]

    def get_planet_image(self):
        self.random_planet = random.randint(0, 7)
        return self.planet_list[self.random_planet]