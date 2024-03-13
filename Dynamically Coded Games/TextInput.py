# source: https://blog.enterprisedna.co/how-to-use-chatgpt-for-python/

import pygame
import random
import sys
import openai
import re

# API Key
openai.api_key = "keep this hidden"


# invalid game screen
from Invalid import InvalidCode
invalid = InvalidCode()

# saves invalid error message
error_str = ''

# Specify the new file path where the modified code will be saved
new_file_path = "ModifiedTextGame.py"
file_path = "BaseGame.py"
old_code = ''

# reads the contents of the original file or the modified file
try:
    with open(new_file_path, "r") as file:
        old_code = file.read()
except FileNotFoundError:
    with open(file_path, "r") as file:
        old_code = file.read()

# Define the number of visible lines in the output box
visible_lines = 7
scroll_position = 0
            
        
# allows for user to return to text game when exit button is clicked
return_code = '''
    # for key clicks where one by one key pressing is preferred
    for event in pygame.event.get():
        # if the user quits the game
        if event.type == pygame.QUIT:
            # reads the contents of DynamicGame.py
            file_path = "TextInput.py"
            old_code = ''
            with open(file_path, "r") as file:
                old_code = file.read()
            # returns to text box game
            exec(old_code)
'''

# uses API to send user prompt to ChatGPT
def TextChatCode(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = response.choices[0].text.strip()
        return message

    except openai.error.RateLimitError:
        # Handle rate limit error
        invalid.set_error("OpenAI API rate limit reached.")
        invalid.run("TextInput.py") # current game file as return code argument
    except Exception as e:
        # Handle other exceptions
        invalid.set_error("An error occurred: {str(e)}")
        invalid.run("TextInput.py") # current game file as return code argument


# used try catch exception to determine if code is calid
def is_valid_code(code):
    global error_str
    try:
        exec(code)
        return True
    except Exception as e:
        error_str = str(e)
        return False


# Set up the display
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("OpenAI Interface Game Generator")

# Initialize the font before using it
font = pygame.font.Font(None, 36)
# tracks user text input
user_text = ''

pygame.init()
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))

    # creates the input text box
    text_box = pygame.Rect(150, 200, 700, 150)
    pygame.draw.rect(screen, (5, 110, 120), text_box)
    text_surface = font.render(user_text, True, (255, 255, 255))
    
    # creates code output text box
    output_box = pygame.Rect(150, 390, 700, 270)
    pygame.draw.rect(screen, (5, 110, 120), output_box)
    output_surface = font.render(old_code, True, (255, 255, 255))

    # displays instructions for input
    press_enter = font.render("Press 'Enter' to set text prompt", True, (255, 255, 255))
    switch_game = font.render("'Enter' to switch back to game generator", True, (255, 255, 255))
    screen.blit(press_enter, (320, 70))
    screen.blit(switch_game, (270, 120))

    # extracts integers from the input text
    text_ints = [0]
    # only sets text int variable to non-zero if numbers are in input text
    text_ints = [int(i) for i in user_text.split() if i.isdigit()]

    
    # for key clicks where one by one key pressing is preferred
    for event in pygame.event.get():
        # if the user quits the game
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # checks to see if the enter key has been pressed
            if event.key == pygame.K_RETURN:
            
                # creates new game
                if 'create' in user_text:
                    old_code = TextChatCode(user_text)
                        
                    # Open the file in write mode ("w")
                    with open(new_file_path, "w") as file:
                        # Writes the new code to the output file
                        file.write(old_code)
                        
                    old_code = old_code
                    exec(old_code)
                
                            
                # executes current saved file
                else: 
                    # Open the file in write mode ("w")
                    with open(new_file_path, "w") as file:
                        # Writes the new code to the output file
                        file.write(old_code)
                    
                    # splits the initial code into lines
                    lines = old_code.splitlines()
                    # obtains integer from user input
                    user_int = str(text_ints[0]) if text_ints else None
                
                
                    # Replace the first integer in the line where 'ball' is found with 150
                    for i, line in enumerate(lines):
                        # checks for upper case characters
                        match = re.search(r"([A-Z]+)", line)
                        if match and user_int != '':
                            char_combination = match.group(1)
                            # check if the same character combination exists in user_text
                            if char_combination in user_text and (user_int is not None) and len(line) < 21:
                                lines[i] = re.sub(r'\b\d+\b', user_int, line, 1)
                
                    # Recombines code lines and adds return code
                    old_code = '\n'.join(lines)
                    old_code = old_code + '\n' + return_code
                    
                    # execute the response string as code
                    validity = is_valid_code(old_code)
                    if validity == True:
                        exec(old_code) # executes new file
                    else:
                        invalid.set_error(error_str)
                        invalid.run("TextInput.py") # current game file as return code argument

                # erases existing input text
                user_text = ''
                
                
            # Check for mouse wheel events for scrolling
            elif event.key == pygame.K_UP:
                scroll_position = max(0, scroll_position - 1)
            elif event.key == pygame.K_DOWN:
                scroll_position = min(len(old_code_lines) - visible_lines, scroll_position + 1)

            # checks for backspace
            elif event.key == pygame.K_BACKSPACE:
                # removes most recently written text
                user_text = user_text[:-1]

            # saves the unicode input into the user text string
            else:
                user_text += event.unicode
                
    
    # checks if code is null
    if old_code == '':
        with open(new_file_path, "r") as file:
            old_code = file.read()
            old_code = old_code + '\n' + return_code
    
    # Split the old_code into lines
    old_code_lines = old_code.splitlines()
    line_surfaces = []
    
    # Check if the index exists before entering the loop
    if scroll_position + visible_lines < len(old_code_lines):
        # Render each line of old_code separately
        for i in range(scroll_position, scroll_position + visible_lines):
            line_surface = font.render(old_code_lines[i], True, (255, 255, 255))
            line_surfaces.append(line_surface)
            screen.blit(line_surface, (output_box.x + 5, output_box.y + 5 + (i - scroll_position) * 36))
    
    # renders and sets the width of the text fields
    screen.blit(text_surface, (text_box.x + 5, text_box.y + 5))
    text_box.w = max(100, text_surface.get_width() + 10)  # updates width with input text
    
    # Check if line_surfaces is not empty before calculating max width
    if line_surfaces:
        output_box.w = max(100, max(line_surface.get_width() for line_surface in line_surfaces) + 10)
    else:
        output_box.w = 100  # Default width if no lines in line_surfaces
    
    pygame.display.flip()

    pygame.display.update()
    clock.tick(30)

pygame.quit()