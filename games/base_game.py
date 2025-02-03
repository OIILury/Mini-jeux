from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils.score_manager import ScoreManager

class BaseGame(ABC):
    def __init__(self, name, game_id):
        self._name = name
        self.game_id = game_id
        self.score_manager = ScoreManager()
        self.current_score = 0
        self.game_colors = {
            'bg_primary': '#065499',      # Bleu principal
            'bg_secondary': '#0A6CBD',    # Bleu légèrement plus clair
            'text_primary': '#FFFFFF',    # Blanc
            'text_secondary': '#E0E0E0',  # Gris clair
            'accent': '#FFD700'           # Or pour les scores/succès
        }
        
    def create_game_widgets(self, parent):
        """Crée l'interface de base du jeu"""
        self.parent = parent
        self.setup_styles()
        
        # Configuration de la fenêtre de jeu
        self.parent.resizable(True, True)  # Permet le redimensionnement
        self.parent.geometry("800x600")    # Taille par défaut plus petite
        
        # Configurer la fenêtre parent pour qu'elle s'étende
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Frame principal avec une marge plus petite
        self.main_frame = ttk.Frame(parent, style='Game.TFrame')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)  # Marges réduites
        
        # Configurer main_frame pour qu'il s'étende
        self.main_frame.grid_rowconfigure(2, weight=1)  # game_frame row
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre du jeu avec une police plus petite
        self.title_label = ttk.Label(
            self.main_frame,
            text=self._name,
            style='GameTitle.TLabel'
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))  # Padding réduit
        
        # Zone de score
        self.score_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        self.score_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # Configurer score_frame pour qu'il s'étende
        self.score_frame.grid_columnconfigure(0, weight=1)
        self.score_frame.grid_columnconfigure(1, weight=1)

        self.score_label = ttk.Label(
            self.score_frame,
            text=f"Score: {self.current_score}",
            style='GameScore.TLabel'
        )
        self.score_label.grid(row=0, column=0, sticky='w', padx=5)
        
        # Meilleur score
        high_score = self.score_manager.get_high_score(self.game_id)
        if high_score is not None:
            high_score_text = f"Meilleur: {high_score['score']}"
            if 'player' in high_score:
                high_score_text += f" ({high_score['player']})"
            self.high_score_label = ttk.Label(
                self.score_frame,
                text=high_score_text,
                style='GameHighScore.TLabel'
            )
            self.high_score_label.grid(row=0, column=1, sticky='e', padx=5)
        
        # Zone de jeu
        self.game_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        self.game_frame.grid(row=2, column=0, sticky='nsew', pady=10)
        
        # Boutons de contrôle
        self.control_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        self.control_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        
        # Configurer control_frame pour qu'il s'étende
        self.control_frame.grid_columnconfigure(0, weight=1)

        self.quit_button = ttk.Button(
            self.control_frame,
            text="Quitter",
            style='Game.TButton',
            command=self.quit_game
        )
        self.quit_button.grid(row=0, column=0, sticky='e', padx=5)
        
        # Initialisation du jeu spécifique
        self.init_game(self.game_frame)
        
    def setup_styles(self):
        """Configure les styles pour le jeu"""
        style = ttk.Style()
        
        # Style général
        style.configure(
            'Game.TFrame',
            background=self.game_colors['bg_primary']
        )
        
        # Style pour le titre avec une taille de police réduite
        style.configure(
            'GameTitle.TLabel',
            font=('Helvetica', 20, 'bold'),  # Taille réduite de 24 à 20
            foreground=self.game_colors['text_primary'],
            background=self.game_colors['bg_primary']
        )
        
        # Style pour le score avec une taille de police réduite
        style.configure(
            'GameScore.TLabel',
            font=('Helvetica', 12),  # Taille réduite de 14 à 12
            foreground=self.game_colors['text_primary'],
            background=self.game_colors['bg_primary']
        )
        
        # Style pour le meilleur score avec une taille de police réduite
        style.configure(
            'GameHighScore.TLabel',
            font=('Helvetica', 12),  # Taille réduite de 14 à 12
            foreground=self.game_colors['accent'],
            background=self.game_colors['bg_primary']
        )
        
        # Style pour les boutons
        style.configure(
            'Game.TButton',
            font=('Helvetica', 12),
            padding=5,
            background=self.game_colors['bg_secondary'],
            foreground=self.game_colors['text_primary']
        )
        
    def update_score(self, points):
        """Met à jour le score actuel"""
        try:
            self.current_score += points
            if hasattr(self, 'score_label'):
                self.score_label.config(text=f"Score: {self.current_score}")
                
            # Met à jour le meilleur score si nécessaire
            high_score = self.score_manager.get_high_score(self.game_id)
            if high_score is None or self.current_score > high_score['score']:
                if hasattr(self, 'high_score_label'):
                    self.high_score_label.config(
                        text=f"Meilleur: {self.current_score}"
                    )
        except Exception as e:
            print(f"Erreur lors de la mise à jour du score : {e}")
            
    def save_score(self, player_name=None):
        """Sauvegarde le score actuel"""
        try:
            if not player_name:
                player_name = "Joueur"
            if self.current_score > 0:  # Ne sauvegarde que les scores positifs
                self.score_manager.save_score(self.game_id, player_name, self.current_score)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")
            messagebox.showerror(
                "Erreur",
                "Impossible de sauvegarder le score. Veuillez réessayer."
            )
        
    def show_game_over(self, message="Partie terminée !"):
        """Affiche l'écran de fin de partie"""
        try:
            if self.current_score > 0:  # Ne montre le score que s'il est positif
                message = f"{message}\nScore final: {self.current_score}"
            messagebox.showinfo("Fin de partie", message)
            self.save_score()
            self.quit_game()
        except Exception as e:
            print(f"Erreur lors de l'affichage de fin de partie : {e}")
            self.quit_game()
        
    def quit_game(self):
        """Ferme la fenêtre du jeu"""
        try:
            if hasattr(self, 'cleanup'):
                self.cleanup()
            self.parent.destroy()
        except Exception as e:
            print(f"Erreur lors de la fermeture du jeu : {e}")
            # Force la fermeture même en cas d'erreur
            if hasattr(self, 'parent'):
                self.parent.destroy()
        
    def resource_path(self, relative_path):
        """Obtient le chemin absolu des ressources"""
        try:
            base_path = os.environ.get('GAME_ASSETS', '.')
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path
            
    @abstractmethod
    def init_game(self, game_frame):
        """Initialise les éléments spécifiques du jeu"""
        pass