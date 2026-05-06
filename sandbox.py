import pygame
import os 
import random
import cv2

pygame.init()

# automatically use the native desktop resolution
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = WIN.get_size()
pygame.display.set_caption("Conway: The 10-Cell Challenge")

CLOCK = pygame.time.Clock()

try:
    font_path = os.path.join('assets', 'fonts', 'JetBrainsMonoNerdFont-Regular.ttf')
    heavy_font_path = os.path.join('assets', 'fonts', 'JetBrainsMonoNerdFont-Bold.ttf')
    MY_FONT = pygame.font.Font(font_path, 20)
    TITLE_FONT = pygame.font.Font(heavy_font_path, 30)
    UNDER_TITLE = pygame.font.Font(font_path, 15)
    DETAIL_FONT_path = os.path.join('assets', 'fonts', 'JetBrainsMonoNerdFont-Regular.ttf') 
    DETAIL_FONT = pygame.font.Font(DETAIL_FONT_path, 12) if os.path.exists(DETAIL_FONT_path) else pygame.font.SysFont('Consolas', 12)
except FileNotFoundError:
    MY_FONT = pygame.font.SysFont('Consolas', 20)
    TITLE_FONT = pygame.font.SysFont('Consolas', 60, bold=True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
DARK_GRAY = (32, 32, 32)
LIGHT_GRAY = (180, 180, 180) 

FPS = 60
UPDATE_RATE = 50 
CELL_SIZE = 10
TARGET_SCORE = 100
MAX_CELLS = 10


SINGLE = {(0, 0)}
TOAD = {(0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1)}
METHUSELAH = {(0, -1), (1, -1), (-1, 0), (0, 0), (0, 1)}
ACORN = {(1, -1), (3, 0), (0, 1), (1, 1), (4, 1), (5, 1), (6, 1)}
GLIDER = {(0, 0), (1, 0), (2, 0), (2, -1), (1, -2)}

# add your new presets here when you code them!
PRESETS = {
    "Single Cell": SINGLE,
    "Glider": GLIDER,
    "Toad": TOAD,
    "Methuselah": METHUSELAH,
    "Acorn": ACORN
}

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
            
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_window(touched_cells, alive_cells, camera_x, camera_y, 
                fps_surface, ui_surfaces, paused, game_won, hint_level=0, hint_pattern=None):
    WIN.fill(BLACK)
    
    for (x, y) in touched_cells:
        screen_x = (x * CELL_SIZE) - camera_x + (WIDTH // 2) - (CELL_SIZE // 2)
        screen_y = (y * CELL_SIZE) - camera_y + (HEIGHT // 2) - (CELL_SIZE // 2)
        pygame.draw.rect(WIN, DARK_GRAY, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
    
    for (x, y) in alive_cells:
        screen_x = (x * CELL_SIZE) - camera_x + (WIDTH // 2) - (CELL_SIZE // 2)
        screen_y = (y * CELL_SIZE) - camera_y + (HEIGHT // 2) - (CELL_SIZE // 2) 
        color = GREEN if game_won else WHITE
        pygame.draw.rect(WIN, color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
        
    if hint_pattern and paused and not game_won:
        for i in range(hint_level):
            hx, hy = hint_pattern[i]
            if (hx, hy) not in alive_cells:
                screen_x = (hx * CELL_SIZE) - camera_x + (WIDTH // 2) - (CELL_SIZE // 2)
                screen_y = (hy * CELL_SIZE) - camera_y + (HEIGHT // 2) - (CELL_SIZE // 2)
                pygame.draw.rect(WIN, (255, 255, 0), (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 2)
    
    WIN.blit(fps_surface, (20, 20))
    for i, surface in enumerate(ui_surfaces):
        WIN.blit(surface, (20, 60 + (i * 30)))
    
    pygame.draw.circle(WIN, RED, (WIDTH // 2, HEIGHT // 2), 3)

    if game_won:
        win_surface = TITLE_FONT.render("TARGET REACHED! YOU WIN!", True, GREEN)
        WIN.blit(win_surface, (WIDTH // 2 - win_surface.get_width() // 2, 20))
        win_surface = UNDER_TITLE.render("Try different configurations to explore more solutions.", True, WHITE)
        WIN.blit(win_surface, (WIDTH // 2 - win_surface.get_width() // 2, 60))
        sub_surface = MY_FONT.render("Press 'R' to play again.", True, WHITE)
        WIN.blit(sub_surface, (WIDTH // 2 - sub_surface.get_width() // 2, 120))
    elif paused:
        pause_surface = TITLE_FONT.render("PAUSED - SYSTEM HALTED", True, RED)
        WIN.blit(pause_surface, (WIDTH // 2 - pause_surface.get_width() // 2, 20))
        
    pygame.display.update()

def main_menu():
    run = True
    clock = pygame.time.Clock()
    
    video_path = os.path.join('assets', 'menu_video.mp4')
    video = cv2.VideoCapture(video_path)
    
    button_width, button_height = 250, 50
    start_button = Button(
        WIDTH // 2 - button_width // 2, HEIGHT // 2 + 10, 
        button_width, button_height, 
        "CHALLENGE MODE", MY_FONT, 
        DARK_GRAY, GREEN, WHITE
    )
    
    sandbox_button = Button(
        WIDTH // 2 - button_width // 2, HEIGHT // 2 + 70, 
        button_width, button_height, 
        "SANDBOX MODE", MY_FONT, 
        DARK_GRAY, BLUE, WHITE
    )
    
    quit_button = Button(
        WIDTH // 2 - button_width // 2, HEIGHT // 2 + 130, 
        button_width, button_height, 
        "QUIT", MY_FONT, 
        DARK_GRAY, RED, WHITE
    )
    
    while run:
        clock.tick(FPS)
        
        success, frame = video.read()
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = video.read()

        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.transpose(1, 0, 2)
            video_surface = pygame.surfarray.make_surface(frame)
            video_surface = pygame.transform.scale(video_surface, (WIDTH, HEIGHT))
            WIN.blit(video_surface, (0, 0))


        title_label = TITLE_FONT.render("CONWAY's Set the Sail", True, WHITE)
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 80))
        
        start_button.draw(WIN)
        sandbox_button.draw(WIN)
        quit_button.draw(WIN)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
            if start_button.is_clicked(event):
                video.release()
                run = False
                challenge_mode()
                
            if sandbox_button.is_clicked(event):
                video.release()
                run = False
                sandbox_mode()
                
            if quit_button.is_clicked(event):
                video.release()
                pygame.quit()
                quit()

def process_generation(alive_cells, touched_cells):
    touched_cells.update(alive_cells)
    sparse = {}
    for (x, y) in alive_cells:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                neighbor = (x + i, y + j)
                sparse[neighbor] = sparse.get(neighbor, 0) + 1

    new_alive_cells = set()
    for (x, y), count in sparse.items():
        if count == 3 or (count == 2 and (x, y) in alive_cells):
            new_alive_cells.add((x, y))
    return new_alive_cells

def sandbox_mode():
    clock = pygame.time.Clock()
    run = True
    
    camera_x, camera_y = 0, 0
    alive_cells = set() 
    touched_cells = set()
    
    last_update_tick = pygame.time.get_ticks()
    update_rate = UPDATE_RATE
    gen = 0
    paused = True
    game_won = False # never triggered in sandbox
    
    preset_names = list(PRESETS.keys())
    preset_idx = 0
    
    while run:
        clock.tick(FPS)
        current_tick = pygame.time.get_ticks()

        score = len(alive_cells)
        fps = int(clock.get_fps())
        fps_surface = MY_FONT.render(f"FPS: {fps}", True, WHITE)
        
        ui_surfaces = [
            MY_FONT.render("MODE: SANDBOX (Infinite Setup)", True, BLUE),
            MY_FONT.render(f"Brush: {preset_names[preset_idx]} (Press Q/E to cycle)", True, GREEN),
            MY_FONT.render(f"Current Population: {score}", True, WHITE),
            MY_FONT.render(f"Generation: {gen}", True, WHITE),
            MY_FONT.render("Controls: [L-Click] Place Brush | [R-Click] Delete Cell | [Space] Play | [C] Clear | [ESC] Menu", True, LIGHT_GRAY)
        ]

        if not paused:
            if current_tick - last_update_tick >= update_rate:
                gen += 1
                last_update_tick = current_tick
                alive_cells = process_generation(alive_cells, touched_cells)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_q: # cycle brush left
                    preset_idx = (preset_idx - 1) % len(preset_names)
                if event.key == pygame.K_e: # cycle brush right
                    preset_idx = (preset_idx + 1) % len(preset_names)
                if event.key == pygame.K_c: # clear board
                    alive_cells.clear()
                    touched_cells.clear()
                    gen = 0
                if event.key == pygame.K_ESCAPE:
                    run = False
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    mx, my = pygame.mouse.get_pos()
                    grid_x = (mx + camera_x - (WIDTH // 2) + (CELL_SIZE // 2)) // CELL_SIZE
                    grid_y = (my + camera_y - (HEIGHT // 2) + (CELL_SIZE // 2)) // CELL_SIZE
                    
                    if event.button == 1: # Left click places entire pattern
                        current_pattern = PRESETS[preset_names[preset_idx]]
                        for (px, py) in current_pattern:
                            alive_cells.add((grid_x + px, grid_y + py))
                    elif event.button == 3: # Right click removes a single cell
                        cell = (grid_x, grid_y)
                        if cell in alive_cells:
                            alive_cells.remove(cell)

        draw_window(touched_cells, alive_cells, camera_x, camera_y, fps_surface, ui_surfaces, paused, game_won)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]: camera_y -= 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: camera_y += 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: camera_x += 10
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: camera_x -= 10

def challenge_mode(): 
    clock = pygame.time.Clock()
    run = True
    
    camera_x, camera_y = 0, 0
    alive_cells = set() 
    touched_cells = set()
    
    last_update_tick = pygame.time.get_ticks()
    update_rate = UPDATE_RATE
    gen = 0
    paused = True
    game_won = False
    
    hint_level = 0
    hint_pattern = [(1, -1), (3, 0), (0, 1), (1, 1), (4, 1), (5, 1), (6, 1)]
    
    while run:
        clock.tick(FPS)
        current_tick = pygame.time.get_ticks()

        score = len(alive_cells)
        fps = int(clock.get_fps())
        fps_surface = MY_FONT.render(f"FPS: {fps}", True, WHITE)
        
        cells_left = MAX_CELLS - (score if paused and gen == 0 else 0)
        
        ui_surfaces = [
            MY_FONT.render(f"Goal: Reach {TARGET_SCORE} Population", True, GREEN),
            MY_FONT.render(f"Starting Cells Left: {max(0, cells_left)}", True, RED if cells_left <= 0 else WHITE),
            MY_FONT.render(f"Current Population: {score}", True, WHITE),
            MY_FONT.render(f"Generation: {gen}", True, WHITE),
            MY_FONT.render("Controls: [Click] Place | [Space] Play | [R] Reset | [H] Hint | [ESC] Menu", True, LIGHT_GRAY)
        ]
        
        if score >= TARGET_SCORE and not game_won:
            game_won = True
            paused = True

        if not paused and not game_won:
            if current_tick - last_update_tick >= update_rate:
                gen += 1
                last_update_tick = current_tick
                alive_cells = process_generation(alive_cells, touched_cells)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_won:
                    paused = not paused
                    
                if event.key == pygame.K_h and paused and gen == 0 and not game_won:
                    if hint_level < len(hint_pattern):
                        hint_level += 1
                
                if event.key == pygame.K_ESCAPE:
                    run = False
                        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if paused and gen == 0 and not game_won:
                    mx, my = pygame.mouse.get_pos()
                    grid_x = (mx + camera_x - (WIDTH // 2) + (CELL_SIZE // 2)) // CELL_SIZE
                    grid_y = (my + camera_y - (HEIGHT // 2) + (CELL_SIZE // 2)) // CELL_SIZE
                    
                    cell = (grid_x, grid_y)
                    if cell in alive_cells:
                        alive_cells.remove(cell) 
                    elif len(alive_cells) < MAX_CELLS:
                        alive_cells.add(cell)

        draw_window(touched_cells, alive_cells, camera_x, camera_y, 
                    fps_surface, ui_surfaces, paused, game_won, hint_level, hint_pattern)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]: camera_y -= 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: camera_y += 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: camera_x += 10
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: camera_x -= 10
            
        if keys[pygame.K_r]:
            alive_cells.clear() 
            touched_cells.clear()
            gen = 0
            hint_level = 0
            camera_x, camera_y = 0, 0
            paused = True
            game_won = False

if __name__ == "__main__":
    while True:
        main_menu()