"""Pong game using pygame."""

from __future__ import annotations

import sys

import pygame

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6
PADDLE_MARGIN = 30

# Ball
BALL_SIZE = 15
BALL_SPEED_INITIAL = 5
BALL_SPEED_INCREMENT = 0.5
BALL_MAX_SPEED = 15

# Score
WINNING_SCORE = 10
FONT_SIZE = 48


class Paddle:
    """A paddle controlled by a player."""

    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0

    def move(self, up: bool) -> None:
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def center(self) -> None:
        self.rect.y = (SCREEN_HEIGHT - self.rect.height) // 2


BALL_SERVE_DELAY = 60  # frames to wait before serving


class Ball:
    """The pong ball."""

    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.reset()
        self.current_speed = BALL_SPEED_INITIAL

    def reset(self) -> None:
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dx = 0
        self.dy = 0
        self.current_speed = BALL_SPEED_INITIAL
        self.wait_timer = BALL_SERVE_DELAY

    def serve(self) -> None:
        self.dx = BALL_SPEED_INITIAL * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
        self.dy = BALL_SPEED_INITIAL * (-1 if pygame.time.get_ticks() % 3 == 0 else 1)

    def move(self) -> None:
        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self.serve()
            return
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

    def bounce_off_walls(self) -> bool:
        """Bounce off top/bottom walls. Returns True if ball scored."""
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1
        return False

    def bounce_off_paddle(self, paddle: Paddle) -> None:
        self.dx *= -1
        self.current_speed = min(self.current_speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        # Adjust angle based on where ball hit the paddle
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        self.dy = self.current_speed * offset


class AI:
    """Simple AI that tracks the ball."""

    def __init__(self, paddle: Paddle, difficulty: float = 0.6) -> None:
        self.paddle = paddle
        self.difficulty = difficulty  # 0.0 = slow, 1.0 = perfect

    def update(self, ball: Ball) -> None:
        if ball.dx > 0:
            # Ball coming towards AI: track it
            target_y = ball.rect.centery
        else:
            # Ball moving away: return to center
            target_y = SCREEN_HEIGHT // 2

        # Add some imperfection based on difficulty
        error = (1 - self.difficulty) * 50
        if self.paddle.rect.centery < target_y - error:
            self.paddle.move(up=False)
        elif self.paddle.rect.centery > target_y + error:
            self.paddle.move(up=True)


class PongGame:
    """Main game class."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, 32)
        self.ai_mode = True  # Default to single player
        self.ai: AI | None = None
        self.game_over = False
        self.winner = ""
        self.show_menu = True

    def reset_game(self) -> None:
        self.left_paddle = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.game_over = False
        self.winner = ""
        self.show_menu = False
        if self.ai_mode:
            self.ai = AI(self.right_paddle, difficulty=0.6)
        else:
            self.ai = None

    def handle_input(self) -> bool:
        """Handle events. Returns False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.show_menu:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.ai_mode = True
                        self.reset_game()
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.ai_mode = False
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    if event.key == pygame.K_ESCAPE:
                        self.show_menu = True
        return True

    def update(self) -> None:
        if self.game_over or self.show_menu:
            return

        keys = pygame.key.get_pressed()
        # Left paddle: W/S or Arrow keys (single player)
        if keys[pygame.K_w] or (self.ai and keys[pygame.K_UP]):
            self.left_paddle.move(up=True)
        if keys[pygame.K_s] or (self.ai and keys[pygame.K_DOWN]):
            self.left_paddle.move(up=False)

        # Right paddle: AI or Arrow keys
        if self.ai:
            self.ai.update(self.ball)
        else:
            if keys[pygame.K_UP]:
                self.right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(up=False)

        self.ball.move()
        self.ball.bounce_off_walls()

        # Paddle collision
        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.dx < 0:
            self.ball.bounce_off_paddle(self.left_paddle)
        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.dx > 0:
            self.ball.bounce_off_paddle(self.right_paddle)

        # Scoring
        if self.ball.rect.left <= 0:
            self.right_paddle.score += 1
            self.check_winner()
            if not self.game_over:
                self.ball.reset()
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.left_paddle.score += 1
            self.check_winner()
            if not self.game_over:
                self.ball.reset()

    def check_winner(self) -> None:
        if self.left_paddle.score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 1 (Left)"
        elif self.right_paddle.score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 2 (Right)"

    def draw(self) -> None:
        self.screen.fill(BLACK)

        if self.show_menu:
            self.draw_menu()
            return

        # Center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH // 2 - 2, y, 4, 10))

        # Paddles
        pygame.draw.rect(self.screen, WHITE, self.left_paddle.rect)
        pygame.draw.rect(self.screen, WHITE, self.right_paddle.rect)

        # Ball
        pygame.draw.rect(self.screen, WHITE, self.ball.rect)

        # Scores
        left_text = self.font.render(str(self.left_paddle.score), True, WHITE)
        right_text = self.font.render(str(self.right_paddle.score), True, WHITE)
        self.screen.blit(left_text, (SCREEN_WIDTH // 4 - left_text.get_width() // 2, 20))
        self.screen.blit(right_text, (3 * SCREEN_WIDTH // 4 - right_text.get_width() // 2, 20))

        # Mode indicator
        mode = "1P vs AI" if self.ai_mode else "2P Local"
        mode_text = self.small_font.render(mode, True, (128, 128, 128))
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, SCREEN_HEIGHT - 30))

        # Game over
        if self.game_over:
            win_text = self.font.render(f"{self.winner} wins! Press R to restart", True, WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))

        pygame.display.flip()

    def draw_menu(self) -> None:
        title = self.font.render("PONG", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        opt1 = self.small_font.render("[1] Single Player (vs AI)", True, WHITE)
        opt2 = self.small_font.render("[2] Two Players (Local)", True, WHITE)
        opt3 = self.small_font.render("[Esc] Quit", True, (128, 128, 128))
        self.screen.blit(opt1, (SCREEN_WIDTH // 2 - opt1.get_width() // 2, 280))
        self.screen.blit(opt2, (SCREEN_WIDTH // 2 - opt2.get_width() // 2, 330))
        self.screen.blit(opt3, (SCREEN_WIDTH // 2 - opt3.get_width() // 2, 400))

        controls = [
            "Controls:",
            "Left paddle: W / S or Arrows (1P)",
            "Right paddle: Arrows (2P only)",
            "NumPad 1/2 also works for menu",
            "Esc: Menu  |  R: Restart",
        ]
        for i, line in enumerate(controls):
            text = self.small_font.render(line, True, (180, 180, 180))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460 + i * 30))

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


def main() -> None:
    game = PongGame()
    game.run()


if __name__ == "__main__":
    main()
