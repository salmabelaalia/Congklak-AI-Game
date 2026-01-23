# ai.py - IA avec 3 niveaux
import math
import copy
import random

class CongklakAI:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.depth = 1
        elif difficulty == "medium":
            self.depth = 2  # Réduit pour éviter le blocage
        elif difficulty == "hard":
            self.depth = 3  # Réduit pour éviter le blocage
    
    def get_best_move(self, game):
        """Trouve le meilleur coup selon le niveau"""
        moves = game.get_possible_moves(1)  # IA est joueur 1
        
        if not moves:
            return None
            
        if self.difficulty == "easy":
            # Niveau facile : aléatoire
            return random.choice(moves)
            
        elif self.difficulty == "medium":
            # Niveau moyen : minimax limité
            return self.minimax_move(game, moves, self.depth)
            
        elif self.difficulty == "hard":
            # Niveau difficile : minimax avec alpha-beta
            return self.alpha_beta_move(game, moves, self.depth)
    
    def minimax_move(self, game, moves, depth):
        """Minimax simple"""
        best_move = None
        best_value = -math.inf
        
        for move in moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move)
            
            value = self.minimax(game_copy, depth-1, False)
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move or random.choice(moves)
    
    def alpha_beta_move(self, game, moves, depth):
        """Minimax avec alpha-beta pruning"""
        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        
        for move in moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move)
            
            value = self.alpha_beta(game_copy, depth-1, alpha, beta, False)
            
            if value > best_value:
                best_value = value
                best_move = move
            
            alpha = max(alpha, best_value)
        
        return best_move or random.choice(moves)
    
    def minimax(self, game, depth, maximizing_player):
        """Algorithme Minimax"""
        if depth == 0 or game.is_game_over():
            return self.evaluate(game)
        
        if maximizing_player:
            max_eval = -math.inf
            for move in game.get_possible_moves(1):
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval = self.minimax(game_copy, depth-1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_possible_moves(0):
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval = self.minimax(game_copy, depth-1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    
    def alpha_beta(self, game, depth, alpha, beta, maximizing_player):
        """Minimax avec élagage alpha-beta"""
        if depth == 0 or game.is_game_over():
            return self.evaluate(game)
        
        if maximizing_player:
            max_eval = -math.inf
            for move in game.get_possible_moves(1):
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval = self.alpha_beta(game_copy, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Élagage beta
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_possible_moves(0):
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval = self.alpha_beta(game_copy, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Élagage alpha
            return min_eval
    
    def evaluate(self, game):
        """Fonction d'évaluation"""
        # Score de base : différence de billes dans les homes
        score_ia = game.board[0]    # Home IA
        score_human = game.board[8] # Home humain
        base_score = score_ia - score_human
        
        # Bonus pour avoir plus de coups possibles
        moves_ia = len(game.get_possible_moves(1))
        moves_human = len(game.get_possible_moves(0))
        mobility_bonus = (moves_ia - moves_human) * 0.1
        
        return base_score + mobility_bonus