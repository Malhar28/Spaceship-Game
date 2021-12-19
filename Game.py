import pygame
import os


pygame.font.init()
pygame.mixer.init()

# Defining Game Specific Variables
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

SPACESHIP_WIDTH = 55
SPACESHIP_HEIGTH = 40

FPS = 60

VELOCITY = 4
BULLET_VEL = 7.3

MAX_BULLETS = 3

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONTS = pygame.font.SysFont("comicsans", 40)
WINNER_FONTS = pygame.font.SysFont("comicsans", 90)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))
BACKGORUND_SONG = pygame.mixer.Sound(os.path.join('Assets', 'bg_song.mp3'))
WINNING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Winning_Sound.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH,HEIGHT))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGTH)), 90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGTH)), 270)

RED_HEALTH = 10
YELLOW_HEALTH = 10


# Defining Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
meganta = (255, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
sky_blue = (0, 255, 255)
blue = (0, 0, 255)
grey = (233, 220, 229)
banana_color = (227, 207, 87)
brown = (165, 42, 42)
brick = (156, 102, 31)
skin = (255, 211, 155)
gold = (255, 215, 0)
light_grey = (224, 224, 224)
light_green = (0, 238, 0)
pink = (255, 110, 180)
dark_blue = (0, 0, 128)
orange = (255, 128, 0)
olive = (192, 255, 62)
pale_green = (152, 251, 152)
rose_brown = (188, 143, 143)
smoke_white = (245, 245, 245)


# Creating Loop for Drawing or Adding things in thw window
def DrawWindow(RED, YELLOW, RED_BULLETS, YELLOW_BULLETS, RED_HEALTH, YELLOW_HEALTH):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, black, BORDER)

    RED_HEALTH_TEXT = HEALTH_FONTS.render(f"Health: {str(RED_HEALTH)}",1, white)
    YELLOW_HEALTH_TEXT = HEALTH_FONTS.render(f"Health: {str(YELLOW_HEALTH)}",1, white)

    WINDOW.blit(RED_HEALTH_TEXT, (WIDTH-RED_HEALTH_TEXT.get_width() -10,10))
    WINDOW.blit(YELLOW_HEALTH_TEXT, (10,10))
    WINDOW.blit(YELLOW_SPACESHIP, (YELLOW.x, YELLOW.y))
    WINDOW.blit(RED_SPACESHIP , (RED.x, RED.y))
    
    for Bullets in YELLOW_BULLETS:
        pygame.draw.rect(WINDOW, yellow, Bullets)

    for Bullets in RED_BULLETS:
        pygame.draw.rect(WINDOW, red, Bullets)

    pygame.display.update()


def DRAW_TEXT(text):
    DRAW_TEXT = WINNER_FONTS.render(text, 1, white)
    WINDOW.blit(DRAW_TEXT, (WIDTH/2 - DRAW_TEXT.get_width()/2, HEIGHT/2 - DRAW_TEXT.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

    


def YELLOW_MOVEMENT(Keys_Pressed, YELLOW):
    if Keys_Pressed[pygame.K_a] and YELLOW.x - VELOCITY > 0 - 3:
        YELLOW.x -= VELOCITY
    if Keys_Pressed[pygame.K_d] and YELLOW.x +  VELOCITY + YELLOW.width < BORDER.x + 15:
        YELLOW.x += VELOCITY
    if Keys_Pressed[pygame.K_w] and YELLOW.y - VELOCITY > 0:
        YELLOW.y -= VELOCITY
    if Keys_Pressed[pygame.K_s] and YELLOW.y + VELOCITY + YELLOW.height < HEIGHT - 15:
        YELLOW.y += VELOCITY

def RED_MOVEMENT(Keys_Pressed, RED):
    if Keys_Pressed[pygame.K_RIGHT] and RED.x +  VELOCITY + RED.width < WIDTH + 17:
        RED.x += VELOCITY
    if Keys_Pressed[pygame.K_LEFT] and RED.x - VELOCITY > BORDER.x + BORDER.width:
        RED.x -= VELOCITY
    if Keys_Pressed[pygame.K_UP] and RED.y - VELOCITY > 0:
        RED.y -= VELOCITY
    if Keys_Pressed[pygame.K_DOWN] and RED.y + VELOCITY + RED.height < HEIGHT - 15:
        RED.y += VELOCITY

def HANDLE_BULLETS(YELLOW_BULLETS, RED_BULLETS, YELLOW, RED):
    for BULLETS in YELLOW_BULLETS:
        BULLETS.x += BULLET_VEL
        if RED.colliderect(BULLETS):
            pygame.event.post(pygame.event.Event(RED_HIT))
            YELLOW_BULLETS.remove(BULLETS)
        elif BULLETS.x > WIDTH:
            YELLOW_BULLETS.remove(BULLETS)


    for BULLETS in RED_BULLETS:
        BULLETS.x -= BULLET_VEL
        if YELLOW.colliderect(BULLETS):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            RED_BULLETS.remove(BULLETS)
        elif BULLETS.x < 0:
            RED_BULLETS.remove(BULLETS)

# Crreating the Game Loop
def MAIN():
    BACKGORUND_SONG.play()
    global RED_HEALTH, YELLOW_HEALTH
    RED = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGTH)
    YELLOW = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGTH)
    
    RED_BULLETS = []
    YELLOW_BULLETS = []

    CLOCK = pygame.time.Clock()

    RUN = True

    while RUN:
        CLOCK.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                RUN = False
                
            
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LCTRL and len(YELLOW_BULLETS) < MAX_BULLETS:
                    BULLET = pygame.Rect(YELLOW.x + YELLOW.width, YELLOW.y + YELLOW.height//2 - 2, 10,5)
                    YELLOW_BULLETS.append(BULLET)
                    BULLET_FIRE_SOUND.play()


                if events.key == pygame.K_RCTRL and len(RED_BULLETS) < MAX_BULLETS:
                    BULLET = pygame.Rect(RED.x, RED.y + RED.height//2 - 2, 10,5)
                    RED_BULLETS.append(BULLET)
                    BULLET_FIRE_SOUND.play()

            if events.type == RED_HIT:
                RED_HEALTH -= 1
                BULLET_HIT_SOUND.play()
 
            if events.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
                BULLET_HIT_SOUND.play()

        WINNER_TEXT = ""
        if RED_HEALTH <= 0:
            WINNER_TEXT = "Yellow Wins!"
            BACKGORUND_SONG.stop()
            WINNING_SOUND.play()


        if YELLOW_HEALTH <= 0:
            WINNER_TEXT = "Red Wins!"
            BACKGORUND_SONG.stop()
            WINNING_SOUND.play()

        if WINNER_TEXT != "":
            DRAW_TEXT(WINNER_TEXT)
            break

        Keys_Pressed = pygame.key.get_pressed()
        
        YELLOW_MOVEMENT(Keys_Pressed, YELLOW)
        RED_MOVEMENT(Keys_Pressed, RED)

        HANDLE_BULLETS(YELLOW_BULLETS, RED_BULLETS, YELLOW, RED)

        DrawWindow(RED, YELLOW, RED_BULLETS, YELLOW_BULLETS, RED_HEALTH, YELLOW_HEALTH)
        

    pygame.quit()



# Running and testing the game 
if __name__ == '__main__':
    MAIN()
