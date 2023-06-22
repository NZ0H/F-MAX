import pygame
class Joueur(pygame.sprite.Sprite):
    """
    Attributs:
        v_lat: int | vitesse horizontale
        v_ver: int | vitesse verticale
        energie: int | points de vie du vaisseau
        x:  int | position du centre du vaisseau en x
        y: int | position du centre du vaisseau en y
        largeur: int | largeur du rectangle de mouvement
        hauteur: int | hauteur du rectangle de mouvement (limites par rapport aux bords de la piste)
        lim_h, lim_b, lim_g, lim_d: int | positions des limites de la piste
        images: list (pygame.Surface) | liste des images pour les différents mouvements
        image: pygame.Surface | image actuelle
        masks: list (pygame.mask.Mask) | liste des masques de collision pour les différents mouvements
        mask: pygame.mask.Mask | masque de collision actuel
        rect: pygame.Rect | rectangle de collision du vaisseau
        mouv_ancien: int | type de mouvment à l'image précédente
        L: int | largeur de l'image du vaisseau
        H: int | hauteur de l'image du vaisseau
        offX: int | décalage horizontal entre le centre et le coin haut-gauche de l'image
        offY: int | décalage vertical entre le centre et le coin haut-gauche de l'image
        son_degat: pygame.mixer.Sound | son joué quand le joueur perd de l'énergie
    Méthodes:
        __init__(position_x,v_lat,v_ver,t_ecran): constructeur de la classe. vitesse horizontale, vitesse verticale, et taille de la fenetre. ne renvoie rien
        move(touches): déplace le vaisseau. liste des touches enfoncées. ne renvoie rien
        draw(fenetre): dessine le vaisseau. surface sur laquelle dessiner le vaisseau. ne renvoie rien
        exploser(): rend le vaisseau hors d'état. aucun argument. ne renvoie rien
        collision(): réduit l'énergie restante. aucun argument. ne renvoie rien
        get_game_over(): aucun argument. renvoie un bool: True si le vaisseau n'a plus d'énergie
        bruit(): joue un son de dégats. aucun argument. ne renvoie rien.
    """
    def __init__(self,v_lat,v_ver,t_ecran):
        self.v_lat = v_lat
        self.v_ver = v_ver
        self.energie = 100
        self.x = t_ecran[0]/2
        self.y = t_ecran[1]-100

        self.largeur = 44
        self.hauteur = 56

        #limites haut bas gauche droite de l'écran
        self.lim_h = self.hauteur/2 + 35 # 35 pixels pour score en haut et pv en bas
        self.lim_b = t_ecran[1]-self.lim_h
        self.lim_g = 50+self.largeur/2 # 50 pixels pour limites gauche/droite
        self.lim_d = t_ecran[0]-self.lim_g

        #graphismes
        pygame.sprite.Sprite.__init__(self)

        # multiples images pour les mouvements gauche/droite
        self.images = [pygame.image.load(i) for i in ("assets/player.png","assets/player_g.png","assets/player_d.png")]
        self.masks = [pygame.mask.from_surface(i) for i in self.images]
        self.mouv_ancien = 1 # on compare à l'état d'avant pour éviter de recharger une image 60 fois par seconde
        
        L = self.images[0].get_width()
        H = self.images[0].get_height()
        #offset pour dessiner le sprite centré sur la position
        self.offX = L//2
        self.offY = H//2

        #son
        pygame.init()
        self.son_degat = pygame.mixer.Sound("assets/audio/damage.ogg")

    def move(self,touches):
        # déterminer le sens des mouvements à partir des flèches
        # si on appuie sur des flèches opposées, les mouvements s'annullent instantanément
        # pas de elif sinon on perdrait ça
        if touches[pygame.K_UP]:
            self.y -= self.v_ver
        if touches[pygame.K_DOWN]:
            self.y += self.v_ver
        if touches[pygame.K_LEFT]:
            self.x -= self.v_lat
        if touches[pygame.K_RIGHT]:
            self.x += self.v_lat

        #empêche de sortir de la zone de jeu
        self.y = max(min(self.lim_b,self.y),self.lim_h)
        self.x = min(max(self.lim_g,self.x),self.lim_d)

        #perdre des pv si le joueur touche le bord de la piste
        distance = min(self.x-self.lim_g,self.lim_d-self.x)
        if distance <= 32:
            self.energie -= 0.5
            self.bruit()

        #changer d'image si on bouge sur les côtés
        if touches[pygame.K_LEFT] and not touches[pygame.K_RIGHT]:
            mouv = 1
        elif touches[pygame.K_RIGHT] and not touches[pygame.K_LEFT]:
            mouv = 2
        else:
            mouv = 0
        if mouv != self.mouv_ancien:
            self.mouv_ancien = mouv
            self.image = self.images[mouv]
            self.mask = self.masks[mouv]

        self.rect = self.image.get_rect(topleft = (self.x-self.offX,self.y-self.offY))

    def draw(self,fenetre):        
        fenetre.blit(self.image, (self.x-self.offX,self.y-self.offY))

    def collision(self):
        self.energie -= 1
        self.bruit()

    def exploser(self):
        self.image = pygame.image.load("assets/player_destroyed.png")
        L = self.image.get_width()
        H = self.image.get_height()
        self.offX = L//2
        self.offY = H//2

    def get_game_over(self):
        return self.energie <= 0

    def bruit(self):
        if not pygame.mixer.get_busy():
            self.son_degat.play()
