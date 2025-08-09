import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Assurez-vous que les dossiers nécessaires existent
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    if not os.path.exists('dist/assets'):
        os.makedirs('dist/assets')
    
    if not os.path.exists('saves'):
        os.makedirs('saves')

    # Vérifier que dico.txt existe dans le dossier source
    source_dico = os.path.join('assets', 'dico.txt')
    if not os.path.exists(source_dico):
        print(f"ERREUR: Le fichier source {source_dico} n'existe pas!")
        return

    # Utilisez le fichier spec
    PyInstaller.__main__.run([
        'Mini-Jeux.spec',
        '--clean',
        '--noconfirm',
    ])

    # Copier manuellement le fichier dico.txt
    dist_dico = os.path.join('dist', 'assets', 'dico.txt')
    try:
        shutil.copy2(source_dico, dist_dico)
        print(f"Fichier dico.txt copié avec succès vers {dist_dico}")
    except Exception as e:
        print(f"Erreur lors de la copie du fichier: {e}")

    # Vérification finale
    if os.path.exists(dist_dico):
        print(f"Vérification: Le fichier {dist_dico} existe bien")
        # Afficher le contenu pour vérification
        try:
            with open(dist_dico, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Nombre de mots dans le dictionnaire: {len(lines)}")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {e}")
    else:
        print(f"ERREUR: Le fichier {dist_dico} n'a pas été créé!")

    print("Build terminé ! L'exécutable se trouve dans le dossier 'dist'")

if __name__ == "__main__":
    build_exe() 