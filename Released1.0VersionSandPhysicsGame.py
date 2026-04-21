# Introduction/Disclaimer from me:
# This is a simple sand simulation I made where you can repel the sand with your mouse its just for fun and for me to learn.
# I made this in like a day so it's not the best but I thought it was pretty cool feel free to give suggestions.
# My Discord is ("dehydratedcupofwater.") if you want to see more projects and same with my GitHub (github.com/dehydratedcupofwater)

# Thanks for checking this out btw

# Imports
import webbrowser

import pygame
import random
import math

# Initialization things (do not touch ts or hell will break loose)
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SandPhysicsGame1.0Release - dehydratedcupofwater")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 30)

# Default settings
PARTICLE_COUNT = 500        # How many sand grains (do not make this too high or the FPS drops had to learn hard way)
REPULSION_RADIUS = 120      # How close mouse needs to be or it doesn't repel (radius around your cursor)
REPULSION_STRENGTH = 3.0    # How hard it pushes (do not make this too high or your sand will probably glitch out)
PARTICLE_SIZE = 2           # Size of each grain in pixels (Usually do like anything just not above like 5 or it lowkey looks weird)
TRAIL_LENGTH = 30           # The lower the number the smaller the trail (0 gives you no trails 100 gives very long trails)
SAND_COLOR = "warm"         # Options: "warm", "cool", "white", "red" I WILL ADD MORE I PROMISE GIVE ME A LIL BIT

# Ui globals
menu_open = False
settings_tabs = ["Sand", "Physics", "Visual", "Credits"]
current_tab = "Sand"

# Dropdowns
color_dropdown_open = False
color_options = ["warm", "cool", "white", "red"]

# Slider values (they go 1-100 but map to different ranges in the actual settings kinda weird idk what to do about this)
slider_particle_count = 50      # 0-100 maps to 50-2000 particles
slider_repulsion_radius = 40    # 0-100 maps to 40-300 pixels
slider_repulsion_strength = 30  # 0-100 maps to 0.5-8.0 strength
slider_particle_size = 20       # 0-100 maps to 1-8 pixels
slider_trail_length = 30        # 0-100 maps to 0-100 alpha

# Which slider is being dragged (None = none)
dragging_slider = None

# UI rectangles (populated dynamically)
color_dropdown_rect = pygame.Rect(0, 0, 0, 0)
color_option_rects = []
slider_rects = {}
tab_rects = {}

# Helper functions and things (you can prolly touch these i think but be careful not to delete something)
def map_range(value, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def update_settings_from_sliders():
    """Updates the actual settings based on slider positions."""
    global PARTICLE_COUNT, REPULSION_RADIUS, REPULSION_STRENGTH
    global PARTICLE_SIZE, TRAIL_LENGTH
    
    PARTICLE_COUNT = int(map_range(slider_particle_count, 0, 100, 50, 2000))
    REPULSION_RADIUS = int(map_range(slider_repulsion_radius, 0, 100, 40, 300))
    REPULSION_STRENGTH = map_range(slider_repulsion_strength, 0, 100, 0.5, 8.0)
    PARTICLE_SIZE = int(map_range(slider_particle_size, 0, 100, 1, 8))
    TRAIL_LENGTH = int(map_range(slider_trail_length, 0, 100, 0, 100))

def sync_sliders_to_settings():
    """Syncs slider positions to current settings."""
    global slider_particle_count, slider_repulsion_radius, slider_repulsion_strength
    global slider_particle_size, slider_trail_length
    
    slider_particle_count = int(map_range(PARTICLE_COUNT, 50, 2000, 0, 100))
    slider_repulsion_radius = int(map_range(REPULSION_RADIUS, 40, 300, 0, 100))
    slider_repulsion_strength = int(map_range(REPULSION_STRENGTH, 0.5, 8.0, 0, 100))
    slider_particle_size = int(map_range(PARTICLE_SIZE, 1, 8, 0, 100))
    slider_trail_length = int(map_range(TRAIL_LENGTH, 0, 100, 0, 100))

# Initialize slider sync
sync_sliders_to_settings()

def adjust_particle_count(new_count):
    """Adds or removes particles to match the target count."""
    global particles, PARTICLE_COUNT
    current = len(particles)
    if new_count > current:
        for _ in range(new_count - current):
            particles.append(Particle())
    elif new_count < current:
        particles = particles[:new_count]
    PARTICLE_COUNT = new_count

# Particle classes and stuff wooo
class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
    
    def update(self, mouse_x, mouse_y):
        global REPULSION_RADIUS, REPULSION_STRENGTH
        
        # Distance to mouse
        dx = self.x - mouse_x
        dy = self.y - mouse_y
        dist = math.hypot(dx, dy)
        
        # Repulsion logic
        if dist < REPULSION_RADIUS and dist > 0:
            force = (REPULSION_RADIUS - dist) / REPULSION_RADIUS
            angle = math.atan2(dy, dx)
            self.vx += math.cos(angle) * force * REPULSION_STRENGTH
            self.vy += math.sin(angle) * force * REPULSION_STRENGTH
        
        # Drift settings
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        
        # Friction settings
        self.vx *= 0.95
        self.vy *= 0.95
        
        # Move
        self.x += self.vx
        self.y += self.vy
        
        # Bounce walls
        if self.x < 0: self.x = 0; self.vx *= -0.5
        if self.x > WIDTH: self.x = WIDTH; self.vx *= -0.5
        if self.y < 0: self.y = 0; self.vy *= -0.5
        if self.y > HEIGHT: self.y = HEIGHT; self.vy *= -0.5
    
    def draw(self, surface):
        global SAND_COLOR, PARTICLE_SIZE
        
        # Sand color logic
        if SAND_COLOR == "warm":
            shade = random.randint(180, 255)
            color = (shade, int(shade * 0.8), 100)
        elif SAND_COLOR == "cool":
            shade = random.randint(100, 200)
            color = (100, int(shade * 0.7), shade)
        elif SAND_COLOR == "white":
            shade = random.randint(180, 255)
            color = (shade, shade, shade)
        elif SAND_COLOR == "red":
            shade = random.randint(150, 255)
            color = (shade, 50, 50)
        else:
            color = (200, 180, 100)
            
        pygame.draw.rect(surface, color, (self.x, self.y, PARTICLE_SIZE, PARTICLE_SIZE))

# Create particles
particles = [Particle() for _ in range(PARTICLE_COUNT)]

# Ui Drawing functions
def draw_menu_button():
    """Draws the button that opens the settings menu."""
    btn_rect = pygame.Rect(WIDTH - 100, 10, 90, 35)
    pygame.draw.rect(screen, (60, 60, 60), btn_rect, border_radius=5)
    pygame.draw.rect(screen, (150, 150, 150), btn_rect, 2, border_radius=5)
    text = font.render("Settings", True, (255, 255, 255))
    screen.blit(text, (WIDTH - 90, 18))
    return btn_rect

def draw_tabs(menu_x, menu_y, menu_width):
    """Draws the tab bar at the top of the menu."""
    global tab_rects
    tab_rects = {}
    tab_width = menu_width // len(settings_tabs)
    
    for i, tab in enumerate(settings_tabs):
        tab_rect = pygame.Rect(menu_x + (i * tab_width), menu_y, tab_width, 35)
        tab_rects[tab] = tab_rect
        
        # Highlight current tab
        if tab == current_tab:
            pygame.draw.rect(screen, (80, 80, 100), tab_rect)
        else:
            pygame.draw.rect(screen, (50, 50, 60), tab_rect)
        
        pygame.draw.rect(screen, (120, 120, 130), tab_rect, 1)
        text = font.render(tab, True, (255, 255, 255))
        text_rect = text.get_rect(center=tab_rect.center)
        screen.blit(text, text_rect)

def draw_slider(x, y, width, value, label, show_value=True, value_suffix=""):
    """Draws a slider and returns its interaction rects."""
    # Label
    label_text = font.render(label, True, (220, 220, 220))
    screen.blit(label_text, (x, y - 5))
    
    # Slider background
    slider_bg = pygame.Rect(x, y + 20, width, 8)
    pygame.draw.rect(screen, (60, 60, 60), slider_bg, border_radius=4)
    
    # Slider fill
    fill_width = int((value / 100) * width)
    fill_rect = pygame.Rect(x, y + 20, fill_width, 8)
    pygame.draw.rect(screen, (100, 150, 200), fill_rect, border_radius=4)
    
    # Slider handle
    handle_x = x + fill_width - 6
    handle_rect = pygame.Rect(handle_x, y + 15, 12, 18)
    pygame.draw.rect(screen, (200, 200, 200), handle_rect, border_radius=3)
    
    # Value display
    if show_value:
        if value_suffix == "%":
            display_val = f"{value}%"
        elif value_suffix == "":
            display_val = str(int(map_range(value, 0, 100, 50, 2000))) if "Count" in label else str(value)
        else:
            display_val = f"{value}{value_suffix}"
        val_text = font.render(display_val, True, (180, 180, 180))
        screen.blit(val_text, (x + width + 10, y + 15))
    
    return slider_bg, handle_rect

def draw_dropdown(x, y, width, label, options, current_value, is_open):
    """Draws a dropdown menu."""
    global color_dropdown_rect, color_option_rects
    
    # Label
    label_text = font.render(label, True, (220, 220, 220))
    screen.blit(label_text, (x, y - 5))
    
    # Dropdown button
    dropdown_rect = pygame.Rect(x, y + 15, width, 30)
    color_dropdown_rect = dropdown_rect
    pygame.draw.rect(screen, (50, 50, 60), dropdown_rect)
    pygame.draw.rect(screen, (120, 120, 130), dropdown_rect, 1)
    
    # Current value
    val_text = font.render(current_value, True, (255, 255, 255))
    screen.blit(val_text, (x + 10, y + 20))
    
    # Arrow
    arrow = font.render("▼" if not is_open else "▲", True, (180, 180, 180))
    screen.blit(arrow, (x + width - 25, y + 20))
    
    # Options if open
    color_option_rects = []
    if is_open:
        for i, option in enumerate(options):
            opt_rect = pygame.Rect(x, y + 45 + (i * 30), width, 30)
            color_option_rects.append((opt_rect, option))
            pygame.draw.rect(screen, (60, 60, 70), opt_rect)
            pygame.draw.rect(screen, (100, 100, 110), opt_rect, 1)
            opt_text = font.render(option, True, (255, 255, 255))
            screen.blit(opt_text, (x + 10, y + 50 + (i * 30)))

def draw_settings_menu():
    """Draws the entire settings panel."""
    global menu_open, color_dropdown_open
    
    if not menu_open:
        return
    
    menu_width = 350
    menu_height = 450
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, (40, 40, 50), menu_rect, border_radius=10)
    pygame.draw.rect(screen, (100, 100, 120), menu_rect, 2, border_radius=10)
    
    title = title_font.render("Settings", True, (255, 255, 255))
    screen.blit(title, (menu_x + 15, menu_y + 10))
    
    close_rect = pygame.Rect(menu_x + menu_width - 30, menu_y + 8, 22, 22)
    pygame.draw.rect(screen, (80, 80, 90), close_rect, border_radius=3)
    close_text = font.render("X", True, (255, 255, 255))
    screen.blit(close_text, (menu_x + menu_width - 24, menu_y + 10))
    
    draw_tabs(menu_x + 10, menu_y + 45, menu_width - 20)
    
    content_y = menu_y + 85
    
    if current_tab == "Sand":
        draw_slider(menu_x + 20, content_y, 220, slider_particle_count, "Particle Count")
        draw_slider(menu_x + 20, content_y + 70, 220, slider_particle_size, "Particle Size")
        draw_dropdown(menu_x + 20, content_y + 140, 200, "Sand Color", color_options, SAND_COLOR, color_dropdown_open)
    
    elif current_tab == "Physics":
        draw_slider(menu_x + 20, content_y, 220, slider_repulsion_radius, "Repulsion Radius")
        draw_slider(menu_x + 20, content_y + 70, 220, slider_repulsion_strength, "Repulsion Strength")
    
    elif current_tab == "Visual":
        draw_slider(menu_x + 20, content_y, 220, slider_trail_length, "Trail Length", value_suffix="%")
    
    elif current_tab == "Credits":
        credits_title = title_font.render("Feedback/ContactInfo", True, (255, 255, 255))
        screen.blit(credits_title, (menu_x + 20, content_y))
        discord_label = font.render("Discord:", True, (180, 180, 180))
        screen.blit(discord_label, (menu_x + 20, content_y + 45))
        discord_value = font.render("dehydratedcupofwater.", True, (100, 180, 255))
        screen.blit(discord_value, (menu_x + 20, content_y + 70))
        
        github_label = font.render("GitHub:", True, (180, 180, 180))
        screen.blit(github_label, (menu_x + 20, content_y + 115))
        github_value = font.render("github.com/dehydratedcupofwater", True, (100, 180, 255))
        screen.blit(github_value, (menu_x + 20, content_y + 140))
        
        thanks = font.render("Thanks for playing dm for feedback!", True, (150, 150, 150))
        screen.blit(thanks, (menu_x + 20, content_y + 200))
        
        version = font.render("Version 1.0", True, (120, 120, 120))
        screen.blit(version, (menu_x + 20, content_y + 240))
    
    return menu_rect, close_rect
    # Click outside dropdown closes it
    color_dropdown_open = False
    return False
def handle_menu_click(mouse_pos, menu_rect, close_rect):
    global menu_open, current_tab, color_dropdown_open, SAND_COLOR
    global dragging_slider, slider_particle_count, slider_repulsion_radius
    global slider_repulsion_strength, slider_particle_size, slider_trail_length
    
    if not menu_open:
        return False
    
    if close_rect.collidepoint(mouse_pos):
        menu_open = False
        return True
    
    for tab, rect in tab_rects.items():
        if rect.collidepoint(mouse_pos):
            current_tab = tab
            return True
    
    menu_x, menu_y = menu_rect.x, menu_rect.y
    content_y = menu_y + 85
    
    if current_tab == "Sand":
        if color_dropdown_rect.collidepoint(mouse_pos):
            color_dropdown_open = not color_dropdown_open
            return True
        
        if color_dropdown_open:
            for opt_rect, option in color_option_rects:
                if opt_rect.collidepoint(mouse_pos):
                    SAND_COLOR = option
                    color_dropdown_open = False
                    return True
        
        handle = pygame.Rect(menu_x + 20 + int((slider_particle_count / 100) * 220) - 6, content_y + 15, 12, 18)
        if handle.collidepoint(mouse_pos):
            dragging_slider = "particle_count"
            return True
        
        handle2 = pygame.Rect(menu_x + 20 + int((slider_particle_size / 100) * 220) - 6, content_y + 85, 12, 18)
        if handle2.collidepoint(mouse_pos):
            dragging_slider = "particle_size"
            return True
    
    elif current_tab == "Physics":
        handle = pygame.Rect(menu_x + 20 + int((slider_repulsion_radius / 100) * 220) - 6, content_y + 15, 12, 18)
        if handle.collidepoint(mouse_pos):
            dragging_slider = "repulsion_radius"
            return True
        
        handle2 = pygame.Rect(menu_x + 20 + int((slider_repulsion_strength / 100) * 220) - 6, content_y + 85, 12, 18)
        if handle2.collidepoint(mouse_pos):
            dragging_slider = "repulsion_strength"
            return True
    
    elif current_tab == "Visual":
        handle = pygame.Rect(menu_x + 20 + int((slider_trail_length / 100) * 220) - 6, content_y + 15, 12, 18)
        if handle.collidepoint(mouse_pos):
            dragging_slider = "trail_length"
            return True
    
    elif current_tab == "Credits":
        discord_rect = pygame.Rect(menu_x + 20, content_y + 70, 200, 25)
        if discord_rect.collidepoint(mouse_pos):
            pygame.display.set_caption("Sand Physics Simulation - Discord: dehydratedcupofwater.")
            return True
        
        github_rect = pygame.Rect(menu_x + 20, content_y + 140, 250, 25)
        if github_rect.collidepoint(mouse_pos):
            webbrowser.open("https://github.com/dehydratedcupofwater")
            return True
    
    color_dropdown_open = False
    return False
def handle_slider_drag(mouse_x):
    """Updates slider values while dragging."""
    global slider_particle_count, slider_repulsion_radius, slider_repulsion_strength
    global slider_particle_size, slider_trail_length
    
    if dragging_slider is None:
        return
    
    menu_width = 350
    menu_x = (WIDTH - menu_width) // 2
    slider_x = menu_x + 20
    slider_width = 220
    
    # Calculate slider percentage
    relative_x = max(0, min(slider_width, mouse_x - slider_x))
    percentage = (relative_x / slider_width) * 100
    
    if dragging_slider == "particle_count":
        slider_particle_count = int(percentage)
    elif dragging_slider == "particle_size":
        slider_particle_size = int(percentage)
    elif dragging_slider == "repulsion_radius":
        slider_repulsion_radius = int(percentage)
    elif dragging_slider == "repulsion_strength":
        slider_repulsion_strength = int(percentage)
    elif dragging_slider == "trail_length":
        slider_trail_length = int(percentage)
    
    # Update actual settings
    old_particle_count = PARTICLE_COUNT
    update_settings_from_sliders()
    
    # Adjust particle count if it changed
    if old_particle_count != PARTICLE_COUNT:
        adjust_particle_count(PARTICLE_COUNT)

# Main loop (do not touch ts either)
running = True
mouse_x, mouse_y = -1000, -1000
menu_btn_rect = pygame.Rect(WIDTH - 100, 10, 90, 35)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if dragging_slider:
                handle_slider_drag(event.pos[0])
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check menu button
                if menu_btn_rect.collidepoint(event.pos):
                    menu_open = not menu_open
                    color_dropdown_open = False
                
                # Handle menu clicks if open
                if menu_open:
                    menu_rect, close_rect = draw_settings_menu()
                    handle_menu_click(event.pos, menu_rect, close_rect)
                else:
                    # Click outside closes dropdown
                    color_dropdown_open = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = None
    
    # Fade effect (trail)
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(TRAIL_LENGTH)
    fade.fill((0, 0, 0))
    screen.blit(fade, (0, 0))
    
    # Update and draw particles
    for p in particles:
        p.update(mouse_x, mouse_y)
        p.draw(screen)
    
    # Draw UI
    menu_btn_rect = draw_menu_button()
    if menu_open:
        draw_settings_menu()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# ================================