import pygame
import os


pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)



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
        self.state = "welcome"
        self.level = None
        self.background = pygame.image.load('asset/Aries.png')
        self.button_start = pygame.image.load('asset/start_btn.png')
        self.button_start_rect = self.button_start.get_rect()
        self.button_start_rect.topleft = (320, 330) 
         # Load and play background music
        pygame.mixer.music.load('asset/music.mp3')  # Replace with your music file path
        pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely


    def welcome_screen(self):
        screen.blit(self.background, (0, 0)) # Draw background image
        screen.blit(self.button_start, self.button_start_rect.topleft)


    def level_selection_screen(self):
        screen.fill(WHITE)
        select_font = pygame.font.SysFont(None, 48)
        select_text = select_font.render("Select Level", True, BLACK)
        screen.blit(select_text, ((SCREEN_WIDTH - select_text.get_width()) // 2, 100))

        # Display level buttons
        for idx, button in enumerate(level_buttons):
            button.draw(screen)

    def load_level(self, level_file):
        with open(level_file, 'r') as f:
            self.level = f.readlines()  # Load map into a list of strings

    def play_game(self):
        screen.fill(WHITE)
        if self.level:
            for y, row in enumerate(self.level):
                for x, char in enumerate(row.strip()):
                    # Draw map (for now just using text representation, you can later draw images or shapes)
                    text = pygame.font.SysFont(None, 32).render(char, True, BLACK)
                    screen.blit(text, (x * 32, y * 32))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "welcome":
                        if  self.button_start_rect.collidepoint(event.pos):
                            self.state = "level_selection"
                    elif self.state == "level_selection":
                        for idx, button in enumerate(level_buttons):
                            if button.is_clicked(event.pos):
                                self.load_level(f"level{idx+1}.txt")
                                self.state = "play_game"
            
            if self.state == "welcome":
                self.welcome_screen()
            elif self.state == "level_selection":
                self.level_selection_screen()
            elif self.state == "play_game":
                self.play_game()

            pygame.display.update()

def main():
    global screen,level_buttons
    pygame.mixer.init()
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Game")
    # Assuming you have 3 levels for demonstration
    level_buttons = [Button(100, 200 + i * 70, BUTTON_WIDTH, BUTTON_HEIGHT, f"Level {i+1}") for i in range(3)]

    # Game instance
    game = SokobanGame()
    game.run()

if __name__ == "__main__":
    main()

pygame.quit()
pygame.mixer.music.stop()  
