"""
PONGstyle module: Contains functions for Pong game styling.
"""
import pygame
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
MAGENTA = (255, 0, 255)


def welcome_screen(screen, screen_rectangle):
    """
    Display a welcome message on the screen for 2 seconds.

    Parameters:
    - screen: Pygame screen surface.
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    """
    screen.fill(BLACK)
    welcome_font = pygame.font.Font('freesansbold.ttf', 48)
    welcome_text = welcome_font.render("Welcome to Pong!", True, WHITE)
    welcome_box = welcome_text.get_rect()
    welcome_box.center = screen_rectangle.center
    screen.blit(welcome_text, welcome_box)

    pygame.display.flip()
    pygame.time.wait(2000)


def goodbye_screen(screen, screen_rectangle):
    """
    Display a goodbye message on the screen for 2 seconds.

    Parameters:
    - screen: Pygame screen surface.
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    """
    screen.fill(BLACK)
    goodbye_font = pygame.font.Font('freesansbold.ttf', 48)
    goodbye_text = goodbye_font.render(
        "Goodbye! Thanks for playing!", True, WHITE)
    goodbye_box = goodbye_text.get_rect()
    goodbye_box.center = screen_rectangle.center
    screen.blit(goodbye_text, goodbye_box)

    pygame.display.flip()
    pygame.time.wait(2000)


def winner_screen(
        screen, winner, screen_rectangle, player1_score, player2_score):
    """
    Display a winner message on the screen for 2 seconds.
    Reset player scores.

    Parameters:
    - screen: Pygame screen surface.
    - winner: String representing the winner ("player 1" or "player 2").
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    - player1_score: Player 1's score.
    - player2_score: Player 2's score.

    Returns:
    - Updated player1_score and player2_score.
    """
    screen.fill(BLACK)
    winner_font = pygame.font.Font('freesansbold.ttf', 48)
    if winner == "player 1":
        winner_text = winner_font.render(
            winner + " you're awesome", True, MAGENTA)
    elif winner == "player 2":
        winner_text = winner_font.render(
            winner + " you're awesome", True, BLUE)
    winner_box = winner_text.get_rect()
    winner_box.center = screen_rectangle.center
    screen.blit(winner_text, winner_box)
    pygame.display.flip()
    pygame.time.wait(2000)
    player1_score = 0
    player2_score = 0
    return player1_score, player2_score


def draw_dashed_line(screen, start, end, orientation, screen_rectangle):
    """
    Draw a dashed line on the screen.

    Parameters:
    - screen: Pygame screen surface.
    - start: Starting position of the line.
    - end: Ending position of the line.
    - orientation: String, either "horizontal" or "vertical".
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    """
    dash_length = 10
    for i in range(start, end, dash_length * 2):
        if orientation == "horizontal":
            pygame.draw.line(screen, WHITE, (i, screen_rectangle.top),
                             (i + dash_length, screen_rectangle.top), width=5)
            pygame.draw.line(
                screen, WHITE,
                (i, screen_rectangle.bottom - dash_length),
                (i + dash_length, screen_rectangle.bottom - dash_length),
                width=5
                    )

        elif orientation == "vertical":
            pygame.draw.line(
                screen, WHITE, (screen_rectangle.centerx, i),
                (screen_rectangle.centerx, i + dash_length), width=5
                )


def draw_background(
            screen, screen_rectangle, msg, msg_box,
            SCRSIZE, player1_score, player2_score):
    """
    Draw the game background, including dashed lines and player scores.

    Parameters:
    - screen: Pygame screen surface.
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    - msg: Pygame surface containing the game message.
    - msg_box: Pygame Rect representing the message box dimensions.
    - SCRSIZE: Tuple representing the screen size.
    - player1_score: Player 1's score.
    - player2_score: Player 2's score.
    """
    screen.fill(BLACK)
    screen.blit(msg, msg_box)
    dash_length = 10
    # Top edge
    draw_dashed_line(screen, 0, SCRSIZE[0], "horizontal", screen_rectangle)
    # Bottom edge
    draw_dashed_line(screen, 0, SCRSIZE[0], "horizontal", screen_rectangle)
    # Middle vertical dashed line
    draw_dashed_line(
            screen, screen_rectangle.top,
            screen_rectangle.bottom - dash_length, "vertical",
            screen_rectangle)

    score_font = pygame.font.Font('freesansbold.ttf', 36)
    player1_text = score_font.render(f"P1: {player1_score}", True, GREEN)
    player2_text = score_font.render(f"P2: {player2_score}", True, GREEN)

    screen.blit(player1_text, (screen_rectangle.left + 20, 20))
    screen.blit(player2_text, (screen_rectangle.right -
                player2_text.get_width() - 20, 20))


def draw_objects(screen, player1, player2, ball):
    """
    Draw player paddles and the ball on the screen.

    Parameters:
    - screen: Pygame screen surface.
    - player1: Pygame Rect representing player 1's paddle.
    - player2: Pygame Rect representing player 2's paddle.
    - ball: Pygame Rect representing the ball.
    """
    pygame.draw.rect(screen, MAGENTA, player1)
    pygame.draw.rect(screen, BLUE, player2)
    pygame.draw.rect(screen, RED, ball)


def move_ball(
                screen, ball, ballvec, player1, player1_score, player2,
                player2_score, screen_rectangle):
    """
    Move the ball and handle collisions.

    Parameters:
    - screen: Pygame screen surface.
    - ball: Pygame Rect representing the ball.
    - ballvec: List containing the ball's velocity [x, y].
    - player1: Pygame Rect representing player 1's paddle.
    - player1_score: Player 1's score.
    - player2: Pygame Rect representing player 2's paddle.
    - player2_score: Player 2's score.
    - screen_rectangle: Pygame Rect representing the screen dimensions.

    Returns:
    - Updated ball, player1_score, and player2_score.
    """
    ball = ball.move(ballvec)
    if ball.colliderect(player1) or ball.colliderect(player2):
        ballvec[0] = -ballvec[0]
    elif ball.top < screen_rectangle.top or\
            ball.bottom > screen_rectangle.bottom:
        ballvec[1] = -ballvec[1]
    elif ball.left < screen_rectangle.left:
        player2_score += 1
        reset_ball(ball, screen_rectangle)
    elif ball.right > screen_rectangle.right:
        player1_score += 1
        reset_ball(ball, screen_rectangle)
    return ball, player1_score, player2_score


def reset_ball(ball, screen_rectangle):
    """
    Reset the ball's position to the center after a score.

    Parameters:
    - ball: Pygame Rect representing the ball.
    - screen_rectangle: Pygame Rect representing the screen dimensions.
    """
    pygame.time.wait(700)
    ball.center = screen_rectangle.center


def move_player1(direction, player1, PLAYER_STEP, screen_rectangle):
    """
    Move player 1's paddle up or down based on the input direction.

    Parameters:
    - direction: String, either "up" or "down".using keyboard arrows.
    - player1: Pygame Rect representing player 1's paddle.
    - PLAYER_STEP: Step size for player movement.
    - screen_rectangle: Pygame Rect representing the screen dimensions.

    Returns:
    - Updated player1.
    """
    if direction == "up":
        player1 = player1.move(0, -PLAYER_STEP)
    elif direction == "down":
        player1 = player1.move(0, PLAYER_STEP)

    if player1.bottom > screen_rectangle.bottom:
        player1.bottom = screen_rectangle.bottom
    elif player1.top < screen_rectangle.top:
        player1.top = screen_rectangle.top
    return player1


def move_player2(direction, player2, PLAYER_STEP, screen_rectangle):
    """
    Move player 2's paddle up or down based on the input direction.

    Parameters:
    - direction: String, either "up" or "down".using key "W" and "S".
    - player2: Pygame Rect representing player 2's paddle.
    - PLAYER_STEP: Step size for player movement.
    - screen_rectangle: Pygame Rect representing the screen dimensions.

    Returns:
    - Updated player2.
    """
    if direction == "up":
        player2 = player2.move(0, -PLAYER_STEP)
    elif direction == "down":
        player2 = player2.move(0, PLAYER_STEP)

    if player2.bottom > screen_rectangle.bottom:
        player2.bottom = screen_rectangle.bottom
    elif player2.top < screen_rectangle.top:
        player2.top = screen_rectangle.top
    return player2
