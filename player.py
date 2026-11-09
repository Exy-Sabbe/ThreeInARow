import pygame

def DecideMove(board):
    if pygame.mouse.get_just_pressed()[0]:
        pos = board.GetSquareByMouse(pygame.mouse.get_pos())
        if board.IsSquareEmpty(pos):
            return pos
    return None