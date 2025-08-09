# 🎮 Mini-Jeux Collection

Une application moderne de collection de mini-jeux développée en Python avec une interface graphique élégante et des fonctionnalités avancées.

## ✨ Fonctionnalités

### 🎲 Jeux Disponibles
- **Devine le Nombre** : Devinez un nombre entre 1 et 100
- **Calcul Mental** : Résolvez des opérations mathématiques rapidement
- **Machine à Sous** : Jeu de hasard avec des symboles colorés
- **Jeu de Frappe** : Testez votre vitesse de frappe
- **Animal Virtuel** : Prenez soin de votre animal de compagnie virtuel

### 🎨 Interface Moderne
- **Thèmes Personnalisables** : 4 thèmes disponibles (Bleu Moderne, Violet Sombre, Nature Verte, Coucher de Soleil)
- **Animations Fluides** : Effets visuels modernes et transitions élégantes
- **Design Responsive** : Adaptation automatique à différentes tailles d'écran
- **Interface Intuitive** : Navigation simple et ergonomique

### 📊 Statistiques Détaillées
- **Graphiques de Progression** : Visualisez votre évolution dans chaque jeu
- **Statistiques Globales** : Suivi complet de vos performances
- **Achievements** : Système de récompenses et de défis
- **Historique des Sessions** : Consultez vos parties précédentes

### ⚙️ Paramètres Avancés
- **Configuration Personnalisable** : Sauvegarde automatique de vos préférences
- **Support Multi-langues** : Français, Anglais, Espagnol, Allemand
- **Mode Plein Écran** : Immersion totale dans le jeu
- **Optimisations de Performance** : Gestion mémoire et cache intelligent

### 🔧 Fonctionnalités Techniques
- **Système de Logging** : Suivi détaillé pour le débogage
- **Tests Unitaires** : Couverture de code complète
- **Gestion d'Erreurs** : Traitement robuste des exceptions
- **Sauvegarde Automatique** : Protection de vos données

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Tkinter (inclus avec Python)

### Installation des Dépendances
```bash
pip install -r requirements.txt
```

### Lancement de l'Application
```bash
python main.py
```

## 🎯 Utilisation

### Interface Principale
1. **Écran d'Accueil** : Sélectionnez "Jeux" pour accéder à la collection
2. **Menu des Jeux** : Choisissez le jeu qui vous intéresse
3. **Paramètres** : Personnalisez votre expérience

### Navigation
- **Touche Échap** : Retour au menu principal ou sortie du plein écran
- **F11** : Basculement mode plein écran
- **Souris** : Navigation intuitive avec clics et survols

### Personnalisation
- **Thèmes** : Changez l'apparence dans les paramètres
- **Langues** : Sélectionnez votre langue préférée
- **Animations** : Activez/désactivez les effets visuels

## 🧪 Tests

### Exécution des Tests
```bash
# Tests unitaires
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=utils --cov=games --cov-report=html
```

### Structure des Tests
- `tests/test_managers.py` : Tests des gestionnaires principaux
- Couverture des fonctionnalités critiques
- Tests d'intégration pour les jeux

## 📦 Compilation

### Création d'un Exécutable
```bash
python build_exe.py
```

### Fichiers Générés
- `dist/Mini-Jeux.exe` : Exécutable Windows
- `build/` : Fichiers temporaires de compilation

## 🏗️ Architecture

### Structure du Projet
```
Mini-jeux/
├── main.py                 # Point d'entrée principal
├── utils/                  # Gestionnaires utilitaires
│   ├── gui_manager.py     # Interface graphique moderne
│   ├── theme_manager.py   # Gestion des thèmes
│   ├── animation_manager.py # Système d'animations
│   ├── config_manager.py  # Configuration centralisée
│   ├── score_manager.py   # Gestion des scores
│   ├── stats_manager.py   # Statistiques détaillées
│   ├── i18n.py           # Internationalisation
│   └── logger.py         # Système de logging
├── games/                 # Implémentations des jeux
│   ├── base_game.py      # Classe de base pour les jeux
│   ├── game_manager.py   # Gestionnaire de jeux
│   ├── number_guess.py   # Devine le Nombre
│   ├── mental_calc.py    # Calcul Mental
│   ├── slot_machine.py   # Machine à Sous
│   ├── typer_game.py     # Jeu de Frappe
│   └── virtual_pet.py    # Animal Virtuel
├── assets/               # Ressources graphiques
├── tests/               # Tests unitaires
├── logs/                # Fichiers de logs
├── translations/         # Fichiers de traduction
└── requirements.txt     # Dépendances Python
```

### Gestionnaires Principaux
- **ConfigManager** : Configuration centralisée avec sauvegarde automatique
- **ThemeManager** : Système de thèmes avec 4 variantes
- **AnimationManager** : Effets visuels et transitions
- **StatsManager** : Statistiques détaillées avec graphiques
- **I18nManager** : Support multi-langues
- **Logger** : Système de logging complet

## 🎨 Thèmes Disponibles

### Bleu Moderne (Par défaut)
- Couleurs : Bleu profond avec accents rouges
- Ambiance : Moderne et professionnelle

### Violet Sombre
- Couleurs : Violets et pourpres
- Ambiance : Mystérieuse et élégante

### Nature Verte
- Couleurs : Verts et teintes naturelles
- Ambiance : Calme et apaisante

### Coucher de Soleil
- Couleurs : Oranges et tons chauds
- Ambiance : Dynamique et énergique

## 📈 Statistiques et Achievements

### Métriques Suivies
- **Scores** : Meilleurs scores par jeu
- **Temps de Jeu** : Durée des sessions
- **Progression** : Évolution des performances
- **Fréquence** : Nombre de parties jouées

### Achievements Disponibles
- 🎮 **Premier Pas** : Joué à votre premier jeu
- 🏆 **Joueur Régulier** : Joué à 10 parties
- ⭐ **Score Élevé** : Atteint un score de 100+
- ⏰ **Passionné** : Joué pendant plus d'une heure

## 🔧 Configuration

### Fichiers de Configuration
- `config.json` : Paramètres utilisateur
- `scores.json` : Scores sauvegardés
- `stats.json` : Statistiques détaillées
- `user_preferences.json` : Préférences utilisateur

### Variables d'Environnement
- `GAME_ASSETS` : Chemin vers les ressources

## 🐛 Dépannage

### Problèmes Courants
1. **Erreur d'import** : Vérifiez l'installation des dépendances
2. **Fenêtre ne s'affiche pas** : Vérifiez la version de Python
3. **Animations lentes** : Désactivez les animations dans les paramètres

### Logs
- Les logs sont sauvegardés dans `logs/app.log`
- Niveau de détail configurable
- Rotation automatique des fichiers

## 🤝 Contribution

### Développement
1. Fork du projet
2. Création d'une branche feature
3. Implémentation avec tests
4. Pull request avec description

### Standards de Code
- PEP 8 pour le style Python
- Docstrings pour la documentation
- Tests unitaires pour les nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- **Tkinter** : Interface graphique native Python
- **Matplotlib** : Graphiques et visualisations
- **PyInstaller** : Compilation d'exécutables
- **Communauté Python** : Outils et bibliothèques

---

**Version** : 2.0.0  
**Dernière mise à jour** : 2024  
**Auteur** : Équipe de développement Mini-Jeux
