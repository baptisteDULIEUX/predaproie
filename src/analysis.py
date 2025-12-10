"""
Module d'analyse statistique et visualisation des résultats.
Comparaison avec le modèle de Lotka-Volterra.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, List


class SimulationAnalyzer:
    """
    Outil d'analyse pour comparer les résultats simulés
    avec les prédictions théoriques de Lotka-Volterra.
    """
    
    def __init__(self, history: Dict[str, List]):
        """
        Initialise l'analyseur avec les données historiques.
        
        Args:
            history: Dictionnaire contenant 'step', 'proies', 'predateurs'
        """
        self.history = history
        self.steps = np.array(history['step'])
        self.proies = np.array(history['proies'])
        self.predateurs = np.array(history['predateurs'])
    
    def plot_populations(self, save_path: str = None):
        """
        Graphique d'évolution temporelle des populations.
        
        Args:
            save_path: Chemin pour sauvegarder l'image (None = affichage)
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(self.steps, self.proies, label='Proies', color='green', linewidth=2)
        ax.plot(self.steps, self.predateurs, label='Prédateurs', color='red', linewidth=2)
        
        ax.set_xlabel('Étapes de simulation', fontsize=12)
        ax.set_ylabel('Population', fontsize=12)
        ax.set_title('Évolution des Populations (Modèle Wa-Tor)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"✅ Graphique sauvegardé : {save_path}")
        else:
            plt.show()
    
    def plot_phase_space(self, save_path: str = None):
        """
        Diagramme de phase (Proies vs Prédateurs).
        Révèle les cycles de Lotka-Volterra.
        
        Args:
            save_path: Chemin de sauvegarde
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Tracé avec gradient de couleur (temps)
        scatter = ax.scatter(
            self.proies, self.predateurs,
            c=self.steps, cmap='viridis',
            alpha=0.6, s=10
        )
        
        # Point de départ et d'arrivée
        ax.plot(self.proies[0], self.predateurs[0], 'go', markersize=10, label='Début')
        ax.plot(self.proies[-1], self.predateurs[-1], 'rx', markersize=10, label='Fin')
        
        ax.set_xlabel('Population de Proies', fontsize=12)
        ax.set_ylabel('Population de Prédateurs', fontsize=12)
        ax.set_title('Espace de Phase (Trajectoire du Système)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Barre de couleur pour le temps
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Étape', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"✅ Diagramme de phase sauvegardé : {save_path}")
        else:
            plt.show()
    
    def compare_lotka_volterra(self, alpha=0.1, beta=0.02, gamma=0.3, delta=0.01, 
                                save_path: str = None):
        """
        Compare la simulation avec le modèle continu de Lotka-Volterra.
        
        Équations différentielles :
        dx/dt = α·x - β·x·y  (Proies)
        dy/dt = δ·x·y - γ·y  (Prédateurs)
        
        Args:
            alpha: Taux de reproduction des proies
            beta: Taux de prédation
            gamma: Taux de mortalité des prédateurs
            delta: Efficacité de conversion proie->prédateur
            save_path: Chemin de sauvegarde
        """
        def lotka_volterra(state, t):
            """Système d'EDO de Lotka-Volterra."""
            x, y = state  # x = proies, y = prédateurs
            dx = alpha * x - beta * x * y
            dy = delta * x * y - gamma * y
            return [dx, dy]
        
        # Conditions initiales (normalisation)
        x0 = self.proies[0]
        y0 = self.predateurs[0]
        
        # Résolution numérique (Runge-Kutta)
        t_theory = np.linspace(0, self.steps[-1], len(self.steps))
        solution = odeint(lotka_volterra, [x0, y0], t_theory)
        
        x_theory = solution[:, 0]
        y_theory = solution[:, 1]
        
        # Affichage comparatif
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Graphique 1 : Superposition temporelle
        ax1.plot(self.steps, self.proies, label='Proies (Simulation)', 
                 color='green', linewidth=2, alpha=0.7)
        ax1.plot(self.steps, self.predateurs, label='Prédateurs (Simulation)', 
                 color='red', linewidth=2, alpha=0.7)
        ax1.plot(t_theory, x_theory, '--', label='Proies (Lotka-Volterra)', 
                 color='darkgreen', linewidth=1.5)
        ax1.plot(t_theory, y_theory, '--', label='Prédateurs (Lotka-Volterra)', 
                 color='darkred', linewidth=1.5)
        
        ax1.set_xlabel('Temps', fontsize=12)
        ax1.set_ylabel('Population', fontsize=12)
        ax1.set_title('Comparaison Temporelle', fontsize=13, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Graphique 2 : Espace de phase comparé
        ax2.plot(self.proies, self.predateurs, label='Simulation (Wa-Tor)', 
                 color='blue', linewidth=2, alpha=0.7)
        ax2.plot(x_theory, y_theory, '--', label='Théorie (Lotka-Volterra)', 
                 color='orange', linewidth=1.5)
        
        ax2.set_xlabel('Proies', fontsize=12)
        ax2.set_ylabel('Prédateurs', fontsize=12)
        ax2.set_title('Espace de Phase Comparé', fontsize=13, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"✅ Comparaison Lotka-Volterra sauvegardée : {save_path}")
        else:
            plt.show()
    
    def compute_statistics(self):
        """
        Calcule des statistiques descriptives sur les populations.
        
        Returns:
            Dictionnaire de statistiques
        """
        stats = {
            'proies': {
                'mean': np.mean(self.proies),
                'std': np.std(self.proies),
                'min': np.min(self.proies),
                'max': np.max(self.proies)
            },
            'predateurs': {
                'mean': np.mean(self.predateurs),
                'std': np.std(self.predateurs),
                'min': np.min(self.predateurs),
                'max': np.max(self.predateurs)
            },
            'duration': len(self.steps)
        }
        
        # Détection de cycles (simplifiée : pics locaux)
        from scipy.signal import find_peaks
        
        peaks_proies, _ = find_peaks(self.proies, distance=10)
        peaks_pred, _ = find_peaks(self.predateurs, distance=10)
        
        stats['cycles'] = {
            'proies_peaks': len(peaks_proies),
            'predateurs_peaks': len(peaks_pred)
        }
        
        return stats
    
    def print_summary(self):
        """Affiche un résumé textuel des résultats."""
        stats = self.compute_statistics()
        
        print("\n" + "="*60)
        print("         RÉSUMÉ DE LA SIMULATION")
        print("="*60)
        print(f"Durée : {stats['duration']} étapes")
        print(f"\n📊 PROIES :")
        print(f"   Moyenne : {stats['proies']['mean']:.1f}")
        print(f"   Écart-type : {stats['proies']['std']:.1f}")
        print(f"   Min/Max : {stats['proies']['min']} / {stats['proies']['max']}")
        print(f"   Pics détectés : {stats['cycles']['proies_peaks']}")
        
        print(f"\n📊 PRÉDATEURS :")
        print(f"   Moyenne : {stats['predateurs']['mean']:.1f}")
        print(f"   Écart-type : {stats['predateurs']['std']:.1f}")
        print(f"   Min/Max : {stats['predateurs']['min']} / {stats['predateurs']['max']}")
        print(f"   Pics détectés : {stats['cycles']['predateurs_peaks']}")
        print("="*60 + "\n")


def analyze_from_csv(csv_path: str):
    """
    Analyse une simulation à partir d'un fichier CSV.
    
    Args:
        csv_path: Chemin vers le fichier de données
    """
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    
    history = {
        'step': df['Step'].tolist(),
        'proies': df['Proies'].tolist(),
        'predateurs': df['Predateurs'].tolist()
    }
    
    analyzer = SimulationAnalyzer(history)
    analyzer.print_summary()
    analyzer.plot_populations()
    analyzer.plot_phase_space()
    analyzer.compare_lotka_volterra()


if __name__ == "__main__":
    # Exemple d'utilisation
    print("Ce module est destiné à être importé.")
    print("Utilisez : python src/main.py pour lancer la simulation.")
