import tkinter as tk
from tkinter import ttk
import random
import time
import json
from pathlib import Path
from games.base_game import BaseGame
import tkinter.messagebox as messagebox

class MentalCalcGame(BaseGame):
    """
    Jeu de calcul mental qui génère des opérations mathématiques aléatoires
    que le joueur doit résoudre.
    """

    def __init__(self):
        super().__init__("Calcul Mental", "mental_calc")
        self.operators = ['+', '-', '*']
        self.current_problem = None
        self.start_time = None
        self.problems_solved = 0
        self.max_problems = 10
        self.current_mode = 'timer'  # Mode par défaut
        self.reset()

    @property
    def name(self):
        return self._name

    def reset(self):
        """Réinitialise l'état du jeu"""
        self.current_score = 0
        self.lives = 3
        self.time_left = 60
        self.timer_running = False
        self.current_question = None
        self.problems_solved = 0

    def generate_problem(self):
        """Génère un nouveau problème de calcul mental"""
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        
        if operation == '+':
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
            self.current_answer = num1 + num2
        elif operation == '-':
            num1 = random.randint(50, 100)
            num2 = random.randint(1, num1)
            self.current_answer = num1 - num2
        else:  # multiplication
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 12)
            self.current_answer = num1 * num2
            
        self.problem_label.config(text=f"{num1} {operation} {num2} = ?")
        
    def check_answer(self):
        """Vérifie la réponse de l'utilisateur"""
        try:
            user_answer = int(self.entry.get())
            self.problems_solved += 1
            
            if user_answer == self.current_answer:
                # Points basés sur la rapidité (max 10 points par problème)
                time_taken = time.time() - self.start_time
                points = max(1, min(10, int(20 - time_taken)))
                self.update_score(points)
                
                # En mode timer, bonus de temps toutes les 10 bonnes réponses
                if self.current_mode == 'timer' and self.problems_solved % 10 == 0:
                    self.time_left += 5
                    self.feedback_label.config(text="Correct ! 👍 +5 secondes bonus !")
                else:
                    self.feedback_label.config(text="Correct ! 👍")
                
                # Vérifier la fin du jeu seulement en mode vies
                if self.current_mode == 'lives' and self.problems_solved >= self.max_problems:
                    self.show_game_over("Bravo ! Vous avez terminé tous les problèmes !")
                else:
                    if self.current_mode == 'lives':
                        self.counter_label.config(text=f"Problème {self.problems_solved + 1}/{self.max_problems}")
                    else:
                        self.counter_label.config(text=f"Problèmes résolus: {self.problems_solved}")
                    self.entry.delete(0, tk.END)
                    self.generate_problem()
                    self.start_time = time.time()
            else:
                if self.current_mode == 'lives':
                    self.lives -= 1
                    if self.lives <= 0:
                        self.show_game_over("Plus de vies ! Partie terminée.")
                        return
                self.feedback_label.config(text=f"Incorrect ! La réponse était {self.current_answer}")
                self.entry.delete(0, tk.END)
                self.update_status()
                # Générer un nouveau problème immédiatement après une erreur
                self.generate_problem()
                self.start_time = time.time()
                
        except ValueError:
            self.feedback_label.config(text="Veuillez entrer un nombre valide")
            self.entry.delete(0, tk.END)
            
        try:
            self.entry.focus()
        except Exception:
            pass  # Ignore les erreurs de focus si la fenêtre n'existe plus

    def init_game(self, game_frame):
        self.parent = game_frame
        self.frame = ttk.Frame(game_frame, padding="20", style='Game.TFrame')
        self.frame.pack(expand=True, fill="both")

        # Titre
        ttk.Label(
            self.frame,
            text="🧮 Calcul Mental 🧮",
            style='GameTitle.TLabel'
        ).pack(pady=20)

        # Sélection du mode
        self.mode_frame = ttk.LabelFrame(
            self.frame,
            text="Mode de jeu",
            padding=10,
            style='Game.TFrame'
        )
        self.mode_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(
            self.mode_frame,
            text="⏱️ Mode Timer (60s)",
            style='Game.TButton',
            command=self.start_timer_mode
        ).pack(side='left', expand=True, padx=5)

        ttk.Button(
            self.mode_frame,
            text="❤️ Mode 3 Vies",
            style='Game.TButton',
            command=self.start_lives_mode
        ).pack(side='left', expand=True, padx=5)

        # Zone de jeu (initialement cachée)
        self.game_frame = ttk.Frame(self.frame, style='Game.TFrame')
        self.game_frame.pack(fill='x', pady=20)
        
        # Informations de jeu
        self.info_frame = ttk.Frame(self.game_frame, style='Game.TFrame')
        self.info_frame.pack(fill='x')
        
        # Compteur de problèmes
        self.counter_label = ttk.Label(
            self.info_frame,
            text="Problèmes résolus: 0",
            style='GameScore.TLabel'
        )
        self.counter_label.pack(side='top', pady=5)
        
        self.score_label = ttk.Label(
            self.info_frame,
            text="Score: 0",
            style='GameScore.TLabel'
        )
        self.score_label.pack(side='left', padx=10)
        
        self.status_label = ttk.Label(
            self.info_frame,
            text="",
            style='GameScore.TLabel'
        )
        self.status_label.pack(side='right', padx=10)

        # Question
        self.problem_label = ttk.Label(
            self.game_frame,
            text="",
            style='GameTitle.TLabel'
        )
        self.problem_label.pack(pady=20)

        # Zone de réponse
        self.entry = ttk.Entry(
            self.game_frame,
            font=('Helvetica', 14),
            justify='center',
            width=10
        )
        self.entry.pack(pady=10)
        
        # Bind la touche Enter pour la validation
        self.entry.bind('<Return>', lambda e: self.check_answer())
        self.entry.bind('<KP_Enter>', lambda e: self.check_answer())  # Pour le pavé numérique
        
        # Bouton de validation
        ttk.Button(
            self.game_frame,
            text="Valider",
            style='Game.TButton',
            command=self.check_answer
        ).pack(pady=10)

        # Message de feedback
        self.feedback_label = ttk.Label(
            self.game_frame,
            text="",
            style='GameScore.TLabel',
            wraplength=300  # Pour permettre le retour à la ligne du message
        )
        self.feedback_label.pack(pady=10)

        # Masquer la zone de jeu au départ
        self.game_frame.pack_forget()

    def start_timer_mode(self):
        """Démarre le mode timer"""
        self.reset()
        self.current_mode = 'timer'
        self.time_left = 60
        self.timer_running = True
        self.mode_frame.pack_forget()
        self.game_frame.pack(fill='x', pady=20)
        self.counter_label.config(text="Problèmes résolus: 0")
        self.update_status()
        self.next_question()
        self.update_timer()
        try:
            self.entry.focus()
        except Exception:
            pass

    def start_lives_mode(self):
        """Démarre le mode vies"""
        self.reset()
        self.current_mode = 'lives'
        self.lives = 3
        self.mode_frame.pack_forget()
        self.game_frame.pack(fill='x', pady=20)
        self.counter_label.config(text=f"Problème 1/{self.max_problems}")
        self.update_status()
        self.next_question()
        try:
            self.entry.focus()
        except Exception:
            pass

    def update_timer(self):
        """Met à jour le timer"""
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.update_status()
            self.timer_id = self.parent.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.game_over()

    def update_status(self):
        """Met à jour l'affichage du statut"""
        if self.current_mode == 'timer':
            self.status_label.config(text=f"Temps: {self.time_left}s")
        else:
            self.status_label.config(text=f"Vies: {'❤️' * self.lives}")

    def next_question(self):
        """Affiche la question suivante"""
        self.generate_problem()
        self.start_time = time.time()

    def game_over(self):
        """Gère la fin de partie"""
        self.cleanup()  # Nettoie les timers et événements
        self.timer_running = False
        self.save_score()
        
        # Message personnalisé selon le mode
        if self.current_mode == 'timer':
            message = f"Temps écoulé !\nProblèmes résolus : {self.problems_solved}\nScore final: {self.current_score}"
        else:
            message = f"Partie terminée!\nScore final: {self.current_score}"
            
        self.problem_label.config(text=message)
        self.entry.pack_forget()
        
        # Bouton nouvelle partie
        ttk.Button(
            self.game_frame,
            text="Nouvelle partie",
            style='Game.TButton',
            command=self.restart_game
        ).pack(pady=10)

    def restart_game(self):
        """Redémarre le jeu"""
        self.cleanup()
        self.reset()
        
        # Nettoyer la zone de jeu
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        # Recréer uniquement les widgets de la zone de jeu
        # Informations de jeu
        self.info_frame = ttk.Frame(self.game_frame, style='Game.TFrame')
        self.info_frame.pack(fill='x')
        
        # Compteur de problèmes
        self.counter_label = ttk.Label(
            self.info_frame,
            text="Problèmes résolus: 0",
            style='GameScore.TLabel'
        )
        self.counter_label.pack(side='top', pady=5)
        
        self.score_label = ttk.Label(
            self.info_frame,
            text="Score: 0",
            style='GameScore.TLabel'
        )
        self.score_label.pack(side='left', padx=10)
        
        self.status_label = ttk.Label(
            self.info_frame,
            text="",
            style='GameScore.TLabel'
        )
        self.status_label.pack(side='right', padx=10)

        # Question
        self.problem_label = ttk.Label(
            self.game_frame,
            text="",
            style='GameTitle.TLabel'
        )
        self.problem_label.pack(pady=20)

        # Zone de réponse avec les mêmes bindings
        self.entry = ttk.Entry(
            self.game_frame,
            font=('Helvetica', 14),
            justify='center',
            width=10
        )
        self.entry.pack(pady=10)
        
        # Bind la touche Enter pour la validation
        self.entry.bind('<Return>', lambda e: self.check_answer())
        self.entry.bind('<KP_Enter>', lambda e: self.check_answer())  # Pour le pavé numérique
        
        # Bouton de validation
        ttk.Button(
            self.game_frame,
            text="Valider",
            style='Game.TButton',
            command=self.check_answer
        ).pack(pady=10)
        
        # Message de feedback
        self.feedback_label = ttk.Label(
            self.game_frame,
            text="",
            style='GameScore.TLabel',
            wraplength=300  # Pour permettre le retour à la ligne du message
        )
        self.feedback_label.pack(pady=10)
        
        # Afficher le mode de sélection
        self.mode_frame.pack(fill='x', padx=20, pady=10)
        self.game_frame.pack_forget()

    def save_score(self):
        """Sauvegarde le score actuel"""
        try:
            player_name = f"Joueur ({self.current_mode})"
            super().save_score(player_name)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")
            messagebox.showerror(
                "Erreur",
                "Impossible de sauvegarder le score. Veuillez réessayer."
            )

    def update_scores_display(self):
        """Met à jour l'affichage des meilleurs scores"""
        for widget in self.scores_frame.winfo_children():
            widget.destroy()

        # Création d'un cadre pour chaque mode
        timer_frame = ttk.Frame(self.scores_frame)
        timer_frame.pack(side='left', expand=True, padx=10)
        ttk.Label(
            timer_frame, 
            text="🕒 Mode Timer", 
            font=('Helvetica', 10, 'bold')
        ).pack(pady=(0,5))
        
        for i, score in enumerate(self.high_scores['timer'][:5], 1):
            ttk.Label(
                timer_frame, 
                text=f"{i}. {score} points",
                font=('Helvetica', 10)
            ).pack(pady=1)

        # Séparateur vertical
        ttk.Separator(
            self.scores_frame, 
            orient='vertical'
        ).pack(side='left', fill='y', padx=10)

        # Scores mode vies
        lives_frame = ttk.Frame(self.scores_frame)
        lives_frame.pack(side='left', expand=True, padx=10)
        ttk.Label(
            lives_frame, 
            text="❤️ Mode Vies", 
            font=('Helvetica', 10, 'bold')
        ).pack(pady=(0,5))
        
        for i, score in enumerate(self.high_scores['lives'][:5], 1):
            ttk.Label(
                lives_frame, 
                text=f"{i}. {score} points",
                font=('Helvetica', 10)
            ).pack(pady=1)

    def update_score_display(self):
        """Met à jour l'affichage du score"""
        self.score_label.config(text=f"Score: {self.current_score}")

    def cleanup(self):
        """Nettoie les timers et événements"""
        if hasattr(self, 'timer_id'):
            self.parent.after_cancel(self.timer_id)
        self.timer_running = False

    def quit_game(self):
        """Ferme la fenêtre du jeu"""
        self.cleanup()
        super().quit_game()