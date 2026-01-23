# gui.py - Interface graphique avec design modernisé
import tkinter as tk
from game import CongklakGame
from ai import CongklakAI

class CongklakGUI:
    def __init__(self):
        self.game = CongklakGame()
        self.ai = CongklakAI(difficulty="medium")
        
        # Créer la fenêtre
        self.window = tk.Tk()
        self.window.title("Congklak AI - Traditional Indonesian Game")
        self.window.geometry("900x700")
        self.window.configure(bg="#2C3E50")  # Fond bleu foncé
        
        # Titre principal
        title_label = tk.Label(
            self.window, 
            text="CONGKLAK", 
            font=("Arial", 32, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.grid(row=0, column=0, columnspan=8, pady=20)
        
        # Créer le plateau
        self.create_board()
        
        # Démarrer le jeu
        self.update_display()
    
    def create_board(self):
        """Crée le plateau de jeu avec le design de l'image"""
        # Cadre principal du plateau
        board_frame = tk.Frame(self.window, bg="#34495E", relief="raised", bd=5)
        board_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
        
        # ---------- SECTION ADVERSARY ----------
        # Titre adversaire (IA)
        self.opponent_label = tk.Label(
            board_frame,
            text="OPPONENT",
            font=("Arial", 18, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        self.opponent_label.grid(row=0, column=0, columnspan=7, pady=10)
        
        # Score adversaire
        self.opponent_score = tk.Label(
            board_frame,
            text="0",
            font=("Arial", 28, "bold"),
            bg="#E74C3C",  # Rouge
            fg="white",
            width=4,
            height=2,
            relief="sunken"
        )
        self.opponent_score.grid(row=0, column=7, padx=10)
        
        # Trous adversaire (7 trous, de droite à gauche comme dans l'image)
        self.opponent_holes = []
        for i in range(7):
            hole = tk.Label(
                board_frame,
                text="7",
                font=("Arial", 16, "bold"),
                bg="#16A085",  # Vert turquoise
                fg="white",
                width=4,
                height=2,
                relief="ridge"
            )
            hole.grid(row=1, column=6-i, padx=5, pady=5)
            self.opponent_holes.append(hole)
        
        # ---------- SECTION PLAYER ----------
        # Trous joueur (7 trous, de gauche à droite)
        self.player_holes = []
        for i in range(7):
            btn = tk.Button(
                board_frame,
                text="7",
                font=("Arial", 16, "bold"),
                bg="#3498DB",  # Bleu
                fg="white",
                width=4,
                height=2,
                relief="raised",
                command=lambda idx=1+i: self.human_move(idx)
            )
            btn.grid(row=2, column=i, padx=5, pady=5)
            self.player_holes.append(btn)
        
        # Titre joueur (Vous)
        self.player_label = tk.Label(
            board_frame,
            text="YOU",
            font=("Arial", 18, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        self.player_label.grid(row=3, column=0, columnspan=7, pady=10)
        
        # Score joueur
        self.player_score = tk.Label(
            board_frame,
            text="0",
            font=("Arial", 28, "bold"),
            bg="#2ECC71",  # Vert
            fg="white",
            width=4,
            height=2,
            relief="sunken"
        )
        self.player_score.grid(row=3, column=7, padx=10)
        
        # ---------- INFORMATIONS DE JEU ----------
        info_frame = tk.Frame(self.window, bg="#2C3E50")
        info_frame.grid(row=2, column=0, columnspan=8, pady=20)
        
        # Game Mode
        tk.Label(
            info_frame,
            text="GAME MODE",
            font=("Arial", 12, "bold"),
            bg="#2C3E50",
            fg="#BDC3C7"
        ).grid(row=0, column=0, padx=10)
        
        self.mode_label = tk.Label(
            info_frame,
            text="Standard7×2",
            font=("Arial", 12),
            bg="#34495E",
            fg="white",
            width=15,
            relief="flat"
        )
        self.mode_label.grid(row=0, column=1, padx=10)
        
        # Difficulty
        tk.Label(
            info_frame,
            text="DIFFICULTY",
            font=("Arial", 12, "bold"),
            bg="#2C3E50",
            fg="#BDC3C7"
        ).grid(row=0, column=2, padx=10)
        
        self.difficulty_label = tk.Label(
            info_frame,
            text="Medium",
            font=("Arial", 12),
            bg="#F39C12",  # Orange
            fg="white",
            width=10,
            relief="flat"
        )
        self.difficulty_label.grid(row=0, column=3, padx=10)
        
        # Seeds Type
        tk.Label(
            info_frame,
            text="SEEDS",
            font=("Arial", 12, "bold"),
            bg="#2C3E50",
            fg="#BDC3C7"
        ).grid(row=0, column=4, padx=10)
        
        self.seeds_label = tk.Label(
            info_frame,
            text="Gemstones",
            font=("Arial", 12),
            bg="#9B59B6",  # Violet
            fg="white",
            width=12,
            relief="flat"
        )
        self.seeds_label.grid(row=0, column=5, padx=10)
        
        # ---------- CONTROLES ----------
        controls_frame = tk.Frame(self.window, bg="#2C3E50")
        controls_frame.grid(row=3, column=0, columnspan=8, pady=10)
        
        # Boutons de contrôle
        buttons = [
            ("UNDO", "#95A5A6"),
            ("HINT", "#3498DB"),
            ("SETTINGS", "#7F8C8D"),
            ("NEW GAME", "#E74C3C")
        ]
        
        for i, (text, color) in enumerate(buttons):
            btn = tk.Button(
                controls_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                width=12,
                height=2,
                relief="raised"
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Label tour actuel
        self.turn_label = tk.Label(
            self.window,
            text="YOUR TURN",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="#F1C40F"  # Jaune
        )
        self.turn_label.grid(row=4, column=0, columnspan=8, pady=10)
    
    def human_move(self, hole_index):
        """Gère le coup du joueur humain"""
        if self.game.current_player == 0:  # C'est bien le tour du joueur
            self.game.make_move(hole_index)
            self.update_display()
            
            # Vérifier si la partie continue
            if not self.game.is_game_over():
                # L'IA joue après un délai
                self.turn_label.config(text="AI THINKING...")
                self.window.after(1000, self.ai_move)
    
    def ai_move(self):
        """L'IA joue son coup"""
        if self.game.current_player == 1:  # C'est le tour de l'IA
            best_move = self.ai.get_best_move(self.game)
            if best_move is not None:
                self.game.make_move(best_move)
                self.update_display()
    
    def update_display(self):
        """Met à jour l'affichage du plateau"""
        # Mettre à jour les trous adversaire
        for i in range(7):
            self.opponent_holes[i]["text"] = str(self.game.board[8 + i])
        
        # Mettre à jour les trous joueur
        for i in range(7):
            self.player_holes[i]["text"] = str(self.game.board[1 + i])
        
        # Mettre à jour les scores
        self.opponent_score["text"] = str(self.game.board[0])  # Home adversaire
        self.player_score["text"] = str(self.game.board[8])    # Home joueur
        
        # Mettre à jour le label de tour
        if self.game.current_player == 0:
            self.turn_label.config(text="YOUR TURN", fg="#2ECC71")  # Vert
        else:
            self.turn_label.config(text="OPPONENT'S TURN", fg="#E74C3C")  # Rouge
        
        # Désactiver/activer les boutons selon le tour
        for i in range(7):
            if self.game.current_player == 0:
                self.player_holes[i]["state"] = "normal"
                self.player_holes[i]["bg"] = "#3498DB"  # Bleu normal
            else:
                self.player_holes[i]["state"] = "disabled"
                self.player_holes[i]["bg"] = "#2980B9"  # Bleu foncé désactivé
    
    def run(self):
        """Lance l'application"""
        self.window.mainloop()

# Pour lancer le jeu
if __name__ == "__main__":
    app = CongklakGUI()
    app.run()