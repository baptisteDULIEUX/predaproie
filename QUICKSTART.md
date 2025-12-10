# 🚀 Quick Start Guide

## Installation Rapide (3 minutes)

### Étape 1 : Préparation de l'environnement
```bash
# Cloner ou décompresser le projet
cd predator_prey_simulation

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# OU
venv\Scripts\activate  # Sur Windows
```

### Étape 2 : Installation des dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Lancement
```bash
# Test rapide (sans interface graphique)
python test_simulation.py

# Simulation complète avec interface Pygame
python src/main.py
```

---

## 🎮 Contrôles de Base

| Touche | Action |
|--------|--------|
| **ESPACE** | Pause / Reprise |
| **R** | Réinitialiser |
| **↑ / ↓** | Vitesse ±0.5x |
| **I** | Toggle infos |
| **ESC** | Quitter |

---

## ⚙️ Configuration Simple

Éditer `src/config.py` :

```python
# Pour une simulation plus rapide
GRID_WIDTH = 50
GRID_HEIGHT = 50

# Pour plus de proies
PROIE_INITIAL_COUNT = 1000

# Pour ralentir la reproduction
PROIE_REPRODUCTION_TIME = 5
```

**Sauvegarder et relancer** `python src/main.py`

---

## 📊 Générer les Graphiques

Après une simulation :

```bash
# Les données sont dans data/simulation_data.csv

# Analyse automatique
python -c "from src.analysis import analyze_from_csv; analyze_from_csv('data/simulation_data.csv')"
```

---

## 🧪 Expérimentations Automatiques

```bash
# Lance plusieurs simulations avec différents paramètres
python run_experiments.py
```

**Durée estimée** : 2-5 minutes
**Résultat** : Graphiques comparatifs dans `data/`

---

## 🐛 Problèmes Courants

### Erreur "No module named 'pygame'"
```bash
pip install pygame --break-system-packages
```

### Simulation trop lente
Dans `config.py` :
```python
GRID_WIDTH = 50  # Réduire la taille
SHOW_GRID = False  # Désactiver la grille
```

### Fenêtre Pygame ne s'affiche pas
Vérifier que vous n'êtes pas en SSH sans X11 forwarding.
Utiliser `test_simulation.py` en mode headless.

---

## 📁 Structure des Fichiers

```
predator_prey_simulation/
│
├── src/
│   ├── main.py          ← Lancer ceci pour l'interface
│   ├── config.py        ← Modifier les paramètres ici
│   └── ...
│
├── test_simulation.py   ← Test rapide sans interface
├── run_experiments.py   ← Expérimentations automatiques
└── README.md            ← Documentation complète
```

---

## 🎓 Pour le Rapport

### Éléments à inclure :
1. **Introduction** : Contexte mathématique (Wa-Tor, Lotka-Volterra)
2. **Architecture** : Diagrammes UML des classes
3. **Résultats** : Graphiques de `data/`
4. **Analyse** : Comparaison simulation vs théorie
5. **Conclusion** : Limites et extensions possibles

### Captures d'écran utiles :
- Interface Pygame en action
- Graphiques d'évolution temporelle
- Diagramme de phase
- Comparaison Lotka-Volterra

---

## 🚀 Prochaines Étapes

1. **Tester** : Lancer `python src/main.py`
2. **Expérimenter** : Modifier `config.py`
3. **Analyser** : Générer les graphiques
4. **Documenter** : Ajouter vos observations dans un rapport

**Bon courage ! 🎉**

---

## 📞 Support

En cas de problème :
1. Vérifier `README.md` (documentation complète)
2. Lire `docs/calibration_guide.md` (aide paramétrage)
3. Vérifier les dépendances : `pip list`
