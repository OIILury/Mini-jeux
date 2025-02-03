import json
import os
from pathlib import Path

class ScoreManager:
    def __init__(self):
        self.scores_file = "scores.json"
        self._ensure_scores_file_exists()

    def _ensure_scores_file_exists(self):
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump({}, f)

    def save_score(self, game_id, player_name, score):
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
            
            if game_id not in scores:
                scores[game_id] = []
            
            scores[game_id].append({
                'player': player_name,
                'score': score
            })
            
            # Trier les scores par ordre décroissant
            scores[game_id] = sorted(
                scores[game_id],
                key=lambda x: x['score'],
                reverse=True
            )
            
            # Garder uniquement les 10 meilleurs scores
            scores[game_id] = scores[game_id][:10]
            
            with open(self.scores_file, 'w') as f:
                json.dump(scores, f)
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")

    def get_high_score(self, game_id):
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
            
            if game_id in scores and scores[game_id]:
                return scores[game_id][0]  # Retourne le meilleur score
            return None
            
        except Exception as e:
            print(f"Erreur lors de la lecture du meilleur score : {e}")
            return None

    def get_all_scores(self, game_id):
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
            return scores.get(game_id, [])
        except Exception as e:
            print(f"Erreur lors de la lecture des scores : {e}")
            return []

    def get_scores_file(self, game_id):
        """Retourne le chemin du fichier de scores pour un jeu donné"""
        return self.scores_dir / f"{game_id}_scores.json"
        
    def format_scores_for_display(self, game_id):
        """Formate les scores pour l'affichage"""
        try:
            scores = self.get_scores(game_id)
            if not scores:
                return "Aucun score enregistré"
                
            formatted = "🏆 Meilleurs Scores 🏆\n\n"
            for i, score in enumerate(scores, 1):
                formatted += f"{i}. {score['player']}: {score['score']}\n"
            return formatted
        except Exception as e:
            print(f"Erreur lors du formatage des scores : {e}")
            return "Erreur lors de l'affichage des scores" 