import pygame
import time
import random

pygame.init()
beige = (248, 250, 229)
dark_brown = (118, 69, 59)
light_brown = (177, 148, 112)
blue = (50, 153, 213)
forest_green = (67, 118, 108)

dis_width = 800
dis_height  = 600
dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption('Snake game by Dana')

clock = pygame.time.Clock()

snake_block=10
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
highest_score_font = pygame.font.SysFont("comicsansms", 20)

def save_high_score(name, score):
    high_scores = load_high_scores()
    high_scores.append((name, score))
    high_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)[:5]  # Keep top 5 scores

    with open("high_scores.txt", "w") as file:
        for entry in high_scores:
            file.write(f"{entry[0]},{entry[1]}\n")

def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
        high_scores = [tuple(line.strip().split(",")) for line in lines]
        high_scores = [(entry[0], int(entry[1])) for entry in high_scores]  # Convert score to int
    except FileNotFoundError:
        high_scores = []
    return high_scores

def display_high_scores(high_scores):
    start_y = dis_height - 200  # Starting y position to display scores
    # title
    score_title_surf = highest_score_font.render("Highest scores", True, dark_brown)
    dis.blit(score_title_surf, [dis_width - 150, start_y])
    start_y += 30
    for index, (name, score) in enumerate(high_scores, start=1):
        score_text = f"{index}. {name} - {score}"
        score_surf = highest_score_font.render(score_text, True, dark_brown)
        dis.blit(score_surf, [dis_width - 150, start_y])
        start_y += 30  # Move down for the next score

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, dark_brown)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, light_brown, [x[0], x[1], snake_block, snake_block])
        
# show the info on the screen
def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/6, dis_height/3])
    
def prompt_for_name():
    input_active = True
    input_text = ''
    input_box = pygame.Rect(dis_width / 2 - 100, dis_height / 2 - 25, 200, 50)
    prompt_text = "Enter Your Name:"
    prompt_surf = font_style.render(prompt_text, True, pygame.Color('white'))

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Clear screen
        dis.fill((30, 30, 30))
        
        # Render prompt and input box
        dis.blit(prompt_surf, (dis_width / 2 - prompt_surf.get_width() / 2, dis_height / 2 - 50))
        pygame.draw.rect(dis, pygame.Color('white'), input_box, 2)
        
        # Render entered text
        text_surf = font_style.render(input_text, True, pygame.Color('white'))
        dis.blit(text_surf, (input_box.x + 5, input_box.y + 5))
        
        pygame.display.flip()
        clock.tick(30)

    return input_text



def gameLoop():
    high_scores = load_high_scores()
    game_over = False
    game_close = False
    game_save = False
    # up: 0, down:1, left:2, right:3
    dir = -1
    x1 = dis_width/2
    y1 = dis_height/2
    # hold the updating values of the x and y coordinates.
    x1_change = 0
    y1_change = 0
    
    snake_List = []
    Length_of_snake = 1
    snake_speed=15
    
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                    
    while not game_over:
        while game_close == True:
            if game_save == False:
                player_name = prompt_for_name()
                save_high_score(player_name, Length_of_snake - 1)
                game_save = True
            dis.fill(beige)
            message("You Lost! Press Q-Quit or C-Play Again", blue)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # up: 0, down:1, left:2, right:3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dir != 3:
                    x1_change = -snake_block
                    y1_change = 0
                    dir = 2
                elif event.key == pygame.K_RIGHT and dir != 2:
                    x1_change = snake_block
                    y1_change = 0
                    dir = 3
                elif event.key == pygame.K_UP and dir != 1:
                    y1_change = -snake_block
                    x1_change = 0
                    dir = 0
                elif event.key == pygame.K_DOWN and dir != 0:
                    y1_change = snake_block
                    x1_change = 0
                    dir = 1
        # hits the boundaries of the screen, then he loses 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
    
        x1 += x1_change
        y1 += y1_change
        dis.fill(beige)
        pygame.draw.rect(dis, forest_green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        # the snake collides with his own body, the game is over 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        display_high_scores(high_scores)
        pygame.display.update()
        
        # when the snake crosses over that food, creat a new fruit
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            snake_speed += 2
            
        # control how fast the game loop runs, effectively controlling the game's frame rate
        clock.tick(snake_speed)

    pygame.quit()
    quit()
    
gameLoop()