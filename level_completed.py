import pygame
import sys
import sqlite3
from random import randint

FPS = 50
size = width, height = 500, 500


def terminate():
    pygame.quit()
    sys.exit()


def level_completed(money, time, current_player, level):
    score = money * 6000 // time
    con = sqlite3.connect("data/login_db.db")
    player_id = con.cursor().execute(
        f"""SELECT id from users
        WHERE name = '{current_player}'""").fetchone()[0]

    max_score = con.cursor().execute(
        f"""SELECT score FROM levels
            WHERE id = {player_id} AND level={level}""").fetchone()
    if max_score is None:
        con.cursor().execute(
            f"""INSERT INTO levels VALUES ({player_id}, {level}, {score}) """)
        con.commit()
        max_score = (0,)
    max_score = max_score[0]
    if max_score < score:
        con.cursor().execute(
            f"""UPDATE levels
                SET score = {score}
                WHERE id = {player_id} AND level={level}""")
        con.commit()

    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 105 <= event.pos[0] <= 405 and 300 <= event.pos[1] <= 350:
                    return
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.Color(50, 50, 230), (105, 300, 300, 50), 0)
        font = pygame.font.Font('data/icons/GorgeousPixel.ttf', 56)
        text = font.render('Level completed!', True,
                           (randint(0, 255), randint(0, 255), randint(0, 255)))
        text_x = 20
        text_y = 100
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 40)
        text_money = font.render(f"Money: {money}", True, (173, 216, 230))
        screen.blit(text_money, (105, 170))

        text_time = font.render("Time: %02d:%02d" % ((time // 1000) // 60, (time // 1000) % 60),
                                True, (173, 216, 230))
        screen.blit(text_time, (105, 210))

        if score > max_score:
            record = font.render(f"РЕКОРД! ", True,
                                 (randint(0, 255), randint(0, 255), randint(0, 255)))
            screen.blit(record, (300, 250))
        text_total = font.render(f"Total: {score}", True, (173, 216, 230))
        screen.blit(text_total, (105, 250))

        font = pygame.font.Font(None, 30)
        text1 = font.render('Continue', True, (173, 216, 230))
        text1_x = 210
        text1_y = 315
        screen.blit(text1, (text1_x, text1_y))
        pygame.display.flip()


