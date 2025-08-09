import unittest
import tempfile
import os
import json
from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.config_manager import ConfigManager
from utils.theme_manager import ThemeManager
from utils.score_manager import ScoreManager
from utils.stats_manager import StatsManager
from utils.i18n import I18nManager

class TestConfigManager(unittest.TestCase):
    """Tests pour le gestionnaire de configuration"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        self.config_manager = ConfigManager(self.config_file)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test de la configuration par défaut"""
        self.assertEqual(self.config_manager.get_theme(), "modern_blue")
        self.assertEqual(self.config_manager.get_language(), "fr")
        self.assertFalse(self.config_manager.is_fullscreen())
        self.assertTrue(self.config_manager.are_animations_enabled())
    
    def test_set_and_get(self):
        """Test de définition et récupération de valeurs"""
        self.config_manager.set("test_key", "test_value")
        self.assertEqual(self.config_manager.get("test_key"), "test_value")
        
        self.config_manager.set("nested.key", "nested_value")
        self.assertEqual(self.config_manager.get("nested.key"), "nested_value")
    
    def test_theme_management(self):
        """Test de la gestion des thèmes"""
        self.config_manager.set_theme("dark_purple")
        self.assertEqual(self.config_manager.get_theme(), "dark_purple")
        
        themes = self.config_manager.get_all_themes()
        self.assertIn("modern_blue", themes)
        self.assertIn("dark_purple", themes)
    
    def test_window_size(self):
        """Test de la gestion de la taille de fenêtre"""
        self.config_manager.set_window_size(1200, 800)
        width, height = self.config_manager.get_window_size()
        self.assertEqual(width, 1200)
        self.assertEqual(height, 800)
    
    def test_reset_to_defaults(self):
        """Test de la réinitialisation aux valeurs par défaut"""
        self.config_manager.set_theme("dark_purple")
        self.config_manager.set_window_size(1200, 800)
        
        self.config_manager.reset_to_defaults()
        
        self.assertEqual(self.config_manager.get_theme(), "modern_blue")
        width, height = self.config_manager.get_window_size()
        self.assertEqual(width, 1000)
        self.assertEqual(height, 700)

class TestThemeManager(unittest.TestCase):
    """Tests pour le gestionnaire de thèmes"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.theme_manager = ThemeManager()
    
    def test_default_theme(self):
        """Test du thème par défaut"""
        self.assertEqual(self.theme_manager.current_theme, "modern_blue")
        
        theme = self.theme_manager.get_current_theme()
        self.assertEqual(theme["name"], "Bleu Moderne")
    
    def test_theme_colors(self):
        """Test des couleurs de thème"""
        bg_color = self.theme_manager.get_color("bg_primary")
        self.assertIsInstance(bg_color, str)
        self.assertTrue(bg_color.startswith("#"))
    
    def test_theme_fonts(self):
        """Test des polices de thème"""
        title_font = self.theme_manager.get_font("title")
        self.assertIsInstance(title_font, tuple)
        self.assertEqual(len(title_font), 3)
    
    def test_theme_spacing(self):
        """Test des espacements de thème"""
        spacing = self.theme_manager.get_spacing("large")
        self.assertIsInstance(spacing, int)
        self.assertEqual(spacing, 20)
    
    def test_available_themes(self):
        """Test des thèmes disponibles"""
        themes = self.theme_manager.get_available_themes()
        self.assertIn("modern_blue", themes)
        self.assertIn("dark_purple", themes)
        self.assertIn("green_nature", themes)
        self.assertIn("sunset_orange", themes)
    
    def test_theme_change(self):
        """Test du changement de thème"""
        self.theme_manager.set_theme("dark_purple")
        self.assertEqual(self.theme_manager.current_theme, "dark_purple")
        
        theme = self.theme_manager.get_current_theme()
        self.assertEqual(theme["name"], "Violet Sombre")

class TestScoreManager(unittest.TestCase):
    """Tests pour le gestionnaire de scores"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.scores_file = os.path.join(self.temp_dir, "test_scores.json")
        self.score_manager = ScoreManager(self.scores_file)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.scores_file):
            os.remove(self.scores_file)
        os.rmdir(self.temp_dir)
    
    def test_save_and_get_score(self):
        """Test de sauvegarde et récupération de scores"""
        self.score_manager.save_score("test_game", "TestPlayer", 100)
        
        scores = self.score_manager.get_scores("test_game")
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]["score"], 100)
        self.assertEqual(scores[0]["player"], "TestPlayer")
    
    def test_high_score(self):
        """Test du meilleur score"""
        self.score_manager.save_score("test_game", "Player1", 50)
        self.score_manager.save_score("test_game", "Player2", 100)
        self.score_manager.save_score("test_game", "Player3", 75)
        
        high_score = self.score_manager.get_high_score("test_game")
        self.assertEqual(high_score["score"], 100)
        self.assertEqual(high_score["player"], "Player2")
    
    def test_score_limit(self):
        """Test de la limite de scores (top 10)"""
        # Ajouter plus de 10 scores
        for i in range(15):
            self.score_manager.save_score("test_game", f"Player{i}", i * 10)
        
        scores = self.score_manager.get_scores("test_game")
        self.assertEqual(len(scores), 10)  # Seulement les 10 meilleurs
        
        # Le meilleur score doit être le plus élevé
        self.assertEqual(scores[0]["score"], 140)
    
    def test_multiple_games(self):
        """Test avec plusieurs jeux"""
        self.score_manager.save_score("game1", "Player1", 100)
        self.score_manager.save_score("game2", "Player2", 200)
        
        scores1 = self.score_manager.get_scores("game1")
        scores2 = self.score_manager.get_scores("game2")
        
        self.assertEqual(len(scores1), 1)
        self.assertEqual(len(scores2), 1)
        self.assertEqual(scores1[0]["score"], 100)
        self.assertEqual(scores2[0]["score"], 200)

class TestStatsManager(unittest.TestCase):
    """Tests pour le gestionnaire de statistiques"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.stats_file = os.path.join(self.temp_dir, "test_stats.json")
        self.stats_manager = StatsManager(self.stats_file)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)
        os.rmdir(self.temp_dir)
    
    def test_record_session(self):
        """Test d'enregistrement d'une session"""
        self.stats_manager.record_game_session("test_game", "Test Game", 100, 60.0, "TestPlayer")
        
        game_stats = self.stats_manager.get_game_stats("test_game")
        self.assertEqual(game_stats["total_sessions"], 1)
        self.assertEqual(game_stats["total_score"], 100)
        self.assertEqual(game_stats["best_score"], 100)
        self.assertEqual(game_stats["total_playtime"], 60.0)
    
    def test_global_stats(self):
        """Test des statistiques globales"""
        self.stats_manager.record_game_session("game1", "Game 1", 100, 60.0)
        self.stats_manager.record_game_session("game2", "Game 2", 200, 120.0)
        
        global_stats = self.stats_manager.get_global_stats()
        self.assertEqual(global_stats["total_games_played"], 2)
        self.assertEqual(global_stats["total_sessions"], 2)
        self.assertEqual(global_stats["total_playtime"], 180.0)
        self.assertEqual(global_stats["best_overall_score"], 200)
    
    def test_format_duration(self):
        """Test du formatage des durées"""
        self.assertEqual(self.stats_manager.format_duration(30), "30s")
        self.assertEqual(self.stats_manager.format_duration(90), "1m 30s")
        self.assertEqual(self.stats_manager.format_duration(3661), "1h 1m")
    
    def test_achievements(self):
        """Test des achievements"""
        # Ajouter une session pour débloquer le premier achievement
        self.stats_manager.record_game_session("test_game", "Test Game", 100, 60.0)
        
        achievements = self.stats_manager.get_achievements()
        self.assertGreater(len(achievements), 0)
        
        # Vérifier le premier achievement
        first_achievement = achievements[0]
        self.assertEqual(first_achievement["id"], "first_game")
        self.assertEqual(first_achievement["name"], "Premier Pas")
        self.assertTrue(first_achievement["unlocked"])

class TestI18nManager(unittest.TestCase):
    """Tests pour le gestionnaire d'internationalisation"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.translations_dir = os.path.join(self.temp_dir, "translations")
        os.makedirs(self.translations_dir, exist_ok=True)
        
        # Créer un fichier de traduction de test
        test_translations = {
            "app": {
                "title": "Test App",
                "games": "Test Games"
            },
            "test": {
                "message": "Hello {}",
                "count": "Count: {}"
            }
        }
        
        with open(os.path.join(self.translations_dir, "en.json"), 'w', encoding='utf-8') as f:
            json.dump(test_translations, f)
        
        self.i18n = I18nManager()
        self.i18n.translations = {"en": test_translations}
        self.i18n.current_language = "en"
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_translation(self):
        """Test de récupération de traduction"""
        title = self.i18n.get("app.title")
        self.assertEqual(title, "Test App")
        
        games = self.i18n.get("app.games")
        self.assertEqual(games, "Test Games")
    
    def test_get_with_formatting(self):
        """Test de traduction avec formatage"""
        message = self.i18n.get("test.message", "World")
        self.assertEqual(message, "Hello World")
        
        count = self.i18n.get("test.count", 42)
        self.assertEqual(count, "Count: 42")
    
    def test_missing_translation(self):
        """Test de traduction manquante"""
        missing = self.i18n.get("missing.key")
        self.assertEqual(missing, "missing.key")
    
    def test_available_languages(self):
        """Test des langues disponibles"""
        languages = self.i18n.get_available_languages()
        self.assertIn("fr", languages)
        self.assertIn("en", languages)
        self.assertIn("es", languages)
        self.assertIn("de", languages)
    
    def test_language_change(self):
        """Test du changement de langue"""
        self.i18n.set_language("fr")
        self.assertEqual(self.i18n.get_current_language(), "fr")
        
        # Retourner à l'anglais pour les tests
        self.i18n.set_language("en")
        self.assertEqual(self.i18n.get_current_language(), "en")

if __name__ == "__main__":
    # Configuration pour les tests
    unittest.main(verbosity=2)
