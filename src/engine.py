"""2.5D engine"""
import pygame
import math
from .helpers import rad


# screen
WIDTH = 1400
HEIGHT = 800
SCREENS = 2
SCREEN_WIDTH = WIDTH / SCREENS
SCREEN_HEIGHT = HEIGHT
FPS = 60


# world
WALLS = [
    ((-1.0, 1.0), (1.0, 1.0), (50, 150, 150)),
    ((1.0, 1.0), (1.0, -1.0), (255, 150, 255)),
    ((-0.5, -1.5), (-1.0, -1.0), (255, 255, 150)),
    ((1.0, -1.0), (0.5, -1.5), (150, 255, 255)),
    ((-1.0, -1.0), (-1.0, 1.0), (150, 255, 150)),
    ((-5.0, -1.0), (-1.0, 1.0), (255, 255, 255)),
    ]

WALL_HEIGHT = 0.25
CEILING_COLOR = (100, 130, 200)
FLOOR_COLOR = (10, 10, 10)


class Control:
    def __init__(self, player):
        pygame.init()
        pygame.display.set_caption("Boom")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 15)

        # hide cursor, and keep it always inside window
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.player = player
        self.running = True


    @staticmethod
    def screen_coords(x, y):
        return ((x / 2 + 0.5) * SCREEN_WIDTH, (-y / 2 + 0.5) * SCREEN_HEIGHT)


    @staticmethod
    def intersect(x1, y1, x2, y2):
        """Returns x of intersecting point with x-axis on graph"""
        return (y1 * x2 - y2 * x1) / (y1 - y2)

    @staticmethod
    def get_middle(wall):
        """return middle point coords of the wall"""
        p1 = wall[0]
        p2 = wall[1]
        x = (p1[0] + p2[0])/2
        y = (p1[1] + p2[1])/2
        return [x, y]

    @staticmethod
    def distance(p1, p2):
        """Distance between two points"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def wall_distance(self, wall):
        """Return distance between wall center and player pos"""
        return self.distance(self.get_middle(wall), self.player.pos)

    def sort_walls(self, walls):
        return sorted(walls, key=self.wall_distance, reverse=True)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            ## Get the change in x position of the mouse since last check, and change the angle by it
            elif event.type == pygame.MOUSEMOTION:
                x_angular_movement = pygame.mouse.get_rel()[0]
                self.player.rot += x_angular_movement * self.player.MOUSE_SENSITIVITY

    def handle_keys(self):
        """Handle keyboard """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
        
        if keys[pygame.K_LEFT]:
            self.player.rot -= ROT_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.rot += ROT_SPEED
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(1, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(-1, 0)
        if keys[pygame.K_d]:
            self.player.move(1, 90)
        if keys[pygame.K_a]:
            self.player.move(-1, 90)


    def render(self, split_screen):
        self.render_2d(split_screen)
        self.render_3d(split_screen)

    def update(self):
        pass

    def render_3d(self, split_screen):
        # Draw walls, floor and ceiling
        pygame.draw.rect(split_screen, CEILING_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
        pygame.draw.rect(split_screen, FLOOR_COLOR, pygame.Rect(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

        sorted_walls = self.sort_walls(WALLS) # the closer the wall, the later it drawn
        for wall in sorted_walls:
            # Wall absolute positions
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]

            # Wall positions relative to player's position
            px1 = x1 - self.player.pos[0]
            py1 = y1 - self.player.pos[1]
            px2 = x2 - self.player.pos[0]
            py2 = y2 - self.player.pos[1]

            # Wall positions relative to player's position and rotation
            rx1 = math.cos(rad(-self.player.rot)) * px1 + math.sin(rad(-self.player.rot)) * py1
            ry1 = math.cos(rad(-self.player.rot)) * py1 - math.sin(rad(-self.player.rot)) * px1
            rx2 = math.cos(rad(-self.player.rot)) * px2 + math.sin(rad(-self.player.rot)) * py2
            ry2 = math.cos(rad(-self.player.rot)) * py2 - math.sin(rad(-self.player.rot)) * px2

            # Don't render walls behind us
            if ry1 <= 0 and ry2 <= 0:
                continue

            # Clip walls intersecting with user plane
            if ry1 <= 0 or ry2 <= 0:
                ix1 = self.intersect(rx1, ry1, rx2, ry2)
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
                self.screen_coords(zx1, zd1),
                self.screen_coords(zx1, zu1),
                self.screen_coords(zx2, zu2),
                self.screen_coords(zx2, zd2)], 0)

        # Render split screen
        self.screen.blit(split_screen, (SCREEN_WIDTH + 1, 0))

    def render_2d(self, split_screen):
        """Render 2d view from top"""
        split_screen.fill((0, 0, 0))

        # Draw each wall
        for wall in WALLS:
            # Wall absolute positions
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]

            # Wall positions relative to player's position
            px1 = (x1 - self.player.pos[0]) / self.player.TOP_ZOOM
            py1 = (y1 - self.player.pos[1]) / self.player.TOP_ZOOM
            px2 = (x2 - self.player.pos[0]) / self.player.TOP_ZOOM
            py2 = (y2 - self.player.pos[1]) / self.player.TOP_ZOOM

            # Wall positions relative to player's position and rotation
            rx1 = math.cos(rad(-self.player.rot)) * px1 + math.sin(rad(-self.player.rot)) * py1
            ry1 = math.cos(rad(-self.player.rot)) * py1 - math.sin(rad(-self.player.rot)) * px1
            rx2 = math.cos(rad(-self.player.rot)) * px2 + math.sin(rad(-self.player.rot)) * py2
            ry2 = math.cos(rad(-self.player.rot)) * py2 - math.sin(rad(-self.player.rot)) * px2

            pygame.draw.line(split_screen, wall[2],
                self.screen_coords(rx1, ry1),
                self.screen_coords(rx2, ry2), 1)

        # Draw player
        pygame.draw.line(split_screen, self.player.RAY_COLOR,
            self.screen_coords(0, 0),
            self.screen_coords(0, self.player.RAY_LENGTH), 1)
        pygame.draw.line(split_screen, self.player.COLOR,
            self.screen_coords(0, 0),
            self.screen_coords(0, 0), 1)

        # Render split screen
        self.screen.blit(split_screen, (0, 0))


    def run(self):
        """Main game loop"""

        while self.running:
            
            self.handle_events()
            self.handle_keys()

            
            split_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            self.render(split_screen)
            
            fps = self.clock.get_fps()
            if fps >= 50:
                color = (50, 200, 100)
            else:
                color = (200, 50, 100)
            fps_text = self.font.render("FPS: " + str(round(fps, 1)), 1, color)
            self.screen.blit(fps_text, (10, 5))

            # Update screen
            pygame.display.update()
            
            # Sleep
            self.clock.tick(FPS)
