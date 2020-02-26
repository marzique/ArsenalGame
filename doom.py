"""
https://gist.github.com/limdingwen/c8bb49474de7765f92ee198a1f0f31d5
"""


# X is left-right
# Y is forwards-backwards
# Z is up-down

import pygame
import math
import time
from src.player import Player


WIDTH = 1400
HEIGHT = 800
SCREENS = 2
SCREEN_WIDTH = WIDTH / SCREENS
SCREEN_HEIGHT = HEIGHT

WALLS = [
    ((-1.0, 1.0), (1.0, 1.0), (50, 150, 150)),
    ((1.0, 1.0), (1.0, -1.0), (255, 150, 255)),
    ((-0.5, -1.5), (-1.0, -1.0), (255, 255, 150)),
    ((1.0, -1.0), (0.5, -1.5), (150, 255, 255)),
    ((-1.0, -1.0), (-1.0, 1.0), (150, 255, 150)),
    ((-5.0, -1.0), (-1.0, 1.0), (255, 255, 255)),
    ]

# TODO: order walls from farest to nearest to player
# https://github.com/mirrorworld/DoomStyleRenderer/blob/39f468a52a3a61d3a6136e902e84443e5146b78b/world.py#L56

WALL_HEIGHT = 0.25

SPEED = 0.05
ROT_SPEED = 2

TOP_ZOOM = 5
RAY_LENGTH = 0.1 / TOP_ZOOM

PLAYER_COLOR = (0, 255, 0)
PLAYER_RAY_COLOR = (255, 0, 0)

CEILING_COLOR = (100, 130, 200)
FLOOR_COLOR = (10, 10, 10)

FPS = 60

MOUSE_SENSITIVITY = 0.15


player = Player('tarn')

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 15)

# hide cursor, and keep it always inside window
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


def screen_coords(x, y):
    return ((x / 2 + 0.5) * SCREEN_WIDTH, (-y / 2 + 0.5) * SCREEN_HEIGHT)


def rad(degrees):
    return degrees / 180 * math.pi


def intersect(x1, y1, x2, y2):
    """Returns x of intersecting point with x-axis on graph"""
    return (y1 * x2 - y2 * x1) / (y1 - y2)


def move_player_pos(mult, rot_disp):
    x = player.pos[0] + math.sin(rad(player.rot + rot_disp)) * SPEED * mult
    y = player.pos[1] + math.cos(rad(player.rot + rot_disp)) * SPEED * mult
    player.pos = (x, y)


def run():
    """Main game loop"""
    running = True
    prev_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ## Get the change in x position of the mouse since last check, and change the angle by it
            elif event.type == pygame.MOUSEMOTION:
                x_angular_movement = pygame.mouse.get_rel()[0]
                player.rot += x_angular_movement * MOUSE_SENSITIVITY ## This is how mouse sensitivity is done, right?


        # Handle keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
        
        if keys[pygame.K_LEFT]:
            player.rot -= ROT_SPEED
        if keys[pygame.K_RIGHT]:
            player.rot += ROT_SPEED
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_player_pos(1, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_player_pos(-1, 0)
        if keys[pygame.K_d]:
            move_player_pos(1, 90)
        if keys[pygame.K_a]:
            move_player_pos(-1, 90)


        # Set up split screen rendering surface
        split_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # SCREEN 1: STATIC PLAYER
        split_screen.fill((0, 0, 0))

        # Draw each wall
        for wall in WALLS:
            # Wall absolute positions
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]

            # Wall positions relative to player's position
            px1 = (x1 - player.pos[0]) / TOP_ZOOM
            py1 = (y1 - player.pos[1]) / TOP_ZOOM
            px2 = (x2 - player.pos[0]) / TOP_ZOOM
            py2 = (y2 - player.pos[1]) / TOP_ZOOM

            # Wall positions relative to player's position and rotation
            rx1 = math.cos(rad(-player.rot)) * px1 + math.sin(rad(-player.rot)) * py1
            ry1 = math.cos(rad(-player.rot)) * py1 - math.sin(rad(-player.rot)) * px1
            rx2 = math.cos(rad(-player.rot)) * px2 + math.sin(rad(-player.rot)) * py2
            ry2 = math.cos(rad(-player.rot)) * py2 - math.sin(rad(-player.rot)) * px2

            pygame.draw.line(split_screen, wall[2],
                screen_coords(rx1, ry1),
                screen_coords(rx2, ry2), 1)

        # Draw player

        pygame.draw.line(split_screen, PLAYER_RAY_COLOR,
            screen_coords(0, 0),
            screen_coords(0, RAY_LENGTH), 1)
        pygame.draw.line(split_screen, PLAYER_COLOR,
            screen_coords(0, 0),
            screen_coords(0, 0), 1)

        # Render split screen
        screen.blit(split_screen, (0, 0))
        
        ###########################################################################
        # SCREEN 2: 2.5D

        split_screen.fill((0, 0, 0))

        # Draw wall, floor and ceiling
        
        pygame.draw.rect(split_screen, CEILING_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
        pygame.draw.rect(split_screen, FLOOR_COLOR, pygame.Rect(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

        for wall in WALLS:
            # Wall absolute positions
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]

            # Wall positions relative to player's position
            px1 = x1 - player.pos[0]
            py1 = y1 - player.pos[1]
            px2 = x2 - player.pos[0]
            py2 = y2 - player.pos[1]

            # Wall positions relative to player's position and rotation
            rx1 = math.cos(rad(-player.rot)) * px1 + math.sin(rad(-player.rot)) * py1
            ry1 = math.cos(rad(-player.rot)) * py1 - math.sin(rad(-player.rot)) * px1
            rx2 = math.cos(rad(-player.rot)) * px2 + math.sin(rad(-player.rot)) * py2
            ry2 = math.cos(rad(-player.rot)) * py2 - math.sin(rad(-player.rot)) * px2

            # Don't render walls behind us
            if ry1 <= 0 and ry2 <= 0:
                continue

            # Clip walls intersecting with user plane
            if ry1 <= 0 or ry2 <= 0:
                ix1 = intersect(rx1, ry1, rx2, ry2)
                if ry1 <= 0:
                    rx1 = ix1
                    ry1 = 0.01
                if ry2 <= 0:
                    rx2 = ix1
                    ry2 = 0.01
            
            # Wall positions relative to player's position, rotation and perspective
            zx1 = rx1 / ry1
            zu1 = WALL_HEIGHT  / ry1 # Up   Z
            zd1 = -WALL_HEIGHT / ry1 # Down Z
            zx2 = rx2 / ry2
            zu2 = WALL_HEIGHT  / ry2 # Up   Z
            zd2 = -WALL_HEIGHT / ry2 # Down Z

            pygame.draw.polygon(split_screen, wall[2], [
                screen_coords(zx1, zd1),
                screen_coords(zx1, zu1),
                screen_coords(zx2, zu2),
                screen_coords(zx2, zd2)], 0)

        # Render split screen
        screen.blit(split_screen, (SCREEN_WIDTH + 1, 0))
        
        fps = clock.get_fps()
        if fps >= 50:
            color = (50, 200, 100)
        else:
            color = (200, 50, 100)
        fps_text = font.render("FPS: " + str(round(fps, 1)), 1, color)
        screen.blit(fps_text, (10, 5))

        # Update screen
        pygame.display.update()
        
        # Sleep
        clock.tick(FPS)


if __name__ == '__main__':
    run()
