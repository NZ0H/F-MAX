import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    """
    Attributs de classe:
        sprites: list (pygame.Surface) | images des objets
        sprites_destroyed: list (pygame.Surface) | images des objets détruits
        masks: list (pygame.mask.Mask) | masques de collision des objets
    Attributs:
        x:  int | position du centre du vaisseau en x
        y: int | position du centre du vaisseau en y
        sorti: bool | True si le vaisseau est sorti de l'écran
        sprite_type: str | couleur du vaisseau
        image: pygame.Surface | image actuelle du vaisseau
        L: int | largeur de l'image du vaisseau
        H: int | hauteur de l'image du vaisseau
        offX: int | décalage horizontal entre le centre et le coin haut-gauche de l'image
        offY: int | décalage vertical entre le centre et le coin haut-gauche de l'image
        rect: pygame.Rect | rectangle de collision du vaisseau
    Méthodes:
        __init__(p_x): constructeur de la classe. position horizontale d'origine de l'objet. ne renvoie rien
        move(vpiste): déplace l'objet. vitesse actuelle de la piste. ne renvoie rien
        draw(fenetre): dessine l'objet. surface sur laquelle dessiner l'objet. ne renvoie rien
        exploser(): rend l'objet hors d'état. aucun argument. ne renvoie rien
    """
    # les images sont chargées à l'avance pour éviter les ralentissements pendant la partie
    sprites = {"caisse":pygame.image.load("assets/caisse.png"),"cone":pygame.image.load("assets/cones.png")}
    sprites_destroyed = {"caisse":pygame.image.load("assets/caisse_destroyed.png"),"cone":pygame.image.load("assets/cones_destroyed.png")}
    masks = {"caisse":pygame.mask.from_surface(sprites["caisse"]),"cone":pygame.mask.from_surface(sprites["cone"])}
    def __init__(self,p_x):
        self.x= p_x
        self.y= 0
        self.sorti=False

        #graphismes
        pygame.sprite.Sprite.__init__(self)
        self.sprite_type=random.choice(["caisse","cone"])
        self.image = self.sprites[self.sprite_type]
        self.mask = self.masks[self.sprite_type]
        L = self.image.get_width()
        H = self.image.get_height()
        #offset pour dessiner le sprite centré sur la position
        self.offX = L//2
        self.offY = H//2

    def move(self,v_piste):
        self.y+= v_piste
        if self.y>800:
            self.sorti=True
        
        self.rect = self.image.get_rect(topleft = (self.x-self.offX,self.y-self.offY))

    def draw(self,fenetre):
        fenetre.blit(self.image, (self.x-self.offX,self.y-self.offY))

    def exploser(self):
        self.image=self.sprites_destroyed[self.sprite_type]


