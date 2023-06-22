import pygame
import random

class Concurrent:
    """
    Attributs de classe:
        sprites: list (pygame.Surface) | images des vaisseaux en course
        sprites_destroyed: list (pygame.Surface) | images des vaisseaux détruits
        mask: pygame.mask.Mask | masque de collision du vaisseau
    Attributs:
        energie: int | points de vie du vaisseau
        x:  int | position du centre du vaisseau en x
        y: int | position du centre du vaisseau en y
        sorti: bool | True si le vaisseau est sorti de l'écran
        sprite_type: str | couleur du vaisseau
        image: pygame.Surface | image actuelle du vaisseau
        L: int | largeur de l'image du vaisseau
        H: int | hauteur de l'image du vaisseau
        offX: int | décalage horizontal entre le centre et le coin haut-gauche de l'image
        offY: int | décalage vertical entre le centre et le coin haut-gauche de l'image
        vitesse: int | vitesse du vaisseau
        rect: pygame.Rect | rectangle de collision du vaisseau
    Méthodes:
        __init__(position_x,vitesse): constructeur de la classe. position horizontale d'origine et vitesse du vaisseau. ne renvoie rien
        move(vitesse_piste): déplace le vaisseau. vitesse actuelle de la piste. ne renvoie rien
        draw(fenetre): dessine le vaisseau. surface sur laquelle dessiner le vaisseau. ne renvoie rien
        exploser(): rend le vaisseau hors d'état. aucun argument. ne renvoie rien
        collision(): réduit l'énergie restante. aucun argument. ne renvoie rien
    """
    # les images sont chargées à l'avance pour éviter les ralentissements pendant la partie
    sprites={"rouge": pygame.image.load("assets/concurrent_rouge.png"),"vert":pygame.image.load("assets/concurrent_vert.png")}
    sprites_destroyed={"rouge": pygame.image.load("assets/concurrent_rouge_destroyed.png"),"vert":pygame.image.load("assets/concurrent_vert_destroyed.png")}
    mask = pygame.mask.from_surface(sprites["vert"])
    def __init__(self,position_x,vitesse):
        self.energie = 80
        self.x = position_x
        self.y = 0
        self.sorti=False

        #graphismes
        self.sprite_type = random.choice(["rouge","vert"])
        self.image = self.sprites[self.sprite_type]
        L = self.image.get_width()
        H = self.image.get_height()
        #offset pour dessiner le sprite centré sur la position
        self.offX = L//2
        self.offY = H//2
        self.vitesse=vitesse

    def move(self,vitesse_piste):
        self.y+=vitesse_piste-self.vitesse
        if self.y>1500:
            self.sorti=True
        if self.energie<1:
            self.exploser()

        self.rect = self.image.get_rect(topleft = (self.x-self.offX,self.y-self.offY))
        
    def draw(self,fenetre):        
        fenetre.blit(self.image, (self.x-self.offX,self.y-self.offY))

    def exploser(self):
        self.image = self.sprites_destroyed[self.sprite_type]
        self.vitesse=0

    def collision(self):
        self.energie -= 1
