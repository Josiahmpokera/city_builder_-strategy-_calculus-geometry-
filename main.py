import pygame
import sys
from game.engine import GameEngine
from game.math_solver import MathSolver
from game.city import City

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1424
WINDOW_HEIGHT = 798
GRID_SIZE = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
LIGHT_GREEN = (144, 238, 144)
MENU_BG = (45, 45, 45)
BUTTON_HOVER = (60, 60, 60)
TEXT_COLOR = (220, 220, 220)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Math City Builder")
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.city = City(WINDOW_WIDTH - 300, WINDOW_HEIGHT, GRID_SIZE)  # Increased menu width
        self.math_solver = MathSolver()
        self.engine = GameEngine(self.city, self.math_solver)
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Building selection menu
        self.building_buttons = [
            {
                "name": "House",
                "color": BLUE,
                "size": 1,
                "rect": pygame.Rect(WINDOW_WIDTH - 280, 120, 240, 60),
                "description": "Basic residential building",
                "cost": "100 coins"
            },
            {
                "name": "Shop",
                "color": RED,
                "size": 2,
                "rect": pygame.Rect(WINDOW_WIDTH - 280, 200, 240, 60),
                "description": "Commercial building",
                "cost": "250 coins"
            },
            {
                "name": "Factory",
                "color": GREEN,
                "size": 3,
                "rect": pygame.Rect(WINDOW_WIDTH - 280, 280, 240, 60),
                "description": "Industrial complex",
                "cost": "500 coins"
            },
            {
                "name": "Park",
                "color": LIGHT_GREEN,
                "size": 2,
                "rect": pygame.Rect(WINDOW_WIDTH - 280, 360, 240, 60),
                "description": "Recreational space",
                "cost": "150 coins"
            }
        ]
        
        self.selected_building = None
        self.show_instructions = True
        self.hovered_button = None

    def draw_menu(self):
        # Draw menu background
        pygame.draw.rect(self.screen, MENU_BG, (WINDOW_WIDTH - 300, 0, 300, WINDOW_HEIGHT))
        
        # Draw title
        title = self.title_font.render("Math City Builder", True, TEXT_COLOR)
        self.screen.blit(title, (WINDOW_WIDTH - 280, 20))
        
        # Draw building buttons
        for button in self.building_buttons:
            # Draw button background
            color = BUTTON_HOVER if self.hovered_button == button["name"] else button["color"]
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, TEXT_COLOR, button["rect"], 2)
            
            # Draw button text
            name_text = self.font.render(button["name"], True, TEXT_COLOR)
            desc_text = self.small_font.render(button["description"], True, TEXT_COLOR)
            cost_text = self.small_font.render(button["cost"], True, TEXT_COLOR)
            
            self.screen.blit(name_text, (button["rect"].x + 10, button["rect"].y + 5))
            self.screen.blit(desc_text, (button["rect"].x + 10, button["rect"].y + 30))
            self.screen.blit(cost_text, (button["rect"].x + 10, button["rect"].y + 45))
        
        # Draw instructions
        if self.show_instructions:
            instructions = [
                "How to Play:",
                "1. Select a building type",
                "2. Click on the grid to place it",
                "3. Solve the math problem",
                "4. Press Enter to submit answer",
                "",
                "Controls:",
                "H - Toggle instructions",
                "ESC - Cancel placement",
                "Enter - Submit answer",
                "Backspace - Delete input",
                "",
                "Press H to hide instructions"
            ]
            
            y = 450
            for line in instructions:
                text = self.small_font.render(line, True, TEXT_COLOR)
                self.screen.blit(text, (WINDOW_WIDTH - 280, y))
                y += 25

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Update hover state
            self.hovered_button = None
            if mouse_pos[0] > WINDOW_WIDTH - 300:
                for button in self.building_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        self.hovered_button = button["name"]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if mouse_pos[0] > WINDOW_WIDTH - 300:
                            for button in self.building_buttons:
                                if button["rect"].collidepoint(mouse_pos):
                                    self.selected_building = button["name"].lower()
                                    self.engine.selected_building = self.selected_building
                        else:
                            self.engine.handle_click(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.show_instructions = not self.show_instructions
                    elif event.key == pygame.K_ESCAPE:
                        self.selected_building = None
                        self.engine.selected_building = None
                        self.engine.showing_problem = False
                        self.engine.current_problem = None
                        self.engine.user_input = ""
                    elif self.engine.showing_problem:
                        if event.key == pygame.K_RETURN:
                            self.engine.handle_enter()
                        elif event.key == pygame.K_BACKSPACE:
                            self.engine.user_input = self.engine.user_input[:-1]
                        else:
                            self.engine.user_input += event.unicode

            # Update game state
            self.engine.update()

            # Draw everything
            self.screen.fill(WHITE)
            self.engine.draw(self.screen)
            self.draw_menu()
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 