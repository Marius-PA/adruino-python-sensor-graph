from serial import Serial
import numpy as np
import turtle, time

# --- SECTION 1: FUNCTIONS & MEMORY ---

# This dictionary remembers the last X,Y coordinates for each sensor
last_positions = {"blue": None, "red": None}

# NEW: remember previous angle
previous_angle = None

def polar_to_cartesian(dist, angle):
    x = dist * np.cos(np.deg2rad(angle))
    y = dist * np.sin(np.deg2rad(angle))
    return x, y

def draw_live_connected(angle, dist, color, current_scale):
    # Filter out junk data
    if dist > 1000 or dist <= 0:
        return 
    
    x, y = polar_to_cartesian(dist, angle)
    screen_x = x * current_scale
    screen_y = y * current_scale

    # Draw line from previous point if it exists
    if last_positions[color] is not None:
        t.penup()
        t.goto(last_positions[color])
        t.pendown()
        t.color(color)
        t.width(2)
        t.goto(screen_x, screen_y)

    # Draw current point
    t.penup()
    t.goto(screen_x, screen_y)
    t.dot(6, color)

    # Save current point
    last_positions[color] = (screen_x, screen_y)

def draw_grid_with_axes(max_dist, grid_size, current_scale):
    """Draws the background grid based on the fixed max distance"""
    t.color("lightgray")
    max_grid = int(np.ceil(max_dist / grid_size) * grid_size)

    # Vertical lines
    x = -max_grid
    while x <= max_grid:
        t.penup()
        t.goto(x * current_scale, -max_grid * current_scale)
        t.pendown()
        t.goto(x * current_scale, max_grid * current_scale)
        x += grid_size

    # Horizontal lines
    y = -max_grid
    while y <= max_grid:
        t.penup()
        t.goto(-max_grid * current_scale, y * current_scale)
        t.pendown()
        t.goto(max_grid * current_scale, y * current_scale)
        y += grid_size

    # X axis
    t.color("black")
    t.penup()
    t.goto(-max_grid * current_scale, 0)
    t.pendown()
    t.goto(max_grid * current_scale, 0)

    for x in range(-max_grid, max_grid + 1, grid_size):
        t.penup()
        t.goto(x * current_scale, -15)
        t.write(f"{x}cm", align="center", font=("Arial", 8, "normal"))

    # Y axis
    t.penup()
    t.goto(0, -max_grid * current_scale)
    t.pendown()
    t.goto(0, max_grid * current_scale)

    for y in range(-max_grid, max_grid + 1, grid_size):
        if y != 0:
            t.penup()
            t.goto(-20, y * current_scale - 5)
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
max_dist_fixed = 350
half_window = min(screen.window_width(), screen.window_height()) / 2 * 0.9
scale = half_window / max_dist_fixed

# Draw the static grid
draw_grid_with_axes(max_dist_fixed, grid_size_cm, scale)
screen.update()

# --- SECTION 3: LIVE EXECUTION ---

with Serial('COM5', 115200, timeout=1) as ser:
    time.sleep(2)

    current_angle = 0

    # Loop to capture data
    # 163
    for i in range(0, 379):

        raw_data = ser.readline().decode('utf-8').strip()

        if not raw_data:
            continue

        pieces = raw_data.split()

        for piece in pieces:
            try:
                if piece.startswith('A'):

                    current_angle = float(piece[1:])

                    # NEW: detect angle wraparound
                    if previous_angle is not None:
                        if previous_angle > current_angle:
                            # Break the line connection
                            last_positions["blue"] = None
                            last_positions["red"] = None

                    previous_angle = current_angle

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