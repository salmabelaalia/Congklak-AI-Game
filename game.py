# game.py - La logique de base du Congklak
class CongklakGame:
    def __init__(self):
        # Plateau: [home_joueur2, trous_j2(7), home_joueur1, trous_j1(7)]
        self.board = [0, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7]
        self.current_player = 0  # 0 = joueur 1, 1 = joueur 2
        
    def get_possible_moves(self, player):
        """Retourne les coups possibles pour un joueur"""
        moves = []
        start = 1 if player == 0 else 9
        for i in range(start, start + 7):
            if self.board[i] > 0:  # Si le trou n'est pas vide
                moves.append(i)
        return moves
    
    def make_move(self, hole_index):
        """Exécute un coup depuis un trou donné"""
        # 1. Prendre toutes les billes du trou
        stones = self.board[hole_index]
        self.board[hole_index] = 0
        
        # 2. Distribuer une par une
        current = hole_index
        while stones > 0:
            current = (current + 1) % 16
            # Sauter le home de l'adversaire
            if (self.current_player == 0 and current == 8) or \
               (self.current_player == 1 and current == 0):
                continue
                
            self.board[current] += 1
            stones -= 1
        
        # 3. Vérifier les règles spéciales
        self.check_special_rules(current)
        
        # 4. Changer de joueur si nécessaire
        if not self.should_play_again(current):
            self.current_player = 1 - self.current_player
    
    def check_special_rules(self, last_hole):
        """Vérifie capture et rejeu"""
        # À implémenter selon les règles de l'article
        pass
    
    def should_play_again(self, last_hole):
        """Vérifie si le joueur rejoue"""
        # Rejoue si dernière bille dans son home
        if self.current_player == 0 and last_hole == 0:
            return True
        if self.current_player == 1 and last_hole == 8:
            return True
        return False
    
    def is_game_over(self):
        """Vérifie si le jeu est terminé"""
        # Vérifie si tous les trous (sauf les homes) sont vides
        for i in range(1, 8):  # Trous du joueur 1
            if self.board[i] > 0:
                return False
        for i in range(9, 16):  # Trous du joueur 2
            if self.board[i] > 0:
                return False
        return True