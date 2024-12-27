import pygame
import sys
from hanoi import main_game_loop
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os


pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 78, 91)
BUTTON_COLOR =(170, 155, 5)
BUTTON_HOVER_COLOR = (227, 213, 68)
BUTTON_TEXT_COLOR = (255,255,255)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Page")

background_image_path = '/Users/selmaaksoy/Desktop/backgroundd.png'
try:
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Failed to load background image: {e}")
    sys.exit()


def draw_button(text, x, y, width, height, color):
    """Draw a button with text on the screen."""
    pygame.draw.rect(screen, color, (x, y, width, height))
    font_path ='/Users/selmaaksoy/Desktop/Tiny5/Tiny5-Regular.ttf'
    font = pygame.font.Font(font_path, 36)
    font = pygame.font.SysFont('Tiny5', 45)
    text_render = font.render(text, True, BUTTON_TEXT_COLOR)
    screen.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))

def main():
    """Main loop for the main page."""
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2) and (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2) else BUTTON_COLOR

        draw_button("START", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, button_color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2) and (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2):
                    main_game_loop()  # Call the game loop from hanoi.py

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
