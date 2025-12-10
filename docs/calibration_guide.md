# 🎛️ Guide de Calibration des Paramètres

## Objectif
Ce guide vous aide à ajuster les paramètres dans `src/config.py` pour obtenir différents comportements de simulation.

---

## 📊 Scénarios Prédéfinis

### 1. 🔵 Équilibre Stable (Cycles de Lotka-Volterra)

**Configuration recommandée :**
```python
GRID_WIDTH = 100
GRID_HEIGHT = 100
PROIE_INITIAL_COUNT = 800
PREDATEUR_INITIAL_COUNT = 80
PROIE_REPRODUCTION_TIME = 4
PREDATEUR_REPRODUCTION_TIME = 10
PREDATEUR_INITIAL_ENERGY = 15
PREDATEUR_ENERGY_GAIN = 5
PREDATEUR_ENERGY_LOSS = 1
```

**Résultat attendu :**
- Cycles réguliers de 200-400 steps
- Oscillations avec déphasage proies-prédateurs
- Pas d'extinction (système stable)

---

### 2. 🟢 Explosion de Proies

**Configuration :**
```python
PREDATEUR_INITIAL_COUNT = 10  # Très peu de prédateurs
PROIE_REPRODUCTION_TIME = 2   # Reproduction rapide
PREDATEUR_ENERGY_LOSS = 2     # Prédateurs affaiblis
```

**Résultat attendu :**
- Croissance exponentielle des proies
- Extinction probable des prédateurs
- Saturation de la grille

---

### 3. 🔴 Extinction Rapide

**Configuration :**
```python
PREDATEUR_INITIAL_COUNT = 100  # Trop de prédateurs
PROIE_INITIAL_COUNT = 200      # Pas assez de proies
PREDATEUR_ENERGY_GAIN = 2      # Faible gain énergétique
```

**Résultat attendu :**
- Disparition des proies en <50 steps
- Famine collective des prédateurs
- Extinction totale

---

### 4. 🟡 Coexistence Précaire

**Configuration :**
```python
GRID_WIDTH = 150
GRID_HEIGHT = 150
PROIE_INITIAL_COUNT = 1500
PREDATEUR_INITIAL_COUNT = 100
PROIE_REPRODUCTION_TIME = 5
PREDATEUR_REPRODUCTION_TIME = 12
PREDATEUR_INITIAL_ENERGY = 20
PREDATEUR_ENERGY_GAIN = 6
PREDATEUR_ENERGY_LOSS = 1
```

**Résultat attendu :**
- Équilibre fragile
- Longues périodes de stabilité
- Risque d'extinction aléatoire

---

## 🔬 Étude de Sensibilité

### Expérience 1 : Impact du taux de reproduction des proies

**Méthode :**
1. Fixer tous les paramètres
2. Faire varier `PROIE_REPRODUCTION_TIME` : [1, 2, 3, 4, 5, 6]
3. Lancer 10 simulations pour chaque valeur
4. Mesurer : durée avant extinction, amplitude des cycles

**Question :** À partir de quelle valeur le système devient instable ?

---

### Expérience 2 : Ratio proies/prédateurs optimal

**Méthode :**
1. Tester différents ratios : 5:1, 10:1, 15:1, 20:1, 25:1
2. Garder la densité totale constante (ex: 900 agents)
3. Mesurer le temps de survie du système

**Hypothèse :** Ratio optimal autour de 10:1 à 15:1

---

### Expérience 3 : Taille de la grille (effets de densité)

**Méthode :**
1. Grilles testées : 50×50, 100×100, 150×150, 200×200
2. Conserver la même densité d'agents (ex: 10% de la surface)
3. Observer l'impact sur la stabilité

**Hypothèse :** Les grandes grilles favorisent la coexistence (moins de rencontres aléatoires)

---

## 📐 Formules Utiles

### Densité de population
```
Densité_proies = PROIE_INITIAL_COUNT / (GRID_WIDTH × GRID_HEIGHT)
```
**Recommandation :** 0.05 à 0.15 (5% à 15% de remplissage)

### Ratio énergétique
```
Ratio = PREDATEUR_ENERGY_GAIN / PREDATEUR_ENERGY_LOSS
```
**Recommandation :** Ratio ≥ 3 pour survie des prédateurs

### Temps de doublement (proies)
```
T_double ≈ PROIE_REPRODUCTION_TIME × ln(2) / ln(1 + taux_survie)
```

---

## 🎯 Checklist de Calibration

Avant de lancer une simulation longue :

- [ ] Ratio proies:prédateurs entre 8:1 et 15:1
- [ ] Densité totale < 20% de la grille
- [ ] `PREDATEUR_ENERGY_GAIN` ≥ 3 × `PREDATEUR_ENERGY_LOSS`
- [ ] `PREDATEUR_REPRODUCTION_TIME` > 2 × `PROIE_REPRODUCTION_TIME`
- [ ] Grille suffisamment grande (min 50×50)

---

## ⚠️ Erreurs Courantes

### Problème : Extinction immédiate
**Cause :** Trop de prédateurs ou énergie initiale trop faible
**Solution :** Augmenter `PREDATEUR_INITIAL_ENERGY` à 15-20

### Problème : Explosions chaotiques
**Cause :** Reproduction des proies trop rapide
**Solution :** Augmenter `PROIE_REPRODUCTION_TIME` à 4-5

### Problème : Simulation trop lente
**Cause :** Grille trop grande ou affichage de la grille activé
**Solution :** Réduire la taille ou mettre `SHOW_GRID = False`

---

## 📈 Validation des Résultats

Un bon paramétrage doit produire :

1. **Durée** : Au moins 1000 steps sans extinction
2. **Cycles** : 3-5 pics détectés pour chaque espèce
3. **Amplitude** : Max/Min ≤ 10 (pas d'explosions)
4. **Phase** : Déphasage visible entre proies et prédateurs

---

## 🔬 Pour Aller Plus Loin

### Ajout de bruit stochastique
```python
# Dans agents.py, méthode reproduce()
if random.random() < 0.95:  # 95% de réussite
    return Proie(...)
```

### Mutation des paramètres
```python
# Variation aléatoire ±10%
energy_gain = PREDATEUR_ENERGY_GAIN * random.uniform(0.9, 1.1)
```

### Introduction d'événements catastrophiques
```python
# Dans simulation.py
if self.step_count == 500:
    # Éliminer 50% des proies (catastrophe naturelle)
    ...
```

---

**Bon courage pour tes expérimentations ! 🚀**
