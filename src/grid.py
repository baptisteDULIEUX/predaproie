"""
Gestion de la grille de simulation avec topologie torique.
Optimisation : NumPy pour les opérations vectorisées.
"""

import numpy as np
from typing import List, Tuple, Optional
from agents import Animal, Proie, Predateur
import config


class Grid:
    """
    Grille 2D avec topologie torique (pas d'effets de bord).
    Stocke les agents et gère les interactions spatiales.
    """
    
    def __init__(self, width: int, height: int, torus: bool = True):
        """
        Initialise une grille vide.
        
        Args:
            width: Largeur de la grille
            height: Hauteur de la grille
            torus: True pour topologie torique (arithmétique modulaire)
        """
        self.width = width
        self.height = height
        self.torus = torus
        
        # Matrice NumPy pour affichage rapide (0=vide, 1=proie, 2=prédateur)
        self.cells = np.zeros((height, width), dtype=np.int8)
        
        # Dictionnaire pour stocker les références aux agents
        # Clé : (x, y), Valeur : Agent
        self.agents: dict[Tuple[int, int], Animal] = {}
    
    def _wrap_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        Applique l'arithmétique modulaire pour la topologie torique.
        
        Args:
            x, y: Coordonnées brutes
            
        Returns:
            Coordonnées "wrappées" dans [0, width) x [0, height)
        """
        if self.torus:
            return (x % self.width, y % self.height)
        else:
            # Clamp aux bords si pas torique
            return (max(0, min(x, self.width - 1)), 
                    max(0, min(y, self.height - 1)))
    
    def is_empty(self, x: int, y: int) -> bool:
        """Vérifie si une case est vide."""
        return self.cells[y, x] == 0
    
    def is_prey(self, x: int, y: int) -> bool:
        """Vérifie si une case contient une proie."""
        return self.cells[y, x] == config.PROIE_SYMBOL
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Retourne les 4 voisins (Von Neumann) d'une position.
        
        Args:
            x, y: Position centrale
            
        Returns:
            Liste des positions voisines
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Haut, Bas, Droite, Gauche
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = self._wrap_position(x + dx, y + dy)
            neighbors.append((nx, ny))
        
        return neighbors
    
    def get_empty_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Retourne uniquement les voisins vides."""
        neighbors = self.get_neighbors(x, y)
        return [pos for pos in neighbors if self.is_empty(*pos)]
    
    def get_prey_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Retourne uniquement les voisins contenant des proies."""
        neighbors = self.get_neighbors(x, y)
        return [pos for pos in neighbors if self.is_prey(*pos)]
    
    def add_agent(self, agent: Animal):
        """
        Ajoute un agent à la grille.
        
        Args:
            agent: Instance de Proie ou Predateur
        """
        x, y = agent.x, agent.y
        
        # Déterminer le symbole
        if isinstance(agent, Proie):
            symbol = config.PROIE_SYMBOL
        elif isinstance(agent, Predateur):
            symbol = config.PREDATEUR_SYMBOL
        else:
            raise ValueError(f"Type d'agent inconnu : {type(agent)}")
        
        # Mise à jour de la grille
        self.cells[y, x] = symbol
        self.agents[(x, y)] = agent
    
    def remove_agent(self, x: int, y: int):
        """
        Retire un agent de la grille.
        
        Args:
            x, y: Position de l'agent à retirer
        """
        if (x, y) in self.agents:
            del self.agents[(x, y)]
            self.cells[y, x] = 0
    
    def move_agent(self, old_pos: Tuple[int, int], new_pos: Tuple[int, int]):
        """
        Déplace un agent d'une position à une autre.
        
        Args:
            old_pos: Ancienne position (x, y)
            new_pos: Nouvelle position (x, y)
        """
        if old_pos not in self.agents:
            return
        
        agent = self.agents[old_pos]
        
        # Gestion de la collision : si la nouvelle case est occupée
        if new_pos in self.agents:
            target = self.agents[new_pos]
            
            # Prédateur mange proie
            if isinstance(agent, Predateur) and isinstance(target, Proie):
                agent.eat()
                self.remove_agent(*new_pos)  # Retire la proie
            else:
                # Collision non autorisée : annuler le déplacement
                return
        
        # Déplacement effectif
        self.remove_agent(*old_pos)
        agent.x, agent.y = new_pos
        self.add_agent(agent)
    
    def get_agent(self, x: int, y: int) -> Optional[Animal]:
        """Retourne l'agent à la position donnée."""
        return self.agents.get((x, y))
    
    def get_all_agents(self) -> List[Animal]:
        """Retourne tous les agents vivants."""
        return list(self.agents.values())
    
    def clear(self):
        """Vide complètement la grille."""
        self.cells.fill(0)
        self.agents.clear()
