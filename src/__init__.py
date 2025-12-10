"""
Package de simulation multi-agents Proie-Prédateur.
Projet BUT 3 Informatique - Modélisation stochastique.
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"

from agents import Animal, Proie, Predateur
from grid import Grid
from simulation import Simulation
from analysis import SimulationAnalyzer

__all__ = [
    'Animal',
    'Proie',
    'Predateur',
    'Grid',
    'Simulation',
    'SimulationAnalyzer'
]
