🎮 Congklak AI - Implémentation de Minimax avec Alpha-Beta Pruning
Intelligence Artificielle pour le jeu traditionnel Congklak
Projet universitaire M1 IA - Implémentation complète des règles de recherche


============================================================
📋 TABLE DES MATIÈRES
============================================================
🎯 Objectifs du Projet
⚙️ Règles du Jeu Implémentées
🧠 Algorithmes d'IA
📁 Structure des Fichiers
🚀 Installation et Exécution
🎛️ Interface Utilisateur
📊 Résultats et Performances
📚 Références Académiques

============================================================
🎯 OBJECTIFS DU PROJET
============================================================
Ce projet vise à digitaliser le jeu traditionnel Congklak tout en
implémentant une Intelligence Artificielle avancée basée sur la recherche.

Objectifs principaux :
- Créer une application de jeu utilisant l’algorithme Minimax
  avec élagage Alpha-Beta
- Développer une IA performante capable de prendre des décisions
  rapides (≤ 5 secondes)
- Implémenter plusieurs niveaux de difficulté
- Préserver le patrimoine culturel indonésien à travers le numérique

============================================================
⚙️ RÈGLES DU JEU IMPLÉMENTÉES
============================================================
L’implémentation suit exactement les 8 règles définies dans l’article :

1. Plateau avec 16 trous (14 petits + 2 homes)            
2. 7 billes par trou (homes vides au départ)              
3. Distribution anti-horaire (sowing)                     
4. Rejouer si la dernière bille tombe dans son home       
5. Capture (shooting) si dernière bille dans trou vide   
6. Continuer si dernière bille dans trou occupé           
7. Changement de joueur si aucun coup possible            
8. Fin de jeu lorsque tous les trous sont vides           

Particularité :
La règle 5 (capture) est entièrement fonctionnelle,
ce qui constitue une amélioration par rapport à de nombreuses
implémentations existantes.

============================================================
🧠 ALGORITHMES D'IA
============================================================
Minimax avec Élagage Alpha-Beta

La complexité est réduite de :
O(b^m)  →  O(√(b^m))

Comparaison :
- Minimax standard :
  - Nœuds explorés : ~36
  - Temps de décision : ~1.5s
  - Efficacité : moyenne

- Alpha-Beta Pruning :
  - Nœuds explorés : ~3
  - Temps de décision : ~0.3s
  - Efficacité : excellente

Niveaux de difficulté :
- FACILE     : profondeur 2  (< 0.5s)
- MOYEN      : profondeur 4  (~ 1.0s)
- DIFFICILE  : profondeur 6  (~ 1.5s)

============================================================
📁 STRUCTURE DES FICHIERS
============================================================
congklak-ia/
├── gui.py            : Interface graphique PyGame
├── game.py           : Logique complète du jeu
├── ai.py             : IA Minimax + Alpha-Beta
├── main.py           : Point d’entrée principal
└── 619-Article.pdf   : Article académique de référence

============================================================
📜 DESCRIPTION DES SCRIPTS
============================================================
gui.py :
- Interface graphique PyGame
- Affichage du plateau
- Gestion souris / clavier
- Boutons de contrôle et scores

game.py :
- Implémentation des 8 règles
- Système de capture (règle 5)
- Gestion des tours
- Détection de fin de partie
- Fonction d’évaluation

ai.py :
- Algorithme Minimax avec Alpha-Beta
- Trois niveaux de difficulté
- Heuristiques d’évaluation
- Optimisation mémoire

main.py :
- Lanceur principal
- Initialisation du jeu
- Gestion des erreurs

============================================================
🚀 INSTALLATION ET EXÉCUTION
============================================================
Prérequis :
- Python 3.x
- PyGame

Installation :
pip install pygame

Lancement :
python main.py
ou
python gui.py

============================================================
🎯 RACCOURCIS CLAVIER
============================================================
1 / 2 / 3  : Changer difficulté
N          : Nouvelle partie
ECHAP      : Quitter le jeu
Clic souris: Sélectionner un trou

============================================================
🎛️ INTERFACE UTILISATEUR
============================================================
Fonctionnalités :
- Homes colorés (IA / joueur)
- Trous interactifs
- Animation pendant la réflexion de l’IA
- Messages de fin de partie
- Boutons accessibles

============================================================
📊 RÉSULTATS ET PERFORMANCES
============================================================
Tous les temps de décision sont inférieurs à 2 secondes.
Objectif initial (< 5s) largement atteint.

Tests fonctionnels :
- Capture (règle 5)        
- Rejouer (règle 4)        
- Fin de partie            
- Multi-difficultés        

============================================================
📚 RÉFÉRENCES ACADÉMIQUES
============================================================
"Implementation of Minimax with Alpha-Beta Pruning as Computer Player
in Congklak"

Brian Sumali
Ivan Michael Siregar
Rosalina

President University, Indonesia
Conference Proceedings, 2018

============================================================
👥 CONTRIBUTIONS ET PERSPECTIVES
============================================================
Améliorations apportées :
- Capture complète (règle 5)
- Interface moderne avec PyGame
- Optimisations Alpha-Beta
- Documentation complète en français

Perspectives futures :
- Apprentissage par renforcement
- Mode multijoueur en réseau
- Statistiques de parties
- Tutoriel intégré

============================================================
🎓 Projet académique M1 Intelligence Artificielle
📅 Janvier 2026
🏆 Toutes les règles du Congklak traditionnel sont respectées
============================================================
