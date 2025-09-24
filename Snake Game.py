import pygame
import sys
import random

pygame.init()

# Dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
BLUE = (0, 120, 215)
GRAY = (20, 20, 30)
YELLOW = (255, 215, 0)
ACCENT = (26, 188, 156)
ACCENT2 = (52, 152, 219)

# Fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Multi Niveaux")
clock = pygame.time.Clock()

# Police
font = pygame.font.SysFont("consolas", 32)
font_big = pygame.font.SysFont("consolas", 50, bold=True)
font_small = pygame.font.SysFont("consolas", 24)

# Particules (étoiles)
stars = []
for _ in range(100):
    stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)])

def draw_space_background():
    screen.fill(BLACK)
    for s in stars:
        pygame.draw.circle(screen, WHITE, (int(s[0]), int(s[1])), s[2])
        s[1] += 0.5 * s[2]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = 0
            s[2] = random.randint(1, 3)

# Classes
class SnakeGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.reset()

    def reset(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.spawn_food()
        self.score = 0
        self.missions_done = 0

        if self.difficulty == "Facile":
            self.speed = 10
            self.max_missions = 10
            self.max_score = 40
        elif self.difficulty == "Normal":
            self.speed = 15
            self.max_missions = 20
            self.max_score = 80
        else:  # Difficile
            self.speed = 20
            self.max_missions = 40
            self.max_score = 120

    def spawn_food(self):
        self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def move(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.spawn_food()
            self.missions_done += 1
        else:
            self.snake.pop()

        return True

    def draw(self, surface):
        surface.fill(BLACK)
        # serpent
        for x, y in self.snake:
            pygame.draw.rect(surface, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # nourriture
        fx, fy = self.food
        pygame.draw.rect(surface, RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # score
        text = font_small.render(f"Score: {self.score}  Missions: {self.missions_done}/{self.max_missions}", True, WHITE)
        surface.blit(text, (10, 10))

    def mission_over(self):
        return self.missions_done >= self.max_missions or self.score >= self.max_score

    def reset_mission_state(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.spawn_food()


# Menu principal
def draw_main_menu():
    draw_space_background()
    title = font_big.render("🐍 Snake Game", True, YELLOW)
    welcome = font_small.render("Bienvenue dans Snake - Choisissez une difficulté", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(welcome, (WIDTH // 2 - welcome.get_width() // 2, 150))

    buttons = [("Facile 🟢", GREEN), ("Normal 🔵", BLUE), ("Difficile 🔴", RED)]
    btn_rects = []

    for i, (label, color) in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - 150, 250 + i * 100, 300, 60)
        pygame.draw.rect(screen, color, rect, border_radius=12)
        text = font.render(label, True, WHITE)
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
        btn_rects.append((rect, label.split()[0]))

    pygame.display.flip()
    return btn_rects


# Menu Game Over
def show_gameover_menu(surface, font, font_small):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    gameover_text = font_big.render("💀 Game Over", True, RED)
    surface.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, 100))

    buttons = [
        ("Reprendre 🔄", GREEN, "reprendre"),
        ("Terminer 🏁", YELLOW, "terminer"),
        ("Menu Principal 🏠", BLUE, "menu"),
        ("Quitter ❌", RED, "quitter")
    ]

    btn_rects = []
    for i, (label, color, action) in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - 150, 220 + i * 80, 300, 60)
        pygame.draw.rect(surface, color, rect, border_radius=12)
        text = font.render(label, True, WHITE)
        surface.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
        btn_rects.append((rect, action))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in btn_rects:
                    if rect.collidepoint(event.pos):
                        return action


# Boucle principale
def main():
    in_menu = True
    in_game = False
    game = None

    while True:
        if in_menu:
            buttons = draw_main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, difficulty in buttons:
                        if rect.collidepoint(event.pos):
                            game = SnakeGame(difficulty)
                            in_game = True
                            in_menu = False

        elif in_game and game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game.direction != (0, 1):
                        game.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and game.direction != (0, -1):
                        game.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and game.direction != (1, 0):
                        game.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and game.direction != (-1, 0):
                        game.direction = (1, 0)

            alive = game.move()
            if not alive:
                action = show_gameover_menu(screen, font, font_small)
                if action == "reprendre":
                    game.reset_mission_state()
                elif action == "terminer":
                    in_menu = True
                    in_game = False
                elif action == "menu":
                    in_menu = True
                    in_game = False
                elif action == "quitter":
                    pygame.quit()
                    sys.exit()

            game.draw(screen)

            if game.mission_over():
                in_menu = True
                in_game = False

            pygame.display.flip()
            clock.tick(game.speed)


if __name__ == "__main__":
    main()
