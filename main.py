import pygame
import os 

WIDTH , HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway Set the Sail(DEV)")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORIGIN_DOT = (0, 0)


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
    pygame.draw.rect(WIN, RED, (camera_x, camera_y, 1, 100))
    pygame.draw.rect(WIN, RED, (camera_x, camera_y, 100, 1))
    
    
    pygame.display.update()
    
def main(): 

    clock = pygame.time.Clock()
    run = True
    
    # initial data for the cells    
    cell_size = 20
    camera_x = WIDTH // 2
    camera_y = HEIGHT // 2
    alive_cells = {(0, 0), (1, 1), (10, 2)}

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        draw_window(alive_cells, camera_x, camera_y, cell_size)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()