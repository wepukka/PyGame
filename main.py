import pygame, os
from random import randrange

pygame.init()

WIDTH,HEIGHT = 1280,720
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
    x = randrange(WIDTH - 100)
    y = randrange(HEIGHT - 100)
    return x,y

def add_targets(targets,target_amount): # Append target to list with randomized x,y vector
    for i in range(target_amount):
        spawn_point = randomize_spawn()
        target = pygame.Rect(spawn_point[0], spawn_point[1], TARGET_HEIGHT,TARGET_WIDTH)
        targets.append(target)

def get_mouse_position(): # current mouse x,y axis
    if pygame.mouse.get_pressed:
        x,y = pygame.mouse.get_pos()
        return x,y

def click_mouse_1(event): # Check if 
    if event.type == pygame.MOUSEBUTTONDOWN: # If mouse1 (Left click) is pressed
        if event.button == 1:
            return True

def handle_hit(targets): #Check if mouse cursor x & y axis inside targets 50px range
    mouse_position = get_mouse_position()
    for target in targets:
        if mouse_position[0] >= target.x and mouse_position[0] <= target.x + 50 and mouse_position[1] >= target.y and mouse_position[1] <= target.y + 50:
                targets.remove(target)
                return True

def draw_window(targets,text_score, text_accuracy, game_over): #Draw everything
    WIN.fill(WHITE)
    if game_over == False:
        for target in targets:
            WIN.blit(TARGET, (target.x, target.y))
            
        WIN.blit(text_score, (WIDTH - 90 , 25))
        WIN.blit(text_accuracy, (WIDTH - 110 , 70))
    else:
        WIN.blit(text_score, (WIDTH - 90 , 25))

    pygame.display.update()

def main():
    click_amount = 0
    game_over = False
    targets = []
    target_amount = 1
    score = 0
    timer = 1
    hit_accuracy = 0
    font = pygame.font.SysFont(None, 50)
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000) # 1000ms
    
    clock = pygame.time.Clock() # Game running speed (FPS)
    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == timer_event:
                add_targets(targets, target_amount)
                timer += 1
                if timer % 25 == 0:
                    target_amount += 1
            if click_mouse_1(event):
                click_amount += 1
                hit_accuracy = score / click_amount
                if handle_hit(targets):
                    score += 1
                    hit_accuracy = score / click_amount
                    
            if len(targets) > 25:
                game_over = True
      
        text_accuracy = font.render(str(int(hit_accuracy * 100)) + "%", True, (BLACK))  
        text_score = font.render(str(score), True, (BLACK))
        
        draw_window(targets,text_score, text_accuracy, game_over)

    pygame.quit()
    
if __name__ == "__main__":
    main()