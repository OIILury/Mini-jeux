import json
import os
from typing import Dict, Any
from pathlib import Path

class I18nManager:
    """Gestionnaire d'internationalisation pour l'application"""
    
    def __init__(self, default_language: str = "fr"):
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Charge toutes les traductions disponibles"""
        translations_dir = Path("translations")
        
        if not translations_dir.exists():
            # Créer le dossier et les fichiers de traduction par défaut
            self.create_default_translations()
        
        # Charger toutes les traductions
        for lang_file in translations_dir.glob("*.json"):
            language = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[language] = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de la traduction {language}: {e}")
    
    def create_default_translations(self):
        """Crée les fichiers de traduction par défaut"""
        translations_dir = Path("translations")
        translations_dir.mkdir(exist_ok=True)
        
        # Traductions françaises (par défaut)
        fr_translations = {
            "app": {
                "title": "🎮 Mini-Jeux Collection 🎮",
                "games": "🎲 Jeux",
                "settings": "⚙️ Paramètres",
                "quit": "Quitter",
                "back": "← Retour au menu principal",
                "play": "Jouer",
                "configure": "Configurer"
            },
            "home": {
                "games_description": "Découvrez notre collection de mini-jeux",
                "settings_description": "Personnalisez votre expérience",
                "stats_title": "📊 Statistiques",
                "available_games": "Jeux disponibles",
                "saved_scores": "Scores sauvegardés",
                "current_theme": "Thème actuel",
                "animations": "Animations"
            },
            "games": {
                "selection_title": "🎲 Sélection du Jeu",
                "no_score": "Aucun score",
                "best_score": "Meilleur: {}",
                "best_score_with_player": "Meilleur: {} ({})"
            },
            "settings": {
                "title": "⚙️ Paramètres",
                "themes_section": "🎨 Thèmes",
                "other_settings": "🔧 Autres Paramètres",
                "enable_animations": "Activer les animations",
                "fullscreen_mode": "Mode plein écran",
                "reset_settings": "Réinitialiser les paramètres",
                "reset_confirm": "Voulez-vous vraiment réinitialiser tous les paramètres ?"
            },
            "themes": {
                "modern_blue": "Bleu Moderne",
                "dark_purple": "Violet Sombre",
                "green_nature": "Nature Verte",
                "sunset_orange": "Coucher de Soleil"
            },
            "game": {
                "score": "Score: {}",
                "pause": "⏸️ Pause",
                "restart": "🔄 Recommencer",
                "quit": "❌ Quitter",
                "game_over": "Partie terminée !",
                "final_score": "Score final: {}",
                "success": "Succès",
                "error": "Erreur",
                "no_record": "Aucun record"
            },
            "errors": {
                "launch_error": "Impossible de lancer {}: {}",
                "save_error": "Impossible de sauvegarder le score. Veuillez réessayer.",
                "stats_error": "Impossible de charger les stats"
            }
        }
        
        # Traductions anglaises
        en_translations = {
            "app": {
                "title": "🎮 Mini-Games Collection 🎮",
                "games": "🎲 Games",
                "settings": "⚙️ Settings",
                "quit": "Quit",
                "back": "← Back to main menu",
                "play": "Play",
                "configure": "Configure"
            },
            "home": {
                "games_description": "Discover our collection of mini-games",
                "settings_description": "Customize your experience",
                "stats_title": "📊 Statistics",
                "available_games": "Available games",
                "saved_scores": "Saved scores",
                "current_theme": "Current theme",
                "animations": "Animations"
            },
            "games": {
                "selection_title": "🎲 Game Selection",
                "no_score": "No score",
                "best_score": "Best: {}",
                "best_score_with_player": "Best: {} ({})"
            },
            "settings": {
                "title": "⚙️ Settings",
                "themes_section": "🎨 Themes",
                "other_settings": "🔧 Other Settings",
                "enable_animations": "Enable animations",
                "fullscreen_mode": "Fullscreen mode",
                "reset_settings": "Reset settings",
                "reset_confirm": "Do you really want to reset all settings?"
            },
            "themes": {
                "modern_blue": "Modern Blue",
                "dark_purple": "Dark Purple",
                "green_nature": "Green Nature",
                "sunset_orange": "Sunset Orange"
            },
            "game": {
                "score": "Score: {}",
                "pause": "⏸️ Pause",
                "restart": "🔄 Restart",
                "quit": "❌ Quit",
                "game_over": "Game over!",
                "final_score": "Final score: {}",
                "success": "Success",
                "error": "Error",
                "no_record": "No record"
            },
            "errors": {
                "launch_error": "Unable to launch {}: {}",
                "save_error": "Unable to save score. Please try again.",
                "stats_error": "Unable to load stats"
            }
        }
        
        # Traductions espagnoles
        es_translations = {
            "app": {
                "title": "🎮 Colección de Mini-Juegos 🎮",
                "games": "🎲 Juegos",
                "settings": "⚙️ Configuración",
                "quit": "Salir",
                "back": "← Volver al menú principal",
                "play": "Jugar",
                "configure": "Configurar"
            },
            "home": {
                "games_description": "Descubre nuestra colección de mini-juegos",
                "settings_description": "Personaliza tu experiencia",
                "stats_title": "📊 Estadísticas",
                "available_games": "Juegos disponibles",
                "saved_scores": "Puntuaciones guardadas",
                "current_theme": "Tema actual",
                "animations": "Animaciones"
            },
            "games": {
                "selection_title": "🎲 Selección de Juego",
                "no_score": "Sin puntuación",
                "best_score": "Mejor: {}",
                "best_score_with_player": "Mejor: {} ({})"
            },
            "settings": {
                "title": "⚙️ Configuración",
                "themes_section": "🎨 Temas",
                "other_settings": "🔧 Otras Configuraciones",
                "enable_animations": "Activar animaciones",
                "fullscreen_mode": "Modo pantalla completa",
                "reset_settings": "Restablecer configuración",
                "reset_confirm": "¿Realmente quieres restablecer toda la configuración?"
            },
            "themes": {
                "modern_blue": "Azul Moderno",
                "dark_purple": "Púrpura Oscuro",
                "green_nature": "Naturaleza Verde",
                "sunset_orange": "Naranja Atardecer"
            },
            "game": {
                "score": "Puntuación: {}",
                "pause": "⏸️ Pausa",
                "restart": "🔄 Reiniciar",
                "quit": "❌ Salir",
                "game_over": "¡Juego terminado!",
                "final_score": "Puntuación final: {}",
                "success": "Éxito",
                "error": "Error",
                "no_record": "Sin récord"
            },
            "errors": {
                "launch_error": "No se puede lanzar {}: {}",
                "save_error": "No se puede guardar la puntuación. Inténtalo de nuevo.",
                "stats_error": "No se pueden cargar las estadísticas"
            }
        }
        
        # Traductions allemandes
        de_translations = {
            "app": {
                "title": "🎮 Mini-Spiele Sammlung 🎮",
                "games": "🎲 Spiele",
                "settings": "⚙️ Einstellungen",
                "quit": "Beenden",
                "back": "← Zurück zum Hauptmenü",
                "play": "Spielen",
                "configure": "Konfigurieren"
            },
            "home": {
                "games_description": "Entdecke unsere Sammlung von Mini-Spielen",
                "settings_description": "Passe deine Erfahrung an",
                "stats_title": "📊 Statistiken",
                "available_games": "Verfügbare Spiele",
                "saved_scores": "Gespeicherte Punkte",
                "current_theme": "Aktuelles Theme",
                "animations": "Animationen"
            },
            "games": {
                "selection_title": "🎲 Spielauswahl",
                "no_score": "Keine Punkte",
                "best_score": "Beste: {}",
                "best_score_with_player": "Beste: {} ({})"
            },
            "settings": {
                "title": "⚙️ Einstellungen",
                "themes_section": "🎨 Themes",
                "other_settings": "🔧 Andere Einstellungen",
                "enable_animations": "Animationen aktivieren",
                "fullscreen_mode": "Vollbildmodus",
                "reset_settings": "Einstellungen zurücksetzen",
                "reset_confirm": "Möchten Sie wirklich alle Einstellungen zurücksetzen?"
            },
            "themes": {
                "modern_blue": "Modernes Blau",
                "dark_purple": "Dunkles Lila",
                "green_nature": "Grüne Natur",
                "sunset_orange": "Sonnenuntergang Orange"
            },
            "game": {
                "score": "Punkte: {}",
                "pause": "⏸️ Pause",
                "restart": "🔄 Neustart",
                "quit": "❌ Beenden",
                "game_over": "Spiel beendet!",
                "final_score": "Endpunktzahl: {}",
                "success": "Erfolg",
                "error": "Fehler",
                "no_record": "Kein Rekord"
            },
            "errors": {
                "launch_error": "Kann {} nicht starten: {}",
                "save_error": "Punkte können nicht gespeichert werden. Bitte versuchen Sie es erneut.",
                "stats_error": "Statistiken können nicht geladen werden"
            }
        }
        
        # Sauvegarder les traductions
        translations = {
            "fr": fr_translations,
            "en": en_translations,
            "es": es_translations,
            "de": de_translations
        }
        
        for lang, trans in translations.items():
            with open(translations_dir / f"{lang}.json", 'w', encoding='utf-8') as f:
                json.dump(trans, f, ensure_ascii=False, indent=2)
    
    def set_language(self, language: str):
        """Change la langue actuelle"""
        if language in self.translations:
            self.current_language = language
        else:
            self.current_language = self.default_language
    
    def get(self, key: str, *args) -> str:
        """Récupère une traduction"""
        keys = key.split('.')
        
        try:
            # Essayer la langue actuelle
            translation = self.translations.get(self.current_language, {})
            for k in keys:
                translation = translation[k]
            
            # Formater avec les arguments si fournis
            if args:
                return translation.format(*args)
            return translation
            
        except (KeyError, TypeError):
            try:
                # Essayer la langue par défaut
                translation = self.translations.get(self.default_language, {})
                for k in keys:
                    translation = translation[k]
                
                if args:
                    return translation.format(*args)
                return translation
                
            except (KeyError, TypeError):
                # Retourner la clé si aucune traduction n'est trouvée
                return key
    
    def get_available_languages(self) -> Dict[str, str]:
        """Retourne la liste des langues disponibles"""
        return {
            "fr": "Français",
            "en": "English", 
            "es": "Español",
            "de": "Deutsch"
        }
    
    def get_current_language(self) -> str:
        """Retourne la langue actuelle"""
        return self.current_language
    
    def get_language_name(self, language_code: str) -> str:
        """Retourne le nom d'une langue"""
        languages = self.get_available_languages()
        return languages.get(language_code, language_code)

# Instance globale
i18n = I18nManager()

def get_i18n() -> I18nManager:
    """Retourne l'instance globale du gestionnaire d'internationalisation"""
    return i18n
