import pygame
import sys

pygame.init()
ventana = pygame.display.set_mode((1040, 700))
pygame.font.init()

fuente_inicio = pygame.font.Font("PressStart2P-Regular.ttf", 50)
fuente_titulo= pygame.font.Font("PressStart2P-Regular.ttf", 110)

# Botones
boton_play = pygame.Rect(330, 300, 380, 85)
boton_score =  pygame.Rect(330, 415, 380, 85)
boton_quit = pygame.Rect(330, 530, 380, 85)

# Renderizar texto
texto_titulo = fuente_titulo.render("Galaga", True, (255, 255, 255))
texto_boton_play = fuente_inicio.render("Play", True, (255, 255, 255))
texto_boton_score = fuente_inicio.render("Score", True, (255, 255, 255))
texto_boton_quit = fuente_inicio.render("Quit", True, (255, 255, 255))

# pantalla de inicio
def pantalla_inicio():

    fondo = pygame.image.load("imagenes/fondo.jpeg")
    fondo = pygame.transform.scale(fondo,(1040,700))

    ventana.blit(fondo, (0, 0))
    ventana.blit(texto_titulo, (180, 100))

    pygame.draw.rect(ventana, (0, 255, 255), boton_play, 4, 35)
    pygame.draw.rect(ventana, (0, 255, 255), boton_score, 4, 35)
    pygame.draw.rect(ventana, (0, 255, 255), boton_quit, 4, 35)
    
    ventana.blit(texto_boton_play, (boton_play.x + 85, boton_play.y + 25))
    ventana.blit(texto_boton_score, (boton_score.x + 65, boton_score.y + 25))
    ventana.blit(texto_boton_quit, (boton_quit.x + 85, boton_quit.y + 25))
    pygame.display.update()



mostrar_inicio = True
run = True
while run:
    if mostrar_inicio:
       pantalla_inicio()
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             run = False
          if event.type == pygame.MOUSEBUTTONDOWN:
             if boton_play.collidepoint(event.pos):
                 run = False
             if boton_score.collidepoint(event.pos):
                 run = False
             if boton_quit.collidepoint(event.pos):
                  run = False


pygame.quit()
sys.exit()

        