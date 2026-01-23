# game.py - Logique du jeu corrigée
import copy

class CongklakGame:
    def __init__(self):
        # Structure: [home_ia, trous_ia(7), home_humain, trous_humain(7)]
        self.board = [0, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7]
        self.current_player = 0  # 0 = humain, 1 = IA
        
    def get_possible_moves(self, player):
        """Retourne les coups possibles pour un joueur"""
        moves = []
        start = 1 if player == 0 else 9  # Humain: 1-7, IA: 9-15
        for i in range(start, start + 7):
            if self.board[i] > 0:
                moves.append(i)
        return moves
    
    def make_move(self, hole_index):
        """Exécute un coup - VERSION CORRIGÉE"""
        # 1. Prendre toutes les billes
        stones = self.board[hole_index]
        if stones == 0:
            return  # Pas de billes, coup invalide
            
        self.board[hole_index] = 0
        
        # 2. Distribuer une par une
        current = hole_index
        for _ in range(stones):
            # Trou suivant
            current = (current + 1) % 16
            
            # Sauter le home adverse
            # Humain (joueur 0) saute index 0 (home IA)
            # IA (joueur 1) saute index 8 (home humain)
            if (self.current_player == 0 and current == 0) or \
               (self.current_player == 1 and current == 8):
                # On saute, donc on prend le prochain trou
                current = (current + 1) % 16
            
            self.board[current] += 1
        
        # 3. Vérifier les règles spéciales
        self.check_special_rules(current)
        
        # 4. Changer de joueur si nécessaire
        if not self.should_play_again(current):
            self.current_player = 1 - self.current_player
    
    def check_special_rules(self, last_hole):
        """Vérifie les règles de capture"""
        # Si dernière bille dans un trou vide du joueur courant
        if self.board[last_hole] == 1:  # Juste la bille qu'on vient de poser
            # Vérifier si c'est un trou du joueur courant
            if self.current_player == 0 and 1 <= last_hole <= 7:
                # Capture : prendre les billes du trou opposé
                opposite_hole = 16 - last_hole
                if opposite_hole >= 9 and opposite_hole <= 15:
                    captured = self.board[opposite_hole]
                    if captured > 0:
                        self.board[8] += captured + 1  # Home humain
                        self.board[opposite_hole] = 0
                        self.board[last_hole] = 0
            elif self.current_player == 1 and 9 <= last_hole <= 15:
                opposite_hole = 16 - last_hole
                if opposite_hole >= 1 and opposite_hole <= 7:
                    captured = self.board[opposite_hole]
                    if captured > 0:
                        self.board[0] += captured + 1  # Home IA
                        self.board[opposite_hole] = 0
                        self.board[last_hole] = 0
    
    def should_play_again(self, last_hole):
        """Vérifie si le joueur rejoue"""
        # Rejoue si dernière bille dans son home
        # Humain: home à index 8, IA: home à index 0
        if self.current_player == 0 and last_hole == 8:
            return True
        if self.current_player == 1 and last_hole == 0:
            return True
        return False
    
    def is_game_over(self):
        """Vérifie si le jeu est terminé"""
        # Vérifier côté humain
        human_empty = all(self.board[i] == 0 for i in range(1, 8))
        # Vérifier côté IA
        ia_empty = all(self.board[i] == 0 for i in range(9, 16))
        return human_empty or ia_empty
    
    def copy(self):
        """Crée une copie du jeu"""
        return copy.deepcopy(self)