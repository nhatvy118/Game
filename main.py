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

class Stone:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.image = pygame.image.load('asset/stone.png')
        self.image = pygame.image.load('asset/stone.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)) 
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('asset/player.png') 
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # Scale to TILE_SIZE
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, dx, dy, stones):
        print('move')
        # Calculate potential new position
        new_x = self.x + dx
        new_y = self.y + dy
        collided_with_stone = False

        # Check collision with stone
        for stone in stones:
            if self.rect.move(dx, dy).colliderect(stone.rect):  # Predict rect position
                stone.move(dx, dy)
                collided_with_stone = True
                break

        # Update player position
        if not collided_with_stone:
            self.x, self.y = new_x, new_y  # Update coordinates only if no collision
        self.rect.topleft = (self.x, self.y)  # Update rect position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SokobanGame:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sokoban Game")
        self.algoType = None
        self.state = "welcome"
        self.level = None
        self.player = None  # Placeholder for Player
        self.stones = []  # Placeholder for Stone
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
        self.current_score = pygame.image.load('asset/Score.png')
        self.current_level = pygame.image.load('asset/Level.png')
        self.current_algo = pygame.image.load('asset/Algo.png')
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
            self.level = f.readlines()  
        self.render_map()

    def map_processing(self):
        ASSET_PATH = 'asset/' 
        global tile_images
        tile_images = {
            "#": pygame.image.load(os.path.join(ASSET_PATH, "wall.png")),
            " ": pygame.image.load(os.path.join(ASSET_PATH, "ground.png")),
            # "$": pygame.image.load(os.path.join(ASSET_PATH, "stone.png")),
            #"@": pygame.image.load(os.path.join(ASSET_PATH, "ares.png")),
            ".": pygame.image.load(os.path.join(ASSET_PATH, "switch_place.png")),
            "*": pygame.image.load(os.path.join(ASSET_PATH, "stone_switch_place.png")),
            #"+": pygame.image.load(os.path.join(ASSET_PATH, "ares_on_switch.png")),
        }

        for key, image in tile_images.items():
            tile_images[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def render_map(self):
        self.screen.blit(self.background, (0, 0))
        if self.level:
            max_width = max(len(row) for row in self.level[1:]) - 1  # Ignore \n
            map_width = max_width * TILE_SIZE 
            map_height = (len(self.level) - 1) * TILE_SIZE  
            offset_x = (SCREEN_WIDTH - map_width) // 2 
            offset_y = (SCREEN_HEIGHT - map_height) // 2
            self.player = None
            self.stones = []

            for y in range(1, len(self.level)):  # Start from the second line
                row = self.level[y] 
                for x in range(len(row)):
                    char = row[x]
                    inside_walls = False  
                    if char == "#":
                        inside_walls = True  

                    if inside_walls:
                        if char not in ("#") and x < len(row)-1:
                            self.screen.blit(tile_images[" "], (offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE)))
                        if char in tile_images and char not in ['@', '$']:
                            self.screen.blit(tile_images[char], (offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE)))
                        elif char == "@":  # Player
                            self.player = Player(offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE))  # Create the player instance
                            self.player.rect.topleft = (offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE))  # Update rect position
                            self.player.draw(self.screen)  # Draw the player immediately
                        elif char == "$":  # Stone
                            stone = Stone(offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE))  # Create a stone instance
                            self.stones.append(stone)  # Add stone to the list
                            stone.draw(self.screen)  # Draw the stone immediately

    def play_game(self):
        custom_font = pygame.font.Font("font/IrishGrover-Regular.ttf", 36)  # Replace with the actual path and desired size

        # Render text for labels
        score_text = custom_font.render("100", True, (255, 255, 255)) 
        level_text = custom_font.render("200", True, (255, 255, 255))
        algo_text = custom_font.render("BFS", True, (255, 255, 255))
        score_x = 17 + (self.current_score.get_width() - score_text.get_width()) // 2
        score_y = 19 + (self.current_score.get_height() - score_text.get_height()) // 2

        level_x = 222 + (self.current_level.get_width() - level_text.get_width()) // 2
        level_y = 19 + (self.current_level.get_height() - level_text.get_height()) // 2

        algo_x = 372 + (self.current_algo.get_width() - algo_text.get_width()) // 2
        algo_y = 19 + (self.current_algo.get_height() - algo_text.get_height()) // 2


        self.screen.blit(self.current_score, (17, 19))
        self.screen.blit(self.current_level, (222, 19))
        self.screen.blit(self.current_algo, (372, 19))
        self.screen.blit(score_text, (score_x, score_y))
        self.screen.blit(level_text, (level_x, level_y))
        self.screen.blit(algo_text, (algo_x, algo_y))
        pygame.display.update()


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

            # Player movement with arrow keys (only in "play_game" state)
            if self.state == "play_game":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.move(-TILE_SIZE, 0, self.stones)
                elif keys[pygame.K_RIGHT]:
                    self.player.move(TILE_SIZE, 0, self.stones)
                elif keys[pygame.K_UP]:
                    self.player.move(0, -TILE_SIZE, self.stones)
                elif keys[pygame.K_DOWN]:
                    self.player.move(0, TILE_SIZE, self.stones)

            pygame.display.update()

    

def main():
    # Game instance
    game = SokobanGame()
    game.run()


if __name__ == "__main__":
    main()
