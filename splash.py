import pygame, sys, time

pygame.init()

#musique
pygame.mixer.music.load("assets/audio/opening_theme.ogg")

# arrière plan
background = pygame.image.load('assets/splash_background.png')
title = pygame.image.load('assets/titre.png')
title = pygame.transform.scale(title, (416, 192))
police = pygame.font.Font("assets/kongtext.ttf",18)
text = police.render("-PRESS 'SPACE' TO START-",1,(200,40,120))

#générer fenêtre de jeu
pygame.display.set_caption("F-MAX")
pygame.display.set_icon(pygame.image.load("assets/icon_32.png"))
screen=pygame.display.set_mode((500, 800))
running=True
i=0
pygame.mixer.music.play(-1)
while running:
    screen.blit(background, (0,0))
    screen.blit(title, (42,200))
    i+=1
    if i<35 :
        screen.blit(text, (30,440))
    elif i==50:
        i=0
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            key_pressed= pygame.key.get_pressed()
            if key_pressed[pygame.K_SPACE]:
                jeu=True
                running=False
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            jeu=False
            running = False
    time.sleep(0.017)

if jeu ==True:
    import main


