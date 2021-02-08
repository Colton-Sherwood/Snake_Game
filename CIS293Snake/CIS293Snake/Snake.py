import os, sys
import pickle
import time
import random
import pygame
from pygame.locals import *
import shelve

import math
import getopt
from socket import *

pygame.init() #start the game
BLUE = (50, 153, 213)
RED = (213, 50, 80)
GREEN = (139, 69, 19)
YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WALL_COLOR = BLACK
high_score = 10

#Prabin
# load the previous score if it exits
try:
    with open('high_score.txt', 'rb') as hisc:
        high_score_str = hisc.read()
        high_score = int(high_score_str)
except:
    high_score = 10


#set title of game
pygame.display.set_caption("Snake game")

dis_width = 600
dis_height = 400

# set size of game window based on tuple
DIS = pygame.display.set_mode((dis_width, dis_height))

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("helvetica", 30)
score_font = pygame.font.SysFont("comicsansms", 35)

#function that loads and returns sound file
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('Sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

# function to Load images and return usable image, and the images corresponding rect
# a rect is a rectangular area that the object occupies
def load_png(name):
    fullname = os.path.join('Images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print ('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()


block = 20

class Player(pygame.sprite.Sprite):
    '''player class that controls the snake and everything it does'''
    def __init__(self):

        self.direction = "up"
        self.x = dis_width / 2
        self.y = dis_height / 2
        self.head = [self.x, self.y]
        self.list = [self.head]
        self.xChange = 0
        self.yChange = 0
        self.length = 1
        self.speed = 5

        '''default constructor loads snake images and sets initial properties'''
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png("SnakeUp.png")
        self.imgU = pygame.transform.scale((load_png("SnakeUp.png.")[0]), (block, block))
        self.imgR = pygame.transform.scale((load_png("SnakeRight.png")[0]), (block, block))
        self.imgD = pygame.transform.scale((load_png("SnakeDown.png")[0]), (block, block))
        self.imgL = pygame.transform.scale((load_png("SnakeLeft.png")[0]), (block, block))
        self.imgTu = pygame.transform.scale((load_png("TailDown.png")[0]), (block, block))
        self.imgTr = pygame.transform.scale((load_png("TailLeft.png")[0]), (block, block))
        self.imgTd = pygame.transform.scale((load_png("TailUp.png")[0]), (block, block))
        self.imgTl = pygame.transform.scale((load_png("TailRight.png")[0]), (block, block))
        self.imgBud = pygame.transform.scale((load_png("BodyUD.png")[0]), (block, block))
        self.imgBlr = pygame.transform.scale((load_png("BodyLR.png")[0]), (block, block))

        self.surf = pygame.transform.scale(self.image[0], (block, block))
        self.rect = self.image[1]



    def update(self, pressed_keys):
        """updates snake based on keys pressed, ensures snake loops
        around display"""
        # read key presses in event log and change position accordingly
        if pressed_keys[K_UP]:
            if self.direction == "down":
                pass
            else:
                self.yChange = -block
                self.xChange = 0
                self.direction = "up"
                self.surf = pygame.transform.scale(self.image[0], (block, block))
        if pressed_keys[K_DOWN]:
            if self.direction == "up":
                pass
            else:
                self.yChange = block
                self.xChange = 0
                self.direction = "down"
                self.surf = self.imgD
        if pressed_keys[K_LEFT]:
            if self.direction == "right":
                pass
            else:
                self.xChange = -block
                self.yChange = 0
                self.direction = "left"
                self.surf = self.imgL
        if pressed_keys[K_RIGHT]:
            if self.direction == "left":
                pass
            else:
                self.xChange = block
                self.yChange = 0
                self.direction = "right"
                self.surf = self.imgR

        # when snake passes the boundaries of the screen it will loop through to the opposite side
        if self.x >= dis_width:
            self.x = 0
        if self.x < 0:
            self.x = dis_width
        if self.y >= dis_height:
            self.y = 0
        if self.y < 0:
            self.y = dis_height

        # add the direction change based on button press
        self.x += self.xChange
        self.y += self.yChange

        self.head = []
        self.head.append(self.x)
        self.head.append(self.y)
        self.head.append(self.direction)
        self.list.append(self.head)

        #if list has more items than the length of snake delete first item in list
        if len(self.list) > self.length:
            del self.list[0]
        
    def die(self):
        #checks every value in list except most recently appended
        #if value == current head position return true
        for pos in self.list[:-1]:
            if pos[0] == self.head[0] and pos[1] == self.head[1]:
                return True


    def eat(self):
        # increase player length & speed
        self.length += 1
        self.speed += 0.5

    def render(self):
        # for each pos in list print to the display
        #draw head (last item in list)
        DIS.blit(self.surf, (self.head[0], self.head[1]))

        #draw for each pos in list besides first and last print body section
        for pos in self.list[1:-1]:
            if pos[2] == "up" or pos[2] == "down":
                DIS.blit(self.imgBud, (pos[0], pos[1]))
            elif pos[2] == "right" or pos[2] == "left":
                DIS.blit(self.imgBlr, (pos[0], pos[1]))

            
        #draw tail as first item in list
        if self.length > 1:
            if self.list[0][2] == "up":
                DIS.blit(self.imgTu, (self.list[0][0], self.list[0][1]))
            elif self.list[0][2] == "right":
                DIS.blit(self.imgTr, (self.list[0][0], self.list[0][1]))
            elif self.list[0][2] == "down":
                DIS.blit(self.imgTd, (self.list[0][0], self.list[0][1]))
            elif self.list[0][2] == "left":
                DIS.blit(self.imgTl, (self.list[0][0], self.list[0][1]))
           

class Food(pygame.sprite.Sprite):
    '''food class that spawns at random location on board'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #load_png returns a tuple (image, image.get_rect())
        self.img = load_png("Apple.png")
        self.surf = pygame.transform.scale(self.img[0], (block, block))
        self.rect = self.img[1]
        self.x = round(random.randrange(0, dis_width - block) / block) * block
        self.y = round(random.randrange(0, dis_height - block) / block) * block

    def update(self):
        self.x = round(random.randrange(0, dis_width - block) / block) * block
        self.y = round(random.randrange(0, dis_height - block) / block) * block


    def render(self):
        DIS.blit(self.surf,(self.x, self.y))

class Enemy(pygame.sprite.Sprite):
    '''enemy class creates an enemy 5 blocks long that moves erratically.'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.length = 5
        self.x = round(random.randrange(0, dis_width - block) / block) * block
        self.y = round(random.randrange(0, dis_height - block) / block) * block
        self.head = [self.x, self.y]
        self.list = [self.head, [self.head[0]-block, self.head[1]], [self.head[0]-(2*block), self.head[1]], [self.head[0]-(3*block), self.head[1]]]

    def update(self):
        if round(random.randrange(0, block) > 10):
            self.y += block
        else: self.x += block

        # when snake passes the boundaries of the screen it will loop through to the opposite side
        if self.x >= dis_width:
            self.x = 0
        if self.x < 0:
            self.x = dis_width
        if self.y >= dis_height:
            self.y = 0
        if self.y < 0:
            self.y = dis_height

        self.head = []
        self.head.append(self.x)
        self.head.append(self.y)
        self.list.append(self.head)

    def render(self):
        for pos in self.list:
            pygame.draw.rect(DIS, WALL_COLOR, [pos[0], pos[1], block, block])

        if len(self.list) > self.length:
            del self.list[0]

    def die(self):
        self.kill()

class Wall(pygame.sprite.Sprite):
    '''class for walls find's initial coordinates and renders in position'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = round(random.randrange(0, dis_width - block) / block) * block
        self.y = round(random.randrange(0, dis_height - block) / block) * block
        self.list = [self.x, self.y], [self.x, self.y - block], [self.x, self.y - (2*block)], [self.x, self.y - (3*block)], [self.x, self.y - (4*block)], [self.x, self.y - (5*block)]

    def render(self):
        for pos in self.list:
            pygame.draw.rect(DIS, WALL_COLOR, [pos[0], pos[1], block, block])

#Prabin
def your_Score(score):
    global high_score
    if (score > high_score):
        high_score = score
        with open("high_score.txt", "r+") as hisc:
            hisc.write(str(high_score))
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    value_high_score = score_font.render("High Score: " + str(high_score), True, YELLOW)
    DIS.blit(value, [0, 0])
    DIS.blit(value_high_score, [330, 0])

def message(msg, color):
    '''Function to display basic message on screen'''
    mesg  = font_style.render(msg, True, color)
    DIS.blit(mesg, [dis_width/8, dis_height/8])

def gameLoop(): # Function to play game

    # load chomp sound
    chomp_sound = load_sound("Chomp.wav")
    ouch_sound = load_sound("Ouch.wav")
    background_music = load_sound("SpiralMountain.mp3")

    #play background music
    background_music.play(-1)

    game_over = False
    game_close = False

    # create initial player and food objects
    player = Player()
    apple = Food()

    # counter's to determine when walls and enemies spawn
    eCount = 1
    wCount = 1

    # Group to add all 'food' items too
    food_group = pygame.sprite.Group()
    food_group.add(apple)

    # Group to add all 'enemy' items too
    enemy_group = pygame.sprite.Group()
    #enemy_group.add(enemy1)

    wall_group = pygame.sprite.Group()

    while not game_over:  #loop over all events happening in game'
        #fill background of game
        DIS.fill(BLUE)

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # pass pressed_keys dictionary to Player's update method to move player
        player.update(pressed_keys)

        #update enemy position each loop
        for enemy in enemy_group:
            enemy.update()

        while game_close == True:
            DIS.fill(BLUE)
            message("You Lost! Press Q to Quit or C to Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        background_music.stop()
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if you press the x game quits
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

        #check if tail/body == head
        if player.die() == True:
            game_close = True
            ouch_sound.play()

        # when head collides enemy 'tail' end the game
        # loop through enemies in enemy_group
        for enemy in enemy_group:
            #loop through coordinates of each enemy according to their list
            for pos in enemy.list[:-1]:
                # Check each position in the enemy list to see if it collides with the player head
                if [pos[0], pos[1]] == [player.head[0],  player.head[1]]:
                    game_close = True
                    ouch_sound.play()
            
        # if an enemy runs into players body they will die
        for pos in player.list[:-1]:
            for enemy in enemy_group:
                if enemy.head == [pos[0], pos[1]]:
                    enemy.die()

        # if player runs into wall the game will end
        for wall in wall_group:
            for pos in wall.list[:]:
                if [pos[0], pos[1]] == [player.head[0], player.head[1]]:
                    game_close = True
                    ouch_sound.play()

        # enemies spawn based on their respective counter values
        if eCount % 8 == 0:
            newEnemy = Enemy()
            enemy_group.add(newEnemy)
            eCount = eCount + 1

        if wCount % 5 == 0:
            newWall = Wall()
            wall_group.add(newWall)
            wCount = wCount + 1

        # if snake head and food are on same location, food is 
        # moved to a different location and 1 is added to the
        # length of the snake speed is also increased by 1
        if player.x == apple.x and player.y == apple.y:
            # make food spawn in new location
            apple.update()
            # increase snake length & speed
            player.eat()
            # play the chomp sound
            chomp_sound.play()
            #increase eCount and wCount to help with spawning enemies
            eCount = eCount + 1
            wCount = wCount + 1

        #update score
        your_Score((player.length - 1) * 10)

        # render all sprites
        for enemy in enemy_group:
            enemy.render()

        for wall in wall_group:
            wall.render()

        player.render()
        apple.render()

        # update the display and tick speed
        pygame.display.update()
        clock.tick(player.speed)

    pygame.quit()
    quit()

#execute game loop
gameLoop()