#MeziFly Game - Before start, if you want to use the handtracking system please start, the 'handtracker.py' (you can find it in the 'handtracking' directory) script, else you can play the game with pressing SPACE button to jump.
# Import module
import random
import sys
import os
import pygame
from pygame.locals import *
from pyvidplayer import Video
from pygame import mixer

# All the Game Variables
window_width = 600
window_height = 499
  
# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('MeziFly - By Team MF')
logo = pygame.image.load('images/logo.png')
pygame.display.set_icon(logo)
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'images/pipe.png'
background_starter_image = 'images/starter-background.jpg'
background_image = 'images/background.jpg'
birdplayer_image = 'images/mezi.png'
sealevel_image = 'images/base.jfif'


 #Intro

mixer.init()

vid = Video("Videos/intro.mp4")
vid.set_size((600,499))

def intro():
    state = True
    while state==True:
        vid.draw(window,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and (event.key == K_SPACE):
                vid.close()
                state = False
  
def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100
  
    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()
  
    # List containing lower pipes
    down_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_pipe[1]['y']},
    ]
  
    # List Containing upper pipes
    up_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
         'y': second_pipe[0]['y']},
    ]
  
    # pipe velocity along x
    pipeVelX = -4
  
    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
  
    bird_flap_velocity = -8
    bird_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
            status = 0
            status_data = list()
            if os.path.exists('handtracking/status.txt'):
                file = open("handtracking/status.txt",'r',encoding="UTF-8")
                for sor in file:
                    sor.strip()
                    status_data.append(sor)
                file.close()
            if len(status_data) > 0:
                status = status_data[-1]
            if int(status) > 0:
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
  
        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                               vertical,
                               up_pipes,
                               down_pipes)
        if game_over:
            return
  
        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Pontszamod {your_score}")
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + \
            min(bird_velocity_y, elevation - vertical - playerHeight)
  
        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
  
        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
  
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))
  
        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
  
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
  
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
  
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

  
def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True
  
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and\
           abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
  
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and\
        abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False
  
  
def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + \
        random.randrange(
            0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},
  
        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe
  
intro()
pygame.mixer
mixer.music.set_volume(0.7)
mixer.music.load('music/1.mp3')
music = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
for i in range(len(music)):
    mixer.music.queue(('music/'+str(music[i])+'.mp3'))
   
mixer.music.play()

# program where the game starts
if __name__ == "__main__":
  
        # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
  
    # Sets the title on top of game window
    pygame.display.set_caption('MeziFly')
  
    # Load all the images which we will use in the game
  
    # images for displaying score
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(
        birdplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(
        sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(
        background_image).convert_alpha()
    game_images['starter_background'] = pygame.image.load(
        background_starter_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(
        pipeimage).convert_alpha(), 180), pygame.image.load(
      pipeimage).convert_alpha())
  
    print("Udvozlunk a MeziFlyban")
    print("Kez felfele emelesevel indithato el a jatek")


    # Here starts the main game

    while True:
  
        # sets the coordinates of flappy bird
  
        horizontal = int(window_width/5)
        vertical = int(
            (window_height - game_images['flappybird'].get_height())/2)
        ground = 0
        while True:
            for event in pygame.event.get():
  
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
               
                # If the user presses space or
                # up key, start the game for them
                if event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):

                    flappygame()
                
                status = 0
                status_data = list()
                if os.path.exists('handtracking/status.txt'):
                    file = open("handtracking/status.txt",'r',encoding="UTF-8")
                    for sor in file:
                        sor.strip()
                        status_data.append(sor)
                    file.close()
                if len(status_data) > 0:
                    status = status_data[-1]
                if int(status) > 0:
                    flappygame()
                    # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['starter_background'], (0, 0))
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)