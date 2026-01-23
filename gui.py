# gui.py - Interface graphique simple
import tkinter as tk
from game import CongklakGame
from ai import CongklakAI

class CongklakGUI:
    def __init__(self):
        self.game = CongklakGame()
        self.ai = CongklakAI(difficulty="medium")
        
        # Créer la fenêtre
        self.window = tk.Tk()
        self.window.title("Congklak AI")
        self.window.geometry("800x600")
        
        # Créer le plateau
        self.create_board()
        
        # Démarrer le jeu
        self.update_display()
    
    def create_board(self):
        """Crée les boutons pour chaque trou"""
        self.buttons = []
        
        # Home joueur 2 (en haut)
        self.home2 = tk.Label(self.window, text="0", font=("Arial", 24), width=5, height=2, relief="ridge")
        self.home2.grid(row=0, column=4)
        
        # Trous joueur 2 (7 trous, de droite à gauche)
        for i in range(7):
            btn = tk.Button(
                self.window, 
                text="7", 
                font=("Arial", 18),
                width=4, 
                height=2,
                command=lambda idx=8+i: self.human_move(idx)
            )
            btn.grid(row=1, column=6-i)
            self.buttons.append(btn)
        
        # Trous joueur 1 (7 trous, de gauche à droite)
        for i in range(7):
            btn = tk.Button(
                self.window, 
                text="7", 
                font=("Arial", 18),
                width=4, 
                height=2,
                command=lambda idx=1+i: self.human_move(idx)
            )
            btn.grid(row=2, column=i)
            self.buttons.append(btn)
        
        # Home joueur 1 (en bas)
        self.home1 = tk.Label(self.window, text="0", font=("Arial", 24), width=5, height=2, relief="ridge")
        self.home1.grid(row=3, column=4)
        
        # Label tour actuel
        self.turn_label = tk.Label(self.window, text="Tour: Joueur", font=("Arial", 16))
        self.turn_label.grid(row=4, column=0, columnspan=7)
    
    def human_move(self, hole_index):
        """Gère le coup du joueur humain"""
        if self.game.current_player == 0:  # C'est bien le tour du joueur
            self.game.make_move(hole_index)
            self.update_display()
            
            # Vérifier si la partie continue
            if not self.game.is_game_over():
                # L'IA joue après un délai
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
        # Mettre à jour les boutons avec le nombre de billes
        for i in range(14):
            if i < 7:  # Trous joueur 2 (indices 8-14 dans board)
                self.buttons[i]["text"] = str(self.game.board[8+i])
            else:       # Trous joueur 1 (indices 1-7 dans board)
                self.buttons[i]["text"] = str(self.game.board[i-6])
        
        # Mettre à jour les homes
        self.home1["text"] = str(self.game.board[0])
        self.home2["text"] = str(self.game.board[8])
        
        # Mettre à jour le label de tour
        player = "Joueur" if self.game.current_player == 0 else "IA"
        self.turn_label["text"] = f"Tour: {player}"
        
        # Désactiver les boutons si ce n'est pas le tour du joueur
        for i in range(7, 14):  # Boutons du joueur humain
            self.buttons[i]["state"] = "normal" if self.game.current_player == 0 else "disabled"
    
    def run(self):
        """Lance l'application"""
        self.window.mainloop()

# Pour lancer le jeu
if __name__ == "__main__":
    app = CongklakGUI()
    app.run()