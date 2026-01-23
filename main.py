from gui import CongklakPygameGUI

def main():
    print("=" * 50)
    print("        JEU CONGKLAK - NOUVELLE INTERFACE")
    print("=" * 50)
    print("Contrôles :")
    print("- Clic sur vos trous (ligne du BAS)")
    print("- 1, 2, 3 : Changer difficulté (Facile, Moyen, Difficile)")
    print("- N : Nouvelle partie")
    print("- ESC : Quitter")
    print("=" * 50)
    print("IMPORTANT :")
    print("- Votre home est à DROITE (bleu)")
    print("- L'home de l'IA est à GAUCHE (rouge)")
    print("- Les trous vides sont grisés")
    print("- L'IA joue automatiquement après votre coup")
    print("=" * 50)
    
    app = CongklakPygameGUI()
    app.run()

if __name__ == "__main__":
    main()