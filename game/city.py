import pygame
from typing import Dict, Tuple, Optional

class City:
    def __init__(self, width: int, height: int, grid_size: int):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid_width = width // grid_size
        self.grid_height = height // grid_size
        self.grid: Dict[Tuple[int, int], str] = {}
        
        # Building types and their properties with enhanced visuals
        self.building_types = {
            "house": {
                "color": (100, 100, 255),
                "size": 1,
                "border_color": (80, 80, 200),
                "roof_color": (150, 150, 255),
                "window_color": (255, 255, 200)
            },
            "shop": {
                "color": (255, 100, 100),
                "size": 2,
                "border_color": (200, 80, 80),
                "sign_color": (255, 255, 100),
                "window_color": (200, 200, 255)
            },
            "factory": {
                "color": (100, 255, 100),
                "size": 3,
                "border_color": (80, 200, 80),
                "smoke_color": (200, 200, 200),
                "window_color": (150, 150, 150)
            },
            "park": {
                "color": (100, 255, 100),
                "size": 2,
                "border_color": (80, 200, 80),
                "tree_color": (50, 150, 50),
                "path_color": (200, 200, 150)
            }
        }

    def draw(self, screen):
        # Draw grass background
        screen.fill((100, 200, 100))
        
        # Draw grid lines with a more subtle look
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(screen, (80, 180, 80), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(screen, (80, 180, 80), (0, y), (self.width, y), 1)

        # Draw buildings
        for (x, y), building_type in self.grid.items():
            self._draw_building(screen, x, y, building_type)

    def _draw_building(self, screen, grid_x: int, grid_y: int, building_type: str):
        building = self.building_types[building_type]
        size = building["size"]
        
        # Calculate base rectangle
        base_rect = pygame.Rect(
            grid_x * self.grid_size,
            grid_y * self.grid_size,
            self.grid_size * size,
            self.grid_size * size
        )
        
        # Draw building base
        pygame.draw.rect(screen, building["color"], base_rect)
        pygame.draw.rect(screen, building["border_color"], base_rect, 2)
        
        # Draw building details based on type
        if building_type == "house":
            self._draw_house_details(screen, base_rect, building)
        elif building_type == "shop":
            self._draw_shop_details(screen, base_rect, building)
        elif building_type == "factory":
            self._draw_factory_details(screen, base_rect, building)
        elif building_type == "park":
            self._draw_park_details(screen, base_rect, building)

    def _draw_house_details(self, screen, rect, building):
        # Draw roof
        roof_points = [
            (rect.left, rect.top),
            (rect.centerx, rect.top - rect.height // 3),
            (rect.right, rect.top)
        ]
        pygame.draw.polygon(screen, building["roof_color"], roof_points)
        
        # Draw windows
        window_size = rect.width // 4
        window_rect = pygame.Rect(
            rect.left + rect.width // 4,
            rect.top + rect.height // 3,
            window_size,
            window_size
        )
        pygame.draw.rect(screen, building["window_color"], window_rect)
        pygame.draw.rect(screen, (0, 0, 0), window_rect, 1)

    def _draw_shop_details(self, screen, rect, building):
        # Draw shop sign
        sign_rect = pygame.Rect(
            rect.left + rect.width // 4,
            rect.top + rect.height // 4,
            rect.width // 2,
            rect.height // 4
        )
        pygame.draw.rect(screen, building["sign_color"], sign_rect)
        pygame.draw.rect(screen, (0, 0, 0), sign_rect, 1)
        
        # Draw windows
        window_size = rect.width // 6
        for i in range(2):
            window_rect = pygame.Rect(
                rect.left + rect.width // 4 + i * rect.width // 2,
                rect.top + rect.height * 2 // 3,
                window_size,
                window_size
            )
            pygame.draw.rect(screen, building["window_color"], window_rect)
            pygame.draw.rect(screen, (0, 0, 0), window_rect, 1)

    def _draw_factory_details(self, screen, rect, building):
        # Draw windows
        window_size = rect.width // 8
        for i in range(3):
            for j in range(2):
                window_rect = pygame.Rect(
                    rect.left + rect.width // 4 + i * rect.width // 3,
                    rect.top + rect.height // 3 + j * rect.height // 3,
                    window_size,
                    window_size
                )
                pygame.draw.rect(screen, building["window_color"], window_rect)
                pygame.draw.rect(screen, (0, 0, 0), window_rect, 1)
        
        # Draw smoke
        for i in range(2):
            smoke_points = [
                (rect.left + rect.width // 3 + i * rect.width // 3, rect.top),
                (rect.left + rect.width // 4 + i * rect.width // 3, rect.top - rect.height // 4),
                (rect.left + rect.width // 2 + i * rect.width // 3, rect.top - rect.height // 6)
            ]
            pygame.draw.polygon(screen, building["smoke_color"], smoke_points)

    def _draw_park_details(self, screen, rect, building):
        # Draw trees
        tree_size = rect.width // 4
        for i in range(2):
            for j in range(2):
                tree_rect = pygame.Rect(
                    rect.left + rect.width // 4 + i * rect.width // 2,
                    rect.top + rect.height // 4 + j * rect.height // 2,
                    tree_size,
                    tree_size
                )
                pygame.draw.rect(screen, building["tree_color"], tree_rect)
        
        # Draw path
        path_rect = pygame.Rect(
            rect.left + rect.width // 4,
            rect.top + rect.height // 4,
            rect.width // 2,
            rect.height // 2
        )
        pygame.draw.rect(screen, building["path_color"], path_rect)

    def draw_building_preview(self, screen, building_type: str, grid_x: int, grid_y: int):
        if self._can_place_building(building_type, grid_x, grid_y):
            color = self.building_types[building_type]["color"]
            border_color = self.building_types[building_type]["border_color"]
        else:
            color = (255, 0, 0)
            border_color = (200, 0, 0)

        size = self.building_types[building_type]["size"]
        rect = pygame.Rect(
            grid_x * self.grid_size,
            grid_y * self.grid_size,
            self.grid_size * size,
            self.grid_size * size
        )
        
        # Draw semi-transparent preview with border
        preview = pygame.Surface((rect.width, rect.height))
        preview.set_alpha(128)
        preview.fill(color)
        screen.blit(preview, rect)
        pygame.draw.rect(screen, border_color, rect, 2)

    def _can_place_building(self, building_type: str, grid_x: int, grid_y: int) -> bool:
        size = self.building_types[building_type]["size"]
        
        # Check if building fits within grid
        if grid_x + size > self.grid_width or grid_y + size > self.grid_height:
            return False
            
        # Check if space is empty
        for x in range(grid_x, grid_x + size):
            for y in range(grid_y, grid_y + size):
                if (x, y) in self.grid:
                    return False
                    
        return True

    def place_building(self, building_type: str, grid_x: int, grid_y: int) -> bool:
        if not self._can_place_building(building_type, grid_x, grid_y):
            return False
            
        size = self.building_types[building_type]["size"]
        for x in range(grid_x, grid_x + size):
            for y in range(grid_y, grid_y + size):
                self.grid[(x, y)] = building_type
        return True

    def get_building_at(self, grid_x: int, grid_y: int) -> Optional[str]:
        return self.grid.get((grid_x, grid_y)) 