"""
Configuration centralisée du projet de simulation Proie-Prédateur
Tous les paramètres sont regroupés ici pour faciliter l'expérimentation
"""

# ==================== PARAMÈTRES DE LA GRILLE ====================
GRID_WIDTH = 100          # Largeur de la grille
GRID_HEIGHT = 100         # Hauteur de la grille
TORUS_MODE = True         # True = topologie torique (pas d'effets de bord)

# ==================== PARAMÈTRES DES PROIES ====================
PROIE_INITIAL_COUNT = 10      # Nombre initial de proies
PROIE_REPRODUCTION_TIME = 3      # Cycles avant reproduction
PROIE_COLOR = (0, 255, 0)        # Vert
PROIE_SYMBOL = 1                 # Identifiant dans la grille

# ==================== PARAMÈTRES DES PRÉDATEURS ====================
PREDATEUR_INITIAL_COUNT = 100  # Nombre initial de prédateurs
PREDATEUR_REPRODUCTION_TIME = 8  # Cycles avant reproduction
PREDATEUR_INITIAL_ENERGY = 10    # Énergie de départ
PREDATEUR_ENERGY_GAIN = 4        # Énergie gagnée en mangeant une proie
PREDATEUR_ENERGY_LOSS = 1        # Énergie perdue par déplacement
PREDATEUR_COLOR = (255, 0, 0)    # Rouge
PREDATEUR_SYMBOL = 2             # Identifiant dans la grille

# ==================== PARAMÈTRES DE SIMULATION ====================
SIMULATION_SPEED = 5           # Pas de simulation par seconde (FPS logique)
MAX_STEPS = 5000                 # Nombre maximum de cycles (0 = infini)
RANDOM_SEED = None               # Seed pour reproductibilité (None = aléatoire)

# ==================== PARAMÈTRES D'AFFICHAGE ====================
WINDOW_WIDTH = 800               # Largeur de la fenêtre Pygame
WINDOW_HEIGHT = 800              # Hauteur de la fenêtre
CELL_SIZE = max(1, WINDOW_WIDTH // GRID_WIDTH)  # Taille d'une cellule en pixels
FPS = 60                     # Rafraîchissement de l'affichage
SHOW_GRID = False                # Afficher la grille (ralentit si True)
BACKGROUND_COLOR = (0, 0, 0)     # Noir
EMPTY_COLOR = (20, 20, 20)       # Gris très foncé pour les cases vides

# ==================== PARAMÈTRES D'ANALYSE ====================
RECORD_DATA = True               # Enregistrer les données de population
DATA_RECORD_INTERVAL = 1         # Enregistrer toutes les N étapes
EXPORT_CSV = True                # Exporter en CSV à la fin
SHOW_PLOTS = True                # Afficher les graphiques Matplotlib
