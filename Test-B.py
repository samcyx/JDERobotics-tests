import numpy as np
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
speed = 4

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
radius = 40
frame_width = 25

dx = speed
dy = 0

current_angle = np.arctan2(dy, dx)

in_rotation = False
rotation_duration = 1000  # in milliseconds
rotation_start_time = 0
initial_angle = 0
target_angle = 0
collision_type = None  # "right", "left", "top", "bottom"

square_size = int(min(screen.get_width(), screen.get_height()) * 0.9)
square_x = (screen.get_width() - square_size) // 2
square_y = (screen.get_height() - square_size) // 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.circle(screen, "blue", player_pos, radius)
    pygame.draw.rect(screen, "black",
                     [square_x, square_y, square_size, square_size], width=frame_width)

    # Check if we are in rotation (paused) state.
    if in_rotation:
        elapsed = pygame.time.get_ticks() - rotation_start_time
        fraction = min(elapsed / rotation_duration, 1)
        diff = ((target_angle - initial_angle + np.pi) % (2 * np.pi)) - np.pi
        current_angle = initial_angle + fraction * diff

        if fraction >= 1.0:
            offset = 5  # pixels to nudge the ball inside the boundary
            if collision_type == "right":
                player_pos.x = square_x + square_size - frame_width - radius - offset
            elif collision_type == "left":
                player_pos.x = square_x + frame_width + radius + offset
            elif collision_type == "top":
                player_pos.y = square_y + frame_width + radius + offset
            elif collision_type == "bottom":
                player_pos.y = square_y + square_size - frame_width - radius - offset

            dx = np.cos(target_angle) * speed
            dy = np.sin(target_angle) * speed
            in_rotation = False
    else:
        # Update ball's direction based on velocity.
        if dx != 0 or dy != 0:
            current_angle = np.arctan2(dy, dx)
        player_pos.x += dx
        player_pos.y += dy

    # Draw the red line indicating the current direction.
    direction_vector = pygame.Vector2(np.cos(current_angle), np.sin(current_angle)) * radius
    line_end = player_pos + direction_vector
    pygame.draw.line(screen, "red", player_pos, line_end, 3)

    # Only check for collisions when not already rotating.
    if not in_rotation:
        # Right wall collision.
        if player_pos.x + radius >= square_x + square_size - frame_width:
            collision_type = "right"
            player_pos.x = square_x + square_size - frame_width - radius
            in_rotation = True
            rotation_start_time = pygame.time.get_ticks()
            initial_angle = current_angle
            target_angle = np.random.uniform(np.pi / 2, 3 * np.pi / 2)
            dx, dy = 0, 0

        # Left wall collision.
        elif player_pos.x - radius <= square_x + frame_width:
            collision_type = "left"
            player_pos.x = square_x + frame_width + radius
            in_rotation = True
            rotation_start_time = pygame.time.get_ticks()
            initial_angle = current_angle
            target_angle = np.random.uniform(-np.pi / 2, np.pi / 2)
            dx, dy = 0, 0

        # Top wall collision.
        elif player_pos.y - radius <= square_y + frame_width:
            collision_type = "top"
            player_pos.y = square_y + frame_width + radius
            in_rotation = True
            rotation_start_time = pygame.time.get_ticks()
            initial_angle = current_angle
            target_angle = np.random.uniform(0, np.pi)
            dx, dy = 0, 0

        # Bottom wall collision.
        elif player_pos.y + radius >= square_y + square_size - frame_width:
            collision_type = "bottom"
            player_pos.y = square_y + square_size - frame_width - radius
            in_rotation = True
            rotation_start_time = pygame.time.get_ticks()
            initial_angle = current_angle
            target_angle = np.random.uniform(np.pi, 2 * np.pi)
            dx, dy = 0, 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
