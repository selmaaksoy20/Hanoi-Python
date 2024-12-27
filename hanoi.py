import pygame
import sys
import time

def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rounded rectangle on the given surface."""
    temp_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))  # Fill with transparent color
    pygame.draw.rect(temp_surface, color, (0, 0, rect[2], rect[3]), border_radius=radius)
    surface.blit(temp_surface, (rect[0], rect[1]))

def format_time(seconds):
    """Format seconds into minutes:seconds."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def show_congrats_message():
    font = pygame.font.SysFont(None, 55)
    message = "Congrats! You won!"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Display the message
    screen.fill(BACKGROUND_COLOR)
    base_rod.draw()
    for rod in rods:
        rod.draw()
    for rod in rods:
        for index, disk in enumerate(reversed(rod.disks)):
            disk.draw(index)
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait for a short period before closing
    pygame.time.wait(2000)

def check_win_condition():
    """Check if all disks are on a rod other than the starting rod."""
    target_rod = rods[2]  # Assuming we want to check if disks are on the third rod
    if len(target_rod.disks) == len(disks) and all(disk.number == len(target_rod.disks) - i for i, disk in enumerate(target_rod.disks)):
        show_congrats_message()
        pygame.quit()
        sys.exit()

def main_game_loop():
    pygame.init()

    global SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, ROD_COLOR, BASE_COLOR, ROD_WIDTH
    global ROD_HEIGHT, BASE_HEIGHT, BASE_Y, ROD_Y, ROD_X, DISK_HEIGHT, DISK_WIDTH_FACTOR, DISK_COLOR
    global TIMER_FONT_SIZE, TIMER_COLOR, screen, base_rod, rods, disks, selected_disk

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (0, 78, 91)
    ROD_COLOR = (240, 240, 240)
    BASE_COLOR = (240, 240, 240)
    ROD_WIDTH = 10
    ROD_HEIGHT = 200
    BASE_HEIGHT = 30
    BASE_Y = SCREEN_HEIGHT - BASE_HEIGHT - 50
    ROD_Y = BASE_Y - ROD_HEIGHT
    ROD_X = [SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, 3 * SCREEN_WIDTH // 4]
    DISK_HEIGHT = 25
    DISK_WIDTH_FACTOR = 50
    DISK_COLOR = [(195, 32, 78), (194, 200, 71), (255, 222, 177)]
    TIMER_FONT_SIZE = 50
    TIMER_COLOR = (255, 255, 255)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower of Hanoi")

    # Initialize timer
    start_time = time.time()

    class Rod:
        def __init__(self, x):
            self.x = x
            self.y = ROD_Y
            self.disks = []

        def draw(self):
            pygame.draw.rect(screen, ROD_COLOR, (self.x - ROD_WIDTH // 2, self.y, ROD_WIDTH, ROD_HEIGHT))

    class BaseRod:
        def __init__(self):
            self.x = 0
            self.y = BASE_Y
            self.width = SCREEN_WIDTH
            self.height = BASE_HEIGHT 

        def draw(self):
            pygame.draw.rect(screen, BASE_COLOR, (self.x, self.y, self.width, self.height))

    class Disk:
        def __init__(self, width, rod, color, number):
            self.width = width
            self.height = DISK_HEIGHT
            self.rod = rod
            self.color = color
            self.number = number
            self.rod.disks.append(self)
            self.selected = False

        def draw(self, index):
            y_position = ROD_Y + ROD_HEIGHT - (index + 1) * DISK_HEIGHT
            draw_rounded_rect(screen, self.color, (self.rod.x - self.width // 2, y_position, self.width, self.height), DISK_HEIGHT // 2)

        def move_to_top_of_rod(self):
            y_position = self.rod.y - 50
            draw_rounded_rect(screen, self.color, (self.rod.x - self.width // 2, y_position, self.width, self.height), DISK_HEIGHT // 2)

        def move_animation(self, target_rod, speed=20):
            # Slide up
            y_position = ROD_Y + ROD_HEIGHT - (len(self.rod.disks)) * DISK_HEIGHT
            while y_position > self.rod.y - 50:
                y_position -= speed
                draw()
                draw_rounded_rect(screen, self.color, (self.rod.x - self.width // 2, y_position, self.width, self.height), DISK_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(10)

            # Slide horizontally
            start_x = self.rod.x
            target_x = target_rod.x
            while start_x != target_x:
                if start_x < target_x:
                    start_x += speed
                    if start_x > target_x:
                        start_x = target_x
                else:
                    start_x -= speed
                    if start_x < target_x:
                        start_x = target_x
                draw()
                draw_rounded_rect(screen, self.color, (start_x - self.width // 2, self.rod.y - 50, self.width, self.height), DISK_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(10)

            # Slide down
            target_y_position = ROD_Y + ROD_HEIGHT - (len(target_rod.disks) + 1) * DISK_HEIGHT
            while y_position < target_y_position:
                y_position += speed
                draw()
                draw_rounded_rect(screen, self.color, (target_rod.x - self.width // 2, y_position, self.width, self.height), DISK_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(10)

            self.rod = target_rod
            target_rod.disks.insert(0, self)

    rods = [Rod(x) for x in ROD_X]
    base_rod = BaseRod()
    disks = [Disk(DISK_WIDTH_FACTOR * (i + 1), rods[0], DISK_COLOR[i % len(DISK_COLOR)], i + 1) for i in range(3)]

    selected_disk = None

    def draw():
        screen.fill(BACKGROUND_COLOR)
        base_rod.draw()
        for rod in rods:
            rod.draw()
        for rod in rods:
            for index, disk in enumerate(reversed(rod.disks)):
                disk.draw(index)
        
        # Draw timer
        elapsed_time = int(time.time() - start_time)
        timer_text = format_time(elapsed_time)
        font = pygame.font.SysFont(None, TIMER_FONT_SIZE)
        text = font.render(timer_text, True, TIMER_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))  # Center at the top of the screen
        screen.blit(text, text_rect)

        pygame.display.flip()

    def get_rod(pos):
        for rod in rods:
            if abs(rod.x - pos[0]) < ROD_WIDTH * 5:
                return rod
        return None

    def is_valid_move(disk, target_rod):
        if not target_rod.disks:
            return True
        return disk.number < target_rod.disks[-1].number

    def move_disk(source, target):
        if source.disks:
            disk = source.disks[0]
            if is_valid_move(disk, target):
                source.disks.remove(disk)  # Remove the disk from the source rod
                disk.move_animation(target)
                check_win_condition()  # Check win condition after moving a disk

    def hanoi(n, source, target, auxiliary):
        if n > 0:
            hanoi(n - 1, source, auxiliary, target)
            move_disk(source, target)
            hanoi(n - 1, auxiliary, target, source)

    running = True
    solving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rod = get_rod(pygame.mouse.get_pos())
                if rod:
                    if selected_disk:
                        if is_valid_move(selected_disk, rod):
                            move_disk(selected_disk.rod, rod)
                        selected_disk = None
                    else:
                        if rod.disks:
                            selected_disk = rod.disks[0]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving:
                    solving = True
                    hanoi(3, rods[0], rods[2], rods[1])
                    
        if not solving:
            draw()
            check_win_condition() 
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_game_loop()
