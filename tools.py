import pygame

def calculate_rect(start, end):
    """Calculates a pygame.Rect based on start and end coordinates."""
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def draw_smooth_line(surface, draw_color, from_pos, to_pos, size):
    """Draws a smooth line (freehand) by capping line ends with circles."""
    pygame.draw.line(surface, draw_color, from_pos, to_pos, size)
    pygame.draw.circle(surface, draw_color, from_pos, size // 2)
    pygame.draw.circle(surface, draw_color, to_pos, size // 2)

def draw_square(surface, color, start, end, thickness):
    """Draws a square using the max dimension as the side length."""
    x1, y1 = start
    x2, y2 = end
    side = max(abs(x2 - x1), abs(y2 - y1))
    dx = 1 if x2 >= x1 else -1
    dy = 1 if y2 >= y1 else -1
    rect = pygame.Rect(x1, y1, side * dx, side * dy)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, thickness)

def draw_right_triangle(surface, color, start, end, thickness):
    """Draws a right triangle based on start and end bounds."""
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, thickness)

def draw_equilateral_triangle(surface, color, start, end, thickness):
    """Draws an isosceles/equilateral-style triangle."""
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    points = [(mid_x, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, thickness)

def draw_rhombus(surface, color, start, end, thickness):
    """Draws a rhombus inscribed in the bounding box."""
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
    pygame.draw.polygon(surface, color, points, thickness)

def flood_fill(surface, pos, target_color):
    """
    Flood-fill implementation using get_at and set_at.
    Fills an enclosed region with the target color.
    """
    target_color = surface.map_rgb(target_color)
    fill_color = surface.get_at(pos)
    
    if fill_color == target_color:
        return
    
    width, height = surface.get_size()
    stack = [pos]
    visited = set([pos])
    
    while stack:
        x, y = stack.pop()
        surface.set_at((x, y), target_color)
        
        # Check all 4 adjacent pixels
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    if surface.get_at((nx, ny)) == fill_color:
                        stack.append((nx, ny))
                        visited.add((nx, ny))