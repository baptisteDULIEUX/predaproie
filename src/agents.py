"""
Définition des classes d'agents pour la simulation multi-agents.
Architecture OOP : Animal (classe abstraite) -> Proie / Predateur
"""

import random
from abc import ABC, abstractmethod
from typing import Tuple, Optional


class Animal(ABC):
    """
    Classe abstraite représentant un agent générique.
    Toutes les espèces héritent de cette classe.
    """
    
    def __init__(self, x: int, y: int, reproduction_time: int):
        """
        Initialise un animal à une position donnée.
        
        Args:
            x: Position X sur la grille
            y: Position Y sur la grille
            reproduction_time: Cycles avant de pouvoir se reproduire
        """
        self.x = x
        self.y = y
        self.reproduction_counter = 0  # Compteur vers la reproduction
        self.reproduction_time = reproduction_time
        self.is_alive = True
    
    @abstractmethod
    def move(self, grid: 'Grid') -> Tuple[int, int]:
        """
        Détermine la prochaine position de l'animal.
        Méthode abstraite à implémenter dans les sous-classes.
        
        Args:
            grid: Référence à la grille de simulation
            
        Returns:
            Tuple (new_x, new_y) de la nouvelle position
        """
        pass
    
    @abstractmethod
    def can_reproduce(self) -> bool:
        """
        Vérifie si l'animal peut se reproduire.
        
        Returns:
            True si reproduction possible, False sinon
        """
        pass
    
    @abstractmethod
    def reproduce(self) -> Optional['Animal']:
        """
        Crée un nouvel animal (reproduction asexuée).
        
        Returns:
            Nouvel animal ou None si reproduction impossible
        """
        pass
    
    def age(self):
        """Incrémente l'âge (compteur de reproduction)."""
        self.reproduction_counter += 1


class Proie(Animal):
    """
    Classe représentant une proie (herbivore).
    Comportement : Fuite, Reproduction simple
    """
    
    def __init__(self, x: int, y: int, reproduction_time: int):
        super().__init__(x, y, reproduction_time)
    
    def move(self, grid: 'Grid') -> Tuple[int, int]:
        """
        Déplacement aléatoire vers une case vide adjacente (Von Neumann).
        
        Args:
            grid: Référence à la grille
            
        Returns:
            Nouvelle position (x, y)
        """
        empty_neighbors = grid.get_empty_neighbors(self.x, self.y)
        
        if empty_neighbors:
            # Choisir aléatoirement parmi les cases vides
            return random.choice(empty_neighbors)
        else:
            # Pas de case vide : rester sur place
            return (self.x, self.y)
    
    def can_reproduce(self) -> bool:
        """Une proie peut se reproduire si elle a atteint l'âge requis."""
        return self.reproduction_counter >= self.reproduction_time
    
    def reproduce(self) -> Optional['Proie']:
        """
        Crée une nouvelle proie à la même position.
        Réinitialise le compteur de reproduction.
        
        Returns:
            Nouvelle proie ou None
        """
        if self.can_reproduce():
            self.reproduction_counter = 0  # Reset après reproduction
            return Proie(self.x, self.y, self.reproduction_time)
        return None


class Predateur(Animal):
    """
    Classe représentant un prédateur (carnivore).
    Comportement : Chasse, Métabolisme énergétique, Reproduction conditionnelle
    """
    
    def __init__(self, x: int, y: int, reproduction_time: int, 
                 initial_energy: int, energy_gain: int, energy_loss: int):
        super().__init__(x, y, reproduction_time)
        self.energy = initial_energy
        self.energy_gain = energy_gain
        self.energy_loss = energy_loss
    
    def move(self, grid: 'Grid') -> Tuple[int, int]:
        """
        Déplacement intelligent : priorité aux cases avec des proies.
        
        Args:
            grid: Référence à la grille
            
        Returns:
            Nouvelle position (x, y)
        """
        # Chercher des proies dans le voisinage
        prey_neighbors = grid.get_prey_neighbors(self.x, self.y)
        
        if prey_neighbors:
            # Chasse : aller vers une proie
            return random.choice(prey_neighbors)
        else:
            # Errance : déplacement aléatoire vers case vide
            empty_neighbors = grid.get_empty_neighbors(self.x, self.y)
            if empty_neighbors:
                return random.choice(empty_neighbors)
            else:
                return (self.x, self.y)  # Rester sur place
    
    def eat(self):
        """Gain d'énergie après avoir mangé une proie."""
        self.energy += self.energy_gain
    
    def lose_energy(self):
        """Perte d'énergie due au métabolisme."""
        self.energy -= self.energy_loss
        if self.energy <= 0:
            self.is_alive = False  # Mort par famine
    
    def can_reproduce(self) -> bool:
        """Un prédateur peut se reproduire s'il a assez d'énergie ET l'âge requis."""
        return (self.reproduction_counter >= self.reproduction_time and 
                self.energy > self.energy_gain * 2)  # Condition énergétique
    
    def reproduce(self) -> Optional['Predateur']:
        """
        Crée un nouveau prédateur.
        Le parent perd de l'énergie lors de la reproduction.
        
        Returns:
            Nouveau prédateur ou None
        """
        if self.can_reproduce():
            self.reproduction_counter = 0
            self.energy //= 2  # Divise l'énergie entre parent et enfant
            return Predateur(
                self.x, self.y, self.reproduction_time,
                self.energy, self.energy_gain, self.energy_loss
            )
        return None
