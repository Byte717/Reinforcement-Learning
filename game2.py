'''Descripcion'''

import pygame
import time
import random
import tensorflow as tf
import numpy as np
import time
import random
import pickle
# Initialize Pygame
lr = 0.001
gamma = 0.99
memory = list()

exploreProb = 1.0
decay = 0.005
actions = 3



model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256,input_shape=(4,), activation='relu'),
    tf.keras.layers.Dense(actions,activation='linear')
])
model.compile(loss="mse",optimizer=tf.keras.optimizers.legacy.Adam(lr=lr))


pygame.init()
pygame.font.init()

# Colors in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Loading the images
images = {}
images["icon"] = pygame.image.load("images/space-invaders.png")
images["player"] = pygame.image.load("images/space-invaders.png")
images["player"] = pygame.transform.scale(images["player"], (64,64))
images["bg"] = pygame.image.load("images/bg.png")
# images["tonga"] = pygame.image.load("images/tonga.png")
images["enemy"] = pygame.image.load("images/enemy.png")
# Creates the fonts
bigFont = pygame.font.SysFont('Times New Roman', 60)
smlFont = pygame.font.SysFont('Times New Roman', 30)
largeText = pygame.font.Font('freesansbold.ttf', 70)

# Create the screen
gameDisplayW, gameDisplayH = 1000, 500
gameDisplay = pygame.display.set_mode((gameDisplayW, gameDisplayH))

# Caption and icon
pygame.display.set_caption("Teaching a bird to fly")
pygame.display.set_icon(images["icon"])


# Function to display text made by Isidro
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((gameDisplayW / 2), (gameDisplayH / 2))
    gameDisplay.blit(TextSurf, TextRect)


# Definition of the classes:
class Button():
    '''
    This class creates a button that is displayed on the gameDisplay
    and that has a color and a text. It's useful for the GUI.
    '''

    def __init__(self, x, y, w, h, color, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text

        self.state = False

        self.buttonTextSurface = bigFont.render(self.text, False, (0, 0, 0))

    def display(self):
        '''Displays the button (rect and text) on the gameDisplay'''
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.w, self.h))
        gameDisplay.blit(self.buttonTextSurface, (self.x, self.y))

    def press(self):
        '''Checks is the mouse is inside the button or not'''
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.w and \
                self.y < pos[1] < self.y + self.h:
            return True
        else:
            return False


class GameObject(object):
    '''Descripcion'''

    def __init__(self, x, y, image):
        '''Descripcion'''
        self.x = x
        self.y = y
        self.image = image

    def display(self):
        '''Descripcion'''
        gameDisplay.blit(self.image, (self.x, self.y))
        pygame.draw.circle(gameDisplay,(0,255,0),(self.x,self.y),2)


class Player(GameObject):
    '''Descripcion'''

    def __init__(self, image):
        '''Descripcion'''
        self.x = (gameDisplayW * 0.1)
        self.y = 250
        self.w = 64
        self.h = 64
        self.image = image
    def reset(self):
        self.x = (gameDisplayW * 0.1)
        self.y = 250
    def jump(self):
        '''Descripcion'''
        pass

    def move(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_SPACE]:
            self.y -= 10
        else:
            self.y += 10
        '''if self.y >= 400:
            self.y = 400
        elif self.y <= 70:
            self.y = 70'''
    def move2(self,order):
        if order == 1:
            self.y += 10
        elif order == 0:
            self.y -= 10

    def dieAndRestart(self):

        '''Descripcion'''
        pass


player = Player(images["player"])
frame = 0


class Danger(GameObject):
    '''Descripcion'''

    def __init__(self):
        '''Descripcion'''
        self.x = 900
        self.y = random.randrange(0, gameDisplayH)
        self.w = 40
        self.h = 40
        self.image = images["enemy3"] = pygame.image.load("images/enemy3.png")

        self.speed = -5

    # def display(self, color):
    # '''Descripcion'''
    # pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.w, self.h])

    def checkOOBAndRestart(self):
        '''Descripcion'''
        if self.x <= 0:
            self.x = 1000
            self.y = random.randrange(0, gameDisplayH)

    def collide(self):
        '''Descripción'''
        if self.x < player.x + player.w and \
                self.x + self.w > player.x and \
                self.y < player.y + player.h and \
                self.y + self.h > player.y:
            restartGame()


class Plataforma(GameObject):
    '''Descripcion'''

    def __init__(self):
        '''Descripcion'''
        pass


class Level():
    def __init__(self):
        '''Descripcion'''
        pass

    def printLevel(self):
        '''Descripcion'''
        pass

    def displayLevel(self):
        '''Descripcion'''
        pass


startButton = Button(gameDisplayW / 2 - 200 / 2, 200, 200, 100, (100, 100, 200), "START")

# In variable names, TS stands for Text Surface
titleTS = bigFont.render("Tongometry Dash", False, (50, 50, 150))
creditsTS = smlFont.render("Creado por I. BORTHA, J. COLASO, T. ONGA. 2020", False, (50, 50, 150))


def titleScreen():
    '''Descripción'''

    global frame
    gameDisplay.fill((200, 255, 255))

    startButton.display()
    gameDisplay.blit(titleTS, (300, 25))
    gameDisplay.blit(creditsTS, (180, 460))

    # Events of the first frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            # Button that goes to the next frame
            if startButton.press():
                gameDisplay.blit(images["bg"], (0, 0))
                frame = 1


def restartGame():
    '''Descripción'''

    message_display('Ouch ouch')
    pygame.display.update()
    player.y = (gameDisplayH * 0.35)
    time.sleep(1)
    gameplay()






    # Code for the first frame
    # if frame == 0:
    #     titleScreen()
    #
    # # Code for the second frame
    # elif frame == 1:
    #     gameplay()
    #     pygame.quit()
    #     quit()


def makeMove(state):
    if np.random.uniform(0,1) < exploreProb:
        return np.random.choice(range(actions))
    else:
        # qVal = model.predict(state,verbose=1)[0]
        qVal = model(state)
        print(np.argmax(qVal))
        return np.argmax(qVal)


def updateProb(exploreProb):
    return exploreProb * np.exp(-decay)



def simulate():

    global bg, clock

    def collide():
        return danger.x < player.x + player.w and danger.x + danger.w > player.x and danger.y < player.y + player.h and danger.y + danger.h > player.y

    danger = Danger()
    clock = pygame.time.Clock()
    bg = GameObject(0,0,images["bg"])
    exit = False
    while not exit:
        currState = np.array([[player.x,player.y,danger.x,danger.y]])
        move = makeMove(currState)
        step(move, danger, bg,clock)
        nextState = np.array([[player.x,player.y,danger.x,danger.y]])
        over = collide()
        outOfBounds = False
        if player.y < 0 or player.y > gameDisplayH:
            outOfBounds = True


        reward = 0
        if over:
            reward = -2
        if player.x > danger.x:
            reward = 2
        if outOfBounds:
            reward = -2


        currentData = {
            "curr": currState,
            "action":move,
            "reward":reward,
            "next":nextState,
            "done": over
        }
        memory.append(currentData)
        if len(memory) > 500:
            memory.pop(0)
        if over or outOfBounds:
            del danger, bg, clock
            exit = True




def step(move,danger,background,clock):
    background.x = background.x - 2
    if background.x == -1000:
        background.x = 0
    gameDisplay.blit(images["bg"], (background.x + 1000, 0))
    gameDisplay.blit(images["bg"], (background.x, 0))

    player.display()
    player.move2(move)

    danger.x += danger.speed
    danger.checkOOBAndRestart()
    danger.display()

    pygame.display.update()
    clock.tick(240)


def train():
    np.random.shuffle(memory)
    # sample = random.sample(memory, 32)
    for i in range(32):
        experience = memory[i]
        input = tf.convert_to_tensor(experience["curr"],dtype=tf.float32)
        # currQ = model.predict(input,verbose=0)
        currQ = model(input).numpy()
        target = experience["reward"]

        if not experience["done"]:
            # target = target + gamma*np.max(model.predict(experience["next"],verbose=0)[0])
            target = target + gamma*np.max(model(experience["next"]))
        currQ[0][experience["action"]] = target
        model.fit(experience["curr"], currQ,epochs=1, verbose=1)

while True:
    # Simulate game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # with open("save.UTF-8","wb") as f:
            #     for i in memory:
            #         pickle.dump(i,f)
                
            pygame.quit()
            break
    simulate()
    exploreProb = updateProb(exploreProb)
    # Train model
    train()
    player.reset()
