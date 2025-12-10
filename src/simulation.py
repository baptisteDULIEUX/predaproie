"""
Moteur de simulation principal.
Gère le cycle de vie : initialisation, step, analyse.
"""

import random
import numpy as np
from typing import List, Tuple
from grid import Grid
from agents import Proie, Predateur, Animal
import config


class Simulation:
    """
    Contrôleur principal de la simulation multi-agents.
    Gère l'initialisation, l'évolution temporelle et les statistiques.
    """
    
    def __init__(self):
        """Initialise la simulation avec les paramètres de config."""
        # Configuration du générateur aléatoire
        if config.RANDOM_SEED is not None:
            random.seed(config.RANDOM_SEED)
            np.random.seed(config.RANDOM_SEED)
        
        # Création de la grille
        self.grid = Grid(config.GRID_WIDTH, config.GRID_HEIGHT, config.TORUS_MODE)
        
        # Compteurs
        self.step_count = 0
        self.is_running = False
        
        # Historique des populations pour analyse
        self.history = {
            'step': [],
            'proies': [],
            'predateurs': []
        }
        
        # Initialisation des populations
        self._initialize_populations()
    
    def _initialize_populations(self):
        """
        Peuplement initial aléatoire de la grille.
        Utilise un échantillonnage sans remise pour éviter les collisions.
        """
        total_cells = config.GRID_WIDTH * config.GRID_HEIGHT
        total_animals = config.PROIE_INITIAL_COUNT + config.PREDATEUR_INITIAL_COUNT
        
        if total_animals > total_cells:
            raise ValueError(
                f"Trop d'animaux ({total_animals}) pour la grille ({total_cells} cases)"
            )
        
        # Génération de positions aléatoires uniques
        all_positions = [
            (x, y) 
            for x in range(config.GRID_WIDTH) 
            for y in range(config.GRID_HEIGHT)
        ]
        random.shuffle(all_positions)
        
        # Placement des proies
        for i in range(config.PROIE_INITIAL_COUNT):
            x, y = all_positions[i]
            proie = Proie(x, y, config.PROIE_REPRODUCTION_TIME)
            self.grid.add_agent(proie)
        
        # Placement des prédateurs
        offset = config.PROIE_INITIAL_COUNT
        for i in range(config.PREDATEUR_INITIAL_COUNT):
            x, y = all_positions[offset + i]
            predateur = Predateur(
                x, y,
                config.PREDATEUR_REPRODUCTION_TIME,
                config.PREDATEUR_INITIAL_ENERGY,
                config.PREDATEUR_ENERGY_GAIN,
                config.PREDATEUR_ENERGY_LOSS
            )
            self.grid.add_agent(predateur)
        
        # Enregistrer l'état initial
        self._record_statistics()
    
    def step(self):
        """
        Exécute un cycle de simulation complet.
        Ordre : Déplacement -> Reproduction -> Mort -> Statistiques
        """
        self.step_count += 1
        
        # Phase 1 : Obtenir tous les agents vivants
        # Important : copie pour éviter modification pendant itération
        agents = self.grid.get_all_agents().copy()
        
        # Mélange aléatoire pour éviter les biais d'ordre
        random.shuffle(agents)
        
        # Phase 2 : Déplacement et actions
        new_borns = []  # Liste des nouveaux-nés
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Vieillissement
            agent.age()
            
            # Déplacement
            old_pos = (agent.x, agent.y)
            new_pos = agent.move(self.grid)
            
            if new_pos != old_pos:
                self.grid.move_agent(old_pos, new_pos)
            
            # Métabolisme (prédateurs uniquement)
            if isinstance(agent, Predateur):
                agent.lose_energy()
            
            # Reproduction
            if agent.can_reproduce():
                offspring = agent.reproduce()
                if offspring:
                    new_borns.append(offspring)
        
        # Phase 3 : Ajouter les nouveaux-nés
        for baby in new_borns:
            # Chercher une case vide adjacente
            empty_neighbors = self.grid.get_empty_neighbors(baby.x, baby.y)
            if empty_neighbors:
                baby.x, baby.y = random.choice(empty_neighbors)
                self.grid.add_agent(baby)
        
        # Phase 4 : Retirer les morts
        dead_positions = [
            (agent.x, agent.y)
            for agent in agents
            if not agent.is_alive
        ]
        
        for pos in dead_positions:
            self.grid.remove_agent(*pos)
        
        # Phase 5 : Enregistrer les statistiques
        if config.RECORD_DATA and self.step_count % config.DATA_RECORD_INTERVAL == 0:
            self._record_statistics()
    
    def _record_statistics(self):
        """Enregistre l'état actuel des populations."""
        agents = self.grid.get_all_agents()
        
        proies_count = sum(1 for a in agents if isinstance(a, Proie))
        predateurs_count = sum(1 for a in agents if isinstance(a, Predateur))
        
        self.history['step'].append(self.step_count)
        self.history['proies'].append(proies_count)
        self.history['predateurs'].append(predateurs_count)
    
    def get_population_counts(self) -> Tuple[int, int]:
        """
        Retourne les compteurs actuels.
        
        Returns:
            Tuple (nombre_proies, nombre_predateurs)
        """
        agents = self.grid.get_all_agents()
        proies = sum(1 for a in agents if isinstance(a, Proie))
        predateurs = sum(1 for a in agents if isinstance(a, Predateur))
        return (proies, predateurs)
    
    def is_extinction(self) -> bool:
        """
        Vérifie si une extinction totale est survenue.
        
        Returns:
            True si au moins une espèce a disparu
        """
        proies, predateurs = self.get_population_counts()
        return proies == 0 or predateurs == 0
    
    def reset(self):
        """Réinitialise complètement la simulation."""
        self.grid.clear()
        self.step_count = 0
        self.history = {'step': [], 'proies': [], 'predateurs': []}
        self._initialize_populations()
    
    def export_data(self, filename: str):
        """
        Exporte les données historiques en CSV.
        
        Args:
            filename: Chemin du fichier de sortie
        """
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Step', 'Proies', 'Predateurs'])
            
            for i in range(len(self.history['step'])):
                writer.writerow([
                    self.history['step'][i],
                    self.history['proies'][i],
                    self.history['predateurs'][i]
                ])
        
        print(f"✅ Données exportées : {filename}")
