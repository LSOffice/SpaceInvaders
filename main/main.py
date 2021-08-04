import pygame, sys, json, os
from scene import scene

if int(sys.version[0]) < 3:
    print("Error detected. Wrong python version. Must run python3")

nameOfGame = "Space Invaders"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(nameOfGame, nameOfGame)
#game_icon = pygame.image.load("./images/LFUT22_Logo_No_BG.png")
#pygame.display.set_icon(game_icon)

active_scene = scene.MainScene(screen)
while active_scene is not None:
    pressed_keys = pygame.key.get_pressed()

    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True

        if quit_attempt:
            active_scene.Terminate()
        else:
            filtered_events.append(event)

    active_scene.ProcessInput(filtered_events, pressed_keys)
    active_scene.Update()
    active_scene.Render(screen)
    active_scene = active_scene.next

    pygame.display.flip()