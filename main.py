

import pygame, sys;
from pygame import *
from TargetPractice import *
from datetime import date
from handleDb import *

clock = pygame.time.Clock()
pygame.init()

today = date.today()
FPS = 60 # ENOUGH FPS TO HANDLE MOUSE INPUT
WIDTH, HEIGHT = 1600, 900
MAX_TARGETS = 20 # MAX TARGETS ON SCREEN
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# BUTTON IMAGES
OPTIONS_IMAGE = pygame.image.load(os.path.join("assets", "Options.png"))
PLAY_IMAGE = pygame.image.load(os.path.join("assets", "Play.png"))
MUTE = pygame.image.load(os.path.join("assets", "Mute.png"))
UNMUTE = pygame.image.load(os.path.join("assets", "Unmute.png"))

# GAME COLORS
WHITE = (255, 255,255)
BLACK = (0,0,0)

# FONTS FOR DRAW_TEXT FUNCTION
normal_font = pygame.font.SysFont(None, 20)
big_font = pygame.font.SysFont(None, 40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def draw_high_scores(scores): # TOP SCORES
    draw_text("TOP 5", big_font, WHITE, WIN, WIDTH/2 +400, HEIGHT/2-100)
    draw_text("Score", big_font, WHITE, WIN, WIDTH/2 +300, HEIGHT/2-50)
    draw_text("Accuracy", big_font, WHITE, WIN, WIDTH/2 + 500, HEIGHT/2-50)
    HS_X = WIDTH/2 + 325
    HS_Y = HEIGHT/2 
    
    # Print top scores 
    length = len(scores)
    if length > 5:
        length = 5
    else:
        length = length
        
    for i in range(length):
        draw_text(str(scores[i]["score"]), big_font, WHITE, WIN, HS_X, HS_Y)
        draw_text(str(int(scores[i]["accuracy"])) + "%", big_font, WHITE, WIN, HS_X + 200, HS_Y)
        HS_Y += 50 # Change y axis for each

click = False
def main_menu(): # LAUNCHES ON STARTUP
    mixer.music.load(os.path.join("assets", "hayden-folker-cast-aside.wav"))
    mixer.music.play(-1) # LOOP
    
    pygame.display.set_caption('MENU')
    
    scores = search_all() # SORT BY SCORE
    for i in range(len(scores)):
        key = scores[i]
        j = i-1
        while j >= 0 and key["score"] > scores[j]["score"] :
            scores[j+1] = scores[j]
            j -= 1
        scores[j+1] = key
        
    while True:
        WIN.fill((BLACK))
        
        draw_high_scores(scores)        
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_1 = pygame.Rect(WIDTH/2-100, HEIGHT/2 -100, 200, 50)
        button_2 = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 50)
        if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                play()
        if button_2.collidepoint((mouse_x, mouse_y)):
            if click:
                options()
         
        WIN.blit(PLAY_IMAGE, (button_1.x, button_1.y))
        WIN.blit(OPTIONS_IMAGE, (button_2.x, button_2.y))
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(FPS)
  
def options(): # Options for music
    options_click = False
    pygame.display.set_caption('OPTIONS')
    running = True
    while running:
        WIN.fill((0,0,0))
        draw_text('Options', big_font, (255, 255, 255), WIN, 20, 20)
        draw_text('Music', big_font, (255, 255, 255), WIN, WIDTH-1400, HEIGHT-600)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_1 = pygame.Rect(WIDTH-1450, HEIGHT/2-100, 200, 50)
        button_2 = pygame.Rect(WIDTH-1450, HEIGHT/2, 200, 50)
        
        if button_1.collidepoint((mouse_x, mouse_y)): # STOP MUSIC
            if options_click:
                pygame.mixer.music.stop()
        if button_2.collidepoint((mouse_x, mouse_y)): # PLAY MUSIC
            if options_click:
                pygame.mixer.music.play()
                
        options_click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    options_click = True
        WIN.blit(MUTE, (button_1.x, button_1.y))
        WIN.blit(UNMUTE, (button_2.x, button_2.y))
        pygame.display.update()
        clock.tick(FPS)
        
def play(): # Game
    pygame.display.set_caption('Target Practice')
    click_amount = 0
    targets = []
    target_amount = 1
    score = 0
    timer = 1
    hit_accuracy = 0
    font = pygame.font.SysFont(None, 50)
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000) # 1000ms
    game_over = False
    running = True
    while running:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key != 1: # other then mouse input will return to menu
                    running = False
                if event.key != 1 and game_over: # game over, save score
                    save_score(score,hit_accuracy,today)
                    running = False
            elif event.type == timer_event: # every second add new target
                add_targets(targets, target_amount)
                timer += 1
                if timer % 25 == 0: # every 25th second increase targets created by one
                    target_amount += 1
            if click_mouse_1(event): # keep store of clicks
                click_amount += 1
                hit_accuracy = score / click_amount
                if handle_hit(targets): # keep store of score
                    score += 1
                    hit_accuracy = score / click_amount
                    
            if len(targets) > MAX_TARGETS: # If targets > x in screen, game over
                game_over = True
      
        text = handle_text(font,score,hit_accuracy, game_over) # accuracy and score during game and game over
        
        draw_window(targets,text, game_over) # Render targets and texts
        clock.tick(FPS)  
 
if __name__ == "__main__":
    main_menu()
    


