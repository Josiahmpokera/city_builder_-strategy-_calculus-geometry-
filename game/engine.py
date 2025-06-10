import pygame
from .city import City
from .math_solver import MathSolver

class GameEngine:
    def __init__(self, city: City, math_solver: MathSolver):
        self.city = city
        self.math_solver = math_solver
        self.selected_building = None
        self.current_problem = None
        self.user_input = ""
        self.showing_problem = False
        self.message = ""
        self.message_timer = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def handle_click(self, mouse_pos):
        if self.showing_problem:
            return

        if not self.selected_building:
            self.show_message("Please select a building type first!")
            return

        # Convert mouse position to grid coordinates
        grid_x = mouse_pos[0] // self.city.grid_size
        grid_y = mouse_pos[1] // self.city.grid_size

        # Check if the placement is valid
        if not self.city._can_place_building(self.selected_building, grid_x, grid_y):
            self.show_message("Cannot place building here!")
            return

        # Generate a math problem based on the building type
        self.current_problem = self.math_solver.generate_problem(self.selected_building)
        self.showing_problem = True
        self.user_input = ""

    def handle_enter(self):
        if not self.showing_problem or not self.current_problem:
            return

        # Check answer
        if self.math_solver.check_answer(self.current_problem, self.user_input):
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // self.city.grid_size
            grid_y = mouse_pos[1] // self.city.grid_size
            if self.city.place_building(self.selected_building, grid_x, grid_y):
                self.show_message("Building placed successfully!")
            else:
                self.show_message("Failed to place building!")
        else:
            self.show_message("Incorrect answer! Try again.")
        
        self.showing_problem = False
        self.current_problem = None
        self.user_input = ""

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, screen):
        # Draw the city grid
        self.city.draw(screen)

        # Draw the selected building preview
        if self.selected_building and not self.showing_problem:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // self.city.grid_size
            grid_y = mouse_pos[1] // self.city.grid_size
            self.city.draw_building_preview(screen, self.selected_building, grid_x, grid_y)

        # Draw math problem if active
        if self.showing_problem:
            self._draw_math_problem(screen)

        # Draw message if any
        if self.message_timer > 0:
            self._draw_message(screen)

    def _draw_math_problem(self, screen):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Create problem box
        box_width = 600
        box_height = 300
        box_x = (screen.get_width() - box_width) // 2
        box_y = (screen.get_height() - box_height) // 2
        
        # Draw problem box background
        pygame.draw.rect(screen, (45, 45, 45), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (220, 220, 220), (box_x, box_y, box_width, box_height), 2)

        # Draw problem text
        problem_text = self.font.render(self.current_problem["question"], True, (220, 220, 220))
        input_text = self.font.render(f"Your answer: {self.user_input}", True, (220, 220, 220))
        hint_text = self.small_font.render("Press Enter to submit, Esc to cancel", True, (180, 180, 180))
        
        # Center text in box
        screen.blit(problem_text, (box_x + (box_width - problem_text.get_width()) // 2, 
                                 box_y + 50))
        screen.blit(input_text, (box_x + (box_width - input_text.get_width()) // 2, 
                               box_y + 150))
        screen.blit(hint_text, (box_x + (box_width - hint_text.get_width()) // 2,
                              box_y + 200))

    def _draw_message(self, screen):
        # Create message box
        text = self.font.render(self.message, True, (255, 255, 255))
        box_width = text.get_width() + 40
        box_height = 50
        box_x = (screen.get_width() - box_width) // 2
        box_y = 20
        
        # Draw message box background
        pygame.draw.rect(screen, (45, 45, 45), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (220, 220, 220), (box_x, box_y, box_width, box_height), 2)
        
        # Draw message text
        screen.blit(text, (box_x + 20, box_y + 10))

    def show_message(self, message, duration=60):
        self.message = message
        self.message_timer = duration 