import random
import copy
import time

class AI:
    def __init__(self, level=1, player=2) -> None:
        self.level = level
        self.player = player

    def random_move(self, board):
        empty_squares = board.get_empty_squares()
        idx = random.randrange(0, len(empty_squares))
        return empty_squares[idx]
    

    def alpha_beta(self, board, maximizing, alpha, beta):
        case = board.final_state()

        # p1 wins
        if case == 1:
            return 1, None  
        # p2 wins
        if case == 2:
            return -1, None 
        # draw
        elif board.isfull():
            return 0, None 
        
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.alpha_beta(temp_board, False, alpha, beta)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

                alpha = max(alpha, max_eval)

                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
            
        else:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.alpha_beta(temp_board, True, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

                beta = min(beta, min_eval)

                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move


    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()

        # p1 wins
        if case == 1:
            return 1, None  
        # p2 wins
        if case == 2:
            return -1, None 
        # draw
        elif board.isfull():
            return 0, None 
        
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            
            return min_eval, best_move
            


    def eval(self, main_board):
        start_time = time.perf_counter()
        
        if self.level == 0:
            # random move
            eval = "random"
            move = self.random_move(main_board)
        else:
            # AI move
            # eval, move = self.minimax(main_board, False)
            eval, move = self.alpha_beta(main_board, False, float('-inf'), float('inf'))

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time 

        print(f"AI chose: {move}, eval: {eval}, time: {elapsed_time}")
        
        return move