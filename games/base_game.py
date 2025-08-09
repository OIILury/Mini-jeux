from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
from utils.score_manager import ScoreManager
from utils.theme_manager import ThemeManager
from utils.animation_manager import AnimationManager
from utils.config_manager import ConfigManager
from utils.logger import get_logger

class BaseGame(ABC):
    def __init__(self, name, game_id):
        self._name = name
        self.game_id = game_id
        self.score_manager = ScoreManager()
        self.current_score = 0
        
        # Initialisation des gestionnaires
        self.theme_manager = ThemeManager()
        self.animation_manager = AnimationManager()
        self.config_manager = ConfigManager()
        self.logger = get_logger()
        
        # Couleurs du thème actuel
        self.game_colors = {
            'bg_primary': self.theme_manager.get_color('bg_primary'),
            'bg_secondary': self.theme_manager.get_color('bg_secondary'),
            'bg_tertiary': self.theme_manager.get_color('bg_tertiary'),
            'text_primary': self.theme_manager.get_color('text_primary'),
            'text_secondary': self.theme_manager.get_color('text_secondary'),
            'accent_primary': self.theme_manager.get_color('accent_primary'),
            'accent_secondary': self.theme_manager.get_color('accent_secondary'),
            'success': self.theme_manager.get_color('success'),
            'warning': self.theme_manager.get_color('warning'),
            'error': self.theme_manager.get_color('error')
        }
        
    def create_game_widgets(self, parent):
        """Crée l'interface de base du jeu avec le nouveau design"""
        self.parent = parent
        self.setup_styles()
        
        # Configuration de la fenêtre de jeu
        self.parent.resizable(True, True)
        width, height = self.config_manager.get_window_size()
        self.parent.geometry(f"{width-100}x{height-100}")
        
        # Configurer la fenêtre parent pour qu'elle s'étende
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Frame principal avec design moderne
        self.main_frame = ttk.Frame(parent, style='Game.TFrame')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        # Configuration de la grille principale
        self.main_frame.grid_rowconfigure(2, weight=1)  # Zone de jeu
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête du jeu
        self.create_game_header()
        
        # Zone de score moderne
        self.create_score_section()
        
        # Zone de jeu principale
        self.game_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        self.game_frame.grid(row=2, column=0, sticky='nsew', pady=10)
        
        # Barre de contrôle en bas
        self.create_control_bar()
        
        # Initialisation du jeu spécifique
        self.init_game(self.game_frame)
        
        # Animation d'entrée si activée
        if self.config_manager.are_animations_enabled():
            self.animation_manager.fade_in(self.main_frame, duration=0.5)
        
        # Log du démarrage du jeu
        self.logger.log_game_event(self._name, "start")
        
    def create_game_header(self):
        """Crée l'en-tête moderne du jeu"""
        header_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        # Configuration de la grille
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Icône du jeu (placeholder)
        icon_label = ttk.Label(
            header_frame,
            text="🎮",
            style='GameIcon.TLabel'
        )
        icon_label.grid(row=0, column=0, padx=(0, 15))
        
        # Titre du jeu
        self.title_label = ttk.Label(
            header_frame,
            text=self._name,
            style='GameTitle.TLabel'
        )
        self.title_label.grid(row=0, column=1, sticky='w')
        
        # Bouton fermer
        close_button = ttk.Button(
            header_frame,
            text="✕",
            style='Close.TButton',
            command=self.quit_game
        )
        close_button.grid(row=0, column=2, padx=(15, 0))
        
    def create_score_section(self):
        """Crée la section de score moderne"""
        score_frame = ttk.Frame(self.main_frame, style='ScoreCard.TFrame')
        score_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # Configuration de la grille
        score_frame.grid_columnconfigure(0, weight=1)
        score_frame.grid_columnconfigure(1, weight=1)
        score_frame.grid_columnconfigure(2, weight=1)
        
        # Score actuel
        self.score_label = ttk.Label(
            score_frame,
            text=f"Score: {self.current_score}",
            style='CurrentScore.TLabel'
        )
        self.score_label.grid(row=0, column=0, sticky='w', padx=15, pady=10)
        
        # Meilleur score
        high_score = self.score_manager.get_high_score(self.game_id)
        if high_score is not None:
            high_score_text = f"Meilleur: {high_score['score']}"
            if 'player' in high_score:
                high_score_text += f" ({high_score['player']})"
        else:
            high_score_text = "Aucun record"
            
        self.high_score_label = ttk.Label(
            score_frame,
            text=high_score_text,
            style='HighScore.TLabel'
        )
        self.high_score_label.grid(row=0, column=1, sticky='w', pady=10)
        
        # Temps/statut (pour les jeux qui en ont besoin)
        self.status_label = ttk.Label(
            score_frame,
            text="",
            style='Status.TLabel'
        )
        self.status_label.grid(row=0, column=2, sticky='e', padx=15, pady=10)
        
    def create_control_bar(self):
        """Crée la barre de contrôle moderne"""
        control_frame = ttk.Frame(self.main_frame, style='Game.TFrame')
        control_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        
        # Configuration de la grille
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        
        # Bouton pause (si applicable)
        self.pause_button = ttk.Button(
            control_frame,
            text="⏸️ Pause",
            style='Secondary.TButton',
            command=self.pause_game
        )
        self.pause_button.grid(row=0, column=0, sticky='w', padx=5)
        
        # Bouton reset
        reset_button = ttk.Button(
            control_frame,
            text="🔄 Recommencer",
            style='Secondary.TButton',
            command=self.reset_game
        )
        reset_button.grid(row=0, column=1, padx=5)
        
        # Bouton quitter
        quit_button = ttk.Button(
            control_frame,
            text="❌ Quitter",
            style='Close.TButton',
            command=self.quit_game
        )
        quit_button.grid(row=0, column=2, sticky='e', padx=5)
        
    def setup_styles(self):
        """Configure les styles modernes pour le jeu"""
        style = ttk.Style()
        
        # Style général pour les frames de jeu
        style.configure(
            'Game.TFrame',
            background=self.game_colors['bg_primary']
        )
        
        # Style pour les cartes de score
        style.configure(
            'ScoreCard.TFrame',
            background=self.game_colors['bg_secondary'],
            relief='flat',
            borderwidth=0
        )
        
        # Style pour le titre du jeu
        style.configure(
            'GameTitle.TLabel',
            font=self.theme_manager.get_font('heading'),
            foreground=self.game_colors['text_primary'],
            background=self.game_colors['bg_primary']
        )
        
        # Style pour l'icône du jeu
        style.configure(
            'GameIcon.TLabel',
            font=('Segoe UI', 24),
            foreground=self.game_colors['accent_primary'],
            background=self.game_colors['bg_primary']
        )
        
        # Style pour le score actuel
        style.configure(
            'CurrentScore.TLabel',
            font=self.theme_manager.get_font('score'),
            foreground=self.game_colors['text_primary'],
            background=self.game_colors['bg_secondary']
        )
        
        # Style pour le meilleur score
        style.configure(
            'HighScore.TLabel',
            font=self.theme_manager.get_font('score'),
            foreground=self.game_colors['accent_secondary'],
            background=self.game_colors['bg_secondary']
        )
        
        # Style pour le statut
        style.configure(
            'Status.TLabel',
            font=self.theme_manager.get_font('body'),
            foreground=self.game_colors['text_secondary'],
            background=self.game_colors['bg_secondary']
        )
        
        # Style pour les boutons de jeu
        style.configure(
            'Game.TButton',
            font=self.theme_manager.get_font('button'),
            padding=(10, 5),
            background=self.game_colors['bg_tertiary'],
            foreground=self.game_colors['text_primary'],
            borderwidth=0,
            focuscolor="none"
        )
        
        # Style pour le bouton fermer
        style.configure(
            'Close.TButton',
            font=self.theme_manager.get_font('button'),
            padding=(8, 4),
            background=self.game_colors['error'],
            foreground=self.game_colors['text_primary'],
            borderwidth=0,
            focuscolor="none"
        )
        
        # Configuration des états de hover
        style.map('Game.TButton',
            background=[('active', self.game_colors['accent_primary'])],
            foreground=[('active', self.game_colors['text_primary'])]
        )
        
        style.map('Close.TButton',
            background=[('active', self.game_colors['error'])],
            foreground=[('active', self.game_colors['text_primary'])]
        )
        
    def update_score(self, points):
        """Met à jour le score actuel avec animation"""
        try:
            old_score = self.current_score
            self.current_score += points
            
            if hasattr(self, 'score_label'):
                # Animation du changement de score
                if self.config_manager.are_animations_enabled() and points > 0:
                    self.animation_manager.pulse(self.score_label, duration=0.3)
                
                self.score_label.config(text=f"Score: {self.current_score}")
                
            # Met à jour le meilleur score si nécessaire
            high_score = self.score_manager.get_high_score(self.game_id)
            if high_score is None or self.current_score > high_score['score']:
                if hasattr(self, 'high_score_label'):
                    self.high_score_label.config(
                        text=f"Meilleur: {self.current_score}"
                    )
                    # Animation pour nouveau record
                    if self.config_manager.are_animations_enabled():
                        self.animation_manager.bounce(self.high_score_label, height=10)
                        
            # Log du changement de score
            self.logger.log_score(self._name, "Joueur", self.current_score, points_gained=points)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "update_score")
            
    def save_score(self, player_name=None):
        """Sauvegarde le score actuel"""
        try:
            if not player_name:
                player_name = "Joueur"
            if self.current_score > 0:  # Ne sauvegarde que les scores positifs
                self.score_manager.save_score(self.game_id, player_name, self.current_score)
                self.logger.log_score(self._name, player_name, self.current_score)
        except Exception as e:
            self.logger.log_error_with_context(e, "save_score")
            messagebox.showerror(
                "Erreur",
                "Impossible de sauvegarder le score. Veuillez réessayer."
            )
        
    def show_game_over(self, message="Partie terminée !"):
        """Affiche l'écran de fin de partie moderne"""
        try:
            if self.current_score > 0:  # Ne montre le score que s'il est positif
                message = f"{message}\nScore final: {self.current_score}"
                
            # Animation avant la boîte de dialogue
            if self.config_manager.are_animations_enabled():
                self.animation_manager.shake(self.main_frame, intensity=3, duration=0.2)
                
            messagebox.showinfo("Fin de partie", message)
            self.save_score()
            self.quit_game()
            
            self.logger.log_game_event(self._name, "game_over", score=self.current_score)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "show_game_over")
            self.quit_game()
        
    def pause_game(self):
        """Met en pause le jeu (à implémenter dans les classes dérivées)"""
        self.logger.log_game_event(self._name, "pause")
        # Cette méthode peut être surchargée par les jeux qui supportent la pause
        
    def reset_game(self):
        """Remet à zéro le jeu"""
        try:
            self.current_score = 0
            if hasattr(self, 'score_label'):
                self.score_label.config(text="Score: 0")
                
            # Réinitialiser le jeu spécifique
            if hasattr(self, 'reset'):
                self.reset()
                
            self.logger.log_game_event(self._name, "reset")
            
        except Exception as e:
            self.logger.log_error_with_context(e, "reset_game")
        
    def quit_game(self):
        """Ferme la fenêtre du jeu"""
        try:
            # Animation de sortie si activée
            if self.config_manager.are_animations_enabled():
                self.animation_manager.fade_in(self.main_frame, duration=0.3, callback=self._destroy_window)
            else:
                self._destroy_window()
                
        except Exception as e:
            self.logger.log_error_with_context(e, "quit_game")
            # Force la fermeture même en cas d'erreur
            if hasattr(self, 'parent'):
                self.parent.destroy()
                
    def _destroy_window(self):
        """Destruction de la fenêtre (utilisé par l'animation)"""
        if hasattr(self, 'cleanup'):
            self.cleanup()
        if hasattr(self, 'parent'):
            self.parent.destroy()
        
    def resource_path(self, relative_path):
        """Obtient le chemin absolu des ressources"""
        try:
            base_path = os.environ.get('GAME_ASSETS', '.')
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path
            
    def update_status(self, status_text):
        """Met à jour le texte de statut"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=status_text)
            
    def show_success_message(self, message):
        """Affiche un message de succès"""
        if self.config_manager.are_animations_enabled():
            self.animation_manager.pulse(self.main_frame, duration=0.2)
        messagebox.showinfo("Succès", message)
        
    def show_error_message(self, message):
        """Affiche un message d'erreur"""
        if self.config_manager.are_animations_enabled():
            self.animation_manager.shake(self.main_frame, intensity=5, duration=0.3)
        messagebox.showerror("Erreur", message)
        
    @abstractmethod
    def init_game(self, game_frame):
        """Initialise les éléments spécifiques du jeu"""
        pass