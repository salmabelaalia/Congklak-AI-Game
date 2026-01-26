import copy

class CongklakGame:
    def __init__(self):
        # Structure: [home_ia, trous_ia(7), home_humain, trous_humain(7)]
        self.board = [0, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7]
        self.current_player = 0  # 0 = humain, 1 = IA
        self.history = []  # Pour undo
        
    def get_possible_moves(self, player=None):
        """Retourne les coups possibles pour un joueur - RÈGLE 7"""
        if player is None:
            player = self.current_player
        
        moves = []
        if player == 0:  # Humain: trous 9-15
            for i in range(9, 16):
                if self.board[i] > 0:
                    moves.append(i)
        else:  # IA: trous 1-7
            for i in range(1, 8):
                if self.board[i] > 0:
                    moves.append(i)
        
        return moves
    
    def make_move(self, hole_index):
        """Exécute un coup avec RÈGLE 6 (continuation)"""
        # Sauvegarder pour undo
        self.history.append({
            'board': self.board.copy(),
            'player': self.current_player
        })
        
        # Vérifier que le coup est valide
        if self.board[hole_index] == 0:
            return False
        
        # RÈGLE 6: Continuation jusqu'à ce que dernière bille dans trou vide adverse
        continue_playing = True
        current_hole = hole_index
        
        while continue_playing:
            # 1. Prendre toutes les billes
            stones = self.board[current_hole]
            self.board[current_hole] = 0
            
            # 2. Distribuer une par une
            last_hole = current_hole
            for _ in range(stones):
                # Trou suivant
                last_hole = (last_hole + 1) % 16
                
                # Sauter le home adverse - RÈGLE 3
                if (self.current_player == 0 and last_hole == 0) or \
                   (self.current_player == 1 and last_hole == 8):
                    last_hole = (last_hole + 1) % 16
                
                self.board[last_hole] += 1
            
            # 3. Vérifier les conditions de fin de tour
            # RÈGLE 4: Dernière bille dans son home -> rejouer
            if (self.current_player == 0 and last_hole == 8) or \
               (self.current_player == 1 and last_hole == 0):
                return True  # Le joueur rejoue
            
            # RÈGLE 5: Dernière bille dans trou vide de son côté -> capture
            elif self.is_own_empty_hole(last_hole):
                self.capture_stones(last_hole)
                continue_playing = False  # Fin du tour
            
            # RÈGLE 6: Dernière bille dans trou occupé de son côté -> continuer
            elif self.is_own_occupied_hole(last_hole):
                current_hole = last_hole  # Continuer avec ce trou
                continue_playing = True
            
            # Dernière bille dans trou adverse -> fin du tour
            else:
                continue_playing = False
        
        # Changer de joueur
        self.current_player = 1 - self.current_player
        return False
    
    def is_own_empty_hole(self, hole):
        """Vérifie si c'est un trou vide du joueur actuel (pour capture)"""
        if self.current_player == 0:  # Humain
            return 9 <= hole <= 15 and self.board[hole] == 1
        else:  # IA
            return 1 <= hole <= 7 and self.board[hole] == 1
    
    def is_own_occupied_hole(self, hole):
        """Vérifie si c'est un trou occupé du joueur actuel (pour continuation)"""
        if self.current_player == 0:  # Humain
            return 9 <= hole <= 15 and self.board[hole] > 1
        else:  # IA
            return 1 <= hole <= 7 and self.board[hole] > 1
    
    def capture_stones(self, last_hole):
        """Capture les billes du trou opposé - RÈGLE 5"""
        # Trou opposé
        opposite_hole = 16 - last_hole
        
        # Calculer les billes capturées
        captured = self.board[opposite_hole] + 1  # Billes opposées + dernière bille
        
        # Ajouter au home du joueur
        if self.current_player == 0:  # Humain
            self.board[8] += captured
        else:  # IA
            self.board[0] += captured
        
        # Vider les trous
        self.board[opposite_hole] = 0
        self.board[last_hole] = 0
    
    def should_play_again(self, last_hole):
        """Vérifie si le joueur rejoue - RÈGLE 4"""
        if self.current_player == 0 and last_hole == 8:
            return True
        if self.current_player == 1 and last_hole == 0:
            return True
        return False
    
    def is_game_over(self):
        """Vérifie si le jeu est terminé - RÈGLE 7 et 8"""
        # Vérifier côté humain
        human_empty = all(self.board[i] == 0 for i in range(9, 16))
        # Vérifier côté IA
        ia_empty = all(self.board[i] == 0 for i in range(1, 8))
        
        # Si un côté est vide, l'autre récupère toutes ses billes
        if human_empty or ia_empty:
            self.collect_remaining_stones()
            return True
        
        return False
    
    def collect_remaining_stones(self):
        """Récupère les billes restantes quand un côté est vide - RÈGLE 7"""
        # Billes restantes côté humain
        human_remaining = sum(self.board[i] for i in range(9, 16))
        # Billes restantes côté IA
        ia_remaining = sum(self.board[i] for i in range(1, 8))
        
        # Ajouter aux homes respectifs
        self.board[8] += human_remaining
        self.board[0] += ia_remaining
        
        # Vider les trous
        for i in range(1, 8):
            self.board[i] = 0
        for i in range(9, 16):
            self.board[i] = 0
    
    def get_winner(self):
        """Détermine le gagnant - RÈGLE 8"""
        if not self.is_game_over():
            return None
        
        if self.board[8] > self.board[0]:
            return 0  # Humain gagne
        elif self.board[0] > self.board[8]:
            return 1  # IA gagne
        else:
            return -1  # Égalité
    
    def copy(self):
        """Crée une copie du jeu"""
        return copy.deepcopy(self)
    
    def undo(self):
        """Annule le dernier coup"""
        if self.history:
            last_state = self.history.pop()
            self.board = last_state['board']
            self.current_player = last_state['player']
            return True
        return False