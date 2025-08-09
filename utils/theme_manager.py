import tkinter as tk
from tkinter import ttk
import json
import os
from typing import Dict, Any

class ThemeManager:
    """Gestionnaire de thèmes pour l'application"""
    
    def __init__(self):
        self.current_theme = "modern_blue"
        self.themes = {
            "modern_blue": {
                "name": "Bleu Moderne",
                "colors": {
                    "bg_primary": "#1a1a2e",
                    "bg_secondary": "#16213e",
                    "bg_tertiary": "#0f3460",
                    "accent_primary": "#e94560",
                    "accent_secondary": "#ffd700",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b8b8b8",
                    "text_muted": "#888888",
                    "success": "#4ade80",
                    "warning": "#fbbf24",
                    "error": "#f87171",
                    "border": "#374151",
                    "hover": "#2d3748"
                },
                "fonts": {
                    "title": ("Segoe UI", 32, "bold"),
                    "subtitle": ("Segoe UI", 24, "bold"),
                    "heading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 12),
                    "button": ("Segoe UI", 12, "bold"),
                    "score": ("Segoe UI", 14, "bold")
                },
                "spacing": {
                    "small": 5,
                    "medium": 10,
                    "large": 20,
                    "xlarge": 30
                },
                "border_radius": 8,
                "shadow": True
            },
            "dark_purple": {
                "name": "Violet Sombre",
                "colors": {
                    "bg_primary": "#2d1b69",
                    "bg_secondary": "#1a103f",
                    "bg_tertiary": "#0f0a1f",
                    "accent_primary": "#a855f7",
                    "accent_secondary": "#fbbf24",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cbd5e1",
                    "text_muted": "#94a3b8",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "border": "#4c1d95",
                    "hover": "#581c87"
                },
                "fonts": {
                    "title": ("Segoe UI", 32, "bold"),
                    "subtitle": ("Segoe UI", 24, "bold"),
                    "heading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 12),
                    "button": ("Segoe UI", 12, "bold"),
                    "score": ("Segoe UI", 14, "bold")
                },
                "spacing": {
                    "small": 5,
                    "medium": 10,
                    "large": 20,
                    "xlarge": 30
                },
                "border_radius": 8,
                "shadow": True
            },
            "green_nature": {
                "name": "Nature Verte",
                "colors": {
                    "bg_primary": "#064e3b",
                    "bg_secondary": "#065f46",
                    "bg_tertiary": "#047857",
                    "accent_primary": "#10b981",
                    "accent_secondary": "#fbbf24",
                    "text_primary": "#ffffff",
                    "text_secondary": "#d1fae5",
                    "text_muted": "#a7f3d0",
                    "success": "#059669",
                    "warning": "#f59e0b",
                    "error": "#dc2626",
                    "border": "#065f46",
                    "hover": "#047857"
                },
                "fonts": {
                    "title": ("Segoe UI", 32, "bold"),
                    "subtitle": ("Segoe UI", 24, "bold"),
                    "heading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 12),
                    "button": ("Segoe UI", 12, "bold"),
                    "score": ("Segoe UI", 14, "bold")
                },
                "spacing": {
                    "small": 5,
                    "medium": 10,
                    "large": 20,
                    "xlarge": 30
                },
                "border_radius": 8,
                "shadow": True
            },
            "sunset_orange": {
                "name": "Coucher de Soleil",
                "colors": {
                    "bg_primary": "#7c2d12",
                    "bg_secondary": "#92400e",
                    "bg_tertiary": "#a16207",
                    "accent_primary": "#f97316",
                    "accent_secondary": "#fbbf24",
                    "text_primary": "#ffffff",
                    "text_secondary": "#fed7aa",
                    "text_muted": "#fdba74",
                    "success": "#16a34a",
                    "warning": "#f59e0b",
                    "error": "#dc2626",
                    "border": "#92400e",
                    "hover": "#a16207"
                },
                "fonts": {
                    "title": ("Segoe UI", 32, "bold"),
                    "subtitle": ("Segoe UI", 24, "bold"),
                    "heading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 12),
                    "button": ("Segoe UI", 12, "bold"),
                    "score": ("Segoe UI", 14, "bold")
                },
                "spacing": {
                    "small": 5,
                    "medium": 10,
                    "large": 20,
                    "xlarge": 30
                },
                "border_radius": 8,
                "shadow": True
            }
        }
        
        self.load_user_preferences()
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Retourne le thème actuel"""
        return self.themes[self.current_theme]
    
    def get_color(self, color_name: str) -> str:
        """Retourne une couleur du thème actuel"""
        return self.get_current_theme()["colors"][color_name]
    
    def get_font(self, font_name: str) -> tuple:
        """Retourne une police du thème actuel"""
        return self.get_current_theme()["fonts"][font_name]
    
    def get_spacing(self, spacing_name: str) -> int:
        """Retourne un espacement du thème actuel"""
        return self.get_current_theme()["spacing"][spacing_name]
    
    def set_theme(self, theme_name: str):
        """Change le thème actuel"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_user_preferences()
    
    def get_available_themes(self) -> Dict[str, str]:
        """Retourne la liste des thèmes disponibles avec leurs noms"""
        return {theme_id: theme_data["name"] for theme_id, theme_data in self.themes.items()}
    
    def load_user_preferences(self):
        """Charge les préférences utilisateur depuis un fichier"""
        try:
            if os.path.exists("user_preferences.json"):
                with open("user_preferences.json", "r", encoding="utf-8") as f:
                    preferences = json.load(f)
                    if "theme" in preferences:
                        self.current_theme = preferences["theme"]
        except Exception as e:
            print(f"Erreur lors du chargement des préférences : {e}")
    
    def save_user_preferences(self):
        """Sauvegarde les préférences utilisateur dans un fichier"""
        try:
            preferences = {
                "theme": self.current_theme
            }
            with open("user_preferences.json", "w", encoding="utf-8") as f:
                json.dump(preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des préférences : {e}")
    
    def apply_theme_to_widget(self, widget, style_name: str = None):
        """Applique le thème actuel à un widget"""
        theme = self.get_current_theme()
        
        if isinstance(widget, ttk.Frame):
            widget.configure(style=f"{style_name}.TFrame" if style_name else "Theme.TFrame")
        elif isinstance(widget, ttk.Label):
            widget.configure(style=f"{style_name}.TLabel" if style_name else "Theme.TLabel")
        elif isinstance(widget, ttk.Button):
            widget.configure(style=f"{style_name}.TButton" if style_name else "Theme.TButton")
    
    def setup_theme_styles(self, style: ttk.Style):
        """Configure tous les styles pour le thème actuel"""
        theme = self.get_current_theme()
        colors = theme["colors"]
        fonts = theme["fonts"]
        
        # Style général pour les frames
        style.configure(
            "Theme.TFrame",
            background=colors["bg_primary"]
        )
        
        # Style pour les labels
        style.configure(
            "Theme.TLabel",
            background=colors["bg_primary"],
            foreground=colors["text_primary"],
            font=fonts["body"]
        )
        
        # Style pour les titres
        style.configure(
            "Title.TLabel",
            background=colors["bg_primary"],
            foreground=colors["text_primary"],
            font=fonts["title"]
        )
        
        # Style pour les sous-titres
        style.configure(
            "Subtitle.TLabel",
            background=colors["bg_primary"],
            foreground=colors["text_primary"],
            font=fonts["subtitle"]
        )
        
        # Style pour les headings
        style.configure(
            "Heading.TLabel",
            background=colors["bg_primary"],
            foreground=colors["text_primary"],
            font=fonts["heading"]
        )
        
        # Style pour les scores
        style.configure(
            "Score.TLabel",
            background=colors["bg_primary"],
            foreground=colors["accent_secondary"],
            font=fonts["score"]
        )
        
        # Style pour les boutons principaux
        style.configure(
            "Primary.TButton",
            background=colors["accent_primary"],
            foreground=colors["text_primary"],
            font=fonts["button"],
            padding=(20, 10),
            borderwidth=0,
            focuscolor="none"
        )
        
        # Style pour les boutons secondaires
        style.configure(
            "Secondary.TButton",
            background=colors["bg_secondary"],
            foreground=colors["text_primary"],
            font=fonts["button"],
            padding=(15, 8),
            borderwidth=0,
            focuscolor="none"
        )
        
        # Style pour les boutons de jeu
        style.configure(
            "Game.TButton",
            background=colors["bg_tertiary"],
            foreground=colors["text_primary"],
            font=fonts["button"],
            padding=(10, 5),
            borderwidth=0,
            focuscolor="none"
        )
        
        # Configuration des états de hover
        style.map("Primary.TButton",
            background=[("active", colors["hover"])],
            foreground=[("active", colors["text_primary"])]
        )
        
        style.map("Secondary.TButton",
            background=[("active", colors["hover"])],
            foreground=[("active", colors["text_primary"])]
        )
        
        style.map("Game.TButton",
            background=[("active", colors["hover"])],
            foreground=[("active", colors["text_primary"])]
        )
