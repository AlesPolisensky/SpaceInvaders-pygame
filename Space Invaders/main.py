import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# vytvoření herního okna, zatím nezůstane zapnuté, ale hned se vypne,
# protože python přečte jen kód a hned se zavře

screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Scuffed Space Invaders")
icon = pygame.image.load("ufo (1).png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("space-invaders (1).png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
# ready state = you can't see the bul let on the screen
# fire = bullet is moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# vytvoření hráče
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# !!!!!GAME LOOP!!!!!
# vytvoříme hodnotu, kdy "running" je zpočátku na True,
# když je running na true vytvoříme while/for smyčku,
# kdy "pygame.event.get()" sleduje jakýkoliv event na screenu,
# včetně zavření okna, dále vytvoříme příkaz if, který změní
# hodnotu "running" na false, když zavřeme herní okno (pygame.QUIT)
# toto ukončí smyčku kterou držela hodnota True u running v pohybu


running = True
while running:
    # Barva pozadí
    screen.fill((0, 0, 0))

    # Background img
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if it's left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # vložení hráče do hry
    player(playerX, playerY)

    # vložení skóre
    show_score(textX, textY)

    # updatování změn
    pygame.display.update()
