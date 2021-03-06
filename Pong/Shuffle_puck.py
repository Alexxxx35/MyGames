import pygame, sys, random, math ,os
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

pygame.init()
clock = pygame.time.Clock()
start_countdown = 3
window_width = 1000
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.font.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

# score and texts
player1_name = 'Alex'
ORDI_name = 'ORDI'
score_player1 = 0
score_ordi = 0
police_path="Pong/polices"

police = pygame.font.Font(os.path.join(police_path,"Sketch3D.otf"), 25)
policeEND = pygame.font.Font(os.path.join(police_path,"Sketch3D.otf"), 50)
score_player1X = window_width * 3 / 4
score_ordiX = window_width / 4
score_player1Y = window_height / 4
score_ordiY = window_height / 4
round_wonJ1 = 0
round_wonORDI = 0
victoryJ1 = 0
victoryORDI = 0

sounds_path="Pong/sounds"
music_game = pygame.mixer.Sound(os.path.join(sounds_path,"ace_combat.wav"))
racket_noise = pygame.mixer.Sound(os.path.join(sounds_path,"shuffle_racket_noise.wav"))
racket_noise2 = pygame.mixer.Sound(os.path.join(sounds_path,"shuffle_racket_noise_ordi.wav"))
obstacle_noise = pygame.mixer.Sound(os.path.join(sounds_path,"shuffle_obstacle_noise.wav"))
goal = pygame.mixer.Sound(os.path.join(sounds_path,"shuffle_puck_goal.wav"))
# music_game.play(-1)

images_path="Pong/images"
pygame.display.set_caption('Shuffle Puck')
icon = pygame.image.load(os.path.join(images_path,"ball.png")).convert_alpha()
player_cursor = pygame.image.load(os.path.join(images_path,"shuffle_racket.png")).convert_alpha()
ordi_cursor = pygame.image.load(os.path.join(images_path,"shuffle_racket2.png")).convert_alpha()
ball = pygame.image.load(os.path.join(images_path,"shuffle_ball.png")).convert_alpha()
pygame.display.set_icon(icon)
background_color = (0, 0, 0)

# rect_player_cursor = player_cursor.get_rect()
player_cursorX = int(window_width / 2) - 30
player_cursorY = int(window_height / 4 * 3)
ordi_cursorX = int(window_width / 2) - 30
ordi_cursorY = 25
ordi_cursor_speed = 5
rect_player = pygame.draw.rect(window, WHITE, (55, 55, 55, 55), 1)
rect_ordi = pygame.draw.rect(window, WHITE, (55, 55, 55, 55), 1)
ballX_start = int(window_width / 2) - 15
ballY_start = int(window_height / 2) - 15
ballX = ballX_start
ballY = ballY_start
rect_ball = pygame.draw.rect(window, WHITE, (50, 50, 50, 50), 1)

random_direction = random.choice([-1, 1])
start_speedX = 3 * random_direction
start_speedY = 3 * random_direction
ballX_speed = 10
ballY_speed = 10

goalXlow = 353
goalXhigh = 652
goalYordi = 60
goalYplayer = window_height - 60
score_time = True
basic_font = pygame.font.Font('freesansbold.ttf', 32)
################ SETTINGS ####################

# mouse blocking
pygame.mouse.set_visible(False)
collision_correction_for_straight_mov = 16
pygame.mouse.set_pos([int(window_width / 2), int(window_height / 4 * 3)])


def collision(rect_, rect_ball):
    if rect_ball.right < rect_.left:
        return False
    if rect_ball.bottom < rect_.top:
        return False
    if rect_ball.left > rect_.right:
        return False
    if rect_ball.top > rect_.bottom:
        return False
    return True


goal_status = "no_goal"
while True:
    random_direction = random.choice([-1, 1])
    window.fill(background_color)
    time_in_miliseconds = pygame.time.get_ticks()
    time_in_seconds = time_in_miliseconds // 1000
    time_in_minutes = time_in_seconds // 60
    countdown = start_countdown + score_time - time_in_seconds
    display_countdown = police.render('cooldown:' + str(countdown), True, pygame.Color(255, 255, 255))
    display_timer = police.render('time:' + str(time_in_minutes) + '.' + str(time_in_seconds), True,
                                  pygame.Color(255, 255, 255))
    display_score_player1 = police.render(str(player1_name) + ':' + str(score_player1), True,
                                          pygame.Color(255, 255, 255))
    display_score_ordi = police.render('ordi:' + str(score_ordi), True,
                                       pygame.Color(255, 255, 255))
    display_J1_victory = policeEND.render(
        '{} has won with {} rounds ahead'.format(player1_name, round_wonJ1 - round_wonORDI), True,
        pygame.Color(255, 255, 255))
    display_ORDI_victory = policeEND.render(
        '{} has won with {} rounds ahead'.format(ORDI_name, round_wonORDI - round_wonJ1), True,
        pygame.Color(255, 255, 255))
    if countdown >= 0:
        start_speedX = 0
        start_speedY = 0
        if countdown <= 3:
            window.blit(display_countdown, (int(window_width / 2 - 60), int(window_height / 3)))
    # ball movements
    ballX += start_speedX
    ballY += start_speedY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION and event.pos[1] > window_height / 2:
            player_cursorX = event.pos[0]
            player_cursorY = event.pos[1]
            rect_player.center = pygame.mouse.get_pos()
            # print(player_cursorX)
            # print(player_cursorY)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # print(ballX)
    # print(ballY)
    if ballX > goalXlow and ballX < goalXhigh:
        if ballY <= 10:
            goal.play()
            score_player1 += 1
            ballX = ballX_start
            ballY = ballY_start
            goal_status = "goal"
            round_wonJ1 += 1
            score_time = pygame.time.get_ticks() // 1000
            start_speedX = start_speedX * random_direction
            start_speedY = start_speedY * random_direction
        if ballY >= window_height - 10:
            goal.play()
            score_ordi += 1
            ballX = ballX_start
            ballY = ballY_start
            goal_status = "goal"
            round_wonORDI += 1
            score_time = pygame.time.get_ticks() // 1000
            start_speedX = start_speedX * random_direction
            start_speedY = start_speedY * random_direction

    if ballX < 0:
        ballX = 0
        start_speedX *= -1
        obstacle_noise.play()
    if ballX >= window_width:
        ballX = window_width
        start_speedX *= -1
        obstacle_noise.play()
    if ballY <= 0:
        ballY = 0
        start_speedY *= -1
        obstacle_noise.play()
    if ballY >= window_height:
        ballY = window_height
        start_speedY *= -1
        obstacle_noise.play()

    if collision(rect_player, rect_ball) == True:
        start_speedX = ballX_speed
        start_speedY = ballY_speed
        racket_noise.play()
        if rect_ball.x < rect_player.x - collision_correction_for_straight_mov and rect_ball.y < rect_player.y:
            start_speedY *= -1
            start_speedX *= -1
        if rect_ball.x > rect_player.x - collision_correction_for_straight_mov and rect_ball.x < rect_player.x + collision_correction_for_straight_mov and rect_ball.y < rect_player.y:
            start_speedX *= 0
            start_speedY *= -1
        if rect_ball.x > rect_player.x + collision_correction_for_straight_mov and rect_ball.y < rect_player.y:
            start_speedX *= 1
            start_speedY *= -1

        if rect_ball.x < rect_player.x - collision_correction_for_straight_mov and rect_ball.y > rect_player.y:
            start_speedY *= 1
            start_speedX *= -1
        if rect_ball.x > rect_player.x + collision_correction_for_straight_mov and rect_ball.x < rect_player.x + collision_correction_for_straight_mov and rect_ball.y > rect_player.y:
            start_speedX *= 0
            start_speedY *= 1
        if rect_ball.x > rect_player.x + collision_correction_for_straight_mov and rect_ball.y > rect_player.y:
            start_speedX *= 1
            start_speedY *= 1

        if rect_ball.x > rect_player.x and rect_ball.y > rect_player.y - collision_correction_for_straight_mov and rect_ball.y < rect_player.y + collision_correction_for_straight_mov:
            start_speedY *= 0
            start_speedX *= 1
        if rect_ball.x < rect_player.x and rect_ball.y > rect_player.y - collision_correction_for_straight_mov and rect_ball.y < rect_player.y + collision_correction_for_straight_mov:
            start_speedY *= 0
            start_speedX *= 1
        if rect_ball.y > rect_player.y and rect_ball.x > rect_player.x - collision_correction_for_straight_mov and rect_ball.x < rect_player.x + collision_correction_for_straight_mov:
            start_speedY *= 1
            start_speedX *= 0

    if collision(rect_ordi, rect_ball):
        start_speedX = ballX_speed
        start_speedY = ballY_speed
        ordi_cursorX = int(window_width / 2)
        racket_noise2.play()
        if rect_ball.x < rect_ordi.x - collision_correction_for_straight_mov and rect_ball.y > rect_ordi.y:
            start_speedY *= 1
            start_speedX *= -1

        if rect_ball.x > rect_ordi.x - collision_correction_for_straight_mov and rect_ball.x < rect_ordi.x + collision_correction_for_straight_mov and rect_ball.y > rect_player.y:
            start_speedX *= 0
            start_speedY *= 1

        if rect_ball.x > rect_ordi.x + collision_correction_for_straight_mov and rect_ball.y > rect_ordi.y:
            start_speedX *= 1
            start_speedY *= 1

        if rect_ball.x < rect_ordi.x - collision_correction_for_straight_mov and rect_ball.y < rect_ordi.y:
            start_speedY *= -1
            start_speedX *= -1

        if rect_ball.x > rect_ordi.x + collision_correction_for_straight_mov and rect_ball.x < rect_ordi.x + collision_correction_for_straight_mov and rect_ball.y < rect_ordi.y:
            start_speedX *= 0
            start_speedY *= -1

        if rect_ball.x > rect_ordi.x + collision_correction_for_straight_mov and rect_ball.y < rect_ordi.y:
            start_speedX *= -1
            start_speedY *= -1

    if ballX > ordi_cursorX:
        ordi_cursorX += ordi_cursor_speed
    if ballX < ordi_cursorX:
        ordi_cursorX -= ordi_cursor_speed
    if ballY < ordi_cursorY:
        ordi_cursorY -= ordi_cursor_speed
    if ballY > ordi_cursorY:
        ordi_cursorY += ordi_cursor_speed
    if ordi_cursorX < goalXlow:
        ordi_cursorX = goalXlow
    if ordi_cursorX > goalXhigh:
        ordi_cursorX = goalXhigh
    if ordi_cursorY > goalYordi:
        ordi_cursorY = goalYordi

    if player_cursorY <= int(window_height / 2):
        player_cursorY = int(window_height / 2)
    if player_cursorY >= window_height - 65:
        player_cursorY = window_height - 65
    if player_cursorX < 0:
        player_cursorX = 0
    if player_cursorX >= window_width - 65:
        player_cursorX = window_width - 65

    if round_wonJ1 == 5:
        while True:
            window.blit(display_J1_victory, (40, int(window_height / 3)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("PRESS ESCAPE TO QUIT")
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
    if round_wonORDI == 5:
        while True:
            window.blit(display_ORDI_victory, window_width / 2, window_height / 2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("PRESS ESCAPE TO QUIT")
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
    pygame.draw.rect(window, WHITE, (int(window_width / 3) + 20, -20, 300, 80), 1)
    pygame.draw.rect(window, WHITE, (int(window_width / 3) + 20, window_height - 60, 300, 80), 1)
    pygame.draw.aaline(window, WHITE, (0, window_height / 2), (window_width, window_height / 2))
    pygame.draw.circle(window, WHITE, [int(window_width / 2), int(window_height / 2)], 80, 1)
    rect_ball.center = (ballX + 15, ballY + 15)
    rect_ordi.center = (ordi_cursorX + 35, ordi_cursorY + 30)
    pygame.draw.rect(window, BLACK, rect_player, 1)
    pygame.draw.rect(window, BLACK, rect_ball, 1)
    pygame.draw.rect(window, BLACK, rect_ordi, 1)
    window.blit(ordi_cursor, (ordi_cursorX, ordi_cursorY))
    window.blit(ball, (ballX, ballY))
    window.blit(player_cursor, (player_cursorX - 35, player_cursorY - 30))
    window.blit(display_score_player1, (int(score_player1X), int(score_player1Y)))
    window.blit(display_score_ordi, (int(score_ordiX), int(score_ordiY)))
    window.blit(display_timer, (30, 30))
    # update
    clock.tick(60)
    pygame.display.update()
