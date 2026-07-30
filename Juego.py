import pygame
from pygame.locals import *
import sys
import random , time
import math


pygame.init()
FPS = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_ANCHO = 1366
SCREEN_ALTO = 768
MARGEN_INFERIOR = 40


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)
you_win = font.render("You Win!", True, GREEN)

texto=game_over.get_rect()
texto.center=(SCREEN_ANCHO/2,SCREEN_ALTO/2)


DISPLAYSURF = pygame.display.set_mode((SCREEN_ANCHO,SCREEN_ALTO))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


background = pygame.image.load("IMAGENES/fondo1.png").convert()
background = pygame.transform.scale(background, (SCREEN_ANCHO, SCREEN_ALTO))

juego_pausado = False
juego_ganado = False
juego_perdido = False


balas_maximas = 10
balas_restantes = 10


boton_pausa_rect = pygame.Rect(1200, 20, 130, 40)

class Mira:
    def __init__(self, origen_x, origen_y, longitud=100):
        self.origen_x = origen_x
        self.origen_y = origen_y
        self.longitud = longitud
        self.angulo = 30  
        self.num_puntos = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            self.angulo += 1.5
        if keys[K_DOWN] or keys[K_s]:
            self.angulo -= 1.5

        self.angulo = max(0, min(self.angulo, 85))

    def draw(self, superficie):
        rad = math.radians(self.angulo)

        fin_x = self.origen_x + self.longitud * math.cos(rad)
        fin_y = self.origen_y - self.longitud * math.sin(rad)

        for i in range(1, self.num_puntos + 1):
            factor = i / self.num_puntos
            px = self.origen_x + (fin_x - self.origen_x) * factor
            py = self.origen_y + (fin_y - self.origen_y) * factor
            pygame.draw.circle(superficie, WHITE, (int(px), int(py)), 3)

class meteor(pygame.sprite.Sprite):
      def __init__(self, tamano=30):
        super().__init__() 
        self.image = pygame.image.load("IMAGENES/meteoro.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamano, tamano))
        self.rect = self.image.get_rect()
        pos_x = random.randint(100, SCREEN_ANCHO + 400)
        pos_y = random.randint(-400, -20)
        self.rect.center = (pos_x, pos_y)
        self.asignar_velocidad()

      def asignar_velocidad(self):
          self.speed_y = random.randint(6, 12)
          self.speed_x = - (self.speed_y *0.8)
 
      def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if (self.rect.bottom > SCREEN_ALTO or self.rect.right < 0):
            pos_x = random.randint(100, SCREEN_ANCHO +400)
            pos_y = random.randint(-200, -20)
            self.rect.center = (pos_x,pos_y)

            self.asignar_velocidad()

class Cazador(pygame.sprite.Sprite):
    def __init__(self, alto=60):
        super().__init__() 

        try:
            hoja_cazador = pygame.image.load("IMAGENES/cazador.png").convert_alpha()
            ancho_hoja = hoja_cazador.get_width()
            alto_hoja = hoja_cazador.get_height()
            ancho_un_cazador = ancho_hoja // 4
            cazador_solo = hoja_cazador.subsurface((0, 0, ancho_un_cazador, alto_hoja))
            proporcion = ancho_un_cazador / alto_hoja
            nuevo_ancho = int(alto * proporcion)
            self.image = pygame.transform.scale(cazador_solo, (nuevo_ancho, alto))

        except pygame.error:
            self.image = pygame.Surface((30, alto))
            self.image.fill((0, 255, 0))
            print("Error: No se pudo cargar IMAGENES/cazador.png")

        self.rect = self.image.get_rect()

        self.rect.left = 15  
        self.rect.bottom = SCREEN_ALTO - MARGEN_INFERIOR


    def move(self):
        pass

class Structure(pygame.sprite.Sprite):
    def __init__(self, x, ancho=80, alto=120):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(BLACK)  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = SCREEN_ALTO - MARGEN_INFERIOR
    def move(self):
        pass   

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, estructura, alto=50):
        super().__init__()
        try:
            imagen_original = pygame.image.load("IMAGENES/dino.png").convert_alpha()
        except pygame.error: 
            self.image = pygame.Surface((30, alto))
            self.image.fill((0, 150, 0))
            self.rect = self.image.get_rect()
            self.rect.bottom = estructura.rect.top
            self.rect.centerx= estructura.rect.centerx
            print("Error cargando dino.png")
            return

        ancho_orig = imagen_original.get_width()
        alto_orig = imagen_original.get_height()
        proporcion = ancho_orig / alto_orig 
        nuevo_ancho = int(alto * proporcion)

        imagen_escalada = pygame.transform.scale(imagen_original, (nuevo_ancho, alto))
        self.image = pygame.transform.flip(imagen_escalada, True, False)
        self.rect = self.image.get_rect()

        self.rect.bottom = estructura.rect.top
        self.rect.centerx = estructura.rect.centerx
        

    def move(self):
        pass


class Barra:
    def __init__(self, x=15, y=600, ancho=120, alto=12):
        self.rect_borde = pygame.Rect(x, y, ancho, alto)
        self.potencia = 0         
        self.cargando = False
        self.velocidad_carga = 1.5  

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_SPACE]:
            self.cargando = True
        
            if self.potencia < 100:
                self.potencia += self.velocidad_carga
                if self.potencia > 100:
                    self.potencia = 100
        else:
            self.cargando = False

    def reset(self):
        self.potencia = 0

    def draw(self, superficie):
        if self.cargando:
            pygame.draw.rect(superficie, WHITE, self.rect_borde, 2, border_radius=3)
            
            ancho_relleno = int((self.potencia / 100) * (self.rect_borde.width - 4))
            if ancho_relleno > 0:
                rect_relleno = pygame.Rect(
                    self.rect_borde.x + 2,
                    self.rect_borde.y + 2,
                    ancho_relleno,
                    self.rect_borde.height - 4
                )
                pygame.draw.rect(superficie, WHITE, rect_relleno, border_radius=2)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, potencia):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        
        velocidad_base = (potencia / 100) * 30
        rad = math.radians(angulo)
        
        self.vel_x = velocidad_base * math.cos(rad)
        self.vel_y = -velocidad_base * math.sin(rad)
        self.gravedad = 0.45 

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.prev_x = self.pos_x
        self.prev_y = self.pos_y

    def move(self):

        self.prev_x = self.pos_x
        self.prev_y = self.pos_y

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.vel_y += self.gravedad  

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)


        if (self.rect.left > SCREEN_ANCHO or 
            self.rect.top > SCREEN_ALTO or 
            self.rect.right < 0 or 
            self.rect.bottom >= SCREEN_ALTO - MARGEN_INFERIOR):
            self.kill()

    def Rebote(self, estructura):
        
        factor_rebote = 0.7

        rect_prev_x = pygame.Rect(int(self.prev_x), self.rect.y, self.rect.width, self.rect.height)
        rect_prev_y = pygame.Rect(self.rect.x, int(self.prev_y), self.rect.width, self.rect.height)

        if not rect_prev_y.colliderect(estructura.rect):
            self.vel_y = -self.vel_y * factor_rebote
            if self.prev_y < estructura.rect.top:
                self.rect.bottom = estructura.rect.top
            else:
                self.rect.top = estructura.rect.bottom
            self.pos_y = float(self.rect.y)

        elif not rect_prev_x.colliderect(estructura.rect):
            self.vel_x = -self.vel_x * factor_rebote
            if self.prev_x < estructura.rect.left:
                self.rect.right = estructura.rect.left
            else:
                self.rect.left = estructura.rect.right
            self.pos_x = float(self.rect.x)
        else:
            self.vel_x = -self.vel_x * factor_rebote
            self.vel_y = -self.vel_y * factor_rebote



    
         
barra_potencia = Barra(x=15, y=580, ancho=120, alto=12)


all_sprites = pygame.sprite.Group()
meteoros = pygame.sprite.Group()
enemies = pygame.sprite.Group()       
estructuras = pygame.sprite.Group()
disparo = pygame.sprite.Group()


for _ in range(6):
    m = meteor(tamano=20)
    meteoros.add(m)
    all_sprites.add(m)


est1 = Structure(x=970, ancho=70, alto=100)
est2 = Structure(x=1070, ancho=60, alto=70)
est3 = Structure(x=1200, ancho=75, alto=130)

estructuras.add(est1, est2, est3)
all_sprites.add(est1, est2, est3)

dino1 = Dinosaur(estructura=est1, alto=60)   
dino2 = Dinosaur(estructura=est2, alto=60)   
dino3 = Dinosaur(estructura=est3, alto=60)


enemies.add(dino1, dino2, dino3)
all_sprites.add(dino1, dino2, dino3)

C1= Cazador(alto=60)
all_sprites.add(C1)

apuntador = Mira(origen_x=C1.rect.right - 10, origen_y=C1.rect.centery - 5, longitud=100)

while True:
      for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if boton_pausa_rect.collidepoint(event.pos):
                    juego_pausado = not juego_pausado


        if event.type == KEYDOWN:
            if event.key == K_p:
                juego_pausado = not juego_pausado


        if event.type == KEYUP and not juego_pausado and not juego_perdido and not juego_ganado:
            if event.key == K_SPACE and barra_potencia.potencia > 0 and balas_restantes > 0:
                bala = Proyectil(
                    x=apuntador.origen_x,
                    y=apuntador.origen_y,
                    angulo=apuntador.angulo,
                    potencia=barra_potencia.potencia
                )
                disparo.add(bala)
                all_sprites.add(bala)
                barra_potencia.reset()
                balas_restantes -= 1

      if not juego_pausado and not juego_ganado and not juego_perdido:
        for entity in all_sprites:
            entity.move()

        apuntador.update()
        barra_potencia.update()

        pygame.sprite.groupcollide(disparo , enemies, True, True)

        colisiones_estructuras = pygame.sprite.groupcollide(disparo, estructuras, False, False)
        
        for bala, lista_estructuras in colisiones_estructuras.items():
            for est in lista_estructuras:
                bala.Rebote(est)


        if len(enemies) == 0:
            juego_ganado = True
        elif balas_restantes == 0 and len(disparo) == 0:
            juego_perdido = True   



      DISPLAYSURF.blit(background, (0, 0))
      pygame.draw.rect(DISPLAYSURF, (35,18,5),(0, SCREEN_ALTO - MARGEN_INFERIOR, SCREEN_ANCHO, MARGEN_INFERIOR))


      for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

      color_btn = (200, 100, 0) if juego_pausado else (0, 150, 0)
      pygame.draw.rect(DISPLAYSURF, color_btn, boton_pausa_rect, border_radius=8)

      txt_btn = font_small.render("REANUDAR" if juego_pausado else "PAUSA", True, WHITE)
      txt_rect = txt_btn.get_rect(center=boton_pausa_rect.center)
      DISPLAYSURF.blit(txt_btn, txt_rect)

      texto_balas = font_small.render(f"Balas: {balas_restantes}/{balas_maximas}", True, WHITE)
      DISPLAYSURF.blit(texto_balas, (20, 20))



      if juego_pausado:
        aviso_pausa = font.render("JUEGO EN PAUSA", True, WHITE)
        aviso_rect = aviso_pausa.get_rect(center=(SCREEN_ANCHO / 2, SCREEN_ALTO / 2))
        DISPLAYSURF.blit(aviso_pausa, aviso_rect)

      if juego_ganado:
        win_rect = you_win.get_rect(center=(SCREEN_ANCHO / 2, SCREEN_ALTO / 2))
        DISPLAYSURF.blit(you_win, win_rect)

      if juego_perdido:
          game_over_rect = game_over.get_rect(center=(SCREEN_ANCHO / 2, SCREEN_ALTO / 2))
          DISPLAYSURF.blit(game_over, game_over_rect)

      if not juego_perdido and not juego_ganado:
        apuntador.draw(DISPLAYSURF)
        barra_potencia.draw(DISPLAYSURF)
    

      
      pygame.display.update()

 
      FPS.tick(60)