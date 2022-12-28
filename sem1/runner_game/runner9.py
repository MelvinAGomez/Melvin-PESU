import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score:{current_time}',False,((250,235,215)))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 303:
                screen.blit(enemy_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)



        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global pengu_surface,player_index

    if player_rectp.bottom <300:
        pengu_surface = pengu_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        pengu_surface = player_walk[int(player_index)]






pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)

#INDUVIDUAL SURFACE AND INDUVIDUAL REACTANGLE
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
end_surface = pygame.image.load('graphics/end1.png').convert_alpha()

#PLAYER SURFACE AND PLAYER REACTANGLE
pengu_surface1 = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
pengu_surface2 = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
pengu_jump = pygame.image.load('graphics/player_jump.png').convert_alpha()
player_walk = [pengu_surface1,pengu_surface2]
player_index = 0
pengu_surface = player_walk[player_index]
player_rectp = pengu_surface.get_rect(midbottom=(100,300))

#FLY
fly_surface1 = pygame.image.load('graphics/Fly1.png').convert_alpha()
fly_surface2 = pygame.image.load('graphics/Fly2.png').convert_alpha()
fly_frames = [fly_surface1,fly_surface2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]


#OUTRO SCREEN
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))


#SNAIL
enemy_surface1 = pygame.image.load('graphics/snail1.png').convert_alpha()
enemy_surface2 = pygame.image.load('graphics/snail2.png').convert_alpha()
snail_frames = [enemy_surface1,enemy_surface2]
snail_frame_index = 0
enemy_surface = snail_frames[snail_frame_index]



obstacle_rect_list = []


#END GAME AND START GAME STUFF
game_name = test_font.render('Runner Game',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render('hit SPACE to run!',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

#TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)



#VARIABLES
player_gravity = 0
game_active = False
start_time = 0
score = 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectp.collidepoint(event.pos):
                    player_gravity = -20


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectp.bottom >=300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #player_recte.left = 800
                start_time =  int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(enemy_surface.get_rect(midbottom=(randint(900,1100),303)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900,1100),210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                enemy_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]






    if game_active:
        screen.blit(sky_surface,(0,-350))
        screen.blit(ground_surface,(0,300))


        score = display_score()



        #PLAYER
        player_gravity += 1
        player_rectp.y += player_gravity
        if player_rectp.bottom >= 300  :
            player_rectp.bottom=300
        player_animation()
        screen.blit(pengu_surface,player_rectp)



        #OBSTACLE MOVEMENT
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rectp,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rectp.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your Final Score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        screen.blit(game_name,game_name_rect)











    pygame.display.update()
    clock.tick(60)
