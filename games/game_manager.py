from games.number_guess import NumberGuessGame
from games.mental_calc import MentalCalcGame
from games.slot_machine import SlotMachineGame
from games.typer_game import TyperGame
from games.virtual_pet import VirtualPetGame

class GameManager:
    def __init__(self):
        """Initialise la collection de jeux"""
        self.games = {
            "1": NumberGuessGame(),
            "2": MentalCalcGame(),
            "3": SlotMachineGame(),
            "4": TyperGame(),
            "5": VirtualPetGame()
        }
        
    def get_game(self, game_id):
        """Récupère un jeu par son ID"""
        return self.games.get(game_id)
        
    def get_all_games(self):
        """Récupère tous les jeux"""
        return self.games 