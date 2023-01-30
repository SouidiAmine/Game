import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
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
        pg.display.set_caption(f'{7-elapsed_time :.1f}'+'  Player 1')



        """text2 = font.render("Score : ", True, (255,255, 0))
        text_rect2 = text2.get_rect()
        text_rect2.center = (100, 20)

        self.screen.blit(text2, text_rect2)"""
        if elapsed_time >= 7:
            with open("mon_fichier.txt", "w") as fichier:
                fichier.write("2,"+str(Map.find_shortest_distance((int(self.player.y),int(self.player.x)))))
                fichier.close()
            print(Map.find_shortest_distance((int(self.player.y),int(self.player.x))))
            #print(self.player.x, self.player.y)
            self.pause_game()
        if Map.find_shortest_distance((int(self.player.y), int(self.player.x))) < 4 :

            self.winner(elapsed_time) #si player 1 attiend le but



    def winner(self,time_Reste):
        if os.stat("winner.txt").st_size == 0:
            with open("winner.txt", "a") as fichier:
                fichier.write(str(time_Reste))

                fichier.close()





    def pause_game(self):
        i = 0

        # Afficher un message indiquant que le jeu est en pause
        pause_text = self.font.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(pause_text, (
        500 / 2 - pause_text.get_width() / 2, 500 / 2 - pause_text.get_height() / 2))
        pg.display.update()
        i = 0 #contrle de score





        while True:
            """text2 = font.render("Score : 22", True, (0, 255, 0))



            text2 = font.render("Score : "+str(i), True, (0, 255, 0))
            i = i+1
            text_rect2 = text2.get_rect()
            text_rect2.center = (100, 20)
            self.screen.blit(text2, text_rect2)
            pg.display.update()"""
            f = open("mon_fichier.txt", "r")
            contenu = f.read()

            chiffres = contenu.split(',')

            f.close()

            if os.stat("winner.txt").st_size != 0:
                f = open("winner.txt", "r")
                contenu = f.read()
                f.close()
                if contenu == "Loser" :
                    loser_screen()
                if contenu == "winner":
                    winner_screen()



            if chiffres[0] == '1' :
                if i == 0 :
                    print(chiffres[1])
                    font2 = pg.font.Font(None, 50)
                    text2 = font2.render("Your Score : "+ chiffres[1], True, (0, 255, 0))
                    font3 = pg.font.Font(None, 30)
                    text3 = font3.render("press k To Continue ", True, (255, 0, 0))


                    text_rect2 = text2.get_rect()
                    text_rect2.center = (220, 50)

                    text_rect3 = text3.get_rect()
                    text_rect3.center = (400, 480)

                    self.screen.blit(text2, text_rect2)
                    self.screen.blit(text3, text_rect3)
                    pg.display.update()
                    i = i +1

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:

                    print("chifre de pause  =  "+chiffres[0])
                    if event.key == pg.K_k  :
                        if int(chiffres[0]) == 1 :
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
    pg.display.set_caption("Player 1 you lost the game")
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
    text = font.render("To Start press S", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (500 // 2, 500 // 2)

    font2 = pg.font.Font(None, 60)
    text2 = font2.render("Player 1", True, (153, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.center = (240, 35)



    background = pg.image.load('resources\\textures\\4.png').convert()



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    return

        #screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)

        pg.display.update()

if __name__ == '__main__':
    pg.init()
    f = open("winner.txt", "w")

    f.close()


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