import json
import os
import pygame

ARCHIVO_PUNTOS = "puntos.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_PUNTOS):
        with open(ARCHIVO_PUNTOS, "r") as f:
            datos = json.load(f)
            return sorted(datos, key=lambda x: x['puntos'], reverse=True)
    return []

def guardar_datos(lista_puntuaciones):
    with open(ARCHIVO_PUNTOS, "w") as f:
        json.dump(lista_puntuaciones, f, indent=4)

def registrar_puntuacion(nombre, puntos_actuales):
    """Guarda el nombre que ya capturamos en Pygame."""
    lista = cargar_datos()
    nuevo_registro = {"nombre": nombre, "puntos": puntos_actuales}
    lista.append(nuevo_registro)
    lista = sorted(lista, key=lambda x: x['puntos'], reverse=True)[:10]
    guardar_datos(lista)

def dibujar_ranking(screen, fuente):
    """Dibuja el Top 10 en la pantalla de 1080x740."""
    lista = cargar_datos()
    screen.fill((0, 0, 0)) # Fondo negro
    
    titulo = fuente.render("=== TOP 10 RANKING ===", True, (255, 215, 0))
    screen.blit(titulo, (1080 // 2 - 150, 50))

    for i, registro in enumerate(lista, 1):
        texto = f"{i}. {registro['nombre']} ........... {registro['puntos']} PTS"
        img = fuente.render(texto, True, (255, 255, 255))
        screen.blit(img, (300, 120 + (i * 45)))