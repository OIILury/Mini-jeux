import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Gestionnaire de configuration pour l'application"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "theme": "modern_blue",
            "language": "fr",
            "window_size": {
                "width": 1000,
                "height": 700
            },
            "fullscreen": False,
            "sound_enabled": True,
            "animations_enabled": True,
            "auto_save": True,
            "difficulty": "normal",
            "game_settings": {
                "number_guess": {
                    "max_attempts": 10,
                    "number_range": [1, 100]
                },
                "mental_calc": {
                    "timer_mode_duration": 60,
                    "lives_mode_lives": 3,
                    "difficulty_levels": ["easy", "normal", "hard"]
                },
                "slot_machine": {
                    "starting_credits": 100,
                    "min_bet": 1,
                    "max_bet": 50
                },
                "typer_game": {
                    "words_per_round": 20,
                    "timer_mode_duration": 60,
                    "lives_mode_lives": 3
                },
                "virtual_pet": {
                    "auto_save_interval": 30,
                    "max_pets": 5
                }
            },
            "ui_settings": {
                "show_animations": True,
                "show_tooltips": True,
                "compact_mode": False,
                "high_contrast": False
            },
            "performance": {
                "enable_logging": True,
                "log_level": "INFO",
                "memory_optimization": True,
                "cache_enabled": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Fusionner avec la configuration par défaut
                    return self.merge_configs(self.default_config, loaded_config)
            else:
                # Créer le fichier avec la configuration par défaut
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration : {e}")
            return self.default_config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Sauvegarde la configuration dans le fichier"""
        try:
            config_to_save = config if config is not None else self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration : {e}")
    
    def merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Fusionne la configuration par défaut avec celle de l'utilisateur"""
        result = default.copy()
        
        def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]):
            for key, value in override.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dicts(base[key], value)
                else:
                    base[key] = value
        
        merge_dicts(result, user)
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Définit une valeur de configuration"""
        keys = key.split('.')
        config = self.config
        
        # Naviguer jusqu'au niveau parent
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Définir la valeur
        config[keys[-1]] = value
        self.save_config()
    
    def get_theme(self) -> str:
        """Récupère le thème actuel"""
        return self.get('theme', 'modern_blue')
    
    def set_theme(self, theme: str):
        """Définit le thème"""
        self.set('theme', theme)
    
    def get_window_size(self) -> tuple:
        """Récupère la taille de la fenêtre"""
        size = self.get('window_size', {'width': 1000, 'height': 700})
        return (size['width'], size['height'])
    
    def set_window_size(self, width: int, height: int):
        """Définit la taille de la fenêtre"""
        self.set('window_size', {'width': width, 'height': height})
    
    def is_fullscreen(self) -> bool:
        """Vérifie si le mode plein écran est activé"""
        return self.get('fullscreen', False)
    
    def set_fullscreen(self, fullscreen: bool):
        """Définit le mode plein écran"""
        self.set('fullscreen', fullscreen)
    
    def is_sound_enabled(self) -> bool:
        """Vérifie si le son est activé"""
        return self.get('sound_enabled', True)
    
    def set_sound_enabled(self, enabled: bool):
        """Définit l'activation du son"""
        self.set('sound_enabled', enabled)
    
    def are_animations_enabled(self) -> bool:
        """Vérifie si les animations sont activées"""
        return self.get('animations_enabled', True)
    
    def set_animations_enabled(self, enabled: bool):
        """Définit l'activation des animations"""
        self.set('animations_enabled', enabled)
    
    def get_game_setting(self, game: str, setting: str, default: Any = None) -> Any:
        """Récupère un paramètre spécifique d'un jeu"""
        return self.get(f'game_settings.{game}.{setting}', default)
    
    def set_game_setting(self, game: str, setting: str, value: Any):
        """Définit un paramètre spécifique d'un jeu"""
        self.set(f'game_settings.{game}.{setting}', value)
    
    def get_ui_setting(self, setting: str, default: Any = None) -> Any:
        """Récupère un paramètre d'interface utilisateur"""
        return self.get(f'ui_settings.{setting}', default)
    
    def set_ui_setting(self, setting: str, value: Any):
        """Définit un paramètre d'interface utilisateur"""
        self.set(f'ui_settings.{setting}', value)
    
    def get_performance_setting(self, setting: str, default: Any = None) -> Any:
        """Récupère un paramètre de performance"""
        return self.get(f'performance.{setting}', default)
    
    def set_performance_setting(self, setting: str, value: Any):
        """Définit un paramètre de performance"""
        self.set(f'performance.{setting}', value)
    
    def get_language(self) -> str:
        """Récupère la langue actuelle"""
        return self.get('language', 'fr')
    
    def set_language(self, language: str):
        """Définit la langue"""
        self.set('language', language)
    
    def get_difficulty(self) -> str:
        """Récupère le niveau de difficulté"""
        return self.get('difficulty', 'normal')
    
    def set_difficulty(self, difficulty: str):
        """Définit le niveau de difficulté"""
        self.set('difficulty', difficulty)
    
    def reset_to_defaults(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def export_config(self, filepath: str):
        """Exporte la configuration vers un fichier"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de l'export de la configuration : {e}")
    
    def import_config(self, filepath: str):
        """Importe la configuration depuis un fichier"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                self.config = self.merge_configs(self.default_config, imported_config)
                self.save_config()
        except Exception as e:
            print(f"Erreur lors de l'import de la configuration : {e}")
    
    def get_all_themes(self) -> Dict[str, str]:
        """Retourne la liste de tous les thèmes disponibles"""
        return {
            "modern_blue": "Bleu Moderne",
            "dark_purple": "Violet Sombre", 
            "green_nature": "Nature Verte",
            "sunset_orange": "Coucher de Soleil"
        }
    
    def get_all_languages(self) -> Dict[str, str]:
        """Retourne la liste de toutes les langues disponibles"""
        return {
            "fr": "Français",
            "en": "English",
            "es": "Español",
            "de": "Deutsch"
        }
    
    def get_all_difficulties(self) -> Dict[str, str]:
        """Retourne la liste de tous les niveaux de difficulté"""
        return {
            "easy": "Facile",
            "normal": "Normal", 
            "hard": "Difficile"
        }
