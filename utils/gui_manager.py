import tkinter as tk
from tkinter import ttk
from games.game_manager import GameManager

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Définition des couleurs
        self.colors = {
            'bg_primary': '#065499',      # Bleu principal
            'bg_secondary': '#0A6CBD',    # Bleu légèrement plus clair pour le contraste
            'text_primary': '#FFFFFF',    # Blanc pour le texte
            'text_secondary': '#E0E0E0',  # Gris clair pour le texte secondaire
            'button_hover': '#0878CC',    # Bleu plus clair pour le hover
            'accent': '#FFD700'           # Or pour les accents
        }
        
        self.title("Application de Jeux")
        self.geometry("800x600")
        self.configure(bg=self.colors['bg_primary'])
        
        # État du plein écran
        self.fullscreen = False
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configuration des styles personnalisés
        self.style.configure(
            'Large.TButton',
            font=('Helvetica', 14),
            padding=10,
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary']
        )
        
        self.style.configure(
            'TLabel',
            foreground=self.colors['text_primary'],
            background=self.colors['bg_primary']
        )
        
        self.style.configure(
            'TFrame',
            background=self.colors['bg_primary']
        )
        
        # Style pour les titres
        self.style.configure(
            'Title.TLabel',
            font=('Helvetica', 32, 'bold'),
            foreground=self.colors['text_primary'],
            background=self.colors['bg_primary']
        )
        
        # Style pour les sous-titres
        self.style.configure(
            'Subtitle.TLabel',
            font=('Helvetica', 24, 'bold'),
            foreground=self.colors['text_primary'],
            background=self.colors['bg_primary']
        )
        
        # Configuration du hover des boutons
        self.style.map('Large.TButton',
            background=[('active', self.colors['button_hover'])],
            foreground=[('active', self.colors['text_primary'])]
        )
        
        self.game_manager = GameManager()
        self.create_home_screen()
        
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.geometry("800x600")
        
    def create_home_screen(self):
        # Supprime les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
            
        # Conteneur principal
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🎮 Salle de Jeux 🎮", 
            style='Title.TLabel'
        )
        title_label.pack(pady=30)
        
        # Conteneur pour les boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True)
        
        # Boutons
        games_button = ttk.Button(
            button_frame, 
            text="Jeux", 
            style='Large.TButton',
            command=self.show_games_menu
        )
        games_button.pack(pady=15, ipadx=30, ipady=10)
        
        settings_button = ttk.Button(
            button_frame,
            text="Paramètres",
            style='Large.TButton',
            command=self.show_settings
        )
        settings_button.pack(pady=15, ipadx=30, ipady=10)
        
        quit_button = ttk.Button(
            button_frame, 
            text="Quitter", 
            style='Large.TButton',
            command=self.quit
        )
        quit_button.pack(pady=15, ipadx=30, ipady=10)
        
    def show_settings(self):
        # Supprime les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
            
        # Conteneur principal
        settings_frame = ttk.Frame(self)
        settings_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(
            settings_frame, 
            text="⚙️ Paramètres ⚙️", 
            style='Subtitle.TLabel'
        )
        title_label.pack(pady=20)
        
        # Option plein écran
        fullscreen_button = ttk.Button(
            settings_frame,
            text="Plein écran" if not self.fullscreen else "Mode fenêtré",
            style='Large.TButton',
            command=self.toggle_fullscreen
        )
        fullscreen_button.pack(pady=15, ipadx=30, ipady=10)
        
        # Bouton retour
        back_button = ttk.Button(
            settings_frame,
            text="Retour au menu principal",
            style='Large.TButton',
            command=self.create_home_screen
        )
        back_button.pack(pady=20, ipadx=30, ipady=10)
        
    def show_games_menu(self):
        # Supprime les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
            
        # Conteneur principal
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🎲 Sélection du Jeu 🎲", 
            style='Subtitle.TLabel'
        )
        title_label.pack(pady=20)
        
        # Grille pour les jeux
        games_frame = ttk.Frame(main_frame)
        games_frame.pack(pady=20)
        
        # Organiser les jeux en grille 2x2 + 1 centré
        games = list(self.game_manager.games.items())
        for i, (game_id, game) in enumerate(games):
            row = i // 2
            col = i % 2
            
            if i == len(games) - 1 and i % 2 == 0:  # Dernier jeu si nombre impair
                # Centrer le dernier bouton
                game_button = ttk.Button(
                    games_frame,
                    text=game.name,
                    style='Large.TButton',
                    command=lambda g=game: self.launch_game(g)
                )
                game_button.grid(row=row, column=0, columnspan=2, pady=10, padx=10)
            else:
                game_button = ttk.Button(
                    games_frame,
                    text=game.name,
                    style='Large.TButton',
                    command=lambda g=game: self.launch_game(g)
                )
                game_button.grid(row=row, column=col, pady=10, padx=10)
        
        # Configurer la grille pour centrer les boutons
        games_frame.grid_columnconfigure(0, weight=1)
        games_frame.grid_columnconfigure(1, weight=1)
        
        # Bouton retour
        back_button = ttk.Button(
            main_frame,
            text="Retour au menu principal",
            style='Large.TButton',
            command=self.create_home_screen
        )
        back_button.pack(pady=20, ipadx=30, ipady=10)
        
    def launch_game(self, game):
        # Crée une nouvelle fenêtre pour le jeu
        game_window = tk.Toplevel(self)
        game_window.title(game.name)
        game_window.geometry("600x800")
        game_window.configure(bg=self.colors['bg_primary'])
        
        # Centre la fenêtre
        game_window.update_idletasks()
        width = game_window.winfo_width()
        height = game_window.winfo_height()
        x = (game_window.winfo_screenwidth() // 2) - (width // 2)
        y = (game_window.winfo_screenheight() // 2) - (height // 2)
        game_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Empêche le redimensionnement
        game_window.resizable(False, False)
        
        # Crée les widgets du jeu
        game.create_game_widgets(game_window)
        
        # Configure la fenêtre pour être modale
        game_window.transient(self)
        game_window.grab_set()
        
        # Attend que la fenêtre soit fermée avant de continuer
        self.wait_window(game_window)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
