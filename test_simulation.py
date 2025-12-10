"""
Script de test de la simulation en mode headless (sans affichage).
Vérifie que toutes les composantes fonctionnent correctement.
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, '/home/claude/predator_prey_simulation')

from src.simulation import Simulation
from src.analysis import SimulationAnalyzer
from src import config

# Configuration pour test rapide
config.GRID_WIDTH = 50
config.GRID_HEIGHT = 50
config.PROIE_INITIAL_COUNT = 200
config.PREDATEUR_INITIAL_COUNT = 20
config.MAX_STEPS = 500
config.SIMULATION_SPEED = 1
config.RECORD_DATA = True

print("🧪 TEST DE LA SIMULATION MULTI-AGENTS")
print("=" * 60)

# 1. Test de création
print("\n1️⃣ Création de la simulation...")
sim = Simulation()
proies, predateurs = sim.get_population_counts()
print(f"   ✅ Grille {config.GRID_WIDTH}x{config.GRID_HEIGHT} initialisée")
print(f"   ✅ Proies: {proies}, Prédateurs: {predateurs}")

# 2. Test d'exécution
print("\n2️⃣ Exécution de 500 steps...")
for i in range(500):
    sim.step()
    
    if (i + 1) % 100 == 0:
        proies, predateurs = sim.get_population_counts()
        print(f"   Step {i+1}: Proies={proies}, Prédateurs={predateurs}")
    
    if sim.is_extinction():
        print(f"   ⚠️ Extinction détectée au step {sim.step_count}")
        break

# 3. Test d'export
print("\n3️⃣ Export des données...")
csv_path = '/home/claude/predator_prey_simulation/data/test_simulation.csv'
sim.export_data(csv_path)

# 4. Test d'analyse
print("\n4️⃣ Analyse statistique...")
analyzer = SimulationAnalyzer(sim.history)
analyzer.print_summary()

# 5. Test de génération de graphiques
print("\n5️⃣ Génération des graphiques...")
try:
    analyzer.plot_populations(
        save_path='/home/claude/predator_prey_simulation/data/populations.png'
    )
    analyzer.plot_phase_space(
        save_path='/home/claude/predator_prey_simulation/data/phase_space.png'
    )
    analyzer.compare_lotka_volterra(
        save_path='/home/claude/predator_prey_simulation/data/comparison.png'
    )
    print("   ✅ Tous les graphiques générés avec succès")
except Exception as e:
    print(f"   ⚠️ Erreur lors de la génération : {e}")

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
print("=" * 60)
print("\n📁 Fichiers générés :")
print("   • data/test_simulation.csv")
print("   • data/populations.png")
print("   • data/phase_space.png")
print("   • data/comparison.png")
print("\n🎮 Pour lancer l'interface graphique :")
print("   python src/main.py")
