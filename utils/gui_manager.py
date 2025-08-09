import tkinter as tk
from tkinter import ttk, messagebox
import time
from games.game_manager import GameManager
from utils.theme_manager import ThemeManager
from utils.animation_manager import AnimationManager
from utils.config_manager import ConfigManager
from utils.logger import get_logger

class ModernGameApp(tk.Tk):
    """Application de jeux moderne avec thèmes et animations"""
    
    def __init__(self):
        super().__init__()
        
        # Initialisation des gestionnaires
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()
        self.animation_manager = AnimationManager()
        self.game_manager = GameManager()
        self.logger = get_logger()
        
        # État de l'application (doit être défini avant setup_window)
        self.current_screen = "home"
        self.fullscreen = self.config_manager.is_fullscreen()
        
        # Configuration de la fenêtre
        self.setup_window()
        
        # Configuration des styles
        self.setup_styles()
        
        # Log du démarrage
        self.logger.log_startup("2.0.0", self.config_manager.config)
        
        # Création de l'interface
        self.create_home_screen()
        
        # Gestionnaire d'événements
        self.bind('<Escape>', self.handle_escape)
        self.bind('<F11>', self.toggle_fullscreen)
        
    def setup_window(self):
        """Configure la fenêtre principale"""
        self.title("🎮 Mini-Jeux Collection 🎮")
        
        # Taille de la fenêtre depuis la configuration
        width, height = self.config_manager.get_window_size()
        self.geometry(f"{width}x{height}")
        
        # Configuration du plein écran
        if self.fullscreen:
            self.attributes('-fullscreen', True)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Configuration de la couleur de fond
        bg_color = self.theme_manager.get_color('bg_primary')
        # Note: ttk ne supporte pas configure(bg=...), la couleur sera gérée par les styles
        
    def setup_styles(self):
        """Configure tous les styles avec le thème actuel"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Appliquer les styles du thème
        self.theme_manager.setup_theme_styles(style)
        
        # Styles supplémentaires
        style.configure(
            'Card.TFrame',
            background=self.theme_manager.get_color('bg_secondary'),
            relief='flat',
            borderwidth=0
        )
        
        style.configure(
            'Stats.TLabel',
            background=self.theme_manager.get_color('bg_secondary'),
            foreground=self.theme_manager.get_color('text_primary'),
            font=self.theme_manager.get_font('body')
        )
        
        style.configure(
            'GameCard.TFrame',
            background=self.theme_manager.get_color('bg_tertiary'),
            relief='flat',
            borderwidth=0
        )
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def handle_escape(self, event):
        """Gestion de la touche Échap"""
        if self.fullscreen:
            self.toggle_fullscreen()
        elif self.current_screen != "home":
            self.create_home_screen()
            
    def toggle_fullscreen(self, event=None):
        """Bascule le mode plein écran"""
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        self.config_manager.set_fullscreen(self.fullscreen)
        
        if not self.fullscreen:
            self.center_window()
            
        self.logger.log_user_action("toggle_fullscreen", fullscreen=self.fullscreen)
        
    def clear_screen(self):
        """Vide l'écran actuel"""
        for widget in self.winfo_children():
            widget.destroy()
            
    def create_home_screen(self):
        """Crée l'écran d'accueil moderne"""
        self.clear_screen()
        self.current_screen = "home"
        
        # Frame principal avec gradient
        main_frame = ttk.Frame(self, style='Theme.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Configuration de la grille
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre animé
        title_frame = ttk.Frame(main_frame, style='Theme.TFrame')
        title_frame.grid(row=0, column=0, pady=(0, 30))
        
        title_label = ttk.Label(
            title_frame,
            text="🎮 Mini-Jeux Collection 🎮",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Animation du titre
        if self.config_manager.are_animations_enabled():
            self.animation_manager.typewriter_effect(
                title_label, 
                "🎮 Mini-Jeux Collection 🎮",
                speed=0.1
            )
        
        # Conteneur principal pour les cartes
        content_frame = ttk.Frame(main_frame, style='Theme.TFrame')
        content_frame.grid(row=1, column=0, sticky='nsew')
        
        # Configuration de la grille pour les cartes
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Carte des jeux
        games_card = self.create_card(
            content_frame,
            "🎲 Jeux",
            "Découvrez notre collection de mini-jeux",
            "Jouer",
            self.show_games_menu,
            row=0, column=0, padx=(0, 10)
        )
        
        # Carte des paramètres
        settings_card = self.create_card(
            content_frame,
            "⚙️ Paramètres",
            "Personnalisez votre expérience",
            "Configurer",
            self.show_settings,
            row=0, column=1, padx=(10, 0)
        )
        
        # Statistiques en bas
        stats_frame = ttk.Frame(main_frame, style='Theme.TFrame')
        stats_frame.grid(row=2, column=0, pady=(20, 0))
        
        self.create_stats_display(stats_frame)
        
        # Animation d'entrée
        if self.config_manager.are_animations_enabled():
            self.animation_manager.fade_in(main_frame, duration=0.8)
            
    def create_card(self, parent, title, description, button_text, command, **grid_options):
        """Crée une carte moderne"""
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.grid(**grid_options, sticky='nsew', pady=10)
        
        # Configuration de la grille
        card_frame.grid_rowconfigure(1, weight=1)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Titre de la carte
        title_label = ttk.Label(
            card_frame,
            text=title,
            style='Heading.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(20, 10))
        
        # Description
        desc_label = ttk.Label(
            card_frame,
            text=description,
            style='Theme.TLabel',
            wraplength=200
        )
        desc_label.grid(row=1, column=0, pady=10, padx=20)
        
        # Bouton
        button = ttk.Button(
            card_frame,
            text=button_text,
            style='Primary.TButton',
            command=command
        )
        button.grid(row=2, column=0, pady=(0, 20))
        
        # Animation au survol
        if self.config_manager.are_animations_enabled():
            button.bind('<Enter>', lambda e: self.animation_manager.pulse(button, duration=0.2))
            
        return card_frame
        
    def create_stats_display(self, parent):
        """Crée l'affichage des statistiques"""
        stats_label = ttk.Label(
            parent,
            text="📊 Statistiques",
            style='Heading.TLabel'
        )
        stats_label.pack(pady=(0, 10))
        
        # Frame pour les stats
        stats_grid = ttk.Frame(parent, style='Theme.TFrame')
        stats_grid.pack()
        
        # Statistiques de base
        stats_data = self.get_basic_stats()
        
        for i, (label, value) in enumerate(stats_data.items()):
            stat_frame = ttk.Frame(stats_grid, style='Stats.TFrame')
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=5)
            
            ttk.Label(
                stat_frame,
                text=f"{label}: {value}",
                style='Stats.TLabel'
            ).pack()
            
    def get_basic_stats(self):
        """Récupère les statistiques de base"""
        try:
            # Compter les jeux disponibles
            game_count = len(self.game_manager.games)
            
            # Compter les scores sauvegardés
            total_scores = 0
            for game_id in self.game_manager.games.keys():
                scores = self.game_manager.games[game_id].score_manager.get_all_scores(game_id)
                total_scores += len(scores)
            
            return {
                "Jeux disponibles": game_count,
                "Scores sauvegardés": total_scores,
                "Thème actuel": self.theme_manager.get_current_theme()["name"],
                "Animations": "Activées" if self.config_manager.are_animations_enabled() else "Désactivées"
            }
        except Exception as e:
            self.logger.log_error_with_context(e, "get_basic_stats")
            return {"Erreur": "Impossible de charger les stats"}
            
    def show_games_menu(self):
        """Affiche le menu des jeux"""
        self.clear_screen()
        self.current_screen = "games"
        
        # Frame principal
        main_frame = ttk.Frame(self, style='Theme.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="🎲 Sélection du Jeu",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))
        
        # Grille des jeux
        games_frame = ttk.Frame(main_frame, style='Theme.TFrame')
        games_frame.pack(expand=True, fill='both')
        
        # Organiser les jeux en grille responsive
        games = list(self.game_manager.games.items())
        cols = 2 if len(games) <= 4 else 3
        
        for i, (game_id, game) in enumerate(games):
            row = i // cols
            col = i % cols
            
            game_card = self.create_game_card(games_frame, game, row, col)
            
        # Configuration de la grille
        for i in range(cols):
            games_frame.grid_columnconfigure(i, weight=1)
            
        # Bouton retour
        back_button = ttk.Button(
            main_frame,
            text="← Retour au menu principal",
            style='Secondary.TButton',
            command=self.create_home_screen
        )
        back_button.pack(pady=20)
        
        # Animation d'entrée
        if self.config_manager.are_animations_enabled():
            self.animation_manager.fade_in(main_frame, duration=0.6)
            
    def create_game_card(self, parent, game, row, col):
        """Crée une carte pour un jeu"""
        card_frame = ttk.Frame(parent, style='GameCard.TFrame')
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configuration de la grille
        card_frame.grid_rowconfigure(1, weight=1)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Titre du jeu
        title_label = ttk.Label(
            card_frame,
            text=game.name,
            style='Heading.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(15, 10))
        
        # Meilleur score
        high_score = game.score_manager.get_high_score(game.game_id)
        if high_score:
            score_text = f"Meilleur: {high_score['score']}"
            if 'player' in high_score:
                score_text += f" ({high_score['player']})"
        else:
            score_text = "Aucun score"
            
        score_label = ttk.Label(
            card_frame,
            text=score_text,
            style='Score.TLabel'
        )
        score_label.grid(row=1, column=0, pady=10)
        
        # Bouton jouer
        play_button = ttk.Button(
            card_frame,
            text="Jouer",
            style='Primary.TButton',
            command=lambda: self.launch_game(game)
        )
        play_button.grid(row=2, column=0, pady=(0, 15))
        
        # Animation au survol
        if self.config_manager.are_animations_enabled():
            play_button.bind('<Enter>', lambda e: self.animation_manager.pulse(play_button, duration=0.2))
            
        return card_frame
        
    def show_settings(self):
        """Affiche l'écran des paramètres"""
        self.clear_screen()
        self.current_screen = "settings"
        
        # Frame principal
        main_frame = ttk.Frame(self, style='Theme.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="⚙️ Paramètres",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))
        
        # Conteneur pour les paramètres
        settings_frame = ttk.Frame(main_frame, style='Theme.TFrame')
        settings_frame.pack(expand=True, fill='both')
        
        # Thèmes
        self.create_theme_selector(settings_frame)
        
        # Autres paramètres
        self.create_other_settings(settings_frame)
        
        # Bouton retour
        back_button = ttk.Button(
            main_frame,
            text="← Retour au menu principal",
            style='Secondary.TButton',
            command=self.create_home_screen
        )
        back_button.pack(pady=20)
        
        # Animation d'entrée
        if self.config_manager.are_animations_enabled():
            self.animation_manager.fade_in(main_frame, duration=0.6)
            
    def create_theme_selector(self, parent):
        """Crée le sélecteur de thèmes"""
        theme_frame = ttk.Frame(parent, style='Card.TFrame')
        theme_frame.pack(fill='x', pady=10)
        
        # Titre de section
        ttk.Label(
            theme_frame,
            text="🎨 Thèmes",
            style='Heading.TLabel'
        ).pack(pady=(15, 10))
        
        # Variables pour les thèmes
        current_theme = self.config_manager.get_theme()
        theme_var = tk.StringVar(value=current_theme)
        
        # Frame pour les boutons de thème
        themes_frame = ttk.Frame(theme_frame, style='Theme.TFrame')
        themes_frame.pack(pady=10)
        
        themes = self.config_manager.get_all_themes()
        for i, (theme_id, theme_name) in enumerate(themes.items()):
            theme_button = ttk.Button(
                themes_frame,
                text=theme_name,
                style='Primary.TButton' if theme_id == current_theme else 'Secondary.TButton',
                command=lambda t=theme_id: self.change_theme(t, theme_var)
            )
            theme_button.grid(row=i//2, column=i%2, padx=5, pady=5)
            
    def create_other_settings(self, parent):
        """Crée les autres paramètres"""
        other_frame = ttk.Frame(parent, style='Card.TFrame')
        other_frame.pack(fill='x', pady=10)
        
        # Titre de section
        ttk.Label(
            other_frame,
            text="🔧 Autres Paramètres",
            style='Heading.TLabel'
        ).pack(pady=(15, 10))
        
        # Variables pour les paramètres
        animations_var = tk.BooleanVar(value=self.config_manager.are_animations_enabled())
        fullscreen_var = tk.BooleanVar(value=self.config_manager.is_fullscreen())
        
        # Frame pour les paramètres
        settings_frame = ttk.Frame(other_frame, style='Theme.TFrame')
        settings_frame.pack(pady=10)
        
        # Animations
        animations_check = ttk.Checkbutton(
            settings_frame,
            text="Activer les animations",
            variable=animations_var,
            command=lambda: self.config_manager.set_animations_enabled(animations_var.get())
        )
        animations_check.pack(anchor='w', pady=5)
        
        # Plein écran
        fullscreen_check = ttk.Checkbutton(
            settings_frame,
            text="Mode plein écran",
            variable=fullscreen_var,
            command=lambda: self.toggle_fullscreen()
        )
        fullscreen_check.pack(anchor='w', pady=5)
        
        # Bouton réinitialiser
        reset_button = ttk.Button(
            settings_frame,
            text="Réinitialiser les paramètres",
            style='Secondary.TButton',
            command=self.reset_settings
        )
        reset_button.pack(pady=10)
        
    def change_theme(self, theme_id, theme_var):
        """Change le thème"""
        old_theme = self.config_manager.get_theme()
        self.config_manager.set_theme(theme_id)
        self.theme_manager.set_theme(theme_id)
        theme_var.set(theme_id)
        
        # Mettre à jour les styles
        self.setup_styles()
        
        # Recharger l'écran actuel
        if self.current_screen == "home":
            self.create_home_screen()
        elif self.current_screen == "games":
            self.show_games_menu()
        elif self.current_screen == "settings":
            self.show_settings()
            
        self.logger.log_theme_change(old_theme, theme_id)
        
    def reset_settings(self):
        """Réinitialise les paramètres"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment réinitialiser tous les paramètres ?"):
            self.config_manager.reset_to_defaults()
            self.theme_manager.set_theme("modern_blue")
            self.setup_styles()
            self.create_home_screen()
            self.logger.log_user_action("reset_settings")
            
    def launch_game(self, game):
        """Lance un jeu dans une nouvelle fenêtre"""
        try:
            # Créer une nouvelle fenêtre pour le jeu
            game_window = tk.Toplevel(self)
            game_window.title(f"{game.name} - Mini-Jeux")
            
            # Configuration de la fenêtre
            width, height = self.config_manager.get_window_size()
            game_window.geometry(f"{width-100}x{height-100}")
            # Note: La couleur de fond sera gérée par les styles ttk
            
            # Centrer la fenêtre
            game_window.update_idletasks()
            x = (game_window.winfo_screenwidth() // 2) - ((width-100) // 2)
            y = (game_window.winfo_screenheight() // 2) - ((height-100) // 2)
            game_window.geometry(f'{width-100}x{height-100}+{x}+{y}')
            
            # Empêcher le redimensionnement
            game_window.resizable(False, False)
            
            # Créer les widgets du jeu
            game.create_game_widgets(game_window)
            
            # Configurer la fenêtre pour être modale
            game_window.transient(self)
            game_window.grab_set()
            
            # Log du lancement
            self.logger.log_game_event(game.name, "launch")
            
            # Attendre que la fenêtre soit fermée
            self.wait_window(game_window)
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"launch_game_{game.name}")
            messagebox.showerror("Erreur", f"Impossible de lancer {game.name}: {str(e)}")

# Alias pour la compatibilité
GameApp = ModernGameApp
