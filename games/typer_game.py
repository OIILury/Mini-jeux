import tkinter as tk
from tkinter import ttk
import random
import time
import json
from pathlib import Path
from games.base_game import BaseGame
import os
import sys
import tkinter.messagebox as messagebox

class TyperGame(BaseGame):
    def __init__(self):
        super().__init__("Jeu de Frappe", "typer_game")
        self.words = self.load_words()
        self.current_word = ""
        self.start_time = None
        self.words_typed = 0
        self.max_words = 20
        self.current_mode = "normal"  # Mode par défaut
        self.scores_file = Path("scores/typer_game_scores.json")
        self.scores_file.parent.mkdir(exist_ok=True)
        self.load_scores()
        self.reset()

    @property
    def name(self):
        return self._name

    def resource_path(self, relative_path):
        """Obtient le chemin absolu des ressources"""
        if getattr(sys, 'frozen', False):
            # Si on est dans l'exe (PyInstaller)
            base_path = sys._MEIPASS
            print(f"Chemin PyInstaller: {base_path}")
        else:
            # Si on est en développement
            base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            print(f"Chemin développement: {base_path}")
        
        full_path = os.path.join(base_path, relative_path)
        print(f"Chemin complet du fichier: {full_path}")
        return full_path

    def load_words(self):
        """Charge la liste des mots depuis le fichier"""
        try:
            file_path = self.resource_path('assets/dico.txt')
            with open(file_path, "r", encoding='utf-8') as file:
                return [word.strip() for word in file.readlines() if word.strip()]
        except Exception as e:
            print(f"Erreur lors du chargement du dictionnaire: {str(e)}")
            return ["python", "programmation", "ordinateur", "clavier", "écran"]

    def reset(self):
        self.score = 0
        self.lives = 3
        self.time_left = 60
        self.timer_running = False
        self.current_word = ""
        self.start_time = None
        self.words_typed = 0
        self.max_words = 20
        
    def init_game(self, game_frame):
        # Frame pour le jeu
        self.game_container = ttk.Frame(game_frame, style='Game.TFrame')
        self.game_container.pack(expand=True, pady=20)
        
        # Compteur de mots
        self.counter_label = ttk.Label(
            self.game_container,
            text=f"Mot 1/{self.max_words}",
            style='GameScore.TLabel'
        )
        self.counter_label.pack(pady=10)
        
        # Zone d'affichage du mot
        self.word_label = ttk.Label(
            self.game_container,
            text="",
            font=('Helvetica', 36, 'bold'),
            style='GameTitle.TLabel'
        )
        self.word_label.pack(pady=20)
        
        # Zone de saisie
        self.entry = ttk.Entry(
            self.game_container,
            font=('Helvetica', 14),
            justify='center',
            width=20
        )
        self.entry.pack(pady=10)
        self.entry.focus()
        
        # Message de feedback
        self.feedback_label = ttk.Label(
            self.game_container,
            text="",
            style='GameScore.TLabel'
        )
        self.feedback_label.pack(pady=10)
        
        # Statistiques
        self.stats_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        self.stats_frame.pack(fill='x', pady=10)
        
        self.wpm_label = ttk.Label(
            self.stats_frame,
            text="WPM: 0",
            style='GameScore.TLabel'
        )
        self.wpm_label.pack(side='left', padx=10)
        
        self.accuracy_label = ttk.Label(
            self.stats_frame,
            text="Précision: 100%",
            style='GameScore.TLabel'
        )
        self.accuracy_label.pack(side='right', padx=10)
        
        # Bind la touche Enter
        self.entry.bind('<Return>', lambda e: self.check_word())
        
        # Démarre le jeu
        self.next_word()
        self.start_time = time.time()
        
    def next_word(self):
        """Affiche le prochain mot"""
        self.current_word = random.choice(self.words)
        self.word_label.config(text=self.current_word)
        self.entry.delete(0, tk.END)
        
    def check_word(self):
        """Vérifie le mot saisi"""
        typed_word = self.entry.get().strip()
        self.words_typed += 1
        
        if typed_word == self.current_word:
            # Points basés sur la longueur du mot
            points = len(typed_word)
            self.update_score(points)
            self.feedback_label.config(text="Correct ! 👍")
        else:
            self.feedback_label.config(text="Incorrect ! 😢")
            
        # Mise à jour des statistiques
        elapsed_time = time.time() - self.start_time
        wpm = int((self.words_typed / elapsed_time) * 60)
        self.wpm_label.config(text=f"WPM: {wpm}")
        
        if self.words_typed >= self.max_words:
            self.show_game_over(f"Terminé ! Vitesse moyenne: {wpm} WPM")
        else:
            self.counter_label.config(text=f"Mot {self.words_typed + 1}/{self.max_words}")
            self.next_word()

    def game_over(self):
        """Gère la fin de partie"""
        self.timer_running = False
        self.save_score()
        self.update_scores_display()
        
        # Afficher le score final
        self.word_label.config(text=f"Partie terminée!\nScore final: {self.score}")
        self.entry.pack_forget()
        
        # Bouton nouvelle partie
        ttk.Button(self.game_container, text="Nouvelle partie", command=self.restart_game).pack(pady=10)

    def restart_game(self):
        """Redémarre le jeu"""
        self.reset()
        for widget in self.game_container.winfo_children():
            widget.destroy()
        self.init_game(self.parent)

    def load_scores(self):
        """Charge les meilleurs scores"""
        self.high_scores = {'timer': [], 'lives': []}
        if self.scores_file.exists():
            with open(self.scores_file, 'r') as f:
                self.high_scores = json.load(f)

    def save_score(self):
        """Sauvegarde le score actuel"""
        try:
            player_name = f"Joueur (WPM: {self.get_current_wpm()})"
            super().save_score(player_name)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")
            messagebox.showerror(
                "Erreur",
                "Impossible de sauvegarder le score. Veuillez réessayer."
            )

    def get_current_wpm(self):
        """Calcule le WPM actuel"""
        if self.start_time is None or self.words_typed == 0:
            return 0
        elapsed_time = time.time() - self.start_time
        return int((self.words_typed / elapsed_time) * 60)

    def update_scores_display(self):
        """Met à jour l'affichage des meilleurs scores"""
        for widget in self.scores_frame.winfo_children():
            widget.destroy()

        timer_frame = ttk.Frame(self.scores_frame)
        timer_frame.pack(side='left', expand=True, padx=10)
        ttk.Label(timer_frame, text="🕒 Mode Timer", font=('Helvetica', 10, 'bold')).pack(pady=(0,5))
        
        for i, score in enumerate(self.high_scores['timer'][:5], 1):
            ttk.Label(timer_frame, text=f"{i}. {score} points", font=('Helvetica', 10)).pack(pady=1)

        ttk.Separator(self.scores_frame, orient='vertical').pack(side='left', fill='y', padx=10)

        lives_frame = ttk.Frame(self.scores_frame)
        lives_frame.pack(side='left', expand=True, padx=10)
        ttk.Label(lives_frame, text="❤️ Mode Vies", font=('Helvetica', 10, 'bold')).pack(pady=(0,5))
        
        for i, score in enumerate(self.high_scores['lives'][:5], 1):
            ttk.Label(lives_frame, text=f"{i}. {score} points", font=('Helvetica', 10)).pack(pady=1)
