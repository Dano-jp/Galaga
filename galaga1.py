import pygame
import sys
import random
import math

# --- CONFIGURACIÓN INICIAL ---
width = 1040
height = 740
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga - Lógica Running y Rebote")
clock = pygame.time.Clock()

# --- CARGA DE FONDO ---
try:
    fondo = pygame.image.load("imagenes/fondo.webp").convert()
    fondo = pygame.transform.scale(fondo, (width, height))
except:
    fondo = pygame.Surface((width, height))
    fondo.fill((10, 10, 30))

imagenes_aliens = ["aliens/alien1.jpeg", "aliens/alien2.jpeg"] 

# --- CLASE JUGADOR ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("imagenes/nave.png").convert()
        except:
            self.image = pygame.Surface((60, 60))
            self.image.fill((0, 255, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10

    def update(self, *args): 
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
        if keystate[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 7

# --- CLASE ALIEN ---
class Alien1(pygame.sprite.Sprite):
    def __init__(self, x_relativa, y_final, delay, lado_inicio, ruta_imagen):
        super().__init__()
        try:
            self.image = pygame.image.load(ruta_imagen).convert()
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))
            
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        
        self.rect.x = -100 if lado_inicio == "izq" else width + 100
        self.rect.y = height // 2
        
        self.px = float(self.rect.x)
        self.py = float(self.rect.y)
        self.x_relativa = x_relativa
        self.target_y = y_final
        self.delay = delay 
        self.angle = 0 
        self.radio = 200 
        self.estado = "ENTRANDO"

    def update(self, ancla_x):
        if self.delay > 0:
            self.delay -= 1
            return

        if self.estado == "ENTRANDO":
            self.angle += 0.12
            self.radio -= 2.5
            if self.radio < 0: self.radio = 0
            objetivo_x = ancla_x + self.x_relativa
            self.px += (objetivo_x - self.px) * 0.1
            self.py += (self.target_y - self.py) * 0.1
            off_x = math.cos(self.angle) * self.radio
            off_y = math.sin(self.angle) * self.radio
            self.rect.x = int(self.px + off_x)
            self.rect.y = int(self.py + off_y)
            if self.radio <= 0 and abs(objetivo_x - self.px) < 1:
                self.estado = "ALINEADO"
        
        elif self.estado == "ALINEADO":
            self.rect.x = int(ancla_x + self.x_relativa)
            self.rect.y = self.target_y

# --- CONFIGURACIÓN DE FORMACIÓN ---
all_sprites = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

columnas = 10
filas = 5 
separacion_x = 80
separacion_y = 60

ancho_bloque = (columnas - 1) * separacion_x
ancla_x = (width - ancho_bloque) // 2

for f in range(filas):
    foto = imagenes_aliens[f % len(imagenes_aliens)]
    lado = "izq" if f % 2 == 0 else "der"
    delay_fila = f * 90
    for c in range(columnas):
        x_rel = c * separacion_x
        y_dest = 80 + (f * separacion_y)
        delay_total = delay_fila + (c * 10)
        alien = Alien1(x_rel, y_dest, delay_total, lado, foto)
        all_sprites.add(alien)
        alien_group.add(alien)

# --- BUCLE PRINCIPAL ---
direccion = 1
velocidad = 3

# AQUÍ ESTÁ EL RUNNING (Punto 1)
running = False 
juego_activo = True 

while juego_activo:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego_activo = False

    # AQUÍ ESTÁ EL IF PARA VERIFICAR LAS 5 HILERAS (Punto 2)
    if not running:
        # 'all' revisa que todos los aliens estén en estado "ALINEADO"
        if all(a.estado == "ALINEADO" for a in alien_group):
            running = True

    # AQUÍ ESTÁ EL MOVIMIENTO Y EL REBOTE IZQUIERDA/DERECHA (Punto 3)
    if running:
        ancla_x += velocidad * direccion

        # Sensor de choque
        choque_borde = False
        for a in alien_group:
            # Si toca la derecha (width), cambia direccion a -1 (izquierda)
            if a.rect.right >= width - 10:
                direccion = -1
                choque_borde = True
                break
            # Si toca la izquierda (0), cambia direccion a 1 (derecha)
            if a.rect.left <= 10:
                direccion = 1
                choque_borde = True
                break
        
        if choque_borde:
            # Empujoncito para evitar que se quede pegado al rebotar
            ancla_x += (velocidad + 1) * direccion

    all_sprites.update(ancla_x)
    screen.blit(fondo, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()