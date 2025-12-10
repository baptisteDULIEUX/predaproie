"""
Script d'expérimentation automatique.
Lance plusieurs simulations avec différents paramètres pour étude de sensibilité.
"""

import sys
sys.path.insert(0, '/home/claude/predator_prey_simulation')

import numpy as np
import matplotlib.pyplot as plt
from src import Simulation
from src import config
import time

# Désactiver l'affichage Pygame pour mode batch
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'


class ExperimentRunner:
    """
    Gestionnaire d'expériences multiples.
    Permet de tester systématiquement différentes configurations.
    """
    
    def __init__(self):
        self.results = []
    
    def run_experiment(self, param_name, param_values, n_runs=3, max_steps=1000):
        """
        Lance une série de simulations en faisant varier un paramètre.
        
        Args:
            param_name: Nom du paramètre à varier (ex: 'PROIE_REPRODUCTION_TIME')
            param_values: Liste des valeurs à tester
            n_runs: Nombre de répétitions par valeur (pour moyenner)
            max_steps: Nombre maximum de steps par simulation
        
        Returns:
            Dictionnaire de résultats
        """
        print(f"\n🔬 EXPÉRIENCE : Impact de {param_name}")
        print("=" * 70)
        
        # Sauvegarder la valeur originale
        original_value = getattr(config, param_name)
        
        results = {
            'param_name': param_name,
            'param_values': param_values,
            'survival_times': [],
            'max_proies': [],
            'max_predateurs': [],
            'cycles_detected': []
        }
        
        for value in param_values:
            print(f"\n📊 Test avec {param_name} = {value}")
            
            survival_times_run = []
            max_proies_run = []
            max_pred_run = []
            cycles_run = []
            
            # Répétitions pour statistiques
            for run in range(n_runs):
                # Modifier le paramètre
                setattr(config, param_name, value)
                config.MAX_STEPS = max_steps
                config.RECORD_DATA = True
                
                # Nouvelle simulation
                sim = Simulation()
                
                # Exécution
                for step in range(max_steps):
                    sim.step()
                    
                    if sim.is_extinction():
                        break
                
                # Collecte des métriques
                survival_times_run.append(sim.step_count)
                max_proies_run.append(max(sim.history['proies']) if sim.history['proies'] else 0)
                max_pred_run.append(max(sim.history['predateurs']) if sim.history['predateurs'] else 0)
                
                # Détection de cycles simplifiée
                proies = np.array(sim.history['proies'])
                if len(proies) > 10:
                    from scipy.signal import find_peaks
                    peaks, _ = find_peaks(proies, distance=10)
                    cycles_run.append(len(peaks))
                else:
                    cycles_run.append(0)
                
                print(f"   Run {run+1}/{n_runs}: {sim.step_count} steps, "
                      f"Proies_max={max(sim.history['proies'])}, "
                      f"Cycles={cycles_run[-1]}")
            
            # Moyennes
            results['survival_times'].append(np.mean(survival_times_run))
            results['max_proies'].append(np.mean(max_proies_run))
            results['max_predateurs'].append(np.mean(max_pred_run))
            results['cycles_detected'].append(np.mean(cycles_run))
        
        # Restaurer la valeur originale
        setattr(config, param_name, original_value)
        
        self.results.append(results)
        return results
    
    def plot_results(self, results, save_path=None):
        """
        Génère des graphiques de l'expérience.
        
        Args:
            results: Dictionnaire de résultats
            save_path: Chemin de sauvegarde (optionnel)
        """
        param_name = results['param_name']
        param_values = results['param_values']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"Étude de Sensibilité : {param_name}", fontsize=16, fontweight='bold')
        
        # Graphique 1 : Temps de survie
        axes[0, 0].plot(param_values, results['survival_times'], 'o-', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel(param_name, fontsize=11)
        axes[0, 0].set_ylabel('Temps de survie (steps)', fontsize=11)
        axes[0, 0].set_title('Durabilité du système', fontsize=12)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Graphique 2 : Populations maximales
        axes[0, 1].plot(param_values, results['max_proies'], 'o-', label='Proies', 
                       color='green', linewidth=2, markersize=8)
        axes[0, 1].plot(param_values, results['max_predateurs'], 's-', label='Prédateurs', 
                       color='red', linewidth=2, markersize=8)
        axes[0, 1].set_xlabel(param_name, fontsize=11)
        axes[0, 1].set_ylabel('Population maximale', fontsize=11)
        axes[0, 1].set_title('Pics de population', fontsize=12)
        axes[0, 1].legend(fontsize=10)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Graphique 3 : Nombre de cycles
        axes[1, 0].bar(param_values, results['cycles_detected'], color='steelblue', alpha=0.7)
        axes[1, 0].set_xlabel(param_name, fontsize=11)
        axes[1, 0].set_ylabel('Nombre de cycles détectés', fontsize=11)
        axes[1, 0].set_title('Stabilité dynamique', fontsize=12)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Graphique 4 : Ratio Max Proies / Max Prédateurs
        ratios = [p / max(pr, 1) for p, pr in zip(results['max_proies'], results['max_predateurs'])]
        axes[1, 1].plot(param_values, ratios, 'o-', color='purple', linewidth=2, markersize=8)
        axes[1, 1].axhline(y=10, color='red', linestyle='--', label='Ratio optimal (~10:1)')
        axes[1, 1].set_xlabel(param_name, fontsize=11)
        axes[1, 1].set_ylabel('Ratio Proies/Prédateurs', fontsize=11)
        axes[1, 1].set_title('Équilibre des populations', fontsize=12)
        axes[1, 1].legend(fontsize=9)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n✅ Graphique sauvegardé : {save_path}")
        else:
            plt.show()


def main():
    """Lancement des expériences prédéfinies."""
    
    print("🚀 LANCEMENT DES EXPÉRIMENTATIONS AUTOMATIQUES")
    print("=" * 70)
    
    runner = ExperimentRunner()
    
    # Expérience 1 : Impact du temps de reproduction des proies
    print("\n" + "="*70)
    print("EXPÉRIENCE 1 : Temps de reproduction des proies")
    print("="*70)
    
    results1 = runner.run_experiment(
        param_name='PROIE_REPRODUCTION_TIME',
        param_values=[2, 3, 4, 5, 6, 7],
        n_runs=3,
        max_steps=1000
    )
    
    runner.plot_results(
        results1,
        save_path='/home/claude/predator_prey_simulation/data/exp1_proie_reproduction.png'
    )
    
    # Expérience 2 : Impact de l'énergie initiale des prédateurs
    print("\n" + "="*70)
    print("EXPÉRIENCE 2 : Énergie initiale des prédateurs")
    print("="*70)
    
    results2 = runner.run_experiment(
        param_name='PREDATEUR_INITIAL_ENERGY',
        param_values=[5, 10, 15, 20, 25],
        n_runs=3,
        max_steps=1000
    )
    
    runner.plot_results(
        results2,
        save_path='/home/claude/predator_prey_simulation/data/exp2_predateur_energy.png'
    )
    
    # Résumé final
    print("\n" + "="*70)
    print("✅ EXPÉRIMENTATIONS TERMINÉES")
    print("="*70)
    print("\n📊 Résultats disponibles dans le dossier data/")
    print("📈 Graphiques générés :")
    print("   • exp1_proie_reproduction.png")
    print("   • exp2_predateur_energy.png")


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed = time.time() - start_time
    print(f"\n⏱️ Temps total : {elapsed:.1f} secondes")
