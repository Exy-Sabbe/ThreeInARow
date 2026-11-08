import pygame
import random
import computer
from enum import Enum

class TileState(Enum):
    Empty = 0,
    Player = 1,
    Computer = 2

class Board():
    def __init__(self, window, bar_width, player_image_path, computer_image_path):
        self.__window = window
        self.__size = window.get_width()
        self.__bar_width = bar_width
        self.__tile_size = (window.get_width() - 2 * bar_width) / 3
        player_image = pygame.image.load(player_image_path)
        self.__player_image = pygame.transform.scale(player_image, (self.__tile_size, self.__tile_size))
        computer_image = pygame.image.load(computer_image_path)
        self.__computer_image = pygame.transform.scale(computer_image, (self.__tile_size, self.__tile_size))
        self.__is_player_turn = bool(random.randint(0, 1))
        self.__board = []
        for _ in range(3):
            row = []
            for _ in range(3):
                row.append(TileState.Empty)
            self.__board.append(row)

    def GetEmptySquares(self):
        squares = []
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                if self.__board[row][col] == TileState.Empty:
                    squares.append((row, col))
        return squares

    def GetBoardState(self):
        return self.__board

    def Update(self):
        if not self.GetEmptySquares():
            return

        if self.__is_player_turn:
            move = computer.DecideMove(self)
            self.__board[move[0]][move[1]] = TileState.Player
        else:
            move = computer.DecideMove(self)
            self.__board[move[0]][move[1]] = TileState.Computer

        self.__is_player_turn = not self.__is_player_turn

    def Draw(self):
        # Background stripes
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(0, self.__size / 3 - self.__bar_width / 2, self.__size, self.__bar_width))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(0, self.__size * 2 / 3 - self.__bar_width / 2, self.__size, self.__bar_width))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__size / 3 - self.__bar_width / 2, 0, self.__bar_width, self.__size))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__size * 2 / 3 - self.__bar_width / 2, 0, self.__bar_width, self.__size))

        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                if self.__board[row][col] == TileState.Empty:
                    continue
                elif self.__board[row][col] == TileState.Player:
                    self.__window.blit(self.__player_image, (row * (self.__bar_width + self.__tile_size), col * (self.__bar_width + self.__tile_size)))
                elif self.__board[row][col] == TileState.Computer:
                    self.__window.blit(self.__computer_image, (row * (self.__bar_width + self.__tile_size), col * (self.__bar_width + self.__tile_size)))