import os
import sys
import time
from utils.gui_manager import ModernGameApp
from utils.logger import get_logger
from utils.config_manager import ConfigManager

def resource_path(relative_path):
    """Obtient le chemin absolu des ressources, fonctionne en dev et en exe"""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    """Fonction principale de l'application"""
    start_time = time.time()
    
    # Initialisation du logger
    logger = get_logger()
    
    try:
        # Configuration des chemins des ressources
        os.environ['GAME_ASSETS'] = resource_path('assets')
        
        # Log du démarrage
        logger.log_startup("2.0.0", {"assets_path": os.environ['GAME_ASSETS']})
        
        # Création et lancement de l'application
        app = ModernGameApp()
        
        # Log du temps de démarrage
        startup_time = time.time() - start_time
        logger.log_performance("application_startup", startup_time)
        
        # Lancement de la boucle principale
        app.mainloop()
        
    except Exception as e:
        logger.log_error_with_context(e, "main")
        print(f"Erreur fatale lors du démarrage de l'application: {e}")
        sys.exit(1)
    
    finally:
        # Log de l'arrêt
        logger.log_shutdown("normal")

if __name__ == "__main__":
    main() 