import tkinter as tk
from tkinter import ttk, colorchooser
import random
from games.base_game import BaseGame
import time
import json
from pathlib import Path

class Item:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = 4
        self.types = {
            'coin': {'color': 'gold', 'value': 1},
            'gem': {'color': 'purple', 'value': 5},
            'food': {'color': 'brown', 'value': 3}
        }
        self.type = random.choice(list(self.types.keys()))
        self.color = self.types[self.type]['color']
        self.value = self.types[self.type]['value']
        
        self.body = canvas.create_rectangle(
            x-self.size, y-self.size,
            x+self.size, y+self.size,
            fill=self.color,
            outline='white'
        )

    def to_dict(self):
        """Convertit l'item en dictionnaire pour la sauvegarde"""
        return {
            'type': self.type,
            'color': self.color,
            'value': self.value,
            'x': self.x,
            'y': self.y
        }
    
    @staticmethod
    def from_dict(canvas, data):
        """Crée un item à partir d'un dictionnaire"""
        item = Item(canvas, data['x'], data['y'])
        item.type = data['type']
        item.color = data['color']
        item.value = data['value']
        return item

class Pet:
    def __init__(self, canvas, x, y, name=None, stats=None, color='red'):
        self.canvas = canvas
        self.name = name or f"Pet_{random.randint(1000, 9999)}"
        self.color = color
        self.size = 5
        self.body = canvas.create_oval(
            x-self.size, y-self.size, 
            x+self.size, y+self.size, 
            fill=color, 
            outline='darkred'
        )
        
        self.stats = stats or {
            'HP': 20,
            'ATK': 5,
            'DEF': 0,
            'MANA': 0,
            'SPD': 5,
            'LUCK': 1
        }
        
        self.x = x
        self.y = y
        self.target = None
        self.is_attacking = False
        self.speed = 2
        self.moving = True
        self.start_random_movement()
        self.inventory = []  # Liste des objets collectés
        self.collecting = False  # État de collecte
        
    def start_random_movement(self):
        """Démarre le mouvement aléatoire du pet"""
        if self.moving and not self.is_attacking:
            # Calcul du nouveau déplacement aléatoire
            dx = random.randint(-self.speed, self.speed)
            dy = random.randint(-self.speed, self.speed)
            
            # Vérification des limites du canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            new_x = self.x + dx
            new_y = self.y + dy
            
            if 5 <= new_x <= canvas_width-5 and 5 <= new_y <= canvas_height-5:
                self.x = new_x
                self.y = new_y
                self.canvas.move(self.body, dx, dy)
            
            # Planifier le prochain mouvement
            self.canvas.after(50, self.start_random_movement)

    def move_to_target(self, target, callback=None):
        """Déplace le pet vers une cible (pet ou item)"""
        if isinstance(target, Pet):
            target_x = target.x
            target_y = target.y
        else:  # Item
            target_x = target.x
            target_y = target.y

        if self.is_attacking or self.collecting:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 15:  # Si assez proche de la cible
                self.is_attacking = False
                self.collecting = False
                if callback:
                    callback()
                return
            
            # Normalisation du vecteur de déplacement
            speed = self.stats['SPD'] * 0.5
            dx = (dx/distance) * speed
            dy = (dy/distance) * speed
            
            self.x += dx
            self.y += dy
            self.canvas.move(self.body, dx, dy)
            
            # Continue le mouvement
            self.canvas.after(50, lambda: self.move_to_target(target, callback))

    def update_color(self, color):
        """Met à jour la couleur du pet"""
        self.color = color
        self.canvas.itemconfig(self.body, fill=color)

    def to_dict(self):
        """Convertit le pet en dictionnaire pour la sauvegarde"""
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'color': self.color,
            'stats': self.stats,
            'inventory': [item.to_dict() for item in self.inventory]
        }

    @staticmethod
    def from_dict(canvas, data):
        """Crée un pet à partir d'un dictionnaire"""
        pet = Pet(
            canvas=canvas,
            x=data['x'],
            y=data['y'],
            name=data['name'],
            stats=data['stats'],
            color=data['color']
        )
        # Création des items de l'inventaire sans représentation visuelle
        pet.inventory = []
        for item_data in data.get('inventory', []):
            item = Item(canvas, 0, 0)  # Position non importante pour l'inventaire
            item.type = item_data['type']
            item.color = item_data['color']
            item.value = item_data['value']
            canvas.delete(item.body)  # Supprimer la représentation visuelle
            pet.inventory.append(item)
        return pet

    def die(self):
        """Crée une tombe à l'emplacement de la mort du pet"""
        self.canvas.delete(self.body)
        
        # Crée une croix (tombe)
        size = self.size * 1.5
        # Ligne verticale de la croix
        self.canvas.create_line(
            self.x, self.y - size,
            self.x, self.y + size,
            fill='gray70',
            width=2
        )
        # Ligne horizontale de la croix
        self.canvas.create_line(
            self.x - size, self.y,
            self.x + size, self.y,
            fill='gray70',
            width=2
        )
        # Texte du nom
        self.canvas.create_text(
            self.x, self.y + size + 10,
            text=f"RIP {self.name}",
            fill='gray70',
            font=('Arial', 8)
        )

    def collect_item(self, item):
        """Collecte un objet et l'ajoute à l'inventaire"""
        self.inventory.append(item)
        self.canvas.delete(item.body)
        self.collecting = False
        self.moving = True
        self.start_random_movement()

    def move_to_item(self, item, callback=None):
        """Déplace le pet vers un objet"""
        if self.collecting and item in self.canvas.find_all():  # Vérifie si l'item existe toujours
            dx = item.x - self.x
            dy = item.y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 10:  # Si assez proche de l'objet
                self.collecting = False
                if callback and item in self.canvas.find_all():  # Double vérification
                    callback()
                return
            
            # Normalisation du vecteur de déplacement
            speed = self.stats['SPD'] * 0.5
            dx = (dx/distance) * speed
            dy = (dy/distance) * speed
            
            self.x += dx
            self.y += dy
            self.canvas.move(self.body, dx, dy)
            
            # Continue le mouvement seulement si l'item existe toujours
            if item in self.canvas.find_all():
                self.canvas.after(50, lambda: self.move_to_item(item, callback))
            else:
                self.collecting = False
                self.moving = True
                self.start_random_movement()

class PetStatsFrame(ttk.Frame):
    def __init__(self, parent, pet, game):
        super().__init__(parent)
        self.pet = pet
        self.game = game
        
        # Frame principale avec le nom du pet
        self.main_frame = ttk.LabelFrame(self, text=f"Stats de {pet.name}", padding="5")
        self.main_frame.pack(fill='x', pady=5, padx=5)
        
        # Frame pour les stats
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill='x', expand=True)
        
        # Création des labels pour chaque stat (en ligne)
        self.stat_labels = {}
        column = 0
        for stat, value in pet.stats.items():
            # Container pour chaque paire stat/valeur
            stat_container = ttk.Frame(stats_frame)
            stat_container.grid(row=0, column=column, padx=5)
            
            ttk.Label(stat_container, text=f"{stat}:").pack(side='left')
            label = ttk.Label(stat_container, text=str(value))
            label.pack(side='left')
            self.stat_labels[stat] = label
            column += 1
        
        # Configure les colonnes pour qu'elles s'étirent uniformément
        for i in range(column):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Boutons de contrôle
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(
            button_frame,
            text="Contrôler",
            command=lambda: self.game.open_control_window(self.pet)
        ).pack(side='left', padx=2, expand=True)
        
        ttk.Button(
            button_frame,
            text="Couleur",
            command=self.change_color
        ).pack(side='left', padx=2, expand=True)
        
        self.pack(fill='x')

    def change_color(self):
        """Ouvre un sélecteur de couleur"""
        color = colorchooser.askcolor(color=self.pet.color)[1]
        if color:
            self.pet.update_color(color)

    def update_stats(self):
        """Met à jour l'affichage des stats"""
        for stat, label in self.stat_labels.items():
            label.config(text=str(self.pet.stats[stat]))
            
            # Change la couleur si les HP sont bas
            if stat == 'HP':
                if self.pet.stats['HP'] <= 5:
                    label.config(foreground='red')
                elif self.pet.stats['HP'] <= 10:
                    label.config(foreground='orange')
                else:
                    label.config(foreground='black')

    def update_name(self, new_name):
        """Met à jour l'affichage du nom"""
        self.main_frame.configure(text=f"Stats de {new_name}")

class PetControlWindow(tk.Toplevel):
    def __init__(self, parent, pet, game):
        super().__init__(parent)
        self.pet = pet
        self.game = game
        
        # Configuration de la fenêtre
        self.title(f"Contrôle de {pet.name}")
        self.geometry("300x500")
        
        # Frame principale
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")
        
        # Frame pour le nom
        name_frame = ttk.LabelFrame(main_frame, text="Nom", padding="5")
        name_frame.pack(fill='x', pady=5)
        
        # Champ de texte pour le nom
        self.name_var = tk.StringVar(value=pet.name)
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Bouton pour changer le nom
        ttk.Button(
            name_frame,
            text="Renommer",
            command=self.rename_pet
        ).pack(side='right', padx=5)
        
        # Informations du pet
        info_frame = ttk.LabelFrame(main_frame, text="Informations", padding="5")
        info_frame.pack(fill='x', pady=5)
        
        self.name_label = ttk.Label(info_frame, text=f"Nom: {pet.name}")
        self.name_label.pack()
        
        # Stats actuelles
        for stat, value in pet.stats.items():
            ttk.Label(info_frame, text=f"{stat}: {value}").pack()
        
        # Actions disponibles
        actions_frame = ttk.LabelFrame(main_frame, text="Actions", padding="5")
        actions_frame.pack(fill='x', pady=5)
        
        # Bouton Attaquer
        ttk.Button(
            actions_frame,
            text="Attaquer un pet",
            command=self.show_attack_menu
        ).pack(fill='x', pady=2)
        
        # Bouton Entraînement
        ttk.Button(
            actions_frame,
            text="S'entraîner",
            command=self.train_pet
        ).pack(fill='x', pady=2)
        
        # Bouton Collecter
        ttk.Button(
            actions_frame,
            text="Collecter objet proche",
            command=self.collect_nearest_item
        ).pack(fill='x', pady=2)
        
        # Bouton Inventaire
        ttk.Button(
            actions_frame,
            text="Ouvrir l'inventaire",
            command=self.show_inventory
        ).pack(fill='x', pady=2)
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="Journal", padding="5")
        log_frame.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap='word')
        self.log_text.pack(fill='both', expand=True)

    def show_attack_menu(self):
        """Affiche le menu d'attaque"""
        attack_window = tk.Toplevel(self)
        attack_window.title("Choisir une cible")
        attack_window.geometry("200x300")
        
        frame = ttk.Frame(attack_window, padding="10")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(
            frame,
            text="Choisir un pet à attaquer:",
            font=('Arial', 10, 'bold')
        ).pack(pady=5)
        
        # Liste des pets disponibles (excluant le pet actuel)
        available_targets = [p for p in self.game.pets if p != self.pet]
        
        if not available_targets:
            ttk.Label(
                frame,
                text="Aucune cible disponible",
                foreground='red'
            ).pack(pady=10)
            return
        
        for target in available_targets:
            ttk.Button(
                frame,
                text=f"{target.name} (HP: {target.stats['HP']})",
                command=lambda t=target: self.attack_pet(t)
            ).pack(fill='x', pady=2)

    def attack_pet(self, target):
        """Gère l'attaque d'un pet sur un autre"""
        self.pet.is_attacking = True
        self.pet.moving = False
        
        def perform_attack():
            damage = self.pet.stats['ATK'] - target.stats['DEF']
            damage = max(1, damage)  # Au moins 1 point de dégât
            
            target.stats['HP'] -= damage
            
            self.log_text.insert('1.0', f"{self.pet.name} attaque {target.name} et inflige {damage} dégâts!\n")
            
            if target.stats['HP'] <= 0:
                self.log_text.insert('1.0', f"{target.name} est vaincu!\n")
                self.game.remove_pet(target)
            else:
                self.game.update_pet_stats(target)
            
            # Reprendre le mouvement normal
            self.pet.is_attacking = False
            self.pet.moving = True
            self.pet.start_random_movement()
        
        # Déplacer le pet vers sa cible
        self.pet.move_to_target(target, perform_attack)
        self.log_text.insert('1.0', f"En route vers {target.name}...\n")

    def train_pet(self):
        """Entraîne le pet en améliorant une stat aléatoire"""
        stats = ['ATK', 'DEF', 'MANA', 'SPD', 'LUCK']
        stat_to_improve = random.choice(stats)
        
        # Amélioration basée sur la chance du pet
        improvement = random.randint(1, max(1, self.pet.stats['LUCK']))
        self.pet.stats[stat_to_improve] += improvement
        
        # Mise à jour du log
        self.log_text.insert('1.0', f"Entraînement: +{improvement} en {stat_to_improve}!\n")
        
        # Mise à jour des stats affichées
        if hasattr(self.game, 'update_pet_stats'):
            self.game.update_pet_stats(self.pet)

    def show_inventory(self):
        """Affiche l'inventaire dans une nouvelle fenêtre"""
        inventory_window = tk.Toplevel(self)
        inventory_window.title(f"Inventaire de {self.pet.name}")
        inventory_window.geometry("200x300")
        
        frame = ttk.Frame(inventory_window, padding="10")
        frame.pack(fill='both', expand=True)
        
        # En-tête avec valeur totale
        total_value = sum(item.value for item in self.pet.inventory)
        ttk.Label(
            frame,
            text=f"Inventaire de {self.pet.name}\nValeur totale: {total_value}",
            font=('Arial', 12, 'bold')
        ).pack(pady=5)
        
        # Liste des objets
        inventory_text = tk.Text(frame, height=10, wrap='word')
        inventory_text.pack(fill='both', expand=True)
        
        if not self.pet.inventory:
            inventory_text.insert('1.0', "Inventaire vide")
        else:
            counts = {}
            values = {}
            for item in self.pet.inventory:
                counts[item.type] = counts.get(item.type, 0) + 1
                values[item.type] = item.value
            
            for item_type, count in counts.items():
                value = values[item_type] * count
                inventory_text.insert('end', f"{item_type}: {count} (Valeur: {value})\n")
        
        inventory_text.config(state='disabled')  # Lecture seule

    def collect_nearest_item(self):
        """Envoie le pet collecter l'objet le plus proche"""
        nearest_item = self.game.find_nearest_item(self.pet)
        if nearest_item:
            if nearest_item in self.game.items:  # Vérification supplémentaire
                self.pet.collecting = True
                self.pet.moving = False
                
                def on_collect():
                    if nearest_item in self.game.items:  # Vérification finale
                        self.pet.collect_item(nearest_item)
                        self.game.items.remove(nearest_item)
                        self.log_text.insert('1.0', f"Objet collecté: {nearest_item.type}\n")
                    
                    self.pet.moving = True
                    self.pet.start_random_movement()
                
                self.pet.move_to_target(nearest_item, on_collect)
                self.log_text.insert('1.0', f"En route vers l'objet...\n")
        else:
            self.log_text.insert('1.0', "Aucun objet à proximité\n")

    def rename_pet(self):
        """Change le nom du pet"""
        new_name = self.name_var.get().strip()
        if new_name:
            old_name = self.pet.name
            self.pet.name = new_name
            # Mettre à jour le titre de la fenêtre
            self.title(f"Contrôle de {new_name}")
            # Mettre à jour l'affichage des stats
            if self.pet in self.game.pet_frames:
                frame = self.game.pet_frames[self.pet]
                frame.update_name(new_name)
            # Log du changement
            self.log_text.insert('1.0', f"Nom changé de {old_name} à {new_name}\n")

class VirtualPetGame(BaseGame):
    def __init__(self):
        super().__init__("Tamagotchi", "virtual_pet")
        self.happiness = 100
        self.hunger = 0
        self.energy = 100
        self.last_update = time.time()
        self.pet_color = "#FFD700"  # Couleur par défaut
        self.pets = []
        self.pet_frames = {}
        self.items = []
        self.save_file = Path("virtual_pets.json")
        self.save_file.parent.mkdir(exist_ok=True)
        self.selected_pet = None
        self.spawn_timer = None

    @property
    def name(self):
        return self._name

    def init_game(self, game_frame):
        # Frame pour le jeu
        self.game_container = ttk.Frame(game_frame, style='Game.TFrame')
        self.game_container.pack(expand=True, pady=20)
        
        # Zone de dessin du pet
        self.canvas = tk.Canvas(
            self.game_container,
            width=200,
            height=200,
            bg=self.game_colors['bg_primary'],
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Dessine le pet
        self.draw_pet()
        
        # Statistiques
        stats_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        stats_frame.pack(fill='x', pady=10)
        
        # Bonheur
        self.happiness_label = ttk.Label(
            stats_frame,
            text=f"Bonheur: {self.happiness}%",
            style='GameScore.TLabel'
        )
        self.happiness_label.pack(side='left', padx=10)
        
        # Faim
        self.hunger_label = ttk.Label(
            stats_frame,
            text=f"Faim: {self.hunger}%",
            style='GameScore.TLabel'
        )
        self.hunger_label.pack(side='left', padx=10)
        
        # Énergie
        self.energy_label = ttk.Label(
            stats_frame,
            text=f"Énergie: {self.energy}%",
            style='GameScore.TLabel'
        )
        self.energy_label.pack(side='left', padx=10)
        
        # Boutons d'action
        actions_frame = ttk.Frame(self.game_container, style='Game.TFrame')
        actions_frame.pack(pady=20)
        
        ttk.Button(
            actions_frame,
            text="Nourrir 🍖",
            style='Game.TButton',
            command=self.feed_pet
        ).pack(side='left', padx=5)
        
        ttk.Button(
            actions_frame,
            text="Jouer 🎾",
            style='Game.TButton',
            command=self.play_with_pet
        ).pack(side='left', padx=5)
        
        ttk.Button(
            actions_frame,
            text="Dormir 💤",
            style='Game.TButton',
            command=self.sleep_pet
        ).pack(side='left', padx=5)
        
        ttk.Button(
            actions_frame,
            text="Couleur 🎨",
            style='Game.TButton',
            command=self.change_color
        ).pack(side='left', padx=5)
        
        # Démarre la mise à jour périodique
        self.update_pet_status()
        
    def draw_pet(self):
        """Dessine le pet sur le canvas"""
        self.canvas.delete("all")
        
        # Corps
        self.canvas.create_oval(50, 50, 150, 150, fill=self.pet_color, width=2)
        
        # Yeux
        eye_state = "normal" if self.energy > 30 else "tired"
        if eye_state == "normal":
            self.canvas.create_oval(80, 80, 95, 95, fill="black")
            self.canvas.create_oval(105, 80, 120, 95, fill="black")
        else:
            self.canvas.create_line(80, 87, 95, 87, fill="black", width=2)
            self.canvas.create_line(105, 87, 120, 87, fill="black", width=2)
            
        # Bouche
        if self.happiness > 70:
            # Sourire
            self.canvas.create_arc(75, 70, 125, 120, start=0, extent=-180, fill="black")
        elif self.happiness > 30:
            # Neutre
            self.canvas.create_line(75, 110, 125, 110, fill="black", width=2)
        else:
            # Triste
            self.canvas.create_arc(75, 110, 125, 160, start=0, extent=180, fill="black")
            
    def update_pet_status(self):
        """Met à jour le statut du pet périodiquement"""
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        # Mise à jour des stats
        self.hunger = min(100, self.hunger + elapsed * 2)
        self.energy = max(0, self.energy - elapsed * 1.5)
        self.happiness = max(0, min(100, self.happiness - elapsed * 1))
        
        # Mise à jour des labels
        self.happiness_label.config(text=f"Bonheur: {int(self.happiness)}%")
        self.hunger_label.config(text=f"Faim: {int(self.hunger)}%")
        self.energy_label.config(text=f"Énergie: {int(self.energy)}%")
        
        # Mise à jour du score
        score = int((self.happiness + (100 - self.hunger) + self.energy) / 3)
        self.update_score(score)
        
        # Redessine le pet
        self.draw_pet()
        
        # Vérifie les conditions de game over
        if self.hunger >= 100 or self.happiness <= 0:
            self.show_game_over("Votre pet est malheureux !")
        else:
            self.last_update = current_time
            self.parent.after(1000, self.update_pet_status)
            
    def feed_pet(self):
        """Nourrit le pet"""
        if self.hunger > 0:
            self.hunger = max(0, self.hunger - 30)
            self.happiness = min(100, self.happiness + 10)
            self.draw_pet()
            
    def play_with_pet(self):
        """Joue avec le pet"""
        if self.energy > 20:
            self.happiness = min(100, self.happiness + 20)
            self.energy = max(0, self.energy - 20)
            self.hunger = min(100, self.hunger + 10)
            self.draw_pet()
            
    def sleep_pet(self):
        """Fait dormir le pet"""
        if self.energy < 100:
            self.energy = min(100, self.energy + 50)
            self.hunger = min(100, self.hunger + 20)
            self.draw_pet()
            
    def change_color(self):
        """Change la couleur du pet"""
        color = colorchooser.askcolor(color=self.pet_color)[1]
        if color:
            self.pet_color = color
            self.draw_pet()

    def create_game_widgets(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(expand=True, fill="both")

        # Frame pour les notifications
        self.notification_frame = ttk.Frame(self.frame)
        self.notification_frame.pack(fill='x', pady=5)

        # Canvas pour l'affichage des pets
        self.canvas = tk.Canvas(
            self.frame,
            width=400,
            height=300,
            bg='black',
            highlightthickness=2,
            highlightbackground='gray'
        )
        self.canvas.pack(pady=10)
        
        # Binding pour la sélection des pets
        self.canvas.bind('<Button-1>', self.select_pet)

        # Frame pour les boutons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5)
        
        ttk.Button(
            button_frame,
            text="Nouveau Pet",
            command=self.create_new_pet
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Sauvegarder",
            command=self.save_game
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Charger",
            command=self.load_game
        ).pack(side='left', padx=5)

        # Frame scrollable pour les stats des pets
        self.stats_container = ttk.Frame(self.frame)
        self.stats_container.pack(fill='both', expand=True)
        
        # Scrollbar et canvas pour le défilement
        self.canvas_stats = tk.Canvas(self.stats_container)
        scrollbar = ttk.Scrollbar(self.stats_container, orient="vertical", 
                                command=self.canvas_stats.yview)
        self.scrollable_frame = ttk.Frame(self.canvas_stats)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_stats.configure(
                scrollregion=self.canvas_stats.bbox("all")
            )
        )

        self.canvas_stats.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_stats.configure(yscrollcommand=scrollbar.set)

        self.canvas_stats.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Démarrer le spawn d'objets
        self.start_item_spawner()
    
    def start_item_spawner(self):
        """Démarre le système de spawn d'objets"""
        self.spawn_item()
        # Programmer le prochain spawn dans 5-10 secondes
        self.spawn_timer = self.frame.after(
            random.randint(5000, 10000),
            self.start_item_spawner
        )
    
    def spawn_item(self):
        """Fait apparaître un nouvel objet sur la carte"""
        if len(self.items) < 10:  # Limite max d'objets
            x = random.randint(10, 390)
            y = random.randint(10, 290)
            item = Item(self.canvas, x, y)
            self.items.append(item)
    
    def find_nearest_item(self, pet):
        """Trouve l'objet le plus proche d'un pet"""
        if not self.items:
            return None
            
        nearest = None
        min_distance = float('inf')
        
        for item in self.items:
            dx = item.x - pet.x
            dy = item.y - pet.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < min_distance:
                min_distance = distance
                nearest = item
        
        return nearest
    
    def reset(self):
        """Réinitialise le jeu"""
        if self.spawn_timer:
            self.frame.after_cancel(self.spawn_timer)
        self.canvas.delete('all')
        for frame in list(self.pet_frames.values()):
            frame.destroy()
        self.pet_frames.clear()
        self.pets.clear()
        self.items.clear()
        self.start_item_spawner()
    
    def show_notification(self, message):
        """Affiche une notification temporaire"""
        # Nettoyer les anciennes notifications
        for widget in self.notification_frame.winfo_children():
            widget.destroy()

        # Créer la nouvelle notification
        notification = ttk.Label(
            self.notification_frame,
            text=message,
            background='yellow',
            padding=5
        )
        notification.pack(fill='x')
        
        # Programmer la suppression
        self.frame.after(2000, notification.destroy)

    def save_game(self):
        """Sauvegarde l'état du jeu"""
        try:
            save_data = {
                'pets': [pet.to_dict() for pet in self.pets],
                'items_on_ground': [item.to_dict() for item in self.items]
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
                
            self.show_notification("Jeu sauvegardé!")
            
        except Exception as e:
            self.show_notification(f"Erreur de sauvegarde: {str(e)}")
            print(f"Détails de l'erreur: {str(e)}")

    def load_game(self):
        """Charge l'état du jeu"""
        if not self.save_file.exists():
            self.show_notification("Aucune sauvegarde trouvée!")
            return
            
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            # Nettoyer l'état actuel
            self.reset()
            
            # Charger les items au sol
            self.items = []
            for item_data in save_data.get('items_on_ground', []):
                try:
                    item = Item.from_dict(self.canvas, item_data)
                    self.items.append(item)
                except Exception as e:
                    print(f"Erreur lors du chargement d'un item: {str(e)}")
                    continue
            
            # Charger les pets
            for pet_data in save_data.get('pets', []):
                try:
                    pet = Pet.from_dict(self.canvas, pet_data)
                    self.pets.append(pet)
                    pet_frame = PetStatsFrame(self.scrollable_frame, pet, self)
                    self.pet_frames[pet] = pet_frame
                except Exception as e:
                    print(f"Erreur lors du chargement d'un pet: {str(e)}")
                    continue
            
            self.show_notification("Jeu chargé!")
            
        except Exception as e:
            self.show_notification(f"Erreur lors du chargement: {str(e)}")
            print(f"Détails de l'erreur: {str(e)}")

    def create_new_pet(self):
        """Crée un nouveau pet"""
        print("Creating new pet...")
        x = random.randint(10, 390)
        y = random.randint(10, 290)
        
        pet = Pet(self.canvas, x, y)
        self.pets.append(pet)
        
        pet_frame = PetStatsFrame(self.scrollable_frame, pet, self)
        self.pet_frames[pet] = pet_frame
        print(f"New pet created at {x}, {y}")

    def select_pet(self, event):
        """Sélectionne un pet quand on clique dessus"""
        clicked_item = self.canvas.find_closest(event.x, event.y)
        
        if clicked_item:
            # Chercher le pet correspondant à l'item cliqué
            for pet in self.pets:
                if pet.body == clicked_item[0]:
                    self.selected_pet = pet
                    self.open_control_window(pet)
                    return

    def open_control_window(self, pet):
        """Ouvre la fenêtre de contrôle pour un pet"""
        control_window = PetControlWindow(self.parent, pet, self)
        control_window.focus()  # Met la fenêtre au premier plan

    def update_pet_stats(self, pet):
        """Met à jour l'affichage des stats d'un pet"""
        if pet in self.pet_frames:
            self.pet_frames[pet].update_stats()

    def remove_pet(self, pet):
        """Supprime un pet du jeu"""
        if pet in self.pets:
            pet.die()  # Crée la tombe
            if pet in self.pet_frames:
                self.pet_frames[pet].destroy()
                del self.pet_frames[pet]
            self.pets.remove(pet)