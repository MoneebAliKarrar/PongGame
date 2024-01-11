"""
Pong Game: Main Script
"""
from PONGstyle import *
import pygame
import sys
import random
BALL_SIZE = 15
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 60
PLAYER_HIGH = 30
PLAYER_DISTANCE = 15
PLAYER_STEP = 14
SCRSIZE = (1000, 400)
KEY_REPEAT_DELAY = 50
KEY_REPEAT_INTERVAL = 50


def main():
    """
    Run the main Pong game loop.
    """

    pygame.init()
    fps = pygame.time.Clock()
    screen = pygame.display.set_mode(SCRSIZE)
    screen_rectangle = screen.get_rect()

    player1_score = 0
    player2_score = 0
    # Initialize player paddles and ball
    player1 = pygame.Rect(10, screen_rectangle.centery -
                          PLAYER_HIGH, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(
        screen_rectangle.right - PLAYER_WIDTH,
        screen_rectangle.centery - PLAYER_HIGH,
        PLAYER_WIDTH, PLAYER_HEIGHT)
    ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
    # Initialize player positions, ball position, and ball velocity
    player2.right = screen_rectangle.right - PLAYER_DISTANCE
    player1.left = screen_rectangle.left + PLAYER_DISTANCE
    ball.center = screen_rectangle.center

    ball_x_random = random.randint(1, 2)
    ball_y_random = random.randint(1, 2)
    ballvec = [ball_x_random, ball_y_random]

    pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render(" LET'S SCOOOOORE ", True, GREEN)

    msg_box = msg.get_rect()
    msg_box.center = screen_rectangle.center
    welcome_screen(screen, screen_rectangle)
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN):
                goodbye_screen(screen, screen_rectangle)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Handle player movements based on key presses
                if event.key == pygame.K_w:
                    player1 = move_player1(
                        "up", player1, PLAYER_STEP, screen_rectangle)
                elif event.key == pygame.K_s:
                    player1 = move_player1(
                        "down", player1, PLAYER_STEP, screen_rectangle)
                elif event.key == pygame.K_UP:
                    player2 = move_player2(
                        "up", player2, PLAYER_STEP, screen_rectangle)
                elif event.key == pygame.K_DOWN:
                    player2 = move_player2(
                        "down", player2, PLAYER_STEP, screen_rectangle)
        # Draw the game background, player paddles, and the ball
        draw_background(screen, screen_rectangle, msg, msg_box,
                        SCRSIZE, player1_score, player2_score)
        draw_objects(screen, player1, player2, ball)
        # Move the ball and handle collisions
        ball, player1_score, player2_score = move_ball(
            screen, ball, ballvec, player1, player1_score,
            player2, player2_score, screen_rectangle)
        # Check if a player has won
        if player1_score == 2 or player2_score == 2:
            player1_score, player2_score = winner_screen(
                screen, "player 1" if player1_score == 2 else "player 2",
                screen_rectangle, player1_score, player2_score)
            reset_ball(ball, screen_rectangle)
        pygame.display.flip()
        fps.tick(100)


if __name__ == "__main__":
    main()
