# ai.py - Algorithme Minimax avec Alpha-Beta
import math
import copy

# Dans ai.py
class CongklakAI:
    def __init__(self, difficulty="medium"):
        if difficulty == "easy":
            self.depth = 1
        elif difficulty == "medium":
            self.depth = 3
        elif difficulty == "hard":
            self.depth = 5
        
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """Algorithme Minimax avec élagage Alpha-Beta"""
        if depth == 0 or game.is_game_over():
            return self.evaluate(game)
        
        if maximizing_player:
            max_eval = -math.inf
            for move in game.get_possible_moves(1):  # IA est joueur 1
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                
                eval = self.minimax(game_copy, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                
                if beta <= alpha:  # Élagage Beta
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_possible_moves(0):  # Humain est joueur 0
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                
                eval = self.minimax(game_copy, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                if beta <= alpha:  # Élagage Alpha
                    break
            return min_eval
    
    def evaluate(self, game):
        """Fonction d'évaluation simple: différence de score"""
        # Score = billes dans home
        score_ia = game.board[0]    # Home joueur 1 (IA)
        score_human = game.board[8] # Home joueur 2 (humain)
        return score_ia - score_human
    
    def get_best_move(self, game):
        """Trouve le meilleur coup pour l'IA"""
        best_move = None
        best_value = -math.inf
        
        for move in game.get_possible_moves(1):  # IA est joueur 1
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move)
            
            move_value = self.minimax(
                game_copy, 
                self.depth-1, 
                -math.inf, 
                math.inf, 
                False
            )
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        return best_move