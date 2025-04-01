import numpy as np
import pygame

class BrownianMotion:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.speed = 4

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.radius = 40
        self.frame_width = 25

        self.dx = self.speed
        self.dy = 0

        self.current_angle = np.arctan2(self.dy, self.dx)

        self.in_rotation = False
        self.rotation_duration = 1000  # in milliseconds
        self.rotation_start_time = 0
        self.initial_angle = 0
        self.target_angle = 0
        self.collision_type = None  # "right", "left", "top", "bottom"

        self.square_size = int(min(self.screen.get_width(), self.screen.get_height()) * 0.9)
        self.square_x = (self.screen.get_width() - self.square_size) // 2
        self.square_y = (self.screen.get_height() - self.square_size) // 2

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("white")
            pygame.draw.circle(self.screen, "blue", self.player_pos, self.radius)
            pygame.draw.rect(self.screen, "black",
                             [self.square_x, self.square_y, self.square_size, self.square_size],
                             width=self.frame_width)

            # Check if we are in rotation (paused) state.
            if self.in_rotation:
                elapsed = pygame.time.get_ticks() - self.rotation_start_time
                fraction = min(elapsed / self.rotation_duration, 1)
                diff = ((self.target_angle - self.initial_angle + np.pi) % (2 * np.pi)) - np.pi
                self.current_angle = self.initial_angle + fraction * diff

                if fraction >= 1.0:
                    offset = 3  # pixels to nudge the ball inside the boundary
                    if self.collision_type == "right":
                        self.player_pos.x = self.square_x + self.square_size - self.frame_width - self.radius - offset
                    elif self.collision_type == "left":
                        self.player_pos.x = self.square_x + self.frame_width + self.radius + offset
                    elif self.collision_type == "top":
                        self.player_pos.y = self.square_y + self.frame_width + self.radius + offset
                    elif self.collision_type == "bottom":
                        self.player_pos.y = self.square_y + self.square_size - self.frame_width - self.radius - offset

                    self.dx = np.cos(self.target_angle) * self.speed
                    self.dy = np.sin(self.target_angle) * self.speed
                    self.in_rotation = False
            else:
                # Update ball's direction based on velocity.
                if self.dx != 0 or self.dy != 0:
                    self.current_angle = np.arctan2(self.dy, self.dx)
                self.player_pos.x += self.dx
                self.player_pos.y += self.dy

            # Draw the red line indicating the current direction.
            direction_vector = pygame.Vector2(np.cos(self.current_angle), np.sin(self.current_angle)) * self.radius
            line_end = self.player_pos + direction_vector
            pygame.draw.line(self.screen, "red", self.player_pos, line_end, 3)

            # Only check for collisions when not already rotating.
            if not self.in_rotation:
                # Right wall collision.
                if self.player_pos.x + self.radius >= self.square_x + self.square_size - self.frame_width:
                    self.collision_type = "right"
                    self.player_pos.x = self.square_x + self.square_size - self.frame_width - self.radius
                    self.in_rotation = True
                    self.rotation_start_time = pygame.time.get_ticks()
                    self.initial_angle = self.current_angle
                    self.target_angle = np.random.uniform(np.pi / 2, 3 * np.pi / 2)
                    self.dx, self.dy = 0, 0

                # Left wall collision.
                elif self.player_pos.x - self.radius <= self.square_x + self.frame_width:
                    self.collision_type = "left"
                    self.player_pos.x = self.square_x + self.frame_width + self.radius
                    self.in_rotation = True
                    self.rotation_start_time = pygame.time.get_ticks()
                    self.initial_angle = self.current_angle
                    self.target_angle = np.random.uniform(-np.pi / 2, np.pi / 2)
                    self.dx, self.dy = 0, 0

                # Top wall collision.
                elif self.player_pos.y - self.radius <= self.square_y + self.frame_width:
                    self.collision_type = "top"
                    self.player_pos.y = self.square_y + self.frame_width + self.radius
                    self.in_rotation = True
                    self.rotation_start_time = pygame.time.get_ticks()
                    self.initial_angle = self.current_angle
                    self.target_angle = np.random.uniform(0, np.pi)
                    self.dx, self.dy = 0, 0

                # Bottom wall collision.
                elif self.player_pos.y + self.radius >= self.square_y + self.square_size - self.frame_width:
                    self.collision_type = "bottom"
                    self.player_pos.y = self.square_y + self.square_size - self.frame_width - self.radius
                    self.in_rotation = True
                    self.rotation_start_time = pygame.time.get_ticks()
                    self.initial_angle = self.current_angle
                    self.target_angle = np.random.uniform(np.pi, 2 * np.pi)
                    self.dx, self.dy = 0, 0

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


app = BrownianMotion()
app.run()
