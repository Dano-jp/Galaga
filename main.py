from game import GalagaGame
from arcade_machine_sdk import GameMeta
import pygame

if not pygame.get_init():
    pygame.init()

metadata = (GameMeta()
            .with_title("Galaga Edition Toad")
            .with_description("Clásico juego shooter Galaga")
            .with_release_date("17/02/2026")
            .with_group_number(3)
            .add_tag("Arcade")
            .add_tag("Shooter")
            .add_tag("Toad")
            .add_author("Génesis Bentancourt")
            .add_author("Luis Lameda"))

game = GalagaGame(metadata)

if __name__ == "__main__":
    game.run_independently()