"""Tests for pong game logic."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

pygame.init()

from src.pong.game import WINNING_SCORE, Ball, Paddle, PongGame


def test_paddle_stays_in_bounds() -> None:
    paddle = Paddle(50, 0)
    paddle.move(up=True)
    assert paddle.rect.y >= 0

    paddle.rect.y = 600 - paddle.rect.height
    paddle.move(up=False)
    assert paddle.rect.y <= 600 - paddle.rect.height


def test_ball_resets_to_center() -> None:
    ball = Ball()
    ball.rect.x = 100
    ball.rect.y = 100
    ball.reset()
    assert ball.rect.centerx == 800 // 2
    assert ball.rect.centery == 600 // 2


def test_ball_bounces_off_walls() -> None:
    ball = Ball()
    ball.rect.top = 0
    ball.dy = -5
    ball.bounce_off_walls()
    assert ball.dy == 5


def test_game_score_starts_at_zero() -> None:
    game = PongGame()
    assert game.left_paddle.score == 0
    assert game.right_paddle.score == 0
    assert game.game_over is False


def test_winning_score() -> None:
    game = PongGame()
    game.left_paddle.score = WINNING_SCORE - 1
    game.ball.rect.left = 0
    game.update()
    assert game.left_paddle.score == WINNING_SCORE
    assert game.game_over is True
    assert game.winner == "Player 1 (Left)"
