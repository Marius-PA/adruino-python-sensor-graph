import random
from serial import Serial
import numpy as np
import turtle, time

# --- SECTION 1: FUNCTIONS & MEMORY ---

# This dictionary remembers the last X,Y coordinates for each sensor
last_positions = {"blue": None, "red": None}

def polar_to_cartesian(dist, angle):
    x = dist * np.cos(np.deg2rad(angle))
    y = dist * np.sin(np.deg2rad(angle))
    return x, y

def draw_live_connected(angle, dist, color, current_scale):
    # Filter out junk data
    if dist > 1000 or dist <= 0: return 
    
    x, y = polar_to_cartesian(dist, angle)
    screen_x = x * current_scale
    screen_y = y * current_scale

    # 1. If we have a previous point for this color, draw a line from it!
    if last_positions[color] is not None:
        t.penup()
        t.goto(last_positions[color])  # Go to the previous point
        t.pendown()                    # Put pen down to draw
        t.color(color)
        t.width(2)                     # Make the line slightly thicker
        t.goto(screen_x, screen_y)     # Draw the line to the new point

    # 2. Draw the new dot at the current location
    t.penup()
    t.goto(screen_x, screen_y)
    t.dot(6, color)

    # 3. Update the memory with the new location for next time
    last_positions[color] = (screen_x, screen_y)

def draw_grid_with_axes(max_dist, grid_size, current_scale):
    """Draws the background grid based on the fixed max distance"""
    t.color("lightgray")
    max_grid = int(np.ceil(max_dist / grid_size) * grid_size)

    # Lignes verticales
    x = -max_grid
    while x <= max_grid:
        t.penup()
        t.goto(x * current_scale, -max_grid * current_scale)
        t.pendown()
        t.goto(x * current_scale, max_grid * current_scale)
        x += grid_size

    # Lignes horizontales
    y = -max_grid
    while y <= max_grid:
        t.penup()
        t.goto(-max_grid * current_scale, y * current_scale)
        t.pendown()
        t.goto(max_grid * current_scale, y * current_scale)
        y += grid_size

    # Axe X (Y=0) en noir avec repères
    t.color("black")
    t.penup()
    t.goto(-max_grid * current_scale, 0)
    t.pendown()
    t.goto(max_grid * current_scale, 0)

    for x in range(-max_grid, max_grid + 1, grid_size):
        t.penup()
        t.goto(x * current_scale, 0 - 15)  
        t.write(f"{x}cm", align="center", font=("Arial", 8, "normal"))

    # Axe Y (X=0) en noir avec repères
    t.penup()
    t.goto(0, -max_grid * current_scale)
    t.pendown()
    t.goto(0, max_grid * current_scale)

    for y in range(-max_grid, max_grid + 1, grid_size):
        if y != 0:
            t.penup()
            t.goto(0 - 20, y * current_scale - 5) 
            t.write(f"{y}cm", align="right", font=("Arial", 8, "normal"))


# --- SECTION 2: SETUP & VARIABLES ---
screen = turtle.Screen()
screen.title("Cartographie de la pièce (Lignes Connectées)")
screen.setup(width=1.0, height=1.0)  
screen.tracer(0) 
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Set up the physical scale limits
grid_size_cm = 25
max_dist_fixed = 350  # Sets the edge of the screen to 10 meters
half_window = min(screen.window_width(), screen.window_height()) / 2 * 0.9
scale = half_window / max_dist_fixed

# Draw the static grid BEFORE the loop starts
draw_grid_with_axes(max_dist_fixed, grid_size_cm, scale)
screen.update()

# --- SECTION 3: LIVE EXECUTION ---
with Serial('COM5', 115200, timeout=1) as ser:
    time.sleep(2)
    current_angle = 0
    
    # Loop to capture data
    for i in range(0, 55):
        raw_data = ser.readline().decode('utf-8').strip()
        if not raw_data: continue
        pieces = raw_data.split()
    
        for piece in pieces:
            try:
                if piece.startswith('A'):
                    current_angle = float(piece[1:])
                    
                elif piece.startswith('B'):
                    dist1 = float(piece[1:]) / 10
                    if 1 < dist1 < 350: 
                        draw_live_connected(current_angle, dist1, "blue", scale)
                        
                elif piece.startswith('C'):
                    dist2 = float(piece[1:]) / 10
                    if 1 < dist2 < 350: 
                        draw_live_connected((current_angle + 180) % 360, dist2, "red", scale)
                        
            except ValueError:
                pass
            
        screen.update()

turtle.done()