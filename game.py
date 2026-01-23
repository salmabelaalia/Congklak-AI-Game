# game.py - Logique du jeu Congklak avec règles complètes
import copy

class CongklakGame:
    def __init__(self):
        # Initialisation du plateau
        # Indices: 0 = home IA, 1-7 = trous IA, 8 = home joueur, 9-15 = trous joueur
        self.board = [0] * 16  # 16 trous au total
        
        # Initialiser avec 7 billes dans chaque petit trou
        for i in range(1, 8):      # Trous 1-7 (IA)
            self.board[i] = 7
        for i in range(9, 16):     # Trous 9-15 (Joueur)
            self.board[i] = 7
        
        # Home IA (0) et Home Joueur (8) restent à 0
        self.board[0] = 0  # Home IA
        self.board[8] = 0  # Home Joueur
        
        # Joueur 0 = humain, Joueur 1 = IA
        self.current_player = 0
        
        # Historique pour undo
        self.history = []
    
    def get_possible_moves(self, player=None):
        """Retourne les coups possibles pour le joueur donné"""
        if player is None:
            player = self.current_player
        
        moves = []
        if player == 0:  # Humain
            # Trous 1-7 = IA
            # Pour l'humain, ce sont les trous 9-15
            for i in range(9, 16):
                if self.board[i] > 0:
                    moves.append(i)
        else:  # IA
            # Trous 1-7 pour l'IA
            for i in range(1, 8):
                if self.board[i] > 0:
                    moves.append(i)
        
        return moves
    
    def distribute_seeds(self, start_hole):
        """Distribue les billes à partir d'un trou donné"""
        seeds = self.board[start_hole]
        self.board[start_hole] = 0
        current_pos = start_hole
        
        while seeds > 0:
            # Passer au trou suivant
            current_pos = (current_pos + 1) % 16
            
            # Si on arrive au home adverse, on le saute
            if (self.current_player == 0 and current_pos == 0) or \
               (self.current_player == 1 and current_pos == 8):
                continue
            
            # Ajouter une bille
            self.board[current_pos] += 1
            seeds -= 1
        
        return current_pos  # Retourne la position de la dernière bille
    
    def make_move(self, hole):
        """Exécute un coup à partir d'un trou donné"""
        # Sauvegarder l'état avant le coup
        self.history.append({
            'board': self.board.copy(),
            'player': self.current_player
        })
        
        # Vérifier que le coup est valide
        if self.board[hole] == 0:
            print(f"Erreur: trou {hole} vide")
            return False
        
        # Déterminer les zones de jeu
        if self.current_player == 0:  # Joueur humain
            player_holes = list(range(9, 16))  # Trous 9-15
            player_home = 8
            opponent_home = 0
        else:  # IA
            player_holes = list(range(1, 8))   # Trous 1-7
            player_home = 0
            opponent_home = 8
        
        # Vérifier que le trou appartient au joueur actuel
        if hole not in player_holes:
            print(f"Erreur: trou {hole} n'appartient pas au joueur {self.current_player}")
            return False
        
        # Distribution des billes
        last_hole = self.distribute_seeds(hole)
        
        # RÈGLE 5: CAPTURE (règle manquante - "shooting")
        # Si la dernière bille tombe dans un trou vide du joueur actuel
        if (last_hole in player_holes and 
            self.board[last_hole] == 1 and  # Était vide avant, maintenant a 1 bille
            last_hole != player_home and last_hole != opponent_home):
            
            # Calculer le trou opposé
            opposite_hole = 16 - last_hole
            
            # Vérifier si le trou opposé a des billes
            if self.board[opposite_hole] > 0:
                # CAPTURE de toutes les billes
                captured = self.board[opposite_hole] + 1  # Billes opposées + dernière bille
                self.board[player_home] += captured
                self.board[last_hole] = 0
                self.board[opposite_hole] = 0
                
                print(f"Capture ! Joueur {self.current_player} capture {captured} billes")
        
        # RÈGLE 4: REJOUER si dernière bille dans son home
        if last_hole == player_home:
            # Le joueur rejoue, ne pas changer de joueur
            print(f"Joueur {self.current_player} rejoue (dernière bille dans son home)")
            return True
        
        # RÈGLE 6: Continuer si dernière bille dans trou occupé
        
        # Sinon, changer de joueur
        self.switch_player()
        return True
    
    def switch_player(self):
        """Change le joueur actif"""
        self.current_player = 1 - self.current_player  # 0->1 ou 1->0
    
    def is_game_over(self):
        """Vérifie si la partie est terminée"""
        # Vérifier si tous les trous d'un côté sont vides
        player1_empty = all(self.board[i] == 0 for i in range(9, 16))
        player2_empty = all(self.board[i] == 0 for i in range(1, 8))
        
        return player1_empty or player2_empty
    
    def get_winner(self):
        """Détermine le gagnant"""
        if not self.is_game_over():
            return None
        
        player1_score = self.board[8]  # Home joueur
        player2_score = self.board[0]  # Home IA
        
        if player1_score > player2_score:
            return 0  # Joueur gagne
        elif player2_score > player1_score:
            return 1  # IA gagne
        else:
            return -1  # Égalité
    
    def get_scores(self):
        """Retourne les scores des deux joueurs"""
        return {
            'player': self.board[8],  # Home joueur
            'ai': self.board[0]       # Home IA
        }
    
    def undo(self):
        """Annule le dernier coup"""
        if not self.history:
            return False
        
        last_state = self.history.pop()
        self.board = last_state['board']
        self.current_player = last_state['player']
        return True
    
    def get_board_copy(self):
        """Retourne une copie du plateau"""
        return copy.deepcopy(self.board)
    
    def print_board(self):
        """Affiche le plateau dans la console"""
        print("\n" + "="*50)
        print("Plateau de jeu:")
        print(f"Home IA ({self.board[0]})")
        print("Trous IA: ", end="")
        for i in range(1, 8):
            print(f"{i}:{self.board[i]} ", end="")
        print("\nTrous Joueur: ", end="")
        for i in range(9, 16):
            print(f"{i}:{self.board[i]} ", end="")
        print(f"\nHome Joueur ({self.board[8]})")
        print(f"Joueur actuel: {'Humain' if self.current_player == 0 else 'IA'}")
        print("="*50)
    
    def evaluate(self, player):
        """Évalue le plateau pour un joueur donné (pour l'IA)"""
        if player == 0:  # Humain
            score = self.board[8] - self.board[0]  # Différence home joueur - home IA
            
            # Bonus pour avoir plus de billes de son côté
            player_seeds = sum(self.board[i] for i in range(9, 16))
            ai_seeds = sum(self.board[i] for i in range(1, 8))
            score += (player_seeds - ai_seeds) * 0.1
            
            # Malus si l'adversaire peut capturer
            for i in range(1, 8):
                if self.board[i] == 0:
                    opposite = 16 - i
                    if self.board[opposite] > 0:
                        score -= 2
            
        else:  # IA
            score = self.board[0] - self.board[8]  # Différence home IA - home joueur
            
            # Bonus pour avoir plus de billes de son côté
            player_seeds = sum(self.board[i] for i in range(1, 8))
            human_seeds = sum(self.board[i] for i in range(9, 16))
            score += (player_seeds - human_seeds) * 0.1
            
            # Malus si l'adversaire peut capturer
            for i in range(9, 16):
                if self.board[i] == 0:
                    opposite = 16 - i
                    if self.board[opposite] > 0:
                        score -= 2
        
        return score

# Test simple
if __name__ == "__main__":
    game = CongklakGame()
    game.print_board()
    
    # Test d'un coup simple
    print("\nTest du coup du joueur (trou 9):")
    game.make_move(9)
    game.print_board()
    
    # Test de la capture
    print("\nTest de capture:")
    # Configuration pour tester la capture
    test_game = CongklakGame()
    test_game.board = [0] * 16
    test_game.board[9] = 1  # 1 bille dans le trou 9 du joueur
    test_game.board[7] = 5  # 5 billes dans le trou opposé 7
    test_game.current_player = 0
    test_game.print_board()
    test_game.make_move(9)
    test_game.print_board()