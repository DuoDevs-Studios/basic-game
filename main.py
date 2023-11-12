import pygame
import random
import sys

pygame.init()

# Determine the screen width and height
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Dodge the Blocks")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

player_size = 50
player_x = (WIDTH - player_size) // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

block_size = 50
blocks = []
score = 0
high_score = 0

try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass




# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Difficulty settings
difficulties = {
    "easy": {"block_speed": 2, "block_spawn_chance": 3},
    "medium": {"block_speed": 3, "block_spawn_chance": 5},
    "hard": {"block_speed": 4, "block_spawn_chance": 7},
    "insane": {"block_speed": 5, "block_spawn_chance": 10},
    "impossible": {"block_speed": 6, "block_spawn_chance": 15},
    "nightmare": {"block_speed": 7, "block_spawn_chance": 20},
    "extreme": {"block_speed": 8, "block_spawn_chance": 25},
    "unbelievable": {"block_speed": 9, "block_spawn_chance": 30},
    "godlike": {"block_speed": 10, "block_spawn_chance": 40},
    "legendary": {"block_speed": 11, "block_spawn_chance": 50},
    "mythical": {"block_speed": 12, "block_spawn_chance": 60},
    "divine": {"block_speed": 13, "block_spawn_chance": 70},
    "epic": {"block_speed": 14, "block_spawn_chance": 80},
    "supreme": {"block_speed": 15, "block_spawn_chance": 90},
    "ascendant": {"block_speed": 16, "block_spawn_chance": 100},
    "transcendent": {"block_speed": 17, "block_spawn_chance": 110},
    "unstoppable": {"block_speed": 18, "block_spawn_chance": 120},
    "immortal": {"block_speed": 19, "block_spawn_chance": 130},
    "universe_end": {"block_speed": 20, "block_spawn_chance": 140}
    
}

# Set initial difficulty
current_difficulty = "medium"
difficulty_locked = False

# Main menu variables
main_menu = True
play_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)

# Pause menu variables
pause_menu = False
resume_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 25, 120, 50)
quit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 30, 120, 50)

def show_main_menu():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, play_button)
    play_text = font.render("Play", True, WHITE)
    screen.blit(play_text, (WIDTH // 2 - 25, HEIGHT // 2 - 20))
    pygame.display.flip()

def show_pause_menu():
    pygame.draw.rect(screen, RED, resume_button)
    pygame.draw.rect(screen, RED, quit_button)
    resume_text = font.render("Resume", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    screen.blit(resume_text, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
    screen.blit(quit_text, (WIDTH // 2 - 25, HEIGHT // 2 + 35))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if resume_button.collidepoint(event.pos):
                pause_menu = False
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

# Game loop
alive = True
while alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and main_menu:
            if play_button.collidepoint(event.pos):
                main_menu = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu = not pause_menu
            elif pause_menu and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()  # Quit the game when 'Q' is pressed in the pause menu

    if main_menu:
        show_main_menu()
    elif pause_menu:
        show_pause_menu()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < WIDTH - player_size:
            player_x += player_speed

        if keys[pygame.K_1]:
            current_difficulty = "easy"
        elif keys[pygame.K_2]:
            current_difficulty = "medium"
        elif keys[pygame.K_3]:
            current_difficulty = "hard"
        elif keys[pygame.K_4]:
            current_difficulty = "insane"
        elif keys[pygame.K_5]:
            current_difficulty = "impossible"
        elif keys[pygame.K_6]:
            current_difficulty = "nightmare"
        elif keys[pygame.K_7]:
            current_difficulty = "extreme"
        elif keys[pygame.K_8]:
            current_difficulty = "unbelievable"
        elif keys[pygame.K_9]:
            current_difficulty = "godlike"
        elif keys[pygame.K_0]:
            current_difficulty = "legendary"


        if random.randint(1, 100) < difficulties[current_difficulty]["block_spawn_chance"]:
            block_x = random.randint(0, WIDTH - block_size)
            block_y = -block_size
            blocks.append((block_x, block_y))

        blocks_to_remove = []

        for i, (block_x, block_y) in enumerate(blocks):
            block_y += difficulties[current_difficulty]["block_speed"]
            blocks[i] = (block_x, block_y)

            if (
                player_x < block_x + block_size
                and player_x + player_size > block_x
                and player_y < block_y + block_size
                and player_y + player_size > block_y
            ):
                alive = False  # Player has died3

            if block_y > HEIGHT:
                blocks_to_remove.append(i)

        # Increment the score based on the number of blocks that hit the ground
        score += len(blocks_to_remove)

        for i in reversed(blocks_to_remove):
            blocks.pop(i)

        screen.fill((0, 0, 0))  # Fill the screen with black

        pygame.draw.rect(screen, PURPLE, (player_x, player_y, player_size, player_size))

        for block_x, block_y in blocks:
            pygame.draw.rect(screen, RED, (block_x, block_y, block_size, block_size))

        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        difficulty_text = font.render(f"Difficulty: {current_difficulty.capitalize()}", True, RED)
        screen.blit(difficulty_text, (10, 50))

        pygame.display.flip()

        clock.tick(60)

    if score > high_score:
        high_score = score

    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


if not alive:  # Show death screen
    screen.fill(BLACK)
    death_text = font.render("You Died", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    difficulty_text = font.render(f"Difficulty: {current_difficulty.capitalize()}", True, WHITE)
    
    death_text_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    difficulty_text_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    high_score_text_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
    screen.blit(high_score_text, high_score_text_rect)
    
    screen.blit(death_text, death_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(difficulty_text, difficulty_text_rect)



    if difficulty_locked:
        locked_difficulty_text = font.render("Difficulty locked after starting", True, WHITE)
        locked_difficulty_text_rect = locked_difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
        screen.blit(locked_difficulty_text, locked_difficulty_text_rect)
    else:
        locked_difficulty_text = font.render("Difficulty can be changed until you start", True, WHITE)
        locked_difficulty_text_rect = locked_difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
        screen.blit(locked_difficulty_text, locked_difficulty_text_rect)

    pygame.display.flip()
    pygame.time.delay(4000)  # Pause for 4 seconds
