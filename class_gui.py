import pygame
from colorsys import hsv_to_rgb
class GUI:
    """
    Attributs:
        image: pygame.Surface | image de la piste
        overlay: pygame.Surface | image de l'effet visuel sur la barre d'énergie
        police: pygame.font | police d'écriture du score
    Méthodes:
        __init__(): constructeur de la classe. aucun argument. ne renvoie rien
        background(fenetre,i): dessine la piste. surface sur laquelle dessiner la piste et décalage vertical de la piste. ne renvoie rien
        draw(fenetre,energie): dessine l'interface. surface sur laquelle dessiner l'interrface et energie du joueur. ne renvoie rien
    """
    def __init__(self):
        self.image = pygame.image.load("assets/piste.png")
        self.overlay = pygame.image.load("assets/overlay.png")
        self.police = pygame.font.Font("assets/kongtext.ttf", 24)

    def background(self,fenetre,i):
        fenetre.blit(self.image, (0,i-32))

    def draw(self,fenetre,energie,score):
        #bordures
        pygame.draw.rect(fenetre,[0,0,0],(0,0,500,35)) # haut
        pygame.draw.rect(fenetre,[0,0,0],(0,765,500,35)) # bas

        # score
        scoretext = self.police.render("Score:{0}".format(int(score)), 1, (255,255,255))
        fenetre.blit(scoretext, (5, 5))
        
        # barre energie
        energie = max(0,energie) # éviter les valeur impossibles
        rempli = round((energie/100)*500)
        couleur = [int(i*255) for i in hsv_to_rgb(rempli/1000,1,1)]
        pygame.draw.rect(fenetre,couleur,(0,765,rempli,35))        
        fenetre.blit(self.overlay, (0,765))
