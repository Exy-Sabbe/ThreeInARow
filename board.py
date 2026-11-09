import pygame
import pygame.freetype
import random
import math
import copy
import computer
import player
from enum import Enum

class TileState(Enum):
    Empty = 1
    Player = 2
    Computer = 3

class Board():
    def __init__(self, window, bar_width, player_image_path, computer_image_path):
        self.__tile_amount = 3
        self.__window = window
        self.__size = window.get_width()
        self.__bar_width = bar_width
        self.__tile_size = (window.get_width() - 2 * bar_width) / self.__tile_amount
        player_image = pygame.image.load(player_image_path)
        self.__player_image = pygame.transform.scale(player_image, (self.__tile_size, self.__tile_size))
        computer_image = pygame.image.load(computer_image_path)
        self.__computer_image = pygame.transform.scale(computer_image, (self.__tile_size, self.__tile_size))
        self.__font = pygame.freetype.SysFont("Arial", 60)
        self.__is_player_turn = bool(random.randint(0, 1))
        self.__board = []
        self.__filled_squares = 0
        self.__winner = None
        for _ in range(self.__tile_amount):
            row = []
            for _ in range(self.__tile_amount):
                row.append(TileState.Empty)
            self.__board.append(row)

    def __ResetGame(self):
        for row in range(self.__tile_amount):
            for col in range(self.__tile_amount):
                self.__board[row][col] = TileState.Empty
        self.__filled_squares = 0
        self.__is_player_turn = bool(random.randint(0, 1))
        self.__winner = None

    def __IsGameOver(self, lastMove):
        checkState = TileState(3 - int(self.__is_player_turn))
        # Check row
        for col in range(self.__tile_amount):
            if self.__board[lastMove[0]][col] != checkState:
                break
            if col == self.__tile_amount - 1:
                self.__winner = checkState

        # Check col
        for row in range(self.__tile_amount):
            if self.__board[row][lastMove[1]] != checkState:
                break
            if row == self.__tile_amount - 1:
                self.__winner = checkState
            
        # Check diag
        if lastMove[0] == lastMove[1]:
            for i in range(self.__tile_amount):
                if self.__board[i][i] != checkState:
                    break
                if i == self.__tile_amount - 1:
                    self.__winner = checkState

        # Check antidiag
        if lastMove[0] + lastMove[1] == self.__tile_amount - 1:
            for i in range(self.__tile_amount):
                if self.__board[i][self.__tile_amount - i - 1] != checkState:
                    break
                if i == self.__tile_amount - 1:
                    self.__winner = checkState

        # Check full board
        if self.__filled_squares == self.__tile_amount**2 and self.__winner == None:
            self.__winner = TileState.Empty

    def GetEmptySquares(self):
        squares = []
        for row in range(self.__tile_amount):
            for col in range(self.__tile_amount):
                if self.__board[row][col] == TileState.Empty:
                    squares.append((row, col))
        return squares

    def GetSquareByMouse(self, mousePos):
        return (math.floor(mousePos[0] / self.__size * self.__tile_amount), math.floor(mousePos[1] / self.__size * self.__tile_amount))

    def GetBoardState(self):
        return self.__board

    def IsSquareEmpty(self, pos):
        return self.__board[pos[0]][pos[1]] == TileState.Empty

    def Update(self):
        if self.__winner != None:
            if pygame.mouse.get_just_pressed()[0]:
                self.__ResetGame()
            return

        move = None
        if self.__is_player_turn:
            move = player.DecideMove(self)
            if move == None:
                return
            self.__board[move[0]][move[1]] = TileState.Player
        else:
            move = computer.DecideMove(self)
            self.__board[move[0]][move[1]] = TileState.Computer

        self.__filled_squares += 1
        self.__IsGameOver(move)
        self.__is_player_turn = not self.__is_player_turn

    def Draw(self):
        # Background stripes
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(0, self.__size / self.__tile_amount - self.__bar_width / 2, self.__size, self.__bar_width))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(0, self.__size * 2 / self.__tile_amount - self.__bar_width / 2, self.__size, self.__bar_width))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__size / self.__tile_amount - self.__bar_width / 2, 0, self.__bar_width, self.__size))
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__size * 2 / self.__tile_amount - self.__bar_width / 2, 0, self.__bar_width, self.__size))

        for row in range(self.__tile_amount):
            for col in range(self.__tile_amount):
                if self.__board[row][col] == TileState.Empty:
                    continue
                elif self.__board[row][col] == TileState.Player:
                    self.__window.blit(self.__player_image, (row * (self.__bar_width + self.__tile_size), col * (self.__bar_width + self.__tile_size)))
                elif self.__board[row][col] == TileState.Computer:
                    self.__window.blit(self.__computer_image, (row * (self.__bar_width + self.__tile_size), col * (self.__bar_width + self.__tile_size)))

        text = ""
        if self.__winner == None:
            return
        elif self.__winner == TileState.Player:
            text = "You Win!"
        elif self.__winner == TileState.Computer:
            text = "You Lose!"
        elif self.__winner == TileState.Empty:
            text = "Draw!"

        text_rect = self.__font.get_rect(text)
        text_rect.center = (self.__size / 2, self.__size / 2)
        black_rect = copy.copy(text_rect)
        black_rect.x -= 22
        black_rect.y -= 22
        black_rect.width += 44
        black_rect.height += 44
        white_rect = copy.copy(text_rect)
        white_rect.x -= 20
        white_rect.y -= 20
        white_rect.width += 40
        white_rect.height += 40
        pygame.draw.rect(self.__window, (50, 50, 50), black_rect)
        pygame.draw.rect(self.__window, (255, 255, 255), white_rect)
        self.__font.render_to(self.__window, text_rect, text, (0, 0, 0))