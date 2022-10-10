from codecs import BufferedIncrementalEncoder
from msilib.schema import EventMapping, Icon
from operator import iconcat
from turtle import distance
import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# titles and logo
pygame.display.set_caption("Space Gladiator")
icon=pygame.image.load('project.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('spaceship.png')
playerX = 365
playerY = 490
playerX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 18

for i in range (num_of_enemies):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(30)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 12
# ready - you cant see the bullet on the screen
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 70)

def show_score(x, y):
    score = font.render("score:" + " " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))
 
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#main game function
if __name__ == '__main__':
    running = True
    while running:
      
      # color: red green blue
      screen.fill((0, 0, 0))

      # background
      screen.blit(background, (0, 0))

      # for exiting the game
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          # keystroke is pressed whether its left or right
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  playerX_change = -4
              if event.key == pygame.K_RIGHT:
                  playerX_change = 4
              if event.key == pygame.K_SPACE:
                  # get the current x coordinate of the bullet
                  if bullet_state is "ready":
                      bullet_Sound = mixer.Sound('laser.mp3')
                      bullet_Sound.play()
                      bulletX = playerX
                      fire_bullet(bulletX, bulletY)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                  playerX_change = 0

      # checking if player goes out of bounds
      playerX += playerX_change

      if playerX <=0:
          playerX = 0
      elif playerX >=736:
          playerX = 736

      # enemy movement
      for i in range (num_of_enemies):

          # game over
          if enemyY[i] > 440:
              for j in range (num_of_enemies):
                  enemyY[j] = 2000
              game_over_text()
              break

          enemyX[i] += enemyX_change[i]

          if enemyX[i] <=0:
              enemyX_change[i] = 3
              enemyY[i] += enemyY_change[i]
          elif enemyX[i] >=736:
              enemyX_change[i] = -3
              enemyY[i] += enemyY_change[i]

          # collision
          collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
          if collision:
              explosion_Sound = mixer.Sound('Explosion.wav')
              explosion_Sound.play()
              bulletY = 490
              bullet_state = "ready"
              score_value += 1
              enemyX[i] = random.randint(0,735)
              enemyY[i] = random.randint(50,150)
          
          enemy(enemyX[i], enemyY[i], i)

      # bullet movement
      if bulletY <= 0:
          bulletY = 490
          bullet_state = "ready"

      if bullet_state is "fire":
          fire_bullet(bulletX, bulletY)
          bulletY -= bulletY_change

      player(playerX, playerY)
      show_score(textX, textY)
      pygame.display.update()
