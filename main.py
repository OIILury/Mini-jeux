import os
import sys
from utils.gui_manager import GameApp

def resource_path(relative_path):
    """Obtient le chemin absolu des ressources, fonctionne en dev et en exe"""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # Configurez les chemins des ressources
    os.environ['GAME_ASSETS'] = resource_path('assets')
    app = GameApp()
    app.mainloop()

if __name__ == "__main__":
    main() 