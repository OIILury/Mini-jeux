import tkinter as tk
from tkinter import ttk
import random
from games.base_game import BaseGame

class NumberGuessGame(BaseGame):
    def __init__(self):
        super().__init__("Devine le Nombre", "number_guess")
        self.target_number = None
        self.attempts = 0
        self.max_attempts = 10
        
    @property
    def name(self):
        return self._name

    def init_game(self, game_frame):
        # Initialisation des variables du jeu
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        
        # Frame pour le jeu
        self.game_container = ttk.Frame(game_frame, style='Game.TFrame')
        self.game_container.pack(expand=True, pady=20)
        
        # Instructions
        instructions = ttk.Label(
            self.game_container,
            text="Devinez un nombre entre 1 et 100",
            style='GameScore.TLabel'
        )
        instructions.pack(pady=10)
        
        # Zone de saisie
        self.entry = ttk.Entry(
            self.game_container,
            font=('Helvetica', 14),
            justify='center',
            width=10
        )
        self.entry.pack(pady=10)
        self.entry.focus()
        
        # Bouton de validation
        submit_button = ttk.Button(
            self.game_container,
            text="Valider",
            style='Game.TButton',
            command=self.check_guess
        )
        submit_button.pack(pady=10)
        
        # Message de feedback
        self.feedback_label = ttk.Label(
            self.game_container,
            text="",
            style='GameScore.TLabel'
        )
        self.feedback_label.pack(pady=10)
        
        # Bind la touche Enter
        self.entry.bind('<Return>', lambda e: self.check_guess())
        
    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            
            if guess == self.target_number:
                # Calcul du score basé sur le nombre d'essais
                score = max(0, 100 - (self.attempts - 1) * 10)
                self.update_score(score)
                self.show_game_over(f"Bravo ! Vous avez trouvé en {self.attempts} essais !")
            elif self.attempts >= self.max_attempts:
                self.show_game_over(f"Perdu ! Le nombre était {self.target_number}")
            else:
                if guess < self.target_number:
                    message = "Plus grand !"
                else:
                    message = "Plus petit !"
                self.feedback_label.config(
                    text=f"{message} (Essai {self.attempts}/{self.max_attempts})"
                )
                self.entry.delete(0, tk.END)
                self.entry.focus()
                
        except ValueError:
            self.feedback_label.config(text="Veuillez entrer un nombre valide")
            self.entry.delete(0, tk.END)
            self.entry.focus()