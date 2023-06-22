import pygame, sys
import time
from random import randint
from pygame.locals import *

# classes
from class_joueur import Joueur
from class_obstacle import Obstacle
from class_concurrent import Concurrent
from class_gui import GUI # interface

def dessiner(score,i):
    """dessiner le fond"""
    gui.background(fenetre,i)

    """dessiner les objets"""
    for o in obstacles+concurrents:
        o.draw(fenetre)
    player.draw(fenetre)

    """dessiner l'interface"""
    gui.draw(fenetre,player.energie,int(score))

    """détruire les objets qui sont sortis de l'écran"""
    clear()

    pygame.display.update()
    clock.tick(60)

def creer_obstacle():
    p_x=randint(110,390) # marge des bords de l'écran
    obstacles.append(Obstacle(p_x))

def creer_concurrent():
    p_x=randint(110,390) # marge des bords de l'écran
    concurrents.append(Concurrent(p_x,7))

def clear():
    global obstacles,concurrents
    obstacles = [i for i in obstacles if not i.sorti]
    concurrents = [i for i in concurrents if not i.sorti]

def game_over(v_piste,i):
    # version tronquée de la boucle while principale
    # les commentaires sont là-bas
    pygame.mixer.music.stop()
    f_v_piste = v_piste
    player.exploser()
    running = 250 # décompte avant de passer à l'écran de fin
    while running:
        running -= 1
        f_v_piste *= 0.98
        v_piste = int(f_v_piste)
        i=(i+v_piste)%64
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for o in obstacles+concurrents:
            o.move(v_piste)

        # joueur/obstacle
        for o in obstacles:
            if pygame.sprite.collide_mask(player, o):
                o.exploser()
                
        for c in concurrents:
            for o in obstacles:
                if pygame.sprite.collide_mask(c, o):
                    c.collision()
                    o.exploser()

        dessiner(score,i)

""" pygame """
ecran = 500, 800
pygame.init()
fenetre = pygame.display.set_mode(ecran)
clock = pygame.time.Clock() #limiteur de fps

""" musique/sons """
pygame.mixer.music.load("assets/audio/big_blue.ogg")
pygame.mixer.music.play(-1)
son_explosion = pygame.mixer.Sound('assets/audio/explosion.ogg')

gui = GUI()
obstacles = []
concurrents = []
v_piste = 10
player = Joueur(4,2,ecran) #v_lat, v_ver
i = 0

dec_obstacles=80
dec_concurents=150

score=0

running = True
while running:
    i=(i+v_piste)%64 #décalage fond piste
    score+=0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    """créer des obstacles/concurrents"""
    dec_obstacles-=1
    dec_concurents-=1
    if dec_obstacles ==0:
        creer_obstacle()
        dec_obstacles=randint(20,60)
    if dec_concurents==0:
        creer_concurrent()
        dec_concurents=randint(80,180)

    """faire bouger les objets"""
    player.move(pygame.key.get_pressed())

    for o in obstacles+concurrents:
            o.move(v_piste)

    """collisions"""
    # joueur/obstacle
    for o in obstacles:
        if pygame.sprite.collide_mask(player, o):
            player.collision()
            o.exploser()
            score-=2

    # joueur/concurrent
    for o in concurrents:
        if pygame.sprite.collide_mask(player, o):
            player.collision()
            o.collision()
            score-=5

    # concurrent/obstacle
    for c in concurrents:
        for o in obstacles:
            if pygame.sprite.collide_mask(c, o):
                c.collision()
                o.exploser()

    dessiner(score,i)

    if player.get_game_over():
        running = False
        son_explosion.play()
        game_over(v_piste,i)


""" highscores """
def entrer_nom():
    header = pygame.font.Font("assets/kongtext.ttf", 36).render("YOUR NAME:", 1, (50,180,255))
    fenetre.blit(header, (70, 450))
    background = pygame.Rect(0, 500, 500, 300)
    cara = 0 # compter le caractère en cours
    nom = "___"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                son_cancel.play() # éviter de fermer alors qu'il suffit d'entrer le nom
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    son_cancel.play()
                    cara = max(0,cara-1) # empèche d'aller dans les négatifs
                    nom = nom[:cara]+"_"*(3-cara)
                elif event.key == pygame.K_RETURN:
                    son_done.play()
                    #pygame.draw.rect(fenetre, [0,0,0], pygame.Rect(0, 400, 500, 400)) # effacer 
                    return nom
                else:
                    lettre = event.unicode.upper()
                    if lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789" and len(lettre) > 0:
                        # len pour éviter les touches qui ne sont pas des lettres (flèches, shift...)
                        # car les str de longueur 0 renvoie toujours True sur les opérations in
                        if cara < 3:
                            nom = nom[:cara]+lettre+"_"*(2-cara)
                            cara += 1
                            son_ok.play()
                        else:
                            son_cancel.play()
                    elif  len(lettre) > 0: # ne faire de bruit que si c'est un caractère indisponible
                        son_cancel.play()
            
        pygame.draw.rect(fenetre, [0,0,0], background)

        render_nom = pygame.font.Font("assets/kongtext.ttf", 48).render(nom, 1, (10,10,255))
        fenetre.blit(render_nom, (178, 550))
        
        pygame.display.update()
        clock.tick(60)


del player, obstacles, concurrents, gui, dec_concurents, dec_obstacles, v_piste
import json # sauvegarder les données dans un fichier pour les réuitiliser

#son
son_ok = pygame.mixer.Sound('assets/audio/ok.ogg')
son_cancel = pygame.mixer.Sound('assets/audio/cancel.ogg')
son_done = pygame.mixer.Sound('assets/audio/done.ogg')

score = int(score)
with open('data.txt') as json_file:
    data = json.load(json_file)
noms = list(data.keys())
hscores = list(data.values())

#tri à bulles raccourcis pour trois valeurs
for i in 0,1,0:
    if hscores[i]<hscores[i+1]:
        hscores[i],hscores[i+1] = hscores[i+1],hscores[i]
        noms[i],noms[i+1] = noms[i+1],noms[i]

# égaliser ne suffit pas à prendre une place, le premier arrivé est prioritaire
if score > hscores[0]:
    place = 0
    hscores = [score, hscores[0], hscores[1]]
    noms = ["YOU", noms[0], noms[1]]
elif score > hscores[1]:
    place = 1
    hscores = [hscores[0], score, hscores[1]]
    noms = [noms[0], "YOU", noms[1]]
elif score > hscores[2]:
    place = 2
    hscores = [hscores[0], hscores[1], score]
    noms = [noms[0], noms[1], "YOU"]
else:
    place = 3

if place < 3:
    pygame.mixer.music.load("assets/audio/highscore.ogg")
else:
    pygame.mixer.music.load("assets/audio/end.ogg")
pygame.mixer.music.play(-1)



header = pygame.font.Font("assets/kongtext.ttf", 48).render("HIGHSCORES", 1, (255,255,255))
police = pygame.font.Font("assets/kongtext.ttf", 24)

fenetre.fill([0,0,0])
fenetre.blit(header, (10, 50))

if place < 3: # si nouveau highscore
    for nom,val,i in zip(noms,hscores,range(3)):
        if place == i:
            col = (255, 20, 20)
        else:
            col = (255,255,255)
        scoretext = police.render("{0}:{1}".format(nom,int(val)), 1, col)
        fenetre.blit(scoretext, (5, 250+i*50))
    nom = entrer_nom()
    noms[place] = nom

    data = {n:s for n,s in zip(noms,hscores)}
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fenetre.fill([0,0,0])
        fenetre.blit(header, (10, 50))

        for nom,val,i in zip(noms,hscores,range(3)):
            if place == i:
                col = (255, 20, 20)
            else:
                col = (255,255,255)
            scoretext = police.render("{0}:{1}".format(nom,int(val)), 1, col)
            fenetre.blit(scoretext, (5, 250+i*50))
        
        pygame.display.update()
        clock.tick(60)
else:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fenetre.fill([0,0,0])
        fenetre.blit(header, (10, 50))

        for nom,val,i in zip(noms,hscores,range(3)):
            scoretext = police.render("{0}:{1}".format(nom,int(val)), 1, (255,255,255))
            fenetre.blit(scoretext, (5, 250+i*50))
        scoretext = police.render("YOU:{0}".format(score), 1, (255,20,20))
        fenetre.blit(scoretext, (5, 400))
        
        pygame.display.update()
        clock.tick(60)
    
