import pygame
import sys
import random
import math

# --- CONFIGURACIÓN INICIAL ---
width = 1040
height = 700
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga - Rebote y Regreso Fluido")
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

    def update(self): 
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 8 
        if keystate[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 8

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

        # 1. ENTRADA INICIAL (Pirueta)
        if self.estado == "ENTRANDO":
            self.angle += 0.15
            self.radio -= 3.0
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
        
        # 2. EN FORMACIÓN (Esperando)
        elif self.estado == "ALINEADO":
            self.rect.x = int(ancla_x + self.x_relativa)
            self.rect.y = self.target_y
            self.px = float(self.rect.x)
            self.py = float(self.rect.y)

        # 3. ATACANDO (Bajando)
        elif self.estado == "ATACANDO":
            self.py += 10 
            self.rect.y = int(self.py)
            
            # Si toca el suelo, cambia a estado REGRESANDO
            if self.rect.bottom >= height:
                self.estado = "REGRESANDO"

        # 4. REGRESANDO (Subiendo suavemente a su sitio)
        elif self.estado == "REGRESANDO":
            dest_x = ancla_x + self.x_relativa
            dest_y = self.target_y
            
            # Interpolación lineal para volver a su sitio
            self.px += (dest_x - self.px) * 0.08
            self.py += (dest_y - self.py) * 0.08
            
            self.rect.x = int(self.px)
            self.rect.y = int(self.py)
            
            # Si está muy cerca de su posición original, se vuelve a alinear
            distancia = math.sqrt((dest_x - self.px)**2 + (dest_y - self.py)**2)
            if distancia < 2:
                self.estado = "ALINEADO"

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
    delay_fila = f * 60 
    for c in range(columnas):
        x_rel = c * separacion_x
        y_dest = 80 + (f * separacion_y)
        delay_total = delay_fila + (c * 6)
        alien = Alien1(x_rel, y_dest, delay_total, lado, foto)
        all_sprites.add(alien)
        alien_group.add(alien)

# --- BUCLE PRINCIPAL ---
direccion = 1
velocidad = 3
running = False 
juego_activo = True 

# Cadencia de ataques
ataque_cooldown = 30 
timer_ataque = ataque_cooldown

while juego_activo:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego_activo = False

    if not running:
        if all(a.estado == "ALINEADO" for a in alien_group):
            running = True

    if running:
        # Movimiento lateral de la formación
        ancla_x += velocidad * direccion
        if ancla_x > (width - ancho_bloque) - 50 or ancla_x < 50:
            direccion *= -1

        # Lanzar nuevos atacantes
        timer_ataque -= 1
        if timer_ataque <= 0:
            # Solo elegimos aliens que estén en la formación (ALINEADO)
            aliens_listos = [a for a in alien_group if a.estado == "ALINEADO"]
            if aliens_listos:
                atacante = random.choice(aliens_listos)
                atacante.estado = "ATACANDO"
                timer_ataque = ataque_cooldown

    player.update()
    alien_group.update(ancla_x)
    
    screen.blit(fondo, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()