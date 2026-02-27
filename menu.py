import pygame
import sys
from pathlib import Path

# Intentamos importar puntuaciones, si falla usamos un dummy para que no crashe
try:
    import puntuaciones
except ImportError:
    class puntuaciones:
        @staticmethod
        def obtener_highscores(): return ["Dummy: 100", "Test: 50"]

# Configuración de rutas relativas
CURRENT_DIR = Path(__file__).resolve().parent
IMAGES_DIR = CURRENT_DIR / "imagenes"

def load_font(name, size):
    """Carga fuentes de forma segura."""
    try:
        return pygame.font.Font(str(CURRENT_DIR / name), size)
    except:
        return pygame.font.SysFont("Impact", size)

def draw_menu(surface, mouse_pos):
    """Dibuja la interfaz del menú principal."""
    width, height = surface.get_size()
    BLANCO = (255, 255, 255)
    CYAN = (0, 255, 255)
    BRILLO = (255, 255, 0)

    # Dibujar fondo
    try:
        fondo_menu = pygame.image.load(str(IMAGES_DIR / "fondo.jpeg")).convert()
        fondo_menu = pygame.transform.scale(fondo_menu, (width, height))
        surface.blit(fondo_menu, (0, 0))
    except:
        pass # Si no hay fondo, se queda negro

    fuente_inicio = load_font("PressStart2P-Regular.ttf", 40)
    fuente_titulo = load_font("PressStart2P-Regular.ttf", 100)

    # Título
    titulo = fuente_titulo.render("Galaga", True, BLANCO)
    surface.blit(titulo, (width // 2 - titulo.get_width() // 2, 100))

    # Botones
    btn_width, btn_height = 380, 85
    start_y = 300
    gap = 115
    
    btn_play = pygame.Rect(width//2 - btn_width//2, start_y, btn_width, btn_height)
    btn_score = pygame.Rect(width//2 - btn_width//2, start_y + gap, btn_width, btn_height)
    btn_quit = pygame.Rect(width//2 - btn_width//2, start_y + gap*2, btn_width, btn_height)

    buttons = [
        (btn_play, "Play", "PLAY"),
        (btn_score, "Score", "SCORES"),
        (btn_quit, "Quit", "QUIT")
    ]

    for btn, txt, action in buttons:
        col = BRILLO if btn.collidepoint(mouse_pos) else CYAN
        pygame.draw.rect(surface, col, btn, 4, 35)
        t_render = fuente_inicio.render(txt, True, col)
        surface.blit(t_render, (btn.centerx - t_render.get_width()//2, btn.y + 25))
    
    return buttons

def draw_highscores(surface):
    """Dibuja la tabla de puntuaciones."""
    width, height = surface.get_size()
    BLANCO = (255, 255, 255)
    BRILLO = (255, 255, 0)
    CYAN = (0, 255, 255)

    surface.fill((0, 0, 0))
    
    fuente_inicio = load_font("PressStart2P-Regular.ttf", 40)
    fuente_score = pygame.font.SysFont("Impact", 35)

    titulo_s = fuente_inicio.render("HIGHSCORES", True, BRILLO)
    surface.blit(titulo_s, (width//2 - titulo_s.get_width()//2, 50))

    try:
        lista_scores = puntuaciones.obtener_highscores()
    except:
        lista_scores = ["Error al cargar"]
        
    for i, score in enumerate(lista_scores[:10]):
        txt = fuente_score.render(f"{i+1}. {score}", True, BLANCO)
        surface.blit(txt, (width//2 - txt.get_width()//2, 150 + i * 45))

    volver_txt = fuente_score.render("Presiona ESC para volver", True, CYAN)
    surface.blit(volver_txt, (width//2 - volver_txt.get_width()//2, height - 100))