# settings.py - Paramètres de design
class GameDesign:
    """Paramètres de design du jeu"""
    
    # Couleurs principales
    COLORS = {
        "background": "#2C3E50",
        "board_bg": "#34495E",
        "text_light": "#ECF0F1",
        "text_dark": "#2C3E50",
        
        # Joueurs
        "player": {
            "bg": "#3498DB",      # Bleu
            "disabled": "#2980B9",
            "score_bg": "#2ECC71"  # Vert
        },
        "opponent": {
            "bg": "#16A085",      # Vert turquoise
            "score_bg": "#E74C3C"  # Rouge
        },
        
        # UI Elements
        "difficulty": "#F39C12",  # Orange
        "seeds": "#9B59B6",       # Violet
        "turn_indicator": "#F1C40F",  # Jaune
        
        # Boutons
        "buttons": {
            "undo": "#95A5A6",
            "hint": "#3498DB",
            "settings": "#7F8C8D",
            "new_game": "#E74C3C"
        }
    }
    
    # Polices
    FONTS = {
        "title": ("Arial", 32, "bold"),
        "player_name": ("Arial", 18, "bold"),
        "score": ("Arial", 28, "bold"),
        "hole": ("Arial", 16, "bold"),
        "info_label": ("Arial", 12, "bold"),
        "info_value": ("Arial", 12),
        "turn": ("Arial", 14, "bold"),
        "button": ("Arial", 12, "bold")
    }
    
    # Dimensions
    DIMENSIONS = {
        "window": "900x700",
        "hole_width": 4,
        "hole_height": 2,
        "score_width": 4,
        "score_height": 2
    }
    
    # Texte
    TEXT = {
        "title": "CONGKLAK",
        "opponent": "OPPONENT",
        "player": "YOU",
        "game_mode": "Standard7×2",
        "seeds_type": "Gemstones",
        "buttons": ["UNDO", "HINT", "SETTINGS", "NEW GAME"],
        "turn": {
            "player": "YOUR TURN",
            "ai": "OPPONENT'S TURN",
            "thinking": "AI THINKING..."
        }
    }