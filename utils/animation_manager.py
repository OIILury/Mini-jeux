import tkinter as tk
from tkinter import ttk
import time
import threading
from typing import Callable, Any

class AnimationManager:
    """Gestionnaire d'animations pour l'interface"""
    
    def __init__(self):
        self.animations = {}
        self.animation_speed = 0.05  # Délai entre les frames (en secondes)
    
    def fade_in(self, widget, duration: float = 0.5, callback: Callable = None):
        """Animation de fondu d'entrée pour un widget"""
        if not hasattr(widget, 'original_bg'):
            try:
                # Pour les widgets ttk, on ne peut pas récupérer bg directement
                if isinstance(widget, ttk.Widget):
                    widget.original_bg = None
                else:
                    widget.original_bg = widget.cget('bg')
            except:
                widget.original_bg = None
        
        steps = int(duration / self.animation_speed)
        alpha_step = 1.0 / steps
        
        def animate_fade_in(step=0, alpha=0.0):
            if step <= steps:
                # Calculer la nouvelle transparence
                alpha = min(1.0, alpha + alpha_step)
                
                # Appliquer l'effet de transparence
                if hasattr(widget, 'configure'):
                    try:
                        # Pour les widgets ttk, on utilise le style
                        if isinstance(widget, ttk.Widget):
                            # Les widgets ttk gèrent les couleurs via les styles
                            pass
                        else:
                            # Pour les widgets tk normaux
                            if widget.original_bg:
                                widget.configure(bg=widget.original_bg)
                    except:
                        pass
                
                if step < steps:
                    widget.after(int(self.animation_speed * 1000), 
                               lambda: animate_fade_in(step + 1, alpha))
                elif callback:
                    callback()
        
        animate_fade_in()
    
    def slide_in(self, widget, direction: str = "left", duration: float = 0.5, callback: Callable = None):
        """Animation de glissement d'entrée pour un widget"""
        if not hasattr(widget, 'original_geometry'):
            widget.original_geometry = widget.winfo_geometry()
        
        # Obtenir la position actuelle
        x = widget.winfo_x()
        y = widget.winfo_y()
        
        # Calculer la position de départ selon la direction
        if direction == "left":
            start_x = x - 100
            end_x = x
        elif direction == "right":
            start_x = x + 100
            end_x = x
        elif direction == "top":
            start_y = y - 100
            end_y = y
        elif direction == "bottom":
            start_y = y + 100
            end_y = y
        else:
            return
        
        steps = int(duration / self.animation_speed)
        
        def animate_slide(step=0):
            if step <= steps:
                progress = step / steps
                
                if direction in ["left", "right"]:
                    current_x = start_x + (end_x - start_x) * progress
                    widget.place(x=current_x, y=y)
                else:
                    current_y = start_y + (end_y - start_y) * progress
                    widget.place(x=x, y=current_y)
                
                if step < steps:
                    widget.after(int(self.animation_speed * 1000), 
                               lambda: animate_slide(step + 1))
                elif callback:
                    callback()
        
        animate_slide()
    
    def pulse(self, widget, duration: float = 0.3, callback: Callable = None):
        """Animation de pulsation pour un widget"""
        original_scale = 1.0
        max_scale = 1.1
        
        steps = int(duration / self.animation_speed)
        scale_step = (max_scale - original_scale) / (steps // 2)
        
        def animate_pulse(step=0, growing=True, scale=original_scale):
            if step < steps:
                if growing and step < steps // 2:
                    scale += scale_step
                else:
                    growing = False
                    scale -= scale_step
                
                # Appliquer la transformation d'échelle
                try:
                    if hasattr(widget, 'configure'):
                        # Pour les widgets ttk, on peut ajuster la taille de police
                        if isinstance(widget, ttk.Label):
                            original_font = widget.cget('font')
                            if original_font:
                                font_parts = list(original_font)
                                if len(font_parts) >= 2:
                                    font_parts[1] = int(font_parts[1] * scale)
                                    widget.configure(font=tuple(font_parts))
                except:
                    pass
                
                widget.after(int(self.animation_speed * 1000), 
                           lambda: animate_pulse(step + 1, growing, scale))
            elif callback:
                callback()
        
        animate_pulse()
    
    def shake(self, widget, intensity: int = 5, duration: float = 0.3, callback: Callable = None):
        """Animation de secousse pour un widget"""
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        steps = int(duration / self.animation_speed)
        
        def animate_shake(step=0):
            if step < steps:
                # Calculer l'offset de secousse
                import math
                offset_x = intensity * math.sin(step * 3) * (1 - step / steps)
                offset_y = intensity * math.cos(step * 2) * (1 - step / steps)
                
                widget.place(x=original_x + offset_x, y=original_y + offset_y)
                
                widget.after(int(self.animation_speed * 1000), 
                           lambda: animate_shake(step + 1))
            else:
                # Remettre le widget à sa position originale
                widget.place(x=original_x, y=original_y)
                if callback:
                    callback()
        
        animate_shake()
    
    def bounce(self, widget, height: int = 20, duration: float = 0.5, callback: Callable = None):
        """Animation de rebond pour un widget"""
        original_y = widget.winfo_y()
        
        steps = int(duration / self.animation_speed)
        
        def animate_bounce(step=0):
            if step < steps:
                # Calculer la position Y avec un effet de rebond
                import math
                progress = step / steps
                bounce_height = height * math.sin(progress * math.pi) * (1 - progress)
                
                widget.place(x=widget.winfo_x(), y=original_y - bounce_height)
                
                widget.after(int(self.animation_speed * 1000), 
                           lambda: animate_bounce(step + 1))
            else:
                # Remettre le widget à sa position originale
                widget.place(x=widget.winfo_x(), y=original_y)
                if callback:
                    callback()
        
        animate_bounce()
    
    def typewriter_effect(self, label, text: str, speed: float = 0.05, callback: Callable = None):
        """Effet de machine à écrire pour un label"""
        label.config(text="")
        
        def type_character(index=0):
            if index < len(text):
                current_text = label.cget('text') + text[index]
                label.config(text=current_text)
                label.after(int(speed * 1000), lambda: type_character(index + 1))
            elif callback:
                callback()
        
        type_character()
    
    def progress_bar_animation(self, progress_bar, target_value: float, duration: float = 1.0, callback: Callable = None):
        """Animation de barre de progression"""
        start_value = progress_bar.cget('value') if hasattr(progress_bar, 'cget') else 0
        steps = int(duration / self.animation_speed)
        value_step = (target_value - start_value) / steps
        
        def animate_progress(step=0):
            if step <= steps:
                current_value = start_value + (value_step * step)
                try:
                    progress_bar.configure(value=current_value)
                except:
                    pass
                
                if step < steps:
                    progress_bar.after(int(self.animation_speed * 1000), 
                                     lambda: animate_progress(step + 1))
                elif callback:
                    callback()
        
        animate_progress()
    
    def color_transition(self, widget, start_color: str, end_color: str, duration: float = 1.0, callback: Callable = None):
        """Transition de couleur pour un widget"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        steps = int(duration / self.animation_speed)
        
        def animate_color(step=0):
            if step <= steps:
                progress = step / steps
                
                # Interpolation linéaire entre les couleurs
                current_rgb = tuple(
                    int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress)
                    for i in range(3)
                )
                
                current_color = rgb_to_hex(current_rgb)
                
                try:
                    if isinstance(widget, ttk.Widget):
                        # Les widgets ttk gèrent les couleurs via les styles
                        pass
                    else:
                        widget.configure(bg=current_color)
                except:
                    pass
                
                if step < steps:
                    widget.after(int(self.animation_speed * 1000), 
                               lambda: animate_color(step + 1))
                elif callback:
                    callback()
        
        animate_color()
    
    def create_loading_spinner(self, parent, size: int = 40):
        """Crée un spinner de chargement animé"""
        canvas = tk.Canvas(parent, width=size, height=size, bg='transparent', highlightthickness=0)
        
        # Dessiner le cercle de base
        canvas.create_oval(2, 2, size-2, size-2, outline='gray', width=2)
        
        # Créer l'arc animé
        arc = canvas.create_arc(2, 2, size-2, size-2, start=0, extent=0, outline='blue', width=2)
        
        def animate_spinner(angle=0):
            canvas.itemconfig(arc, start=angle, extent=120)
            angle = (angle + 10) % 360
            canvas.after(50, lambda: animate_spinner(angle))
        
        animate_spinner()
        return canvas
