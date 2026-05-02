import pygame
import os 
import random

WIDTH , HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway Set the Sail(DEV)")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORIGIN_DOT = (0, 0)

# presets for playing around

TOAD = {(0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1)}
METHUSELAH = {(0, -1), (1, -1), (-1, 0), (0, 0), (0, 1)} #favourite
ACORN = {(1, -1), (3, 0), (0, 1), (1, 1), (4, 1), (5, 1), (6, 1)}


FPS = 60

def draw_window(alive_cells, camera_x, camera_y, cell_size):
    WIN.fill(BLACK)
    
    
    #for defining the co-ordinates wrt to camera
    for (x , y) in alive_cells:
        screen_x = (x * cell_size) + camera_x - (cell_size // 2)
        screen_y = (y * cell_size) + camera_y - (cell_size // 2) 
        #the substraction of half of cell size is to center the box on the exact coordinates of camera
        
        #drawing the alive cells
        pygame.draw.rect(WIN, WHITE, (screen_x, screen_y, cell_size, cell_size))
    
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

    update_rate = 50 #1000 ticks = 1 sec ig
    
    sec = 0
    
    while run:
        clock.tick(FPS)
        
        current_tick = pygame.time.get_ticks()
        
        if current_tick - last_update_tick >= update_rate:
            
            sec += 1
            last_update_tick = current_tick

            new_alive_cells = set()
    
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
                elif sparse[(x, y)] == 3:
                    new_alive_cells.add((x, y))

            alive_cells = new_alive_cells
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        draw_window(alive_cells, camera_x, camera_y, cell_size)
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera_y += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_x += 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x -= 5
        if keys[pygame.K_r]:
            alive_cells = preset #to reset the pattern if lags or something :)

    pygame.quit()
    
if __name__ == "__main__":
    main()