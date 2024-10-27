import pygame
import os

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1122, 727
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
TILE_SIZE = 60
tile_images = {}


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class SokobanGame:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sokoban Game")
        self.algoType = None
        self.state = "welcome"
        self.level = None
        self.title = pygame.image.load('asset/Aries.png')
        self.background = pygame.image.load('asset/background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.button_start = pygame.image.load('asset/start_btn.png')
        self.table = pygame.image.load('asset/table.png')
        self.titleTableAlgo = pygame.image.load('asset/title_table_algo.png')
        self.titleTableLevel = pygame.image.load('asset/level_title.png')
        self.button_start_rect = self.button_start.get_rect()
        self.button_start_rect.topleft = (458, 461)
        self.algoBtn = []
        self.algoBtnRects = []
        for i in range(1, 5):
            button_image = pygame.image.load(f'asset/algo{i}.png')
            self.algoBtn.append(button_image)
            self.algoBtnRects.append(button_image.get_rect())

        # Set positions for algorithm buttons
        self.algoBtnRects[0].topleft = (281, 268)
        self.algoBtnRects[1].topleft = (281, 481)
        self.algoBtnRects[2].topleft = (612, 274)
        self.algoBtnRects[3].topleft = (612, 479)
        self.levelBtn = []
        self.levelBtnRects = []
        for i in range(1, 13):
            button_image = pygame.image.load(f'asset/{i}.png')
            self.levelBtn.append(button_image)
            self.levelBtnRects.append(button_image.get_rect())
        self.levelBtnRects[0].topleft = (282.78, 236.48)
        self.levelBtnRects[1].topleft = (435.82, 236.48)
        self.levelBtnRects[2].topleft = (599.59, 236.48)
        self.levelBtnRects[3].topleft = (764.79, 236.48)
        self.levelBtnRects[4].topleft = (282.78, 383.8)
        self.levelBtnRects[5].topleft = (435.82, 383.8)
        self.levelBtnRects[6].topleft = (599.59, 383.8)
        self.levelBtnRects[7].topleft = (764.79, 383.8)
        self.levelBtnRects[8].topleft = (282.78, 531.12)
        self.levelBtnRects[9].topleft = (435.82, 531.12)
        self.levelBtnRects[10].topleft = (599.59, 531.12)
        self.levelBtnRects[11].topleft = (764.79, 531.12)
        self.map_processing()
        
    def welcome_screen(self):
        self.screen.blit(self.background, (0, 0))  # Draw background first
        self.screen.blit(self.title, (187, -50))
        self.screen.blit(self.button_start, self.button_start_rect.topleft)

    def level_selection_screen(self):
        self.screen.blit(self.background, (0, 0))  
        self.screen.blit(self.table, (227, 200))
        self.screen.blit(self.titleTableLevel, (229, 57))
        for i, button in enumerate(self.levelBtn):
            self.screen.blit(button, self.levelBtnRects[i].topleft)
    def algo_selection_screen(self):
        self.screen.blit(self.background, (0, 0))  
        self.screen.blit(self.titleTableAlgo, (229, 57))  
        self.screen.blit(self.table, (227, 200))  
        for i, button in enumerate(self.algoBtn):
            self.screen.blit(button, self.algoBtnRects[i].topleft)

    def load_level(self, level_file):
        with open(level_file, 'r') as f:
            self.level = f.readlines()  # Load map into a list of strings

    def map_processing(self):
        ASSET_PATH = 'asset/' 
        global tile_images
        tile_images = {
            "#": pygame.image.load(os.path.join(ASSET_PATH, "wall.png")),
            " ": pygame.image.load(os.path.join(ASSET_PATH, "ground.png")),
            "$": pygame.image.load(os.path.join(ASSET_PATH, "stone.png")),
            #"@": pygame.image.load(os.path.join(ASSET_PATH, "ares.png")),
            ".": pygame.image.load(os.path.join(ASSET_PATH, "switch_place.png")),
            "*": pygame.image.load(os.path.join(ASSET_PATH, "stone_switch_place.png")),
            #"+": pygame.image.load(os.path.join(ASSET_PATH, "ares_on_switch.png")),
        }

        for key, image in tile_images.items():
            tile_images[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def draw_map(self):
        if self.level:
            max_width = max(len(row) for row in self.level[1:])  # Get the length of the longest row
            map_width = max_width * TILE_SIZE 
            map_height = (len(self.level) - 1) * TILE_SIZE  # Height in pixels

            # Calculate offsets to center the map
            offset_x = (SCREEN_WIDTH - map_width) // 2 
            offset_y = (SCREEN_HEIGHT - map_height) // 2

            for y in range(1, len(self.level)):  # Start from the second line
                row = self.level[y]  # Use the original row string
                inside_walls = False  # Reset the flag for each new row
                for x in range(len(row)):
                    char = row[x]
                    if char == "#":
                        inside_walls = True  

                    if inside_walls:
                        if char not in ("#", " ") and x < len(row)-1:  # If it's not a wall or empty space
                            self.screen.blit(tile_images[" "], (offset_x + (x * TILE_SIZE), offset_y + (y * TILE_SIZE)))
                        if char in tile_images:
                            self.screen.blit(tile_images[char], (offset_x + (x * TILE_SIZE), offset_y + (y * TILE_SIZE)))

            


    def play_game(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_map()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                 # Check for mouse button events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "welcome":
                        if self.button_start_rect.collidepoint(event.pos):
                            self.state = "algo_selection"
                    elif self.state == "algo_selection":
                        for i, rect in enumerate(self.algoBtnRects):
                            if rect.collidepoint(event.pos):
                                self.algoType = i
                                self.state = "level_selection"
                                break
                    elif self.state == "level_selection":
                        for i, rect in enumerate(self.levelBtnRects):
                            if rect.collidepoint(event.pos):
                                self.load_level(f'levels/level{i + 1}.txt')
                                self.state = "play_game"
                                break
                                           
        
            if self.state == "welcome":
                self.welcome_screen()
            elif self.state == "algo_selection":
                self.algo_selection_screen()
            elif self.state == "level_selection":
                self.level_selection_screen()
            elif self.state == "play_game":
                self.play_game()

            pygame.display.update()

def main():
    # Game instance
    game = SokobanGame()
    game.run()


if __name__ == "__main__":
    main()
