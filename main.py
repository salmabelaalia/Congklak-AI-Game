# main.py
from gui import CongklakGUI

def main():
    print("Lancement du jeu Congklak avec IA...")
    print("Règles du jeu:")
    print("- Cliquez sur un de vos trous pour distribuer les billes")
    print("- L'IA répondra automatiquement")
    print("- Le jeu se termine quand tous les trous sont vides")
    print()
    
    app = CongklakGUI()
    app.run()

if __name__ == "__main__":
    main()