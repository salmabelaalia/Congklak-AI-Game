# main.py - Version avec design amélioré
from gui import CongklakGUI

def display_welcome():
    """Affiche un message de bienvenue stylisé"""
    print("╔══════════════════════════════════════════════════════╗")
    print("║           CONGKLAK AI - GAME LAUNCHER               ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  Traditional Indonesian Board Game                  ║")
    print("║  with Minimax AI Implementation                     ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  RULES:                                             ║")
    print("║  • Click on your holes to distribute seeds          ║")
    print("║  • AI responds automatically                        ║")
    print("║  • Game ends when all holes are empty               ║")
    print("║  • Capture opponent's seeds for bonus points        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("🎮 Starting game with modern interface...")
    print("⚙️  Difficulty: Medium | Mode: Standard 7×2 | Seeds: Gemstones")
    print()

def main():
    display_welcome()
    
    try:
        app = CongklakGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error launching game: {e}")
        print("Please ensure all files are in the same directory.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()