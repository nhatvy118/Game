import pygame
import os

import algorithmSimulate
from algorithmSimulate import getKey
import time

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1122, 727
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE = 32
INTERACTION_TIME = 0.1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
TILE_SIZE = 60
tile_images = {}

import pygame

class Stone:
    def __init__(self, x, y, value, on_switch):
        self.x = x
        self.y = y
        self.value = value
        self.original_image = pygame.image.load('asset/stone.png')
        self.image_on_switch = pygame.image.load('asset/stone_on_switch.png')
        self.on_switch = on_switch

        # Choose the appropriate image based on whether it's on a switch
        self.image = self.image_on_switch if self.on_switch else self.original_image
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Initialize font for displaying the value
        self.font = pygame.font.Font(None, 30)

    def move(self, dx, dy, walls, stones, switches):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collisions with walls
        if (new_x, new_y) in walls:
            return  # Prevent movement if colliding with a wall

        # Check for collisions with other stones
        for stone in stones:
            if stone != self and stone.rect.topleft == (new_x, new_y):
                return  
            
        # Update position if no collision
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (self.x, self.y)

        # Check if stone is on a switch
        if (self.x, self.y) in switches:
            if not self.on_switch:  # Resize only once when first moving onto the switch
                self.image = self.image_on_switch  # Change to alternate image
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                self.on_switch = True
        else:
            if self.on_switch:
                self.image = self.original_image  # Revert to normal image
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                self.on_switch = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        value_text = self.font.render(str(self.value), True, (255, 255, 255))
        if self.on_switch:
            text_rect = value_text.get_rect(center=(self.rect.centerx, self.rect.centery + 10))  # Center the text on the stone
        else:
            text_rect = value_text.get_rect(center=(self.rect.centerx - 5, self.rect.centery + 10))

        screen.blit(value_text, text_rect)
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "right"
        self.on_switch = False  # Track if player is on a switch
        self.frame_index = 0

        # Load sprites
        self.image_normal = pygame.image.load('asset/player_standing.png')  # Standing image

        # Load movement sprites (2 frames for right, flip for left)
        self.right_move_frames = [
            pygame.image.load('asset/player_move_right_1.png'),
            pygame.image.load('asset/player_move_right_2.png')
        ]
        self.left_move_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_move_frames]

        self.up_move_frames = [
            pygame.image.load('asset/player_up_1.png'),
            pygame.image.load('asset/player_up_2.png')
        ]
        self.down_move_frames = [
            pygame.image.load('asset/player_down_1.png'),
            pygame.image.load('asset/player_down_2.png')
        ]

        # Initial settings
        self.image = self.image_normal
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, dx, dy, stones, walls, switches):
        current_stone = 0
        # Calculate potential new position for the player
        new_x = self.x + dx
        new_y = self.y + dy
        new_position = (new_x, new_y)

        # Check if the player is trying to move into a wall
        if new_position in walls:
            return current_stone # Stop movement if blocked by a wall

        collided_with_stone = False

        # Check if the player is colliding with any stone
        for stone in stones:
            if self.rect.move(dx, dy).colliderect(stone.rect):
                # Calculate potential new position for the stone
                stone_new_x = stone.x + dx
                stone_new_y = stone.y + dy
                stone_new_position = (stone_new_x, stone_new_y)

                # Check if the stone's new position is blocked by a wall or another stone
                if stone_new_position in walls or any(s.rect.topleft == stone_new_position for s in stones if s != stone):
                    return current_stone  # Stop movement if stone is blocked

                # Move the stone if not blocked
                stone.move(dx, dy, walls, stones, switches)
                collided_with_stone = True
                current_stone = int(stone.value)
                break

        # Update player position if not blocked by a wall or a non-movable stone
        if not collided_with_stone or (collided_with_stone and new_position not in walls):
            self.x, self.y = new_x, new_y
            self.rect.topleft = (self.x, self.y)

            # Determine direction and update frames for animation
            if dx > 0:  # Moving right
                self.direction = "right"
                self.update_animation(self.right_move_frames)
            elif dx < 0:  # Moving left
                self.direction = "left"
                self.update_animation(self.left_move_frames)
            elif dy > 0:  # Moving down
                self.direction = "down"
                self.update_animation(self.down_move_frames)
            elif dy < 0:  # Moving up
                self.direction = "up"
                self.update_animation(self.up_move_frames)
            else:  
                self.image = self.image_normal

        return current_stone


    def update_animation(self, frames):
        """Cycle through the frames for movement animation."""
        self.frame_index = (self.frame_index + 1) % len(frames)
        self.image = frames[self.frame_index]
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # Scale to tile size

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SokobanGame:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sokoban Game")
        
        self.lastInteractionTime = time.time()
        self.isAlgoSimulated = False
        self.solution = ""
        self.solutionIndex = 0
        
        self.algoType = None
        self.state = "welcome"
        self.level_file = None
        self.level = 1
        self.score = 0
        self.step = 0
        self.player = None  
        self.stones = [] 
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
        self.win = False
        self.current_score = pygame.image.load('asset/Score.png')
        self.current_level = pygame.image.load('asset/Level.png')
        self.current_algo = pygame.image.load('asset/Level.png')
        self.back_button = pygame.image.load('asset/back.png')
        self.home_button = pygame.image.load('asset/home.png')
        self.home_button_rect = self.home_button.get_rect(topleft=(1000, 25))
        self.back_button_rect = self.back_button.get_rect(topleft=(24, 25))
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
        self.walls = []
        self.switches = []
        
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
        self.screen.blit(self.back_button, (24, 25))
        self.screen.blit(self.home_button, (1000, 25))

    def algo_selection_screen(self):
        self.screen.blit(self.background, (0, 0))  
        self.screen.blit(self.titleTableAlgo, (229, 57))  
        self.screen.blit(self.table, (227, 200))  
        for i, button in enumerate(self.algoBtn):
            self.screen.blit(button, self.algoBtnRects[i].topleft)
        self.screen.blit(self.home_button, (1000, 25))

    def load_level(self, level_file):
        with open(level_file, 'r') as f:
            self.level_file = f.readlines()  
        self.initialize_map()
        
    def map_processing(self):
        ASSET_PATH = 'asset/' 
        global tile_images
        tile_images = {
            "#": pygame.image.load(os.path.join(ASSET_PATH, "wall.png")),
            " ": pygame.image.load(os.path.join(ASSET_PATH, "ground.png")),
            ".": pygame.image.load(os.path.join(ASSET_PATH, "switch_place.png")),
            "+": pygame.image.load(os.path.join(ASSET_PATH, "switch_place.png")),
            "*": pygame.image.load(os.path.join(ASSET_PATH, "switch_place.png"))
        }

        for key, image in tile_images.items():
            tile_images[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def initialize_map(self):
        self.walls = []
        self.stones = []
        self.switches = []
        self.player = None
        self.step = 0
        self.score = 0
        self.screen.blit(self.background, (0, 0))
        if self.level_file:
            max_width = max(len(row) for row in self.level_file[1:]) - 1  # Ignore \n
            map_width = max_width * TILE_SIZE 
            map_height = (len(self.level_file) - 1) * TILE_SIZE  
            offset_x = (SCREEN_WIDTH - map_width) // 2 
            offset_y = (SCREEN_HEIGHT - map_height) // 2
            stones_value = self.level_file[0][:-1].split(' ')
            cnt_stone = 0

            for y in range(1, len(self.level_file)):
                row = self.level_file[y] 
                inside_walls = False  
                for x in range(len(row)):
                    char = row[x]
                    if char == "#":
                        inside_walls = True  
                        wall_position = (offset_x + (x * TILE_SIZE), offset_y + ((y - 1) * TILE_SIZE))
                        self.walls.append(wall_position)

                    if inside_walls:
                        if char in ('@', '+'):
                            self.player = Player(offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE))
                        if char in ('$'):
                            self.stones.append(Stone(offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE), stones_value[cnt_stone], False))
                            cnt_stone += 1
                        if char in ('*'):
                            self.stones.append(Stone(offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE), stones_value[cnt_stone], True))
                            cnt_stone += 1
                        if char in ('.', '+', '*'):
                            self.switches.append((offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE)))

    def render_map(self):
        self.screen.blit(self.background, (0, 0))
        if self.level_file:
            max_width = max(len(row) for row in self.level_file[1:]) - 1  # Ignore \n
            map_width = max_width * TILE_SIZE 
            map_height = (len(self.level_file) - 1) * TILE_SIZE  
            offset_x = (SCREEN_WIDTH - map_width) // 2 
            offset_y = (SCREEN_HEIGHT - map_height) // 2

            for y in range(1, len(self.level_file)):  # Start from the second line
                row = self.level_file[y] 
                inside_walls = False  
                for x in range(len(row)):
                    char = row[x]
                    if char == "#":
                        inside_walls = True  

                    if inside_walls:
                        if char not in ("#") and x < len(row) - 1:
                            self.screen.blit(tile_images[" "], (offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE)))
                        if char in tile_images and char not in ('@', '$'):
                            self.screen.blit(tile_images[char], (offset_x + (x * TILE_SIZE), offset_y + ((y-1) * TILE_SIZE)))

    def play_game(self):
        self.screen.blit(self.background, (0, 0)) 
        self.render_map() 
        
        # Custom font setup
        custom_font = pygame.font.Font("font/JustAnotherHand-Regular.ttf", 36)
        # Render and draw the score, level, and algorithm labels

        if self.algoType == 0:
            self.algoType = "A*"
        elif self.algoType == 1:
            self.algoType = "BFS"
        elif self.algoType == 2:
            self.algoType = "DFS"
        elif self.algoType == 3:
            self.algoType = "UCS"

        score_text = custom_font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = custom_font.render(f"Level: {self.level}", True, (255, 255, 255))
        algo_text = custom_font.render(f"{self.algoType}", True, (255, 255, 255))
        step_text = custom_font.render(f"Step: {self.step}", True, (255, 255, 255))
        score_x = 25 
        score_y = 19 + (self.current_score.get_height() - score_text.get_height()) // 2 + 3
        level_x = 604 + (self.current_level.get_width() - level_text.get_width()) // 2
        level_y = 19 + (self.current_level.get_height() - level_text.get_height()) // 2 + 3
        algo_x = 448 + (self.current_algo.get_width() - algo_text.get_width()) // 2
        algo_y = 19 + (self.current_algo.get_height() - algo_text.get_height()) // 2 + 3
        step_x = 240 
        step_y = 19 + (self.current_score.get_height() - score_text.get_height()) // 2 + 3
        self.screen.blit(self.current_score, (17, 19))
        self.screen.blit(self.current_score, (232, 19)) # For step
        self.screen.blit(self.current_level, (604, 19))
        self.screen.blit(self.current_algo, (448, 19))
        self.screen.blit(score_text, (score_x, score_y))
        self.screen.blit(level_text, (level_x, level_y))
        self.screen.blit(algo_text, (algo_x, algo_y))
        self.screen.blit(step_text, (step_x, step_y))
        self.player.draw(self.screen)
        for stone in self.stones:
            stone.draw(self.screen)

        self.win = all(stone.on_switch for stone in self.stones)
        if self.win:
            # Blurring effect
            blur_surface = pygame.transform.smoothscale(self.screen, (self.screen.get_width() // 2, self.screen.get_height() // 2))
            blur_surface = pygame.transform.smoothscale(blur_surface, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(blur_surface, (0, 0))
            

            # Display win message with score
            win_font = pygame.font.Font("font/IrishGrover-Regular.ttf", 64)
            win_text = win_font.render("You Win!", True, (18, 55, 42))
            score_display_text = win_font.render(f"Score: {self.score}", True, (18, 55, 42))

            # Center win text
            win_x = (self.screen.get_width() - win_text.get_width()) // 2
            win_y = (self.screen.get_height() - win_text.get_height()) // 2 - 50
            score_x = (self.screen.get_width() - score_display_text.get_width()) // 2
            score_y = win_y + win_text.get_height() + 20

            self.screen.blit(win_text, (win_x, win_y))
            self.screen.blit(score_display_text, (score_x, score_y))
            

        self.screen.blit(self.home_button, (1000, 25))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "play_game" and not self.win:
                        if event.key == pygame.K_LEFT:
                            value = self.player.move(-TILE_SIZE, 0, self.stones, self.walls, self.switches)
                            self.step += 1
                            if value != 0:
                                self.score += value + 1
                            else:
                                self.score += 1
                        elif event.key == pygame.K_RIGHT:
                            value = self.player.move(TILE_SIZE, 0, self.stones, self.walls, self.switches)
                            self.step += 1
                            if value != 0:
                                self.score += value + 1
                            else:
                                self.score += 1
                        elif event.key == pygame.K_UP:
                            value = self.player.move(0, -TILE_SIZE, self.stones, self.walls, self.switches)
                            self.step += 1
                            if value != 0:
                                self.score += value + 1
                            else:
                                self.score += 1
                        elif event.key == pygame.K_DOWN:
                            value = self.player.move(0, TILE_SIZE, self.stones, self.walls, self.switches)
                            self.step += 1
                            if value != 0:
                                self.score += value + 1
                            else:
                                self.score += 1

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
                        if (self.home_button_rect.collidepoint(event.pos)):
                            self.state = "welcome"
                    elif self.state == "level_selection":
                        for i, rect in enumerate(self.levelBtnRects):
                            if rect.collidepoint(event.pos):
                                self.load_level(f'levels/level{i + 1}.txt')
                                
                                self.isAlgoSimulated, self.solution = algorithmSimulate.process(f'levels/level{i + 1}.txt', self.algoType, i + 1)
                                self.solutionIndex = 0
                                
                                self.state = "play_game"
                                self.level = i + 1
                                break
                        if (self.back_button_rect.collidepoint(event.pos)):
                            self.state = "algo_selection"
                            self.isAlgoSimulated = False
                            
                        if (self.home_button_rect.collidepoint(event.pos)):
                            self.state = "welcome"
                            self.isAlgoSimulated = False
                            
                    elif self.state == "play_game":
                        if (self.home_button_rect.collidepoint(event.pos)):
                            self.state = "welcome"
                            self.isAlgoSimulated = False
                       
            if (self.state == "play_game" and self.isAlgoSimulated == True):
                if (self.solutionIndex >= len(self.solution)):
                    self.isAlgoSimulated = False
                    self.solution = ""
                    self.solutionIndex = 0
                
                else:
                    currTime = time.time()
                    if (currTime - self.lastInteractionTime >= INTERACTION_TIME):
                        key = getKey(self.solution[self.solutionIndex])
                        self.solutionIndex += 1
                        
                        simulated_event = pygame.event.Event(pygame.KEYDOWN, key=key)
                        pygame.event.post(simulated_event)
                        
                        self.lastInteractionTime = currTime
                    
        
            if self.state == "welcome":
                self.welcome_screen()
            elif self.state == "algo_selection":
                self.algo_selection_screen()
            elif self.state == "level_selection":
                self.level_selection_screen()
            elif self.state == "play_game":
                self.play_game()
            
            pygame.display.flip()

def main():
    # Game instance
    game = SokobanGame()
    game.run()


if __name__ == "__main__":
    main()
