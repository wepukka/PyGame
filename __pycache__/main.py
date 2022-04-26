import pygame, os
from random import randrange

WIDTH,HEIGHT = 1600,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("MONEYY")

BLACK = (0,0,0)
WHITE = (255, 255,255)
YELLOW = (255,255,0)

FPS = 30

# CHARACTER DEFAULT WIDTH 100, HEIGHT 100 # RESIZE method = pygame.transform.scale(image, (width, height))
CHARACTER_WIDTH, CHARACTER_HEIGHT = 100, 100
CHARACTER_FACE_BACKWARD = pygame.image.load(os.path.join("assets", "CharFaceBackward.png"))

CHARACTER_DEAD = pygame.transform.rotate(CHARACTER_FACE_BACKWARD, (180)) #Turn upside down


def get_mouse_position(player_location):
    if pygame.mouse.get_pressed:
        x,y = pygame.mose.get_pos()
       
def draw_borders():
    BORDER_RIGHT = pygame.Rect(WIDTH- 8,0,10, HEIGHT)
    BORDER_LEFT = pygame.Rect(WIDTH- 1600,0, 10, HEIGHT)
    pygame.draw.rect(WIN, BLACK, BORDER_RIGHT)
    pygame.draw.rect(WIN, BLACK, BORDER_LEFT)

def draw_window(player):
    WIN.fill(WHITE)
    WIN.blit(CHARACTER_FACE_BACKWARD, (player.x, player.y))
    draw_borders()
    pygame.display.update()

def randomize_spawn():
    x = randrange(800)
    y = randrange(1500)
    return x,y
    

def main():
    
    player = pygame.Rect(800, 750, CHARACTER_HEIGHT,CHARACTER_WIDTH)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.MOUSEBUTTONDOWN]:
            print("mouse1")
        draw_window(player)
        
        
          
    pygame.quit()
    
if __name__ == "__main__":
    main()