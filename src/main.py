"""
Interface graphique Pygame pour visualisation en temps réel.
Contrôles : Pause/Reprise, Vitesse, Réinitialisation.
"""

import pygame
import sys
from simulation import Simulation
from agents import Proie, Predateur
import config


class PygameViewer:
    """
    Gestionnaire d'affichage Pygame avec boucle événementielle.
    Suit le pattern MVC : Vue séparée du Modèle (Simulation).
    """
    
    def __init__(self, simulation: Simulation):
        """
        Initialise la fenêtre Pygame.
        
        Args:
            simulation: Instance de la simulation à visualiser
        """
        pygame.init()
        
        self.simulation = simulation
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Simulation Proie-Prédateur (Wa-Tor)")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # État de l'interface
        self.running = True
        self.paused = False
        self.show_info = True
        
        # Contrôle de vitesse
        self.speed_multiplier = 1.0  # 1x par défaut
    
    def handle_events(self):
        """Gestion des événements clavier et souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Pause / Reprise
                    self.paused = not self.paused
                
                elif event.key == pygame.K_r:
                    # Réinitialisation
                    self.simulation.reset()
                    self.paused = False
                
                elif event.key == pygame.K_i:
                    # Toggle info
                    self.show_info = not self.show_info
                
                elif event.key == pygame.K_UP:
                    # Accélérer
                    self.speed_multiplier = min(10.0, self.speed_multiplier + 0.5)
                
                elif event.key == pygame.K_DOWN:
                    # Ralentir
                    self.speed_multiplier = max(0.1, self.speed_multiplier - 0.5)
                
                elif event.key == pygame.K_ESCAPE:
                    # Quitter
                    self.running = False
    
    def draw_grid(self):
        """Affiche la grille avec les agents colorés."""
        self.screen.fill(config.BACKGROUND_COLOR)
        
        # Dessiner chaque cellule
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                cell_value = self.simulation.grid.cells[y, x]
                
                # Déterminer la couleur
                if cell_value == config.PROIE_SYMBOL:
                    color = config.PROIE_COLOR
                elif cell_value == config.PREDATEUR_SYMBOL:
                    color = config.PREDATEUR_COLOR
                else:
                    color = config.EMPTY_COLOR
                
                # Calculer la position du rectangle
                rect = pygame.Rect(
                    x * config.CELL_SIZE,
                    y * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE
                )
                
                pygame.draw.rect(self.screen, color, rect)
                
                # Optionnel : grille de séparation
                if config.SHOW_GRID and config.CELL_SIZE > 2:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
    
    def draw_info(self):
        """Affiche les informations de simulation (HUD)."""
        if not self.show_info:
            return
        
        proies, predateurs = self.simulation.get_population_counts()
        
        # Fond semi-transparent pour le texte
        info_surface = pygame.Surface((config.WINDOW_WIDTH, 120))
        info_surface.set_alpha(180)
        info_surface.fill((0, 0, 0))
        self.screen.blit(info_surface, (0, 0))
        
        # Informations principales
        texts = [
            f"Step: {self.simulation.step_count}",
            f"Proies: {proies}",
            f"Prédateurs: {predateurs}",
            f"Vitesse: {self.speed_multiplier:.1f}x"
        ]
        
        y_offset = 10
        for text in texts:
            # Couleur selon le type d'info
            if "Proies" in text:
                color = config.PROIE_COLOR
            elif "Prédateurs" in text:
                color = config.PREDATEUR_COLOR
            else:
                color = (255, 255, 255)
            
            surface = self.small_font.render(text, True, color)
            self.screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Message de pause
        if self.paused:
            pause_text = self.font.render("PAUSE", True, (255, 255, 0))
            text_rect = pause_text.get_rect(
                center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)
            )
            self.screen.blit(pause_text, text_rect)
        
        # Contrôles
        controls = [
            "ESPACE: Pause | R: Reset | I: Info",
            "↑/↓: Vitesse | ESC: Quitter"
        ]
        
        y_offset = config.WINDOW_HEIGHT - 60
        for control in controls:
            surface = self.small_font.render(control, True, (150, 150, 150))
            self.screen.blit(surface, (10, y_offset))
            y_offset += 25
    
    def run(self):
        """
        Boucle principale d'affichage.
        Synchronise FPS d'affichage et vitesse de simulation.
        """
        steps_per_frame = max(1, int(config.SIMULATION_SPEED * self.speed_multiplier))
        
        while self.running:
            self.handle_events()
            
            # Exécuter les steps de simulation (si pas en pause)
            if not self.paused:
                for _ in range(steps_per_frame):
                    self.simulation.step()
                    
                    # Vérifier extinction
                    if self.simulation.is_extinction():
                        print(f"⚠️ Extinction détectée au step {self.simulation.step_count}")
                        self.paused = True
                        break
                    
                    # Limite de steps
                    if (config.MAX_STEPS > 0 and 
                        self.simulation.step_count >= config.MAX_STEPS):
                        print(f"✅ Simulation terminée : {config.MAX_STEPS} steps atteints")
                        self.paused = True
                        break
            
            # Rendu graphique
            self.draw_grid()
            self.draw_info()
            pygame.display.flip()
            
            # Contrôle du framerate
            self.clock.tick(config.FPS)
        
        # Cleanup
        pygame.quit()


def main():
    """Point d'entrée principal."""
    print("🚀 Démarrage de la simulation Proie-Prédateur")
    print(f"   Grille : {config.GRID_WIDTH}x{config.GRID_HEIGHT}")
    print(f"   Proies initiales : {config.PROIE_INITIAL_COUNT}")
    print(f"   Prédateurs initiaux : {config.PREDATEUR_INITIAL_COUNT}")
    print("-" * 50)
    
    # Création de la simulation
    simulation = Simulation()
    
    # Lancement de l'interface
    viewer = PygameViewer(simulation)
    viewer.run()
    
    # Export des données à la fin
    if config.EXPORT_CSV and len(simulation.history['step']) > 0:
        simulation.export_data('/home/chrled/PycharmProjects/projet_MMath/data/test_simulation.csv')
    
    print("👋 Simulation terminée")


if __name__ == "__main__":
    main()
