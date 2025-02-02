import json
import os
from pathlib import Path

class ScoreManager:
    def __init__(self):
        self.scores_dir = Path("scores")
        self.scores_dir.mkdir(exist_ok=True)
        
    def get_scores_file(self, game_id):
        """Retourne le chemin du fichier de scores pour un jeu donné"""
        return self.scores_dir / f"{game_id}_scores.json"
        
    def save_score(self, game_id, player_name, score):
        """Sauvegarde un score pour un jeu"""
        try:
            if not isinstance(score, (int, float)) or score < 0:
                raise ValueError("Le score doit être un nombre positif")
            if not isinstance(player_name, str) or not player_name.strip():
                raise ValueError("Le nom du joueur est invalide")
                
            scores_file = self.get_scores_file(game_id)
            scores = self.get_scores(game_id)
            
            new_score = {
                "player": player_name.strip(),
                "score": int(score),
            }
            
            scores.append(new_score)
            # Trie les scores par ordre décroissant
            scores.sort(key=lambda x: x.get("score", 0), reverse=True)
            # Garde uniquement les 10 meilleurs scores
            scores = scores[:10]
            
            # Assure que le dossier existe
            scores_file.parent.mkdir(exist_ok=True)
            
            with open(scores_file, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")
            raise  # Propage l'erreur pour la gestion dans BaseGame
            
    def get_scores(self, game_id):
        """Récupère les scores pour un jeu"""
        try:
            scores_file = self.get_scores_file(game_id)
            if not scores_file.exists():
                return []
                
            with open(scores_file, "r", encoding="utf-8") as f:
                scores = json.load(f)
                # Vérifie et nettoie les scores
                valid_scores = []
                for score in scores:
                    if isinstance(score, dict) and "score" in score and "player" in score:
                        if isinstance(score["score"], (int, float)) and isinstance(score["player"], str):
                            valid_scores.append(score)
                return valid_scores
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Erreur lors de la lecture des scores : {e}")
            return []
            
    def get_high_score(self, game_id):
        """Récupère le meilleur score pour un jeu"""
        try:
            scores = self.get_scores(game_id)
            if not scores:
                return None
            return scores[0]
        except Exception as e:
            print(f"Erreur lors de la récupération du meilleur score : {e}")
            return None
        
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