import pygame
import sys
import random
import math
import Puntaciones
# --- CONFIGURACIÓN INICIAL ---
width = 800
height = 600
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga - Hileras con Diferentes Skins")
clock = pygame.time.Clock()

# --- CARGA DE FONDO ---
try:
    fondo = pygame.image.load("imagenes/fondo.webp").convert()
    fondo = pygame.transform.scale(fondo, (width, height))
except:
    fondo = pygame.Surface((width, height))
    fondo.fill((10, 10, 30))

# --- LISTA DE IMÁGENES (Skins) ---
# Asegúrate de que estos nombres y carpetas existan en tu PC
imagenes_aliens = ["aliens/alien1.jpeg", "aliens/alien2.jpeg"] 
# --- PEDIR INPUT DEL NOMBRE EN EL JUEGO---
def pedir_nombre_visual(puntos_finales):
    nombre = ""
    fuente = pygame.font.SysFont("Consolas", 50)
    corriendo_input = True
    
    while corriendo_input:
        screen.fill((10, 10, 30)) # Fondo oscuro espacial
        
        # Dibujar instrucciones y puntos
        txt_puntos = fuente.render(f"SCORE FINAL: {puntos_finales}", True, (255, 215, 0))
        txt_guia = fuente.render("INICIALES (MÁX 5):", True, (255, 255, 255))
        txt_nombre = fuente.render(nombre + "_", True, (0, 255, 0))
        
        screen.blit(txt_puntos, (ANCHO//2 - 200, 200))
        screen.blit(txt_guia, (ANCHO//2 - 250, 300))
        screen.blit(txt_nombre, (ANCHO//2 - 50, 400))
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nombre) > 0:
                    corriendo_input = False # Termina al pulsar Enter
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 5:
                    nombre += evento.unicode.upper()
    return nombre

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
            self.rect.x -= 7
        if keystate[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 7

# --- CLASE ALIEN ---
class Alien1(pygame.sprite.Sprite):
    # 1. Modificamos el constructor para que reciba 'ruta_imagen'
    def __init__(self, x_final, y_final, delay, lado_inicio, ruta_imagen):
        super().__init__()
        try:
            # 2. Cargamos la imagen que nos mandan desde el bucle
            self.image = pygame.image.load(ruta_imagen).convert()
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))
            
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        
        # Salida lateral inferior
        self.rect.x = -60 if lado_inicio == "izq" else width + 60
        self.rect.y = height - 100 
        
        self.target_x = x_final
        self.target_y = y_final
        self.delay = delay 
        self.angle = 0 
        self.radio = 100 
        self.estado = "ESPERANDO"

    def update(self, direccion):
        if self.estado == "ESPERANDO":
            self.delay -= 1
            if self.delay <= 0:
                self.estado = "DANDO_VUELTA"
        
        elif self.estado == "DANDO_VUELTA":
            self.angle += 0.1 
            if self.rect.y > self.target_y + 100:
                 self.radio = 100
            else:
                 self.radio -= 2 
            
            if self.radio < 0: self.radio = 0

            offset_x = math.cos(self.angle) * self.radio
            offset_y = math.sin(self.angle) * self.radio
            
            self.rect.x += (self.target_x - self.rect.x) * 0.05 + offset_x * 0.2
            self.rect.y += (self.target_y - self.rect.y) * 0.05 + offset_y * 0.2
            
            if self.rect.y <= self.target_y + 5 and self.radio <= 10:
                self.rect.y = self.target_y
                self.estado = "HORIZONTAL"
        
        elif self.estado == "HORIZONTAL":
            self.rect.x += 2 * direccion

# --- GRUPOS Y CONFIGURACIÓN ---
all_sprites = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

total_hileras = 4 # Probemos con 4 hileras
aliens_por_hilera = 8
separacion_x = 70
separacion_y = 60 
retraso_entre_hileras = 240 # 4 segundos entre hileras

# --- BUCLE DE CREACIÓN ---
for h in range(total_hileras):
    lado = random.choice(["izq", "der"])
    y_objetivo = 80 + (h * separacion_y) 
    x_inicio_fila = (width - (aliens_por_hilera * separacion_x)) // 2
    
    # 3. Elegimos la imagen para toda esta hilera ANTES de crear los aliens
    # Usamos h % len(...) para que si hay 4 hileras y 2 fotos, se repitan 1-2-1-2
    foto_hilera = imagenes_aliens[h % len(imagenes_aliens)]
    
    for i in range(aliens_por_hilera):
        delay_total = (h * retraso_entre_hileras) + (i * 15)
        
        # 4. Pasamos 'foto_hilera' como quinto argumento
        alien = Alien1(x_inicio_fila + (i * separacion_x), y_objetivo, delay_total, lado, foto_hilera)
        all_sprites.add(alien)
        alien_group.add(alien)

# --- BUCLE PRINCIPAL ---
direccion_aliens = 1
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    toco_borde = False
    for alien in alien_group:
        if alien.estado == "HORIZONTAL":
            if alien.rect.right >= width or alien.rect.left <= 0:
                toco_borde = True
                break
    if toco_borde:
        direccion_aliens *= -1

    player.update()
    alien_group.update(direccion_aliens)

    screen.blit(fondo, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()