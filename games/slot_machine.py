import tkinter as tk
from tkinter import ttk
import random
from games.base_game import BaseGame
import time

class SlotMachineGame(BaseGame):
    def __init__(self):
        super().__init__("Machine à Sous", "slot_machine")
        # Suppression de la gestion individuelle des scores - utilise ScoreManager
        
        # Liste des émojis possibles avec leurs couleurs
        self.symbols = ["🍒", "🍊", "🍋", "🍇", "💎", "7️⃣"]
        self.symbol_values = {
            "🍒": 10,
            "🍊": 20,
            "🍋": 30,
            "🍇": 40,
            "💎": 100,
            "7️⃣": 777
        }
        
        # Paramètres d'animation ajustés
        self.initial_speed = 20  # Vitesse initiale plus rapide
        self.max_speed = 5  # Vitesse maximale pendant la rotation
        self.spin_slowdown = 1.18  # Ralentissement plus progressif
        self.min_spins = 70  # Plus de rotations pour un meilleur effet
        self.symbol_height = 90
        
        # Paramètres d'inertie
        self.acceleration_phase = 5  # Nombre d'étapes pour atteindre la vitesse max
        self.deceleration_phase = 8  # Nombre d'étapes pour le ralentissement
        
        # État des rouleaux
        self.reel_speeds = [0, 0, 0]  # Vitesse actuelle de chaque rouleau
        self.reel_positions = [0, 0, 0]  # Position Y de chaque rouleau
        
        # Table des gains
        self.payouts = {
            "🍒": 10,
            "🍊": 20,
            "🍋": 30,
            "🍇": 40,
            "💎": 100,
            "7️⃣": 777
        }
        
        # Paramètres pour l'animation verticale
        self.visible_symbols = 3  # Nombre de symboles visibles par rouleau
        self.reel_strips = []  # Liste des bandes de symboles pour chaque rouleau
        self.current_positions = [0, 0, 0]  # Position actuelle de chaque rouleau
        
        # Créer les bandes de symboles pour chaque rouleau
        for _ in range(3):
            strip = self.symbols * 3  # Répète les symboles pour créer une bande
            random.shuffle(strip)  # Mélange les symboles
            self.reel_strips.append(strip)

        self.credits = 1000
        self.bet = 10
        self.is_spinning = False
        self.max_credits = 1000  # Pour suivre le maximum de crédits atteints

        self.reset()

    @property
    def name(self):
        return self._name

    def reset(self):
        self.credits = 1000
        self.bet = 10
        self.reels = [self.symbols[0] for _ in range(3)]  # État initial des rouleaux
        self.is_spinning = False
        self.max_credits = 1000  # Pour suivre le maximum de crédits atteints

    def init_game(self, game_frame):
        # Frame pour le jeu
        self.game_container = ttk.Frame(game_frame, style='Game.TFrame')
        self.game_container.pack(expand=True, pady=20)
        
        # Crédits et mise
        info_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        info_frame.pack(fill='x', pady=10)
        
        self.credits_label = ttk.Label(
            info_frame,
            text=f"Crédits: {self.credits}",
            style='GameScore.TLabel'
        )
        self.credits_label.pack(side='left', padx=10)
        
        self.bet_label = ttk.Label(
            info_frame,
            text=f"Mise: {self.bet}",
            style='GameScore.TLabel'
        )
        self.bet_label.pack(side='right', padx=10)
        
        # Zone des symboles
        symbols_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        symbols_frame.pack(pady=20)
        
        self.symbol_labels = []
        for i in range(3):
            label = ttk.Label(
                symbols_frame,
                text="❓",
                font=('Helvetica', 48),
                style='GameTitle.TLabel'
            )
            label.pack(side='left', padx=20)
            self.symbol_labels.append(label)
            
        # Boutons de contrôle
        control_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        control_frame.pack(pady=20)
        
        ttk.Button(
            control_frame,
            text="- Mise",
            style='Game.TButton',
            command=self.decrease_bet
        ).pack(side='left', padx=5)
        
        self.spin_button = ttk.Button(
            control_frame,
            text="SPIN !",
            style='Game.TButton',
            command=self.spin
        )
        self.spin_button.pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="+ Mise",
            style='Game.TButton',
            command=self.increase_bet
        ).pack(side='left', padx=5)
        
        # Message de résultat
        self.result_label = ttk.Label(
            self.game_container,
            text="",
            style='GameScore.TLabel'
        )
        self.result_label.pack(pady=10)

    def update_credits(self, amount):
        """Met à jour les crédits"""
        self.credits += amount
        self.credits_label.config(text=f"Crédits: {self.credits}")
        self.update_score(amount if amount > 0 else 0)
        
        if self.credits <= 0:
            self.show_game_over("Plus de crédits ! Partie terminée.")
            
    def increase_bet(self):
        """Augmente la mise"""
        if not self.is_spinning and self.bet < min(100, self.credits):
            self.bet += 10
            self.bet_label.config(text=f"Mise: {self.bet}")
            
    def decrease_bet(self):
        """Diminue la mise"""
        if not self.is_spinning and self.bet > 10:
            self.bet -= 10
            self.bet_label.config(text=f"Mise: {self.bet}")
            
    def spin(self):
        """Lance la machine"""
        if self.is_spinning or self.credits < self.bet:
            return
            
        self.is_spinning = True
        self.spin_button.config(state='disabled')
        self.update_credits(-self.bet)
        self.result_label.config(text="")
        
        # Animation de spin
        self.animate_spin(10)
        
    def animate_spin(self, remaining):
        """Anime le spin des symboles"""
        if remaining > 0:
            for label in self.symbol_labels:
                label.config(text=random.choice(self.symbols))
            self.after(100, lambda: self.animate_spin(remaining - 1))
        else:
            self.finish_spin()
            
    def finish_spin(self):
        """Termine le spin et calcule les gains"""
        # Tire les symboles finaux
        final_symbols = [random.choice(self.symbols) for _ in range(3)]
        for label, symbol in zip(self.symbol_labels, final_symbols):
            label.config(text=symbol)
            
        # Calcule les gains
        if len(set(final_symbols)) == 1:  # Tous identiques
            win = self.symbol_values[final_symbols[0]] * self.bet
            self.result_label.config(text=f"🎉 JACKPOT ! +{win} crédits !")
            self.update_credits(win)
        elif len(set(final_symbols)) == 2:  # Deux identiques
            win = self.bet
            self.result_label.config(text=f"👍 Petite victoire ! +{win} crédits")
            self.update_credits(win)
        else:
            self.result_label.config(text="😢 Perdu !")
            
        self.is_spinning = False
        self.spin_button.config(state='normal')
        
    def after(self, ms, func):
        """Wrapper pour la fonction after de tkinter"""
        self.parent.after(ms, func)

    # Suppression des méthodes de gestion individuelle des scores - utilise ScoreManager centralisé 