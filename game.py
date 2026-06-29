import pygame
import elytra_physics
 
from pygame.locals import *

class Sq(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((5,15))
        self.surf.fill((0,120,120))

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 24)

win = pygame.display.set_mode((1800,600))

s1 = Sq()

original1 = s1.surf.copy()

angleX = 0

angleY = 0

vx = 0

vy = 0

vz = 0

x = 0

y = 50

z = 0





run = True

clock = pygame.time.Clock()

frame = 0

with open("out.txt", "r") as file:
    # Use int(line) if they are whole numbers, or float(line) for decimals
    number_list = [float(line.strip()) for line in file]


while run:
    clock.tick(20)
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
            run = False

    keys = pygame.key.get_pressed()

    angleX += number_list[frame]
    if (angleX > 90):
        angleX = 90
    elif (angleX < -90):
        angleX = -90


    frame += 1

    

    """if keys[pygame.K_a]:
        angleX += -5
    if keys[pygame.K_d]:
        angleX += +5

    if (angleX > 90):
        angleX = 90
    elif (angleX < -90):
        angleX = -90
    """

    win.fill((0, 0, 0))
    text_string = f"Pitch Angle: {angleX}°"
    text_surface = my_font.render(text_string, True, (255, 255, 255)) # White text

    text2_string = f"Y: {y}"
    text2_surface = my_font.render(text2_string, True, (255, 255, 255)) # White text

    text3_string = f"Z: {z}"
    text3_surface = my_font.render(text3_string, True, (255, 255, 255)) # White text

    x, y, z, vx, vy, vz = elytra_physics.next_physics(vx, vy, vz, angleX, angleY, x, y, z)

    rotated_surf = pygame.transform.rotate(original1, -(angleX+90))

    rotated_rect = rotated_surf.get_rect(center=(z, 600-y))

    

    win.blit(rotated_surf, rotated_rect.topleft)

    

    win.blit(text_surface, (10, 10))
    win.blit(text2_surface, (10, 34))
    win.blit(text3_surface, (10, 58))
    pygame.display.flip()



