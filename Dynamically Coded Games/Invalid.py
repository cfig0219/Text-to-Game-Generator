import pygame
import sys

class InvalidCode:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen = pygame.display.set_mode((800, 600))
        # Set up the font
        self.font = pygame.font.Font(None, 36)

        # Set up the clock
        self.clock = pygame.time.Clock()
        self.FPS = 60  # Adjust the frame rate as needed
        
        # error message
        self.error_msg = "Game Code Invalid"
        
    def set_error(self, message):
        self.error_msg = message

    def run(self, file_name):
        # Game loop
        while True:
            # for key clicks where one by one key pressing is preferred
            for event in pygame.event.get():
                # if the user quits the game
                if event.type == pygame.QUIT:
                    file_path = file_name
                    old_code = ''
                    with open(file_path, "r") as file:
                        old_code = file.read()
                    # returns to text box game
                    exec(old_code)

            # Draw everything
            self.screen.fill((0, 0, 0))

            # Render text
            error_text = self.font.render(self.error_msg, True, (255, 255, 255))
            # Display text on the screen
            self.screen.blit(error_text, (200, 280))  # Adjust the position as needed

            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            self.clock.tick(self.FPS)