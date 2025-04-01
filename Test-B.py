import numpy as np
import pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
dx = 3
dy = 0
speed = 4
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
radius = 40
frame_width = 25
angle = 0
square_size = int(min(screen.get_width(),screen.get_height())*0.9)
square_x = (screen.get_width() - square_size) // 2
square_y = (screen.get_height() - square_size) // 2
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    pygame.draw.circle(screen, "blue", player_pos, radius)
    pygame.draw.rect(screen, "black",
                      [square_x, square_y, square_size, square_size], width=frame_width) 
    direction = pygame.Vector2(dx, dy).normalize() * radius
    line_end = player_pos + direction
    pygame.draw.line(screen, "red", player_pos, line_end, 3)

    player_pos.x += dx
    player_pos.y += dy

    # flip() the display to put your work on screen
    pygame.display.flip()

    angle =  np.random.uniform(0, np.pi)
    #Right wall collision
    if player_pos.x + radius >= square_x + square_size - frame_width:
        angle = angle + np.pi/2
        dy = np.sin(angle) * speed
        dx = np.cos(angle) * speed

    # Left wall collision
    elif player_pos.x - radius <= square_x + frame_width:
        angle = angle + np.pi * 3/2
        dy = np.sin(angle) * speed
        dx = np.cos(angle) * speed

    # Top wall collision
    elif player_pos.y - radius <= square_y + frame_width:
        dy = np.sin(angle) * speed
        dx = np.cos(angle) * speed
        pass

    # Bottom wall collision
    elif player_pos.y + radius >= square_y + square_size - frame_width:
        angle = angle + np.pi
        dy = np.sin(angle) * speed
        dx = np.cos(angle) * speed
        pass

    dt = clock.tick(60) / 1000

pygame.quit()