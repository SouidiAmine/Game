import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
import time
import os

from sound import *
from pathfinding import *


class Game:


    def __init__(self,RES):


        self.start_time = pg.time.get_ticks()
        pg.init()

        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)

        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

        self.font = pg.font.Font(None, 36)


    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        #self.object_handler = ObjectHandler(self)
        #self.weapon = Weapon(self)
        #self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        #pg.mixer.music.plwwwwwwdddday(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        #self.object_handler.update()
        #self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)


        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        pg.display.set_caption(f'{7 - elapsed_time :.1f}' + '  Player 2')
        if elapsed_time >= 7:
            f = open("mon_fichier.txt", "r")
            contenu = f.read()

            chiffres = contenu.split(',')
            score = int(chiffres[1])

            f.close()

            with open("mon_fichier.txt", "w") as fichier:



                print("distance reste " +str(Map.find_shortest_distance((int(self.player.y), int(self.player.x)))))
                #print("score = "+str(score))
                fichier.write("1,"+str(Map.find_shortest_distance((int(self.player.y),int(self.player.x)))-int(score)))
                fichier.close()
            #print(Map.find_shortest_distance((int(self.player.y),int(self.player.x))))
            #print(Map.find_shortest_distance((int(self.player.y),int(self.player.x))))
            self.pause_game(str(int(score)-Map.find_shortest_distance((int(self.player.y),int(self.player.x)))))
        if Map.find_shortest_distance((int(self.player.y), int(self.player.x))) < 4 :
            print("time rest "+str(7-elapsed_time))
            self.winner(elapsed_time)

    def pause_game(self,score):
        if os.stat("winner.txt").st_size != 0:
            with open("winner.txt", "w") as fichier:
                fichier.write("winner")

                fichier.close()
                loser_screen()

        # Afficher un message indiquant que le jeu est en pause
        pause_text = self.font.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(pause_text, (
        500 / 2 - pause_text.get_width() / 2, 500 / 2 - pause_text.get_height() / 2))

        font2 = pg.font.Font(None, 50)
        text2 = font2.render("Your Score : " + score, True, (0, 255, 0))
        font3 = pg.font.Font(None, 30)
        text3 = font3.render("press k To Continue ", True, (255, 0, 0))

        text_rect2 = text2.get_rect()
        text_rect2.center = (220, 50)

        text_rect3 = text3.get_rect()
        text_rect3.center = (400, 480)

        self.screen.blit(text2, text_rect2)
        self.screen.blit(text3, text_rect3)

        pg.display.update()


        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    f = open("mon_fichier.txt", "r")
                    contenu = f.read()

                    chiffres = contenu.split(',')


                    f.close()
                    if event.key == pg.K_k :
                        if os.stat("mon_fichier.txt").st_size != 0:
                            if int(chiffres[0]) == 2 :
                                self.start_time = pg.time.get_ticks()
                        return


    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()

        #self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            #self.player.single_fire_event(event)

    def run(self):

        while True:
            self.check_events()
            self.update()
            self.draw()
    def winner(self,time_Reste):
        if os.stat("winner.txt").st_size == 0:
            with open("winner.txt", "a") as fichier:
                fichier.write("Loser")
                print("winner")
                fichier.close()
                winner_screen()

        if os.stat("winner.txt").st_size != 0:
            with open("winner.txt", "r+") as fichier:
                content = fichier.read()
                fichier.close()
                if (time_Reste > int(float(content)*1000)):
                    fichier.write("Loser")
                    winner_screen()
                    fichier.close()
                if (time_Reste == int(float(content)*1000)):
                    fichier.write("Winner")
                    winner_screen()
                    fichier.close()
                if (time_Reste < int(float(content)*1000)):
                    fichier.write("Winner")
                    loser_screen()
                    fichier.close()





def winner_screen():
    pg.init()
    pg.display.set_caption("Player 1 you Win the game")
    screen = pg.display.set_mode((500, 500))


    background = pg.image.load('resources\\textures\\winner.png').convert()

    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                start_screen()

                return

        #screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        pg.display.update()


def loser_screen():
    pg.init()
    pg.display.set_caption("Player 2 you lost the game")
    screen = pg.display.set_mode((500, 500))


    background = pg.image.load('resources\\textures\\game__over.png').convert()

    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                start_screen()

                return

        #screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        pg.display.update()




def start_screen():
    pg.init()
    pg.display.set_caption("Lancement de jeu")
    screen = pg.display.set_mode((500, 500))

    font = pg.font.Font(None, 36)
    text = font.render("To Start press S", True, (255, 0, 255))
    text_rect = text.get_rect()
    text_rect.center = (500 // 2, 500 // 2)

    font2 = pg.font.Font(None, 60)
    text2 = font2.render("Player 2", True, (153, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.center = (240, 35)

    background = pg.image.load('resources\\textures\\4.png').convert()

    while True:
        for event in pg.event.get():
            f = open("mon_fichier.txt", "r")
            contenu = f.read()

            chiffres = contenu.split(',')
            score = int(chiffres[1])
            #print("first s = "+str(score ))

            f.close()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                print(int(chiffres[0]))
                chiffre = int(chiffres[0])
                if (chiffre== 2):
                    return

        #screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        pg.display.update()

if __name__ == '__main__':
    pg.init()
    score = 0
    screen = pg.display.set_mode((500, 500))
    font = pg.font.Font(None, 36)
    start_screen()
    game = Game((500, 500))
    game.run()
    """
    key = False
    while key == False:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    key = True
    game.run()
    """