
import pygame, pygame.font
import random
import os 
import time
import sys 

from pygame.mixer import Sound 

 


# Pygame init
pygame.init()
temp = pygame.display.Info()
displLength = (temp.current_w, temp.current_h)
surface = pygame.display.set_mode(displLength, pygame.FULLSCREEN)
# Font init
pygame.font.init()
fontObj = pygame.font.Font(pygame.font.get_default_font(), 14)
sampleLetter = fontObj.render('_', False, (0, 111, 0))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0) 
 
COLOR1 = (255, 0, 0)
COLOR2 = (0, 255, 0)
COLOR3 = (0, 0, 255)
COLOR4 = (122, 122, 122)
COLOR5 =  (0, 122, 0)
 

 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 11
HEIGHT = 11

# This sets the margin between each cell
MARGIN = 1

# Set the number of rows and columns of the grid
ROWS = 73
COLS = 23



# The code for creating the grid is based on the example from 
# http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
# Full credit to the original author 


# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(ROWS):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(COLS):
        grid[row].append(0)  # Append a cell
 
 
 # read message message

def open_message(file_name):
    lines = []
    try:
        file_path = os.path.join(os.path.dirname(__file__),file_name)
        print file_path

        with open(file_path, "r+")  as f:
            g_row  = 0
            # read one line at a time from file
            for line in f: 
                l = line.strip()
                #read one character at a time into the grid		
                g_col = 0
                for i in xrange(len(l)):
                    if '1' in l[i]:
                        grid[g_row][g_col] = 1
                    g_col = g_col + 1
                g_row = g_row + 1				
    except:
        str = ''
        print "Error"



#### clear

def clear():
  for g_row in range(ROWS):
      for g_col in range(COLS):
        grid[g_row][g_col] = 0



### save message to text file

def save(file_name):
    lines = ''

    file_path = os.path.join(os.path.dirname(__file__),file_name)

    with open(file_path, 'w') as f:
        for g_row in range(ROWS):
            line = ''
            for g_col in range(COLS):
                line = line + str(grid[g_row][g_col])
                lines = lines + line

            f.write("%s\n" % line)


 
 

### play beeps...read from top to bottom and play a sound for every 1
def play():
  

    file_path =  os.path.join(os.path.dirname(__file__),"beep_short.mp3")
    print file_path
  
    beep=pygame.mixer.Sound(file_path) 
  
    pygame.event.wait()
 
    save("temp.txt")
    print "message start"
    for g_row in range(ROWS):
        for g_col in range(COLS):
            if grid[g_row][g_col] == 1: 
               beep.play()
               time.sleep(0.1) 
               draw_rect(g_row,g_col,WHITE)    
            else:                                     
                pygame.display.flip()       
    
    open_message("temp.txt")
    print "message ended"

### random color
def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


# checks is the row does not contain a 1
def is_empty_row(row):
    empty = True
    for row in range(ROWS):
        for column in range(COLS):
            if grid[row][column] == 1:
              return False          
    return True          


# draws a rectangle cell
def draw_rect(row, column,  color):
         pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])


# for some reason the mixer needs to be init first 
pygame.mixer.init() 


# Initialize pygame
pygame.init()

WIN_HEIGHT = (ROWS * 12)  
WIN_WIDTH  = (COLS * 12) 

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Press 'S' save 'C' Clear 'P' play")

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# open the default message file

open_message("message.txt")
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one

            # mark or unmark the cell
            if grid[row][column] == 1:
                     grid[row][column] = 0
            else : 
              grid[row][column] = 1


            print("Click ", pos, "Grid coordinates: ", row, column)
        
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_c  :
              clear()
          elif event.key == pygame.K_s :
                    #timestr = time.strftime("%Y%m%d-%H%M%S")
                    file_name = "new_message.txt"
                    save(file_name)
          elif event.key == pygame.K_p  :
               play()
        

       

    # Set the screen background
    screen.fill(BLACK)
  
   



    # Draw the grid
    for row in range(ROWS):
        
        # change the color if we hit an empty row 
        if is_empty_row(row):
             color = random_color   
        
        
        for column in range(COLS):
            color = BLACK
 
            if grid[row][column] == 1:


               if row in range(5):
                  color = COLOR1
               elif row in range(5,10):
                   color = COLOR2
               elif row in range(10,20):
                    color = COLOR3   
        	  
               else:  	
                  color = RED
               
            draw_rect(row,column,color)
            
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.

save("new_message.txt")
pygame.quit()
