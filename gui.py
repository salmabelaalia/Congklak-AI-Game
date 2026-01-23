# new_gui.py - Interface corrigée (sans numéros, IA fonctionnelle)
import pygame
import sys
from game import CongklakGame
from ai import CongklakAI

# Couleurs (Palette Terre Cuite / Bois)
COLOR_BG = (255, 248, 220)      # Off-white
COLOR_BOARD = (160, 82, 45)     # Sienna
COLOR_HOLE = (101, 67, 33)      # Dark Wood
COLOR_SEED = (34, 139, 34)      # Forest Green
COLOR_PLAYER = (30, 144, 255)   # Blue for player
COLOR_AI = (220, 20, 60)        # Red for AI
COLOR_TEXT = (50, 50, 50)       # Dark gray

class CongklakPygameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Congklak")
        
        self.game = CongklakGame()
        self.ai = CongklakAI(difficulty="easy")
        
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)
        
        self.selected_difficulty = "easy"
        self.running = True
        self.waiting_for_ai = False
        
    def get_board_for_display(self):
        """Convertit le board pour l'affichage (HOME INVERSE)"""
        board_display = [0] * 16
        
        # Trous joueur (P1) - ligne du BAS
        for i in range(7):
            board_display[i] = self.game.board[i + 1]  # 1-7
        
        # Home joueur (P1) - À DROITE maintenant
        board_display[7] = self.game.board[8]  # Home humain
        
        # Trous IA (P2) - ligne du HAUT
        for i in range(7):
            board_display[8 + i] = self.game.board[i + 9]  # 9-15
        
        # Home IA (P2) - À GAUCHE maintenant
        board_display[15] = self.game.board[0]  # Home IA
        
        return board_display
    
    def draw_board(self):
        self.screen.fill(COLOR_BG)
        
        # Dessin du plateau principal
        pygame.draw.rect(self.screen, COLOR_BOARD, (50, 150, 900, 250), border_radius=30)
        
        # Titre
        title = self.font_large.render("CONGKLAK", True, COLOR_TEXT)
        self.screen.blit(title, (500 - title.get_width()//2, 30))
        
        # Affichage difficulté
        diff_text = self.font_small.render(f"Difficulté: {self.selected_difficulty.upper()}", 
                                          True, COLOR_TEXT)
        self.screen.blit(diff_text, (500 - diff_text.get_width()//2, 80))
        
        # Homes INVERSE
        board = self.get_board_for_display()
        
        # Home IA (GAUCHE)
        pygame.draw.circle(self.screen, COLOR_AI, (120, 275), 60)
        ai_home_text = self.font_large.render(str(board[15]), True, (255, 255, 255))
        self.screen.blit(ai_home_text, (120 - ai_home_text.get_width()//2, 275 - ai_home_text.get_height()//2))
        
        # Home Joueur (DROITE)
        pygame.draw.circle(self.screen, COLOR_PLAYER, (880, 275), 60)
        home_text = self.font_large.render(str(board[7]), True, (255, 255, 255))
        self.screen.blit(home_text, (880 - home_text.get_width()//2, 275 - home_text.get_height()//2))
        
        # Labels (INVERSE aussi)
        ai_label = self.font_medium.render("IA", True, COLOR_AI)
        player_label = self.font_medium.render("VOUS", True, COLOR_PLAYER)
        self.screen.blit(ai_label, (120 - ai_label.get_width()//2, 340))
        self.screen.blit(player_label, (880 - player_label.get_width()//2, 340))
        
        # Trous IA (ligne du HAUT) - SANS NUMÉROS
        self.ai_holes_rects = []
        for i in range(7):
            x = 280 + i * 70
            y = 210  # Plus haut
            
            # Déterminer la couleur en fonction du contenu
            stones = board[8+i]
            if stones > 0:
                hole_color = COLOR_AI
            else:
                hole_color = (180, 180, 180)  # Gris pour vide
            
            pygame.draw.circle(self.screen, hole_color, (x, y), 30)
            
            # Nombre de billes seulement
            if stones > 0:
                count_text = self.font_medium.render(str(stones), True, (255, 255, 255))
                self.screen.blit(count_text, (x - count_text.get_width()//2, y - count_text.get_height()//2))
            
            # Indices de trous IA (9-15 dans le jeu)
            self.ai_holes_rects.append((pygame.Rect(x-30, y-30, 60, 60), i+9))
        
        # Trous Joueur (ligne du BAS) - SANS NUMÉROS
        self.player_holes_rects = []
        for i in range(7):
            x = 280 + i * 70
            y = 340  # Plus bas
            
            # Déterminer la couleur en fonction du contenu
            stones = board[i]
            if stones > 0:
                hole_color = COLOR_PLAYER
            else:
                hole_color = (180, 180, 180)  # Gris pour vide
            
            pygame.draw.circle(self.screen, hole_color, (x, y), 30)
            
            # Nombre de billes seulement
            if stones > 0:
                count_text = self.font_medium.render(str(stones), True, (255, 255, 255))
                self.screen.blit(count_text, (x - count_text.get_width()//2, y - count_text.get_height()//2))
            
            # Indices de trous Joueur (1-7) dans le jeu
            self.player_holes_rects.append((pygame.Rect(x-30, y-30, 60, 60), i+1))
        
        # Indicateur de tour - CORRECTION: vérifier fin de jeu en premier
        turn_y = 420
        
        # CORRECTION: Vérifier d'abord si le jeu est terminé
        if self.game.is_game_over():
            # Déterminer le gagnant
            player_score = board[7]
            ai_score = board[15]
            if player_score > ai_score:
                turn_text = self.font_medium.render("VOUS GAGNEZ !", True, COLOR_PLAYER)
            elif ai_score > player_score:
                turn_text = self.font_medium.render("L'IA GAGNE !", True, COLOR_AI)
            else:
                turn_text = self.font_medium.render("ÉGALITÉ !", True, COLOR_TEXT)
            self.screen.blit(turn_text, (500 - turn_text.get_width()//2, turn_y))
        elif self.game.current_player == 0 and not self.waiting_for_ai:  # Tour du joueur
            turn_text = self.font_medium.render("À VOTRE TOUR", True, COLOR_PLAYER)
            self.screen.blit(turn_text, (500 - turn_text.get_width()//2, turn_y))
        elif self.game.current_player == 1 or self.waiting_for_ai:  # Tour de l'IA
            turn_text = self.font_medium.render("L'IA RÉFLÉCHIT...", True, COLOR_AI)
            self.screen.blit(turn_text, (500 - turn_text.get_width()//2, turn_y))
        
        # Score (INVERSE)
        score_text = self.font_small.render(f"Score: IA {board[15]} - {board[7]} VOUS", 
                                           True, COLOR_TEXT)
        self.screen.blit(score_text, (500 - score_text.get_width()//2, 460))
        
        # Boutons de difficulté
        self.draw_buttons()
    
    def draw_buttons(self):
        difficulties = [
            ("FACILE", (200, 500), COLOR_SEED, "easy"),
            ("MOYEN", (400, 500), (255, 165, 0), "medium"),
            ("DIFFICILE", (600, 500), COLOR_AI, "hard"),
            ("NOUVEAU", (800, 500), (70, 130, 180), "new")
        ]
        
        self.buttons = []
        for text, pos, color, action in difficulties:
            rect = pygame.Rect(pos[0] - 60, pos[1] - 20, 120, 40)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (50, 50, 50), rect, 2, border_radius=10)
            
            btn_text = self.font_small.render(text, True, (255, 255, 255))
            self.screen.blit(btn_text, (pos[0] - btn_text.get_width()//2, 
                                        pos[1] - btn_text.get_height()//2))
            
            self.buttons.append((rect, action))
    
    def handle_click(self, pos):
        x, y = pos
        
        # Vérifier les boutons
        for rect, action in self.buttons:
            if rect.collidepoint(x, y):
                if action == "new":
                    self.game = CongklakGame()
                    self.waiting_for_ai = False
                    return
                elif action in ["easy", "medium", "hard"]:
                    self.ai = CongklakAI(difficulty=action)
                    self.selected_difficulty = action
                    return
        
        # Si c'est le tour de l'IA, ne pas accepter les clics
        if self.game.current_player == 1 or self.waiting_for_ai:
            return
        
        # Vérifier les trous du joueur
        if self.game.current_player == 0:  # Tour du joueur
            for rect, hole_idx in self.player_holes_rects:
                if rect.collidepoint(x, y):
                    # Vérifier que le trou a des billes
                    if self.game.board[hole_idx] > 0:
                        # Faire le coup
                        self.game.make_move(hole_idx)
                        
                        # Vérifier si le jeu est terminé
                        if not self.game.is_game_over():
                            # Si le joueur rejoue (dernière bille dans son home)
                            if self.game.current_player == 0:
                                return  # Le joueur rejoue
                            else:
                                # C'est le tour de l'IA
                                self.waiting_for_ai = True
                                return
                        else:
                            # Fin du jeu
                            return
    
    def ai_move(self):
        """L'IA joue son coup"""
        if self.game.current_player == 1:  # Tour de l'IA
            moves = self.game.get_possible_moves(1)
            if moves:  # Vérifier qu'il y a des coups possibles
                pygame.time.wait(500)
                best_move = self.ai.get_best_move(self.game)
                if best_move is not None:
                    self.game.make_move(best_move)
            
            # Si l'IA rejoue (dernière bille dans son home)
            if self.game.current_player == 1 and not self.game.is_game_over():
                # L'IA rejoue immédiatement
                self.ai_move()
            else:
                self.waiting_for_ai = False
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_n:
                        self.game = CongklakGame()  # Nouvelle partie
                        self.waiting_for_ai = False
                    elif event.key == pygame.K_1:
                        self.ai = CongklakAI(difficulty="easy")
                        self.selected_difficulty = "easy"
                    elif event.key == pygame.K_2:
                        self.ai = CongklakAI(difficulty="medium")
                        self.selected_difficulty = "medium"
                    elif event.key == pygame.K_3:
                        self.ai = CongklakAI(difficulty="hard")
                        self.selected_difficulty = "hard"
            
            # Si on attend que l'IA joue
            if self.waiting_for_ai and not self.game.is_game_over():
                # Attendre un peu pour que l'IA "réfléchisse"
                pygame.time.delay(800)  # 800ms de délai
                self.ai_move()
                self.waiting_for_ai = False
            
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = CongklakPygameGUI()
    app.run()