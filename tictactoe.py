import sys 
import pygame as pg
import configparser as cfg
import numpy as np
from typing import List, Tuple
from ai import AI
import random
from pygame.locals import *

# cfg inits 

config = cfg.ConfigParser()
config.read('config.ini')


# Constants

HEIGHT = config.getint('settings', 'height')
WIDTH = config.getint('settings', 'width')

bg_color_str = config.get('colors', 'bg_color')
BG_COLOR = tuple(map(int, bg_color_str.strip('()').split(',')))
line_color_str = config.get('colors', 'line_color')
LINE_COLOR = tuple(map(int, line_color_str.strip('()').split(',')))
circle_color_str = config.get('colors', 'circle_color')
CIRCLE_COLOR = tuple(map(int, circle_color_str.strip('()').split(',')))
cross_color_str = config.get('colors', 'cross_color')
CROSS_COLOR = tuple(map(int, cross_color_str.strip('()').split(',')))
big_txt_str = config.get('colors', 'big_text_color')
MAIN_TXT_COLOR = tuple(map(int, big_txt_str.strip('()').split(',')))
sub_txt_str = config.get('colors', 'sub_text_color')
SUB_TXT_COLOR = tuple(map(int, sub_txt_str.strip('()').split(',')))


ROWS = config.getint('ui', 'rows')
COLS = config.getint('ui', 'cols')
LINE_WIDTH = config.getint('ui', 'line_width')

SQSIZE = HEIGHT // COLS

CIRCLE_WIDTH = config.getint('ui_icons', 'circle_width')
RADIUS = SQSIZE // 4

CROSS_WIDTH = config.getint('ui_icons', 'cross_width')

OFFSET = config.getint('ui_icons', 'offset')

MAIN_FONT_SIZE = config.getint('ui', 'main_font_size')

SUB_FONT_SIZE = config.getint('ui', 'sub_font_size')

# pygame inits

pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)




class Board:

    def __init__(self) -> None:
        self.squares =  np.zeros((ROWS, COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    # mark square
    def mark_square(self, row, col, player) -> None:
        self.squares[row][col] = player
        self.marked_squares += 1

    # check if the square is empty 
    def empty_square(self, row, col) -> bool:
        return self.squares[row][col] == 0
    
    # check if the board is full
    def isfull(self) -> bool:
        return self.marked_squares == 9

    # check if the board is empty
    def isempty(self) -> bool:
        return self.marked_squares == 0
    
    def get_empty_squares(self) -> List[Tuple[int, int]]:
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    
    # the state of game after game over
    # returns winner
    def final_state(self, show = False) -> int:
        # vertical win
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR 
                    initPos = (col * SQSIZE + SQSIZE // 2, 20)
                    finalPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20) 
                    pg.draw.line(screen, color, initPos, finalPos, CROSS_WIDTH)
                return self.squares[0][col]
            
        # horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR 
                    initPos = (20, row * SQSIZE + SQSIZE // 2)
                    finalPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2) 
                    pg.draw.line(screen, color, initPos, finalPos, CROSS_WIDTH)
                return self.squares[row][0]
        
        # left diagonal win 
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR 
                initPos = (20, 20)
                finalPos = (WIDTH - 20, HEIGHT - 20) 
                pg.draw.line(screen, color, initPos, finalPos, CROSS_WIDTH)

            return self.squares[1][1]
        
        # right diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR 
                initPos = (20, HEIGHT - 20)
                finalPos = (WIDTH - 20, 20) 
                pg.draw.line(screen, color, initPos, finalPos, CROSS_WIDTH)

            return self.squares[1][1]

        # if no win 
        return 0
    


class Game:
    
    def __init__(self) -> None:
        self.show_lines()
        self.player = random.randint(1,2)   
        if self.player == 1: print("You are player 1") 
        else: print("You are player 2")
        self.ai = AI() 
        self.gamemode = "ai"
        self.running = True
        self.board = Board()

    # make move
    def make_move(self, row, col) -> None:
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    # draw lines
    def show_lines(self) -> None:

        screen.fill(BG_COLOR)
        
        # vertical lines
        pg.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pg.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pg.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pg.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    # change player 
    def next_turn(self) -> None:
        self.player = self.player % 2 + 1

    # render x or o 
    def draw_fig(self, row, col) -> None:
        
        # draw cross
        if self.player == 1:
            
            # left line
            start_left = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_left = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pg.draw.line(screen, CROSS_COLOR, start_left, end_left, CROSS_WIDTH) 

            # right line 
            start_right = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_right = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pg.draw.line(screen, CROSS_COLOR, start_right, end_right, CROSS_WIDTH) 


        # draw circle
        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pg.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)
    
    # change mode
    def change_gamemode(self) -> None:
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    # reset game
    def reset(self) -> None:
        self.__init__()

    # check for gameover
    def isOver(self) -> bool:
        font = pg.font.Font(None, MAIN_FONT_SIZE)
        sub_font = pg.font.Font(None, SUB_FONT_SIZE)
        
        case = self.board.final_state(show = True)

        # p1 wins
        if case == 1:
            game_over_txt = font.render("Player 1 won!", True, MAIN_TXT_COLOR)
            reset_txt = sub_font.render("Press R to restart", True, SUB_TXT_COLOR)
            game_over_rect = game_over_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            reset_rect = reset_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

            screen.blit(game_over_txt, game_over_rect)
            screen.blit(reset_txt, reset_rect)  
       
        # p2 wins
        if case == 2:
            game_over_txt = font.render("Player 2 won!", True, MAIN_TXT_COLOR)
            reset_txt = sub_font.render("Press R to restart", True, SUB_TXT_COLOR)
            game_over_rect = game_over_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            reset_rect = reset_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

            screen.blit(game_over_txt, game_over_rect)
            screen.blit(reset_txt, reset_rect)  
        
        # draw
        elif self.board.isfull():
            game_over_txt = font.render("Game was a Draw", True, MAIN_TXT_COLOR)              
            reset_txt = sub_font.render("Press R to restart", True, SUB_TXT_COLOR)
            game_over_rect = game_over_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            reset_rect = reset_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

            screen.blit(game_over_txt, game_over_rect)
            screen.blit(reset_txt, reset_rect)
        


        return self.board.final_state() != 0 or self.board.isfull()



# main function

def main() -> None:

    # Game obj
    game = Game() 
    board = game.board
    ai = game.ai


    # main loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # click event
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    # print(board.squares, "\n")

                    if game.isOver():
                        game.running = False


            # key press events 
            if event.type == pg.KEYDOWN:

                # g => change gamemode
                if event.key == pg.K_g:
                    game.change_gamemode()

                # 1 => change to level 1
                if event.key == pg.K_1:
                    ai.level = 1

                # 0 => change to level 0
                if event.key == pg.K_0:
                    ai.level = 0

                # r => reset
                if event.key == pg.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                    

        if game.gamemode == "ai" and game.player == ai.player and game.running:
            pg.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isOver():
                game.running = False

        pg.display.update()

if __name__ == "__main__":
    main()