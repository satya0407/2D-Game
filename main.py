import pygame
import os
import player
import random
import time
from datetime import datetime

player_name = input('Your name: ')

pygame.init()

fire_images_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\Fire"
player_images_idl_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\character\idl"
player_images_walk_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\character\walk"
player_images_jump_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\character\jump"
player_images_slide_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\character\slide"
player_images_dead_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\character\dead"
player_hit_sound = pygame.mixer.Sound(r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Sounds\Socapex - big punch.wav")

bg_images_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\backgrounds"

enemy_images_run_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\enemy\run"
enemy_images_attack_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\enemy\attack"
enemy_images_dead_path = r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Images\enemy\dead"
enemy_hit_sound = pygame.mixer.Sound(r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Sounds\Socapex - new_hits.wav")

enemy_hit_played = False
player_hit_played = False

main_char = player.Player()

pygame.mixer.music.load('Sounds/menu_music.wav')
start = False

WIDTH = 1000
HEIGHT = 600

start_button_color_active = (0, 255, 0)
start_button_color_passive = (255, 255, 255)

font_1 = pygame.font.SysFont('Ariel', 40, True, True)
start_font_surf = font_1.render("START GAME", True, start_button_color_passive)
start_font_rect = start_font_surf.get_rect(center=(WIDTH/2, 200))

player_score = 0
enemy_score = 0

score_player_surf = font_1.render(f"{player_name}: {player_score}", True, (255, 255, 255))
score_player_rect = score_player_surf.get_rect(topleft=(60, 50))

score_enemy_surf = font_1.render(f"ENEMY: {enemy_score}", True, (255, 255, 255))
score_enemy_rect = score_player_surf.get_rect(topright=(WIDTH-60, 50))



screen = pygame.display.set_mode((WIDTH, HEIGHT))

def import_folder(file_path, size):
    fire_image_list = []
    for _, __, file in os.walk(file_path):
        for pic in file:
            path = file_path + '/' + pic
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.rotozoom(img, 0, size)
            fire_image_list.append(img)
    return fire_image_list

bg_images = import_folder(bg_images_path, 1)
bg_choice = random.randint(0, len(bg_images)-1)
push = 0
if bg_choice == 0:
    push = -45
    bg_images[bg_choice] = pygame.transform.flip(bg_images[bg_choice], 0, 1)
elif bg_choice == 2:
    bg_images[bg_choice] = pygame.transform.rotozoom(bg_images[bg_choice], 0, 0.35)
bg_surf = bg_images[bg_choice]
bg_rect = bg_surf.get_rect(center=(WIDTH/2, HEIGHT/2+push))

ground_surf = pygame.image.load("Images/ground/ground0.png").convert_alpha()
ground_rects = []
shift = 0
for i in range(40):
    ground_rect = ground_surf.get_rect(center=(-800+shift, main_char.player_y+125))
    shift += 120
    ground_rects.append(ground_rect)

fire_surfs = import_folder(fire_images_path, 1)
fire_idx = 0

player_imgs = {
    'idl':import_folder(player_images_idl_path, 0.2),
    'walk':import_folder(player_images_walk_path, 0.2),
    'jump':import_folder(player_images_jump_path, 0.2),
    'slide':import_folder(player_images_slide_path, 0.2),
    'dead':import_folder(player_images_dead_path, 0.2)
}

enemy_images = {
    'run':import_folder(enemy_images_run_path, 0.3),
    'attack':import_folder(enemy_images_attack_path, 0.3),
    'dead':import_folder(enemy_images_dead_path, 0.3)
}

enemy_idx = 0
enemy_x = 600
enemy_speed = 5
enemy_forward = True
collision = False
enemy_status = 'run'
enemy_dead = False

run = True
menu = True

music_started = False

event_handler = 0

world_shift = 0
direction = 0

clock = pygame.time.Clock()
pygame.mixer.music.play()

while run:
    if menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coords = event.pos
                if start_font_rect.collidepoint(mouse_coords):
                    menu = False
                    player_score = 0
                    enemy_score = 0
            if event.type == pygame.MOUSEMOTION:
                mouse = event.pos
                if start_font_rect.collidepoint(mouse):
                    start_font_surf = font_1.render("START GAME", True, start_button_color_active)
                else:
                    start_font_surf = font_1.render("START GAME", True, start_button_color_passive)

        screen.fill((0, 0, 0))

        score_player_surf = font_1.render(f"{player_name}: {player_score}", True, (255, 255, 255))
        score_player_rect = score_player_surf.get_rect(center=(120, 200))

        score_enemy_surf = font_1.render(f"ENEMY: {enemy_score}", True, (255, 255, 255))
        score_enemy_rect = score_player_surf.get_rect(center=(120, 400))

        if fire_idx >= len(fire_surfs):
            fire_idx = 0
        fire_rect = fire_surfs[fire_idx].get_rect(center=(WIDTH/2, HEIGHT/2+100))
        screen.blit(fire_surfs[fire_idx], fire_rect)
        fire_idx += 1
        screen.blit(start_font_surf, start_font_rect)
        screen.blit(score_player_surf, score_player_rect)
        screen.blit(score_enemy_surf, score_enemy_rect)
        clock.tick(60)
        pygame.display.update()
    else:
        if not music_started:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Sounds/game_music.mp3')
            pygame.mixer.music.play()
            music_started = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0, 0, 0))
        screen.blit(bg_surf, bg_rect)


        if main_char.player_x > WIDTH-100 and direction == 1:
            main_char.player_speed = 0
            world_shift = -4
        elif main_char.player_x < 100 and direction == -1:
            main_char.player_speed = 0
            world_shift = 4

        for i in range(len(ground_rects)):
            ground_rects[i].left += world_shift
            screen.blit(ground_surf, ground_rects[i])

        main_char.player_status = 'idl'

        if main_char.jump:
            main_char.on_ground = False
            main_char.player_y += main_char.jump_speed
            main_char.jump_speed += main_char.gravity
            main_char.player_status = 'jump'

            if main_char.player_y >= 450:
                main_char.jump = False
                main_char.on_ground = True
                main_char.jump_speed = -20

        if collision:
            if enemy_dead:
                enemy_status = 'dead'
                if not player_hit_played:
                    player_hit_sound.play()
                    player_hit_played = True
                enemy_speed = 0
            else:
                enemy_status = 'attack'
                if not enemy_hit_played:
                    enemy_hit_sound.play()
                    enemy_hit_played = True
                enemy_speed = 0
                main_char.player_status = 'dead'
        else:
            enemy_hit_played = False
            player_hit_played = False
            if enemy_status == 'dead':
                player_score += 1
            enemy_status = 'run'
            if enemy_forward:
                enemy_speed = 5
            else:
                enemy_speed = -5

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            menu = True
            pygame.mixer.stop()
            pygame.mixer.music.load(r"C:\Users\Hajdu Sándor\PycharmProjects\pythonProject6\Sounds\menu_music.wav")
            pygame.mixer.music.play()
            music_started = False

            score_player_surf = font_1.render(f"{player_name}: {player_score}", True, (255, 255, 255))
            score_player_rect = score_player_surf.get_rect(center=(150, 400))

            score_enemy_surf = font_1.render(f"ENEMY: {enemy_score}", True, (255, 255, 255))
            score_enemy_rect = score_player_surf.get_rect(center=(150, 600))

        if keys[pygame.K_RIGHT] and main_char.player_status != 'dead':
            direction = 1
            main_char.player_x += main_char.player_speed
            main_char.player_status = 'walk'
            main_char.forward = True
        elif keys[pygame.K_LEFT] and main_char.player_status != 'dead':
            direction = -1
            main_char.player_x -= main_char.player_speed
            main_char.player_status = 'walk'
            main_char.forward = False
        else:
            direction = 0
            world_shift = 0
            main_char.player_speed = 5

        if keys[pygame.K_UP] and main_char.on_ground == True:
            main_char.jump = True
        if not main_char.jump:
            main_char.player_y = 450
        if keys[pygame.K_SPACE]:
            main_char.player_status = 'slide'
            main_char.player_y += 20

        if main_char.player_idx >= len(player_imgs[main_char.player_status]):
            if main_char.player_status == 'dead':
                main_char.player_idx = 9
            else:
                main_char.player_idx = 0
        player_surf = player_imgs[main_char.player_status][int(main_char.player_idx)]
        if main_char.forward:
            player_rect = player_surf.get_rect(center=(main_char.player_x, main_char.player_y))
            screen.blit(player_surf, player_rect)
        else:
            player_surf = pygame.transform.flip(player_surf, True, False)
            player_rect = player_surf.get_rect(center=(main_char.player_x, main_char.player_y))
            screen.blit(player_surf, player_rect)

        if enemy_idx >= len(enemy_images[enemy_status]):
            if enemy_status == 'dead':
                enemy_idx = 9
            elif enemy_status == 'attack':
                enemy_idx = 0
                event_handler += 1
                if event_handler > 2:
                    if enemy_x > WIDTH/2:
                        main_char.player_x = enemy_x-550
                        enemy_score += 1
                    else:
                        main_char.player_x = enemy_x+550
                        enemy_score += 1
            else:
                enemy_idx = 0
                event_handler = 0
        enemy_surf = enemy_images[enemy_status][int(enemy_idx)]
        enemy_x += enemy_speed
        if enemy_x >= WIDTH or enemy_x <= 0:
            enemy_speed *= -1
            enemy_forward = not enemy_forward
        if enemy_forward == False:
            enemy_surf = pygame.transform.flip(enemy_surf, True, False)
        enemy_rect = enemy_surf.get_rect(center=(enemy_x, 455))

        if player_rect.colliderect(enemy_rect):
            collision = True
            if main_char.player_status == 'slide':
                enemy_dead = True
            else:
                main_char.player_dead = True
        else:
            collision = False
            enemy_dead = False
            main_char.player_dead = False

        screen.blit(enemy_surf, enemy_rect)

        score_player_surf = font_1.render(f"{player_name}: {player_score}", True, (255, 255, 255))
        score_player_rect = score_player_surf.get_rect(topleft=(60, 50))

        score_enemy_surf = font_1.render(f"ENEMY: {enemy_score}", True, (255, 255, 255))
        score_enemy_rect = score_player_surf.get_rect(topright=(WIDTH - 60, 50))

        screen.blit(score_player_surf, score_player_rect)
        screen.blit(score_enemy_surf, score_enemy_rect)

        main_char.player_idx += 0.25
        enemy_idx += 0.25

        clock.tick(60)
        pygame.display.update()

pygame.quit()

with open("points.txt", "a+") as f:
    d = datetime.now()
    dt = datetime.strftime(d, "%Y-%m-%d\t%H:%M:%S")
    f.write(f"{player_name} {dt}\n{player_name} : {player_score}\tEnemy:{enemy_score}\n\n")
    print(dt)