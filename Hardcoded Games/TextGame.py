import pygame
import math
import numpy as np # for finding smallest/largest list items
import random

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Text to Game Generator")

# initializes image loader class
from Images import ImageLoader
images = ImageLoader()

# Load the background image
background_image = pygame.transform.scale(images.get_space_image(), (1000, 750))


# initializes planets
from Planet import PlanetBuilder
planet = PlanetBuilder()
planet_rect = planet.get_rectangle()
planet_radius = planet.get_radius()
planet2 = PlanetBuilder()

# list of planets
planet_list = [planet, planet2]


# Spaceship attributes
ship_mass = 1000 # mass of rocket
ship_width, ship_height = 60, 60
ship_x, ship_y = planet.get_x(), ((planet.get_y()/2) - (planet.get_radius() - (planet.get_y()/2)))
throttle = 0.0
ship = pygame.image.load('Textures/rocket.png')  # Load the ship image
ship = pygame.transform.scale(ship, (ship_width, ship_height))  # Resize if needed
ship_velocity = pygame.Vector2(0.0, 0.0)  # Initial velocity
# set to decimals to prevent rounding to whole numbers
ship_angle = 0

# gets the center of the planet and ship images
ship_rect = ship.get_rect()  # Get the rectangle of the ship image
ship_rect.center = (ship_x, ship_y)  # Set the initial ship position

# Create a list to store the spaceship's positions for the path
from Orbits import OrbitPath
path = OrbitPath(screen)

# orbital parameters
G = 6.67430e-11  # gravitational constant 'G'
gravitational_force = 0.0
delta_v = 50
apoapsis = 155
periapsis = 150
speed = 0

# tracks user text input
user_text = ''


clock = pygame.time.Clock()


running = True
while running:
    # commented out because it interfered with text input
    # add back in if I want to remove text input
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #running = False
            
    # draws the background image
    screen.blit(background_image, (0, 0))
            
    # draws the planets
    for i in range(len(planet_list)):
        curr_planet = planet_list[i]
        planet_rect = curr_planet.get_rectangle() # updates global planet radius variable
        planet_radius = curr_planet.get_radius()
        curr_planet.set_radius(planet_radius)
        screen.blit(curr_planet.get_planet(), planet_rect)
    
    # draws the ship
    screen.blit(ship, ship_rect)
	
	# saves a copy of the ship to rotate
    saved_image = pygame.image.load('Textures/rocket.png')  # Load the ship image
    saved_image = pygame.transform.scale(saved_image, (ship_width, ship_height))
    
    # tracks game time
    gtime = (pygame.time.get_ticks()) / 1000
    
    
    # function to reset the ship's location and rotation
    def reset_ship(ship_x, ship_y):
        global ship_rect, ship_angle, ship, delta_v, ship_velocity, ship_distances
        ship_rect.center = (ship_x, ship_y)
        ship_velocity.x = 0.0
        ship_velocity.y = 0.0
        delta_v = 50
        
        # clears distances list, adds values to prevent zero list errors
        path.reset_distances()
        
        # resets spin
        ship_angle = 0
        ship = pygame.transform.rotate(saved_image, ship_angle)
        ship_rect = ship.get_rect(center=ship_rect.center)
        
    # applies changes in velocity and delta v
    def apply_throttle():
        global delta_v, ship_velocity
        ship_velocity.x += throttle * math.cos(math.radians(ship_angle+90))
        ship_velocity.y += throttle * -math.sin(math.radians(ship_angle+90))
        delta_v = delta_v - throttle
        
    # function to rotate ship
    def rotate_ship(angle):
        global ship_rect, ship_angle, ship, delta_v
        ship_angle = ship_angle + angle
        ship = pygame.transform.rotate(saved_image, ship_angle)
        ship_rect = ship.get_rect(center=ship_rect.center) # re-centers ship spin
        delta_v = delta_v - (throttle/5)
            
    # allows for continuous detection of keys without having to click one by one
    keys = pygame.key.get_pressed()
    # rotates ship
    if keys[pygame.K_a]:
        rotate_ship(10)
    if keys[pygame.K_d]:
        rotate_ship(-10)

    # moves ship
    if keys[pygame.K_w] and delta_v > 0:
        apply_throttle()
        
    # if spacebar is pressed
    if keys[pygame.K_SPACE]:
        # calls reset game function
        reset_ship(ship_x, ship_y)

    # sets ship throttle
    if keys[pygame.K_UP]:
        throttle = throttle + 0.025
    if keys[pygame.K_DOWN]:
        throttle = throttle - 0.025
        
    # restricts thrust
    if throttle > 1:
    	throttle = 1
    if throttle < 0:
        throttle = 0
        
    # if fuel runs out
    if delta_v < 0:
        delta_v = 0.0
    
    
    # Update ship position based on its velocity
    ship_rect.x += ship_velocity.x
    ship_rect.y += ship_velocity.y
    
    # calculates gravity force on the ship based on the planet's mass
    direction = pygame.Vector2(planet.get_x() - ship_rect.x, planet.get_y() - ship_rect.y)
    distance = direction.length()
    path.store_distance(distance) # stores ship distances
    
    if distance > planet.get_radius() and distance < 600:  # stops gravity at planet's surface
        direction.normalize_ip()
        gravitational_force = G * (planet.get_mass() / distance**2)
        gravity = direction * gravitational_force
        ship_velocity.x += gravity.x
        ship_velocity.y += gravity.y
    
    elif distance > 600:
        # resets game
        reset_ship(ship_x, ship_y)
    else:
        ship_velocity.x = 0.0
        ship_velocity.y = 0.0

    # stores the current position of the spaceship for the path
    path.store_path((int(ship_rect.x+30), int(ship_rect.y+30)))
    path_array = path.get_distances()

    
    # keeps track of the ship parameters
    orbit_height = planet.get_radius() + 50
    speed = round(ship_velocity.length(), 3)
    orbit_goal = round(math.sqrt( (planet.get_mass() * G) / orbit_height ), 3)
    gravitational_force = round(gravitational_force, 3)
    delta_v = round(delta_v, 3)
    percent_throttle = round(throttle*100, 3)
    
    # keeps track of orbital parameters
    apoapsis = round(np.max(path_array), 3)
    periapsis = round(np.min(path_array), 3)
    eccentricity = round((apoapsis-periapsis) / (apoapsis+periapsis), 3)
    altitude = round(distance-planet.get_radius(), 3)
    
    # render text
    font = pygame.font.Font(None, 26)
    speed_text = font.render(f"Velocity (m/s): {speed}", True, (255, 255, 255))
    orbit_text = font.render(f"Orbit Goal (m/s): {orbit_goal}", True, (255, 255, 255))
    gravity_text = font.render(f"Gravity (m/s^2): {gravitational_force}", True, (255, 255, 255))
    delta_text = font.render(f"Delta-V (m/s): {delta_v}", True, (255, 255, 255))
    throttle_text = font.render(f"% Thrust: {percent_throttle}", True, (255, 255, 255))
    time_text = font.render(f"Time (s): {gtime}", True, (255, 255, 255))
    apoapsis_text = font.render(f"Apoapsis (m): {apoapsis}", True, (255, 255, 255))
    periapsis_text = font.render(f"Periapsis (m): {periapsis}", True, (255, 255, 255))
    eccentricity_text = font.render(f"Eccentricity: {eccentricity}", True, (255, 255, 255))
    altitude_text = font.render(f"Altitude: {altitude}", True, (255, 255, 255))
    
    # displays speed text on the screen
    screen.blit(speed_text, (10, 10))
    screen.blit(gravity_text, (10, 30))
    screen.blit(orbit_text, (10, 50))
    screen.blit(delta_text, (10, 70))
    screen.blit(throttle_text, (10, 90))
    screen.blit(time_text, (800, 10))
    screen.blit(apoapsis_text, (800, 30))
    screen.blit(periapsis_text, (800, 50))
    screen.blit(eccentricity_text, (800, 70))
    screen.blit(altitude_text, (800, 90))
    
    
    # creates the input text box
    text_box = pygame.Rect(300, 600, 440, 64)
    pygame.draw.rect(screen, (5,11,120), text_box)
    text_surface = font.render(user_text, True, (255,255,255))
    
    # displays instructions for input
    press_enter = font.render(f"Press 'Enter' to set text prompt", True, (255, 255, 255))
    screen.blit(press_enter, (400, 570))
    
    # extracts integers from the input text
    text_ints = [0]
    # only sets text int variable to non-zero if numbers are in input text
    text_ints = [int(i) for i in user_text.split() if i.isdigit()]
        
        
    # function to change direction of planet or rocket
    def move_by(curr_planet, planet_xdir, planet_ydir, ship_xdir, ship_ydir):
        global ship_x, ship_y
        
        planet_x = curr_planet.get_x()
        planet_y = curr_planet.get_y()
    
        # moves planet by text int amount
        planet_x = planet_x + planet_xdir
        planet_y = planet_y + planet_ydir
        
        # recenters planet
        planet_rect = curr_planet.get_rectangle()
        planet_rect.center = (planet_x+(ship_width/2), planet_y+(ship_height/2))
        
        # resets the x and y coordinates
        curr_planet.set_x(planet_x)
        curr_planet.set_y(planet_y)
                            
        # moves ship spawn
        ship_x = ship_x + ship_xdir
        ship_y = ship_y + ship_ydir
        reset_ship(ship_x, ship_y)
        
        return planet_rect
    
    
    # for key clicks where one by one key pressing is preferred
    for event in pygame.event.get():
        # if user quits game
        if event.type == pygame.QUIT:
            running = False
  
  
        if event.type == pygame.KEYDOWN: 
            # checks to see if enter key has been pressed
            if event.key == pygame.K_RETURN:
            
                # searches for instance of move in input text
                if user_text.find("move") != -1:
                  # checks length of texts list
                  if 1 < len(text_ints):
                
                    # searches for occurrence of "planet"
                    if (user_text.find("planet") != -1) and (text_ints[0] != 0) and (text_ints[1] != 0):
                      # sees if planet index exists
                      if text_ints[0] <= len(planet_list):
                      
                        # keeps track of current planet
                        curr_planet = planet_list[text_ints[0]-1]
                    
                        # moves one of 4 possible directions using move by function
                        if user_text.find("up") != -1:
                            # moves planet by text int amount
                            planet_rect = move_by(curr_planet, 0, -text_ints[1], 0, -text_ints[1])
                        if user_text.find("down") != -1:
                            planet_rect = move_by(curr_planet, 0, text_ints[1], 0, text_ints[1])
                        if user_text.find("right") != -1:
                            planet_rect = move_by(curr_planet, text_ints[1], 0, text_ints[1], 0)
                        if user_text.find("left") != -1:
                            planet_rect = move_by(curr_planet, -text_ints[1], 0, -text_ints[1], 0)
            
                # searches for instance of move in input text
                elif (user_text.find("size")!=-1) or (user_text.find("scale")!=-1):
                  # checks length of texts list
                  if 1 < len(text_ints):
        
                    if (user_text.find("planet") != -1) and (text_ints[0] != 0) and (text_ints[1] != 0):
                      # sees if planet index exists
                      if text_ints[0] <= len(planet_list):
                      
                        # keeps track of current planet
                        curr_planet = planet_list[text_ints[0]-1]
                    
                        # applies the new scale of the planet
                        planet_radius = text_ints[1]
                        curr_planet.set_radius(planet_radius) # calls planet setter function
            
                        # recenters the planet at its new scale
                        planet_rect = curr_planet.get_rectangle()
                        planet_rect.center = (curr_planet.get_x()+(ship_width/2), curr_planet.get_y()+(ship_height/2))
            
                        # resets the ship's spawn point around first planet
                        ship_x, ship_y = planet.get_x(), ((planet.get_y()/2) - (planet_radius - (planet.get_y()/2)))
                        reset_ship(ship_x, ship_y)
                        
                        # recalculates orbital parameters
                        orbit_height = planet.get_radius() + 50
                        orbit_goal = round(math.sqrt( (planet.get_mass() * G) / orbit_height ), 3)
                        
                
                # adds new planet (no gravity)
                elif (user_text.find("new planet")!=-1):
                    new_planet = PlanetBuilder()
                    # adds new planet to planet list
                    planet_list.append(new_planet)
                        
                # erases existing input text
                user_text = ''
                
                
            # checks for backspace 
            elif event.key == pygame.K_BACKSPACE: 
                # removes most recently written text 
                user_text = user_text[:-1] 
  
            # saves the unicode input into the user text string
            else: 
                user_text += event.unicode
    
    # renders and sets the width of the text field
    screen.blit(text_surface, (text_box.x+5, text_box.y+5))
    text_box.w = max(100, text_surface.get_width()+10) # updates width with input text
    pygame.display.flip()
    

    pygame.display.update()
    clock.tick(30)

pygame.quit()
