import pygame
import math
import datetime
from tools import (
    calculate_rect, draw_smooth_line, draw_square, draw_right_triangle,
    draw_equilateral_triangle, draw_rhombus, flood_fill
)

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Paint Application")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)

# App State
color = BLACK
tool = "pencil"
thickness = 5

drawing = False
start_pos = None
current_pos = None
last_pos = None

# Text tool state
text_input_mode = False
current_text = ""
text_pos = (0, 0)

# Base layer to store confirmed drawings
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)

# Fonts
font = pygame.font.SysFont("Verdana", 16)
text_tool_font = pygame.font.SysFont("Verdana", 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # === Text Tool Typing Logic ===
            if text_input_mode:
                if event.key == pygame.K_RETURN:
                    # Commit text to canvas
                    text_surf = text_tool_font.render(current_text, True, color)
                    base_layer.blit(text_surf, text_pos)
                    text_input_mode = False
                    current_text = ""
                elif event.key == pygame.K_ESCAPE:
                    # Cancel text typing
                    text_input_mode = False
                    current_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]
                else:
                    current_text += event.unicode
                continue # Skip other hotkeys while typing

            # === Save logic (Ctrl + S) ===
            mods = pygame.key.get_mods()
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                filename = f"canvas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pygame.image.save(base_layer, filename)
                print(f"Canvas saved as {filename}")

            if event.key == pygame.K_ESCAPE:
                running = False

            # === Tool Selection ===
            if event.key == pygame.K_p: tool = "pencil"
            elif event.key == pygame.K_l: tool = "line"
            elif event.key == pygame.K_r: tool = "rectangle"
            elif event.key == pygame.K_c: tool = "circle"
            elif event.key == pygame.K_e: tool = "eraser"
            elif event.key == pygame.K_s and not (mods & pygame.KMOD_CTRL): tool = "square"
            elif event.key == pygame.K_t: tool = "right_triangle"
            elif event.key == pygame.K_y: tool = "eq_triangle"
            elif event.key == pygame.K_h: tool = "rhombus"
            elif event.key == pygame.K_f: tool = "fill"
            elif event.key == pygame.K_a: tool = "text"

            # === Colors ===
            if event.key == pygame.K_z: color = RED      # Used Z for Red
            elif event.key == pygame.K_g: color = GREEN
            elif event.key == pygame.K_b: color = BLUE
            elif event.key == pygame.K_k: color = BLACK

            # === Brush Sizes ===
            if event.key == pygame.K_1: thickness = 2   # Small
            elif event.key == pygame.K_2: thickness = 5   # Medium
            elif event.key == pygame.K_3: thickness = 10  # Large

            # === Clear Canvas ===
            if event.key == pygame.K_n:
                base_layer.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Cancel or commit text input if clicked elsewhere
                if text_input_mode:
                    text_surf = text_tool_font.render(current_text, True, color)
                    base_layer.blit(text_surf, text_pos)
                    text_input_mode = False
                    current_text = ""

                # Activate Text placement
                if tool == "text":
                    text_input_mode = True
                    text_pos = event.pos
                    current_text = ""
                # Activate Flood-Fill
                elif tool == "fill":
                    flood_fill(base_layer, event.pos, color)
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    current_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos
                
                # Continuous drawing applies directly to base layer
                if tool == "pencil":
                    draw_smooth_line(base_layer, color, last_pos, current_pos, thickness)
                    last_pos = current_pos
                elif tool == "eraser":
                    draw_smooth_line(base_layer, WHITE, last_pos, current_pos, thickness)
                    last_pos = current_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                current_pos = event.pos

                # Commit shapes/lines to the base layer when releasing mouse
                if tool == "line":
                    pygame.draw.line(base_layer, color, start_pos, current_pos, thickness)
                elif tool == "rectangle":
                    rect = calculate_rect(start_pos, current_pos)
                    pygame.draw.rect(base_layer, color, rect, thickness)
                elif tool == "circle":
                    radius = int(math.hypot(current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
                    pygame.draw.circle(base_layer, color, start_pos, radius, thickness)
                elif tool == "square":
                    draw_square(base_layer, color, start_pos, current_pos, thickness)
                elif tool == "right_triangle":
                    draw_right_triangle(base_layer, color, start_pos, current_pos, thickness)
                elif tool == "eq_triangle":
                    draw_equilateral_triangle(base_layer, color, start_pos, current_pos, thickness)
                elif tool == "rhombus":
                    draw_rhombus(base_layer, color, start_pos, current_pos, thickness)

    # -----------------------------
    # Render Logic
    # -----------------------------
    
    # 1. Draw base layer
    screen.blit(base_layer, (0, 0))

    # 2. Draw live preview of shapes/line while dragging
    if drawing and tool not in ["pencil", "eraser", "fill", "text"]:
        if tool == "line":
            pygame.draw.line(screen, color, start_pos, current_pos, thickness)
        elif tool == "rectangle":
            rect = calculate_rect(start_pos, current_pos)
            pygame.draw.rect(screen, color, rect, thickness)
        elif tool == "circle":
            radius = int(math.hypot(current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
            pygame.draw.circle(screen, color, start_pos, radius, thickness)
        elif tool == "square":
            draw_square(screen, color, start_pos, current_pos, thickness)
        elif tool == "right_triangle":
            draw_right_triangle(screen, color, start_pos, current_pos, thickness)
        elif tool == "eq_triangle":
            draw_equilateral_triangle(screen, color, start_pos, current_pos, thickness)
        elif tool == "rhombus":
            draw_rhombus(screen, color, start_pos, current_pos, thickness)

    # 3. Render live text input
    if text_input_mode:
        text_surf = text_tool_font.render(current_text + "|", True, color)
        screen.blit(text_surf, text_pos)

    # 4. Render Top HUD (Heads-Up Display)
    hud_bg = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, (240, 240, 240), hud_bg)
    pygame.draw.line(screen, BLACK, (0, 50), (WIDTH, 50), 2)
    
    info_1 = "TOOLS: P(encil) L(ine) R(ect) C(ircle) S(quare) T(RightTri) Y(EqTri) H(Rhomb) F(ill) A(Text) E(raser)"
    info_2 = f"CURRENT: Tool=[{tool}] Size=[{thickness}px] | SIZES: 1(2px) 2(5px) 3(10px) | COLORS: Z(Red) G B K(Black) | N(Clear) | Ctrl+S(Save)"
    
    screen.blit(font.render(info_1, True, BLACK), (10, 5))
    screen.blit(font.render(info_2, True, BLACK), (10, 25))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()