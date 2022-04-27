import pygame,  os
from random import randrange
from main import WIDTH, HEIGHT

WIDTH = WIDTH
HEIGHT = HEIGHT

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)
WHITE = (255, 255,255)

# TARGET DEFAULT WIDTH 50, HEIGHT 50 # RESIZE method = pygame.transform.scale(image, (width, height))
TARGET_WIDTH, TARGET_HEIGHT = 50,50
TARGET = pygame.image.load(os.path.join("assets", "YellowTarget.png"))

def randomize_spawn(): # Randomize target spawn   
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

def click_mouse_1(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: # If mouse1 (Left click) is pressed
            return True

def handle_hit(targets): # Check if mouse cursor x & y axis inside targets 50px range
    mouse_position = get_mouse_position()
    for target in targets:
        if mouse_position[0] >= target.x and mouse_position[0] <= target.x + 50 and mouse_position[1] >= target.y and mouse_position[1] <= target.y + 50:
                targets.remove(target)
                return True
            
def handle_text(font, score, hit_accuracy, game_over): # Handle texts
    if game_over == False:
        text_score = font.render(str(score), True, (WHITE))
        text_accuracy = font.render(str(int(hit_accuracy * 100)) + "%", True, (WHITE))  
        return text_score, text_accuracy
    else:
        text_score = font.render("Score: " + str(score), True, (WHITE))
        text_accuracy = font.render("Accuracy: " + str(int(hit_accuracy * 100)) + "%", True, (WHITE))
        text_game_over = font.render(("GAME OVER"), True, (WHITE))
        return text_score, text_accuracy, text_game_over
        
    
def draw_window(targets,text, game_over): #Draw everything
    if game_over == False:
        for target in targets:
            WIN.blit(TARGET, (target.x, target.y))
        WIN.blit(text[0], (WIDTH - 90 , 25))
        WIN.blit(text[1], (WIDTH - 110 , 70))
    else: # Game Over
        WIN.blit(text[2], (WIDTH/2 - 100 , HEIGHT/2 - 100))
        WIN.blit(text[0], (WIDTH/2 - 100 , HEIGHT/2))
        WIN.blit(text[1], (WIDTH/2 - 100 , HEIGHT/2+ 100))
     
    pygame.display.update()