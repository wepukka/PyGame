import pygame, os
from random import randrange

WIDTH,HEIGHT = 1600,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("d(-_-)b")

FPS = 60

BLACK = (0,0,0)
WHITE = (255, 255,255)
YELLOW = (255,255,0)
# TARGET DEFAULT WIDTH 50, HEIGHT 50 # RESIZE method = pygame.transform.scale(image, (width, height))
TARGET_WIDTH, TARGET_HEIGHT = 50,50
TARGET = pygame.image.load(os.path.join("assets", "Target.png"))

# CHECK IF
BULLET_WIDTH, BULLET_HEIGHT = 50,50
BULLET = pygame.image.load(os.path.join("assets", "CharFaceBackward.png"))

def randomize_spawn(): # Randomize target spawn insinde display.. x == [0] y == [1]    
    x = randrange(1500)
    y = randrange(800)
    return x,y

def add_targets(targets): # Append target to list with randomized x,y vector
    spawn_point = randomize_spawn()
    target = pygame.Rect(spawn_point[0], spawn_point[1], TARGET_HEIGHT,TARGET_WIDTH)
    targets.append(target)
       
def draw_borders(): # Draw black borders, delete? 
    BORDER_RIGHT = pygame.Rect(WIDTH- 8,0,10, HEIGHT)
    BORDER_LEFT = pygame.Rect(WIDTH- 1600,0, 10, HEIGHT)
    pygame.draw.rect(WIN, BLACK, BORDER_RIGHT)
    pygame.draw.rect(WIN, BLACK, BORDER_LEFT)

def get_mouse_position(): # current mouse x,y axis
    if pygame.mouse.get_pressed:
        x,y = pygame.mouse.get_pos()
        return x,y

def click_mouse_1(event): # Check if 
    if event.type == pygame.MOUSEBUTTONDOWN: # If mouse1 (Left click) is pressed
        if event.button == 1:
            return True

def handle_hit(event,targets): #Check if mouse cursor x & y axis inside targets 50px range
    mouse_position = get_mouse_position()
    if click_mouse_1(event):
        for target in targets:
            if mouse_position[0] >= target.x and mouse_position[0] <= target.x + 50 and mouse_position[1] >= target.y and mouse_position[1] <= target.y + 50:
                    targets.remove(target)
                    return True
    
def draw_window(targets): #Draw everything
    WIN.fill(WHITE)
    for target in targets:
        WIN.blit(TARGET, (target.x, target.y))
        
    draw_borders()
    pygame.display.update()

def main():

    targets = []
    score = 0
    timer = 0

    timer_event = pygame.USEREVENT + 0
    pygame.time.set_timer(timer_event, 1000) # 1000ms
    clock = pygame.time.Clock() # Game running speed (FPS)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == timer_event:
                add_targets(targets)
                timer += 1
            if handle_hit(event, targets):
                score += 1
            
        draw_window(targets)
        
    pygame.quit()
    
if __name__ == "__main__":
    main()