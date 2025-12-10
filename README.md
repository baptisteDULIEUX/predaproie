# 🦊🐰 Simulation Multi-Agents : Modèle Proie-Prédateur

## 📋 Description

Projet de simulation stochastique en temps réel modélisant la dynamique de populations proies-prédateurs basée sur le modèle **Wa-Tor**. Développé dans le cadre du BUT 3 Informatique, ce projet combine :

- **Automates Cellulaires** : Grille discrète avec topologie torique
- **Modélisation Multi-Agents** : Comportements émergents à partir de règles simples
- **Analyse Mathématique** : Comparaison avec les équations de Lotka-Volterra

---

## 🎯 Objectifs Pédagogiques

1. **Architecture Logicielle** : Pattern MVC, POO, modularité
2. **Optimisation** : Utilisation de NumPy pour calculs vectorisés
3. **Visualisation** : Rendu temps réel avec Pygame
4. **Analyse de Données** : Statistiques et graphiques avec Matplotlib

---

## 🛠️ Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets)

### Étapes

```bash
# 1. Cloner le dépôt (ou décompresser l'archive)
cd predator_prey_simulation

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Lancer la simulation

```bash
python src/main.py
```

### Contrôles Interactifs

| Touche | Action |
|--------|--------|
| `ESPACE` | Pause / Reprise |
| `R` | Réinitialiser la simulation |
| `I` | Afficher/Masquer les infos |
| `↑` / `↓` | Accélérer / Ralentir |
| `ESC` | Quitter |

---

## ⚙️ Configuration

Tous les paramètres sont dans `src/config.py` :

```python
# Exemple de modifications
GRID_WIDTH = 150           # Grille plus grande
PROIE_INITIAL_COUNT = 800  # Plus de proies
PREDATEUR_INITIAL_ENERGY = 15  # Prédateurs plus résistants
```

### Paramètres Clés

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `GRID_WIDTH` / `GRID_HEIGHT` | Dimensions de la grille | 100 × 100 |
| `TORUS_MODE` | Topologie torique | `True` |
| `PROIE_REPRODUCTION_TIME` | Cycles avant reproduction (proies) | 3 |
| `PREDATEUR_ENERGY_GAIN` | Énergie gagnée en mangeant | 4 |
| `SIMULATION_SPEED` | Vitesse de simulation | 10 steps/sec |

---

## 📊 Analyse des Résultats

Après la simulation, les données sont exportées automatiquement :

```bash
# Fichier CSV généré
data/simulation_data.csv
```

### Générer les graphiques

```python
from src.analysis import analyze_from_csv

# Analyse complète avec graphiques
analyze_from_csv('data/simulation_data.csv')
```

### Types de Graphiques Produits

1. **Évolution Temporelle** : Courbes de population au fil du temps
2. **Espace de Phase** : Trajectoire (Proies vs Prédateurs)
3. **Comparaison Lotka-Volterra** : Simulation vs Théorie

---

## 🏗️ Architecture du Projet

```
predator_prey_simulation/
│
├── src/
│   ├── __init__.py          # Package principal
│   ├── config.py            # Configuration centralisée
│   ├── agents.py            # Classes Animal, Proie, Predateur
│   ├── grid.py              # Gestion de la grille torique
│   ├── simulation.py        # Moteur de simulation
│   ├── main.py              # Interface Pygame
│   └── analysis.py          # Analyse statistique
│
├── data/                    # Données exportées (CSV)
├── docs/                    # Documentation technique
├── tests/                   # Tests unitaires (à compléter)
│
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
```

---

## 🧪 Expérimentations Suggérées

### 1. Étude de Sensibilité

Modifiez un paramètre et observez l'impact :

```python
# Dans config.py
PROIE_REPRODUCTION_TIME = 2  # Reproduction plus rapide
```

**Questions** :
- À partir de quel seuil les proies deviennent-elles dominantes ?
- Quelle est la relation entre énergie initiale et survie des prédateurs ?

### 2. Détection de Cycles

Analysez la périodicité des oscillations :

```python
from src.analysis import SimulationAnalyzer

analyzer.compute_statistics()
# Affiche le nombre de pics détectés
```

### 3. Comparaison Théorique

Ajustez les paramètres de Lotka-Volterra :

```python
analyzer.compare_lotka_volterra(
    alpha=0.1,  # Taux de reproduction proies
    beta=0.02,  # Taux de prédation
    gamma=0.3,  # Mortalité prédateurs
    delta=0.01  # Efficacité conversion
)
```

---

## 📈 Résultats Attendus

### Scénarios Typiques

| Scénario | Paramètres | Résultat |
|----------|-----------|----------|
| **Équilibre** | Ratio 10:1 (proies:prédateurs) | Cycles stables |
| **Extinction Prédateurs** | Trop peu de proies | Famine collective |
| **Surpopulation Proies** | Pas assez de prédateurs | Croissance exponentielle |

### Indicateurs de Qualité

- **Cycles réguliers** : Bonne calibration
- **Amplitude constante** : Système stable
- **Phase shift** : Déphasage proies-prédateurs ~90° (attendu)

---

## 🔬 Aspects Mathématiques

### Modèle Discret (Wa-Tor)

- **Espace** : Grille torique Z² / (N × M)Z²
- **Voisinage** : Von Neumann (4-connexité)
- **Stochasticité** : Choix aléatoire parmi cases disponibles

### Modèle Continu (Lotka-Volterra)

```
dx/dt = αx - βxy   (Proies)
dy/dt = δxy - γy   (Prédateurs)
```

**Limitations** :
- Lotka-Volterra suppose un mélange homogène
- Wa-Tor introduit des effets de localité spatiale

---

## 🐛 Débogage

### Problèmes Courants

**Simulation trop lente ?**
```python
# Dans config.py
GRID_WIDTH = 50  # Réduire la taille
SHOW_GRID = False  # Désactiver la grille
```

**Extinction rapide ?**
```python
PREDATEUR_INITIAL_COUNT = 30  # Moins de prédateurs
PREDATEUR_ENERGY_LOSS = 0.5  # Métabolisme plus lent
```

**Pas de graphiques ?**
```bash
pip install matplotlib --upgrade
```

---

## 📚 Références

1. **Wa-Tor** : Dewdney, A.K. (1984) "Computer Recreations", Scientific American
2. **Lotka-Volterra** : Volterra, V. (1926) "Variazioni e fluttuazioni del numero d'individui"
3. **Automates Cellulaires** : Wolfram, S. (2002) "A New Kind of Science"

---

## 👨‍💻 Auteur & Licence

**Projet** : Simulation Multi-Agents Proie-Prédateur  
**Année** : 2024-2025  
**Formation** : BUT 3 Informatique  
**Licence** : MIT (pour usage pédagogique)

---

## 🎓 Pour Aller Plus Loin

### Extensions Possibles

- [ ] **3D** : Grille volumétrique (cube)
- [ ] **Multi-espèces** : Ajouter herbivores/plantes
- [ ] **Apprentissage** : IA pour stratégies de fuite/chasse
- [ ] **Parallélisation** : GPU avec CuPy
- [ ] **Web** : Interface HTML5 Canvas via PyScript

---

**Bon courage pour ton projet ! 🚀**
