import pygame
from sys import exit # Terminating the program
from os import path
import board

# ----USEFUL FUNCTIONS----
def GetImagePath(imageName):
    return path.join(path.dirname(path.realpath(__file__)), path.join("images", imageName))

# ----CONSTANTS----
WINDOW_SIZE = 500

BACKGROUND_BAR_WIDTH = 20

# ----INIT GAME----
# Always initialize pygame!
pygame.init()
# Create window of desired size
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
# Set name of window
pygame.display.set_caption("Three In A Row")
# Set icon if wished, commented because of code order swapping around
#pygame.display.set_icon(player_image)
# Get clock for FPS handling
clock = pygame.time.Clock()

gameboard = board.Board(window, BACKGROUND_BAR_WIDTH, GetImagePath("cross.png"), GetImagePath("circle.png"))

game_over = False
# ----GAME LOOP----
while True:
    # Event handler (like inputs)
    for event in pygame.event.get():
        # If user clicks X button on window
        if event.type == pygame.QUIT:
            # Stop both pygame running & quit program
            pygame.quit()
            exit()

    if not game_over:
        # ----UPDATE----
        # Convert delta_time to seconds instead of milliseconds
        gameboard.Update()

        # ----DRAW----
        # Draw background, with 2 horz and 2 vert bars
        window.fill("white")
        gameboard.Draw()

        # Update display every frame
        pygame.display.update()

    # Force game at 60 FPS (basically freeze game loop until enough time has passed for 1 frame)
    clock.tick(60)
