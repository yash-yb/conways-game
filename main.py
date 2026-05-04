import pygame
import os 
import random

pygame.init()
WIDTH , HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway Set the Sail(DEV)")


CLOCK = pygame.time.Clock()

font_path = os.path.join('assets', 'fonts', 'JetBrainsMonoNerdFont-Regular.ttf')
MY_FONT = pygame.font.Font(font_path, 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORIGIN_DOT = (0, 0)
FOREST_GREEN= (34,139,34)
DARK_SEA_GREEN = (143,188,143)
DARK_GRAY = (32, 32, 32)

# presets for playing around

TOAD = {(0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1)}
METHUSELAH = {(0, -1), (1, -1), (-1, 0), (0, 0), (0, 1)} #favourite
ACORN = {(1, -1), (3, 0), (0, 1), (1, 1), (4, 1), (5, 1), (6, 1)}


FPS = 60
UPDATE_RATE = 50 #1000 ticks = 1 sec ig

def draw_window(touched_cells, 
                alive_cells, 
                camera_x, camera_y, cell_size, 
                fps_surface, gen_surface, coordinates_surface, score_surface, simulation_surface,
                paused):
    
    WIN.fill(BLACK)
    
    #copied from below for touched_effect
    for (x , y) in touched_cells:
        screen_x = (x * cell_size) + camera_x - (cell_size // 2)
        screen_y = (y * cell_size) + camera_y - (cell_size // 2)
        
        pygame.draw.rect(WIN, DARK_GRAY, (screen_x, screen_y, cell_size, cell_size))
    
    
    #for defining the co-ordinates wrt to camera
    for (x , y) in alive_cells:
        screen_x = (x * cell_size) + camera_x - (cell_size // 2)
        screen_y = (y * cell_size) + camera_y - (cell_size // 2) 
        #the substraction of half of cell size is to center the box on the exact coordinates of camera
        
        #drawing the alive cells
        pygame.draw.rect(WIN, WHITE, (screen_x, screen_y, cell_size, cell_size))
    
    WIN.blit(fps_surface, (20, 20))
    WIN.blit(gen_surface, (20, 50))
    WIN.blit(coordinates_surface, (20, 80))
    WIN.blit(score_surface, (20,110))
    WIN.blit(simulation_surface, (20,140))
    
    #center crosshair
    pygame.draw.circle(WIN, RED, (WIDTH//2, HEIGHT//2), 3)
    
    #PAUSED indicator
    if paused:
        pause_surface = MY_FONT.render("PAUSED", True, RED)
        WIN.blit(pause_surface, (WIDTH // 2 - pause_surface.get_width() // 2, 20))
    
    # test crosshair
    # pygame.draw.rect(WIN, RED, (camera_x, camera_y, 1, 100))
    # pygame.draw.rect(WIN, RED, (camera_x, camera_y, 100, 1))
    
    pygame.display.update()
    
def main(): 

    clock = pygame.time.Clock()
    run = True
    
    # initial data for the cells 
    preset = ACORN
    cell_size = 5
    camera_x = WIDTH // 2
    camera_y = HEIGHT // 2
    alive_cells = preset

    last_update_tick = pygame.time.get_ticks()

    update_rate = UPDATE_RATE
    
    gen = 0
    
    paused = False
    
    co_x = 0
    co_y = 0
    
    score = 0
    
    #initialising touched region
    touched_cells = set()
    
    while run:
        clock.tick(FPS)
        
        #fps stat
        fps = int(clock.get_fps())
        fps_surface = MY_FONT.render(f"FPS: {fps}", True, WHITE)
        #gen stat
        gen_surface = MY_FONT.render(f"Generation: {gen} th gen", True, WHITE)
        current_tick = pygame.time.get_ticks()
        #coordinates
        coordinates_surface = MY_FONT.render(f"X: {co_x}, Y: {co_y}", True, WHITE) 
        #score 
        score = len(alive_cells)
        score_surface = MY_FONT.render(f"Score: {score}", True, FOREST_GREEN)
        #simulation speed
        simulation_speed = UPDATE_RATE//update_rate
        simulation_surface = MY_FONT.render(f"Simulation Speed: {simulation_speed}x", True, WHITE)
        
        
        if not paused:
            if current_tick - last_update_tick >= update_rate:
            
                gen += 1
                last_update_tick = current_tick

                #logic for touched_region
                new_alive_cells = set()
            
                touched_cells.update(alive_cells)
    
                # this is for random fun :)
                # for (x , y) in alive_cells:
                #     new_alive_cells.add((x+random.randint(-10, 10), y+random.randint(-10, 10))) 
                # alive_cells = new_alive_cells
                # print(sec, 'has passed')
                
                # analysing the space
                sparse = {}
                for (x, y) in alive_cells:
                    for i in range(-1, 2):
                            for j in range(-1, 2):
                                if i == 0 and j == 0:
                                    continue
                                if (i + x, j + y) in sparse:
                                    sparse[(i+x, j+y)] += 1
                                else:
                                    sparse[(i+x, j+y)] = 1

                # making a state for alive_cells
                for (x, y) in sparse:
                    if (x, y) in alive_cells:
                        if sparse[(x, y)] == 2 or sparse[(x, y)] == 3:
                            new_alive_cells.add((x, y))
                    elif sparse[(x, y)] == 3: #or sparse[(x, y)] == 2:
                        new_alive_cells.add((x, y))

                alive_cells = new_alive_cells
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                
        draw_window(touched_cells, alive_cells, 
                    camera_x, camera_y, 
                    cell_size, 
                    fps_surface, gen_surface, coordinates_surface, score_surface, simulation_surface,
                    paused)
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y -= 5
            co_y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera_y += 5
            co_y += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_x += 5
            co_x += 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x -= 5
            co_x -= 5
        if keys[pygame.K_r]:
            alive_cells = preset #to reset the pattern if lags or something :)
            touched_cells = set()
            gen = 0
            camera_x = WIDTH // 2
            camera_y = HEIGHT // 2
            co_x = 0
            co_y = 0
            update_rate = UPDATE_RATE
        if keys[pygame.K_1]:
            update_rate = UPDATE_RATE
        if keys[pygame.K_2]:
            update_rate = UPDATE_RATE//2
        if keys[pygame.K_3]:
            update_rate = UPDATE_RATE//3

    pygame.quit()
    
if __name__ == "__main__":
    main()