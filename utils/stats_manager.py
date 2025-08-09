import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np

class StatsManager:
    """Gestionnaire de statistiques détaillées pour l'application"""
    
    def __init__(self, stats_file: str = "stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()
        
    def load_stats(self) -> Dict[str, Any]:
        """Charge les statistiques depuis le fichier"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.create_default_stats()
        except Exception as e:
            print(f"Erreur lors du chargement des statistiques: {e}")
            return self.create_default_stats()
    
    def create_default_stats(self) -> Dict[str, Any]:
        """Crée des statistiques par défaut"""
        return {
            "games": {},
            "sessions": [],
            "performance": {
                "total_playtime": 0,
                "average_session_time": 0,
                "total_sessions": 0
            },
            "achievements": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def save_stats(self):
        """Sauvegarde les statistiques dans le fichier"""
        try:
            self.stats["last_updated"] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des statistiques: {e}")
    
    def record_game_session(self, game_id: str, game_name: str, score: int, duration: float, player_name: str = "Joueur"):
        """Enregistre une session de jeu"""
        session = {
            "game_id": game_id,
            "game_name": game_name,
            "score": score,
            "duration": duration,
            "player_name": player_name,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.stats["sessions"].append(session)
        
        # Mettre à jour les statistiques du jeu
        if game_id not in self.stats["games"]:
            self.stats["games"][game_id] = {
                "name": game_name,
                "total_sessions": 0,
                "total_score": 0,
                "best_score": 0,
                "average_score": 0,
                "total_playtime": 0,
                "scores": [],
                "playtimes": []
            }
        
        game_stats = self.stats["games"][game_id]
        game_stats["total_sessions"] += 1
        game_stats["total_score"] += score
        game_stats["total_playtime"] += duration
        game_stats["scores"].append(score)
        game_stats["playtimes"].append(duration)
        
        if score > game_stats["best_score"]:
            game_stats["best_score"] = score
        
        game_stats["average_score"] = game_stats["total_score"] / game_stats["total_sessions"]
        
        # Mettre à jour les statistiques globales
        self.stats["performance"]["total_playtime"] += duration
        self.stats["performance"]["total_sessions"] += 1
        self.stats["performance"]["average_session_time"] = (
            self.stats["performance"]["total_playtime"] / self.stats["performance"]["total_sessions"]
        )
        
        self.save_stats()
    
    def get_game_stats(self, game_id: str) -> Dict[str, Any]:
        """Récupère les statistiques d'un jeu spécifique"""
        return self.stats["games"].get(game_id, {})
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques globales"""
        return {
            "total_games_played": len(self.stats["games"]),
            "total_sessions": self.stats["performance"]["total_sessions"],
            "total_playtime": self.stats["performance"]["total_playtime"],
            "average_session_time": self.stats["performance"]["average_session_time"],
            "total_score": sum(game["total_score"] for game in self.stats["games"].values()),
            "best_overall_score": max(
                (game["best_score"] for game in self.stats["games"].values()), 
                default=0
            )
        }
    
    def get_recent_sessions(self, days: int = 7) -> List[Dict[str, Any]]:
        """Récupère les sessions récentes"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = []
        
        for session in self.stats["sessions"]:
            session_date = datetime.fromisoformat(session["timestamp"])
            if session_date >= cutoff_date:
                recent_sessions.append(session)
        
        return recent_sessions
    
    def get_score_progression(self, game_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Récupère la progression des scores pour un jeu"""
        cutoff_date = datetime.now() - timedelta(days=days)
        progression = []
        
        for session in self.stats["sessions"]:
            if session["game_id"] == game_id:
                session_date = datetime.fromisoformat(session["timestamp"])
                if session_date >= cutoff_date:
                    progression.append({
                        "date": session_date,
                        "score": session["score"],
                        "duration": session["duration"]
                    })
        
        return sorted(progression, key=lambda x: x["date"])
    
    def create_score_chart(self, game_id: str, parent_widget) -> FigureCanvasTkAgg:
        """Crée un graphique de progression des scores"""
        progression = self.get_score_progression(game_id)
        
        if not progression:
            # Créer un graphique vide
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, 'Aucune donnée disponible', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Progression des Scores')
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            return canvas
        
        # Préparer les données
        dates = [p["date"] for p in progression]
        scores = [p["score"] for p in progression]
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Graphique des scores
        ax.plot(dates, scores, 'o-', linewidth=2, markersize=6, color='#e94560')
        ax.fill_between(dates, scores, alpha=0.3, color='#e94560')
        
        # Configuration du graphique
        ax.set_title('Progression des Scores', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Score')
        ax.grid(True, alpha=0.3)
        
        # Formatage des dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Créer le canvas
        canvas = FigureCanvasTkAgg(fig, parent_widget)
        return canvas
    
    def create_playtime_chart(self, game_id: str, parent_widget) -> FigureCanvasTkAgg:
        """Crée un graphique du temps de jeu"""
        progression = self.get_score_progression(game_id)
        
        if not progression:
            # Créer un graphique vide
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, 'Aucune donnée disponible', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Temps de Jeu')
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            return canvas
        
        # Préparer les données
        dates = [p["date"] for p in progression]
        playtimes = [p["duration"] for p in progression]
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Graphique du temps de jeu
        ax.bar(dates, playtimes, color='#10b981', alpha=0.7)
        
        # Configuration du graphique
        ax.set_title('Temps de Jeu par Session', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temps (secondes)')
        ax.grid(True, alpha=0.3)
        
        # Formatage des dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Créer le canvas
        canvas = FigureCanvasTkAgg(fig, parent_widget)
        return canvas
    
    def create_global_stats_chart(self, parent_widget) -> FigureCanvasTkAgg:
        """Crée un graphique des statistiques globales"""
        games = list(self.stats["games"].keys())
        total_scores = [self.stats["games"][game]["total_score"] for game in games]
        game_names = [self.stats["games"][game]["name"] for game in games]
        
        if not games:
            # Créer un graphique vide
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, 'Aucune donnée disponible', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Scores Totaux par Jeu')
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            return canvas
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Graphique en barres
        colors = ['#e94560', '#a855f7', '#10b981', '#fbbf24', '#f97316']
        bars = ax.bar(game_names, total_scores, color=colors[:len(games)])
        
        # Configuration du graphique
        ax.set_title('Scores Totaux par Jeu', fontsize=14, fontweight='bold')
        ax.set_xlabel('Jeux')
        ax.set_ylabel('Score Total')
        ax.grid(True, alpha=0.3)
        
        # Rotation des labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Créer le canvas
        canvas = FigureCanvasTkAgg(fig, parent_widget)
        return canvas
    
    def get_achievements(self) -> List[Dict[str, Any]]:
        """Récupère les achievements débloqués"""
        achievements = []
        
        # Achievement: Premier jeu
        if self.stats["performance"]["total_sessions"] >= 1:
            achievements.append({
                "id": "first_game",
                "name": "Premier Pas",
                "description": "Joué à votre premier jeu",
                "icon": "🎮",
                "unlocked": True,
                "date": self.stats["sessions"][0]["timestamp"] if self.stats["sessions"] else None
            })
        
        # Achievement: 10 parties
        if self.stats["performance"]["total_sessions"] >= 10:
            achievements.append({
                "id": "ten_games",
                "name": "Joueur Régulier",
                "description": "Joué à 10 parties",
                "icon": "🏆",
                "unlocked": True,
                "date": None  # À calculer
            })
        
        # Achievement: Score élevé
        best_score = self.stats["performance"].get("best_overall_score", 0)
        if best_score >= 100:
            achievements.append({
                "id": "high_score",
                "name": "Score Élevé",
                "description": f"Atteint un score de {best_score}",
                "icon": "⭐",
                "unlocked": True,
                "date": None  # À calculer
            })
        
        # Achievement: Temps de jeu
        total_playtime = self.stats["performance"]["total_playtime"]
        if total_playtime >= 3600:  # 1 heure
            achievements.append({
                "id": "one_hour",
                "name": "Passionné",
                "description": "Joué pendant plus d'une heure",
                "icon": "⏰",
                "unlocked": True,
                "date": None  # À calculer
            })
        
        return achievements
    
    def format_duration(self, seconds: float) -> str:
        """Formate une durée en secondes en format lisible"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def get_most_played_game(self) -> Optional[str]:
        """Retourne le jeu le plus joué"""
        if not self.stats["games"]:
            return None
        
        most_played = max(
            self.stats["games"].items(),
            key=lambda x: x[1]["total_sessions"]
        )
        return most_played[0]
    
    def get_best_performing_game(self) -> Optional[str]:
        """Retourne le jeu avec la meilleure moyenne de score"""
        if not self.stats["games"]:
            return None
        
        best_performing = max(
            self.stats["games"].items(),
            key=lambda x: x[1]["average_score"]
        )
        return best_performing[0]

# Instance globale
stats_manager = StatsManager()

def get_stats_manager() -> StatsManager:
    """Retourne l'instance globale du gestionnaire de statistiques"""
    return stats_manager
