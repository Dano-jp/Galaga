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
pygame.display.set_caption("Galaga - Formación Sincronizada")
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
        # *args permite recibir ancla_x sin dar error
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
        
        # Inicio fuera de pantalla
        self.rect.x = -100 if lado_inicio == "izq" else width + 100
        self.rect.y = height // 2
        
        self.px = float(self.rect.x)
        self.py = float(self.rect.y)
        
        self.x_relativa = x_relativa # Posición fija en la rejilla
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

            # Su destino es el Ancla (que puede estar quieta o moviéndose) + su X relativa
            objetivo_x = ancla_x + self.x_relativa
            
            self.px += (objetivo_x - self.px) * 0.1
            self.py += (self.target_y - self.py) * 0.1
            
            off_x = math.cos(self.angle) * self.radio
            off_y = math.sin(self.angle) * self.radio
            
            self.rect.x = int(self.px + off_x)
            self.rect.y = int(self.py + off_y)
            
            # Snap: Si ya llegó, se bloquea en modo ALINEADO
            if self.radio <= 0 and abs(objetivo_x - self.px) < 1:
                self.estado = "ALINEADO"
        
        elif self.estado == "ALINEADO":
            # Movimiento rígido pegado al ancla
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

# El 'Ancla' central inicial
ancho_bloque = (columnas - 1) * separacion_x
ancla_x = (width - ancho_bloque) // 2

for f in range(filas):
    foto = imagenes_aliens[f % len(imagenes_aliens)]
    lado = "izq" if f % 2 == 0 else "der"
    delay_fila = f * 120 # Las filas entran una por una
    
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
formacion_lista = False
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. VERIFICAR SI LA FORMACIÓN ESTÁ COMPLETA
    if not formacion_lista:
        formacion_lista = all(a.estado == "ALINEADO" for a in alien_group)

    # 2. LÓGICA DE MOVIMIENTO Y REBOTE
    if formacion_lista:
        ancla_x += velocidad * direccion

        choque_borde = False
        for a in alien_group:
            # Solo los que están vivos y alineados pueden causar rebote
            if a.rect.right >= width - 10:
                choque_borde = True
                direccion = -1 # Rebotar a la izquierda
                break
            if a.rect.left <= 10:
                choque_borde = True
                direccion = 1 # Rebotar a la derecha
                break
        
        if choque_borde:
            # Empuje extra para no quedarse trabado en la colisión
            ancla_x += (velocidad + 1) * direccion

    # 3. ACTUALIZAR TODO
    all_sprites.update(ancla_x)

    # 4. DIBUJAR
    screen.blit(fondo, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()