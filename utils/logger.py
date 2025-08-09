import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class GameLogger:
    """Système de logging pour l'application de jeux"""
    
    def __init__(self, name: str = "MiniJeux", log_level: str = "INFO", log_file: str = "logs/app.log"):
        self.name = name
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.log_file = log_file
        
        # Créer le dossier de logs s'il n'existe pas
        log_dir = Path(log_file).parent
        log_dir.mkdir(exist_ok=True)
        
        # Configuration du logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Éviter les doublons de handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configure les handlers pour le logging"""
        # Handler pour fichier
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # Handler pour console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        
        # Format personnalisé
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """Log de niveau DEBUG"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log de niveau INFO"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de niveau WARNING"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de niveau ERROR"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log de niveau CRITICAL"""
        self.logger.critical(message, extra=kwargs)
    
    def log_game_event(self, game_name: str, event_type: str, details: dict = None):
        """Log spécifique pour les événements de jeu"""
        message = f"Jeu: {game_name} - Événement: {event_type}"
        if details:
            message += f" - Détails: {details}"
        self.info(message, game=game_name, event=event_type, details=details)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log pour les métriques de performance"""
        self.info(f"Performance - {operation}: {duration:.3f}s", 
                 operation=operation, duration=duration, **kwargs)
    
    def log_user_action(self, action: str, **kwargs):
        """Log pour les actions utilisateur"""
        self.info(f"Action utilisateur: {action}", action=action, **kwargs)
    
    def log_error_with_context(self, error: Exception, context: str = "", **kwargs):
        """Log d'erreur avec contexte"""
        error_msg = f"Erreur dans {context}: {str(error)}"
        self.error(error_msg, error_type=type(error).__name__, context=context, **kwargs)
    
    def log_memory_usage(self, memory_mb: float):
        """Log pour l'utilisation mémoire"""
        self.debug(f"Utilisation mémoire: {memory_mb:.2f} MB", memory_mb=memory_mb)
    
    def log_config_change(self, setting: str, old_value, new_value):
        """Log pour les changements de configuration"""
        self.info(f"Configuration changée: {setting} = {old_value} -> {new_value}",
                 setting=setting, old_value=old_value, new_value=new_value)
    
    def log_score(self, game_name: str, player_name: str, score: int, **kwargs):
        """Log pour les scores"""
        self.info(f"Nouveau score - Jeu: {game_name}, Joueur: {player_name}, Score: {score}",
                 game=game_name, player=player_name, score=score, **kwargs)
    
    def log_theme_change(self, old_theme: str, new_theme: str):
        """Log pour les changements de thème"""
        self.info(f"Thème changé: {old_theme} -> {new_theme}",
                 old_theme=old_theme, new_theme=new_theme)
    
    def log_animation_event(self, animation_type: str, widget_type: str, duration: float):
        """Log pour les animations"""
        self.debug(f"Animation: {animation_type} sur {widget_type} ({duration:.3f}s)",
                  animation_type=animation_type, widget_type=widget_type, duration=duration)
    
    def log_file_operation(self, operation: str, filepath: str, success: bool, **kwargs):
        """Log pour les opérations de fichiers"""
        status = "succès" if success else "échec"
        self.info(f"Opération fichier: {operation} {filepath} - {status}",
                 operation=operation, filepath=filepath, success=success, **kwargs)
    
    def log_network_request(self, url: str, method: str, status_code: int, duration: float):
        """Log pour les requêtes réseau (si applicable)"""
        self.info(f"Requête réseau: {method} {url} - {status_code} ({duration:.3f}s)",
                 url=url, method=method, status_code=status_code, duration=duration)
    
    def log_security_event(self, event_type: str, details: str = ""):
        """Log pour les événements de sécurité"""
        self.warning(f"Événement sécurité: {event_type} - {details}",
                    event_type=event_type, details=details)
    
    def log_startup(self, version: str, config: dict):
        """Log pour le démarrage de l'application"""
        self.info(f"Démarrage de l'application - Version: {version}",
                 version=version, config=config)
    
    def log_shutdown(self, reason: str = "normal"):
        """Log pour l'arrêt de l'application"""
        self.info(f"Arrêt de l'application - Raison: {reason}", reason=reason)
    
    def get_log_stats(self) -> dict:
        """Retourne des statistiques sur les logs"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                stats = {
                    'total_lines': len(lines),
                    'error_count': len([l for l in lines if 'ERROR' in l]),
                    'warning_count': len([l for l in lines if 'WARNING' in l]),
                    'info_count': len([l for l in lines if 'INFO' in l]),
                    'debug_count': len([l for l in lines if 'DEBUG' in l])
                }
                
                # Taille du fichier
                stats['file_size_mb'] = os.path.getsize(self.log_file) / (1024 * 1024)
                
                return stats
            else:
                return {'total_lines': 0, 'error_count': 0, 'warning_count': 0, 
                       'info_count': 0, 'debug_count': 0, 'file_size_mb': 0}
        except Exception as e:
            self.error(f"Erreur lors du calcul des statistiques de logs: {e}")
            return {}
    
    def clear_logs(self):
        """Vide le fichier de logs"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            self.info("Fichier de logs vidé")
        except Exception as e:
            self.error(f"Erreur lors du vidage des logs: {e}")
    
    def rotate_logs(self, max_size_mb: int = 10):
        """Rotation des logs si le fichier devient trop gros"""
        try:
            if os.path.exists(self.log_file):
                size_mb = os.path.getsize(self.log_file) / (1024 * 1024)
                if size_mb > max_size_mb:
                    # Créer un backup avec timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = f"{self.log_file}.{timestamp}"
                    os.rename(self.log_file, backup_file)
                    self.info(f"Rotation des logs: {self.log_file} -> {backup_file}")
        except Exception as e:
            self.error(f"Erreur lors de la rotation des logs: {e}")
    
    def set_level(self, level: str):
        """Change le niveau de log"""
        new_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(new_level)
        for handler in self.logger.handlers:
            handler.setLevel(new_level)
        self.log_level = new_level
        self.info(f"Niveau de log changé vers: {level}")

# Instance globale du logger
game_logger = GameLogger()

def get_logger() -> GameLogger:
    """Retourne l'instance globale du logger"""
    return game_logger
