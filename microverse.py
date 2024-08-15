import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" Void Universe")

# Set the background color (black for the void)
black = (0, 0, 0)

# Timer setup
start_time = time.time()

# Star properties
num_stars = 250  # Number of stars
stars = []

# Define colors
colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Initialize stars with random positions, brightness, and colors
for _ in range(num_stars):
    star_x = random.randint(0, screen_width - 1)
    star_y = random.randint(0, screen_height - 1)
    brightness = random.randint(100, 255)
    color = random.choice(colors)
    next_color_change_time = time.time() + random.uniform(0, 10)
    stars.append([star_x, star_y, brightness, color, next_color_change_time])

# Floating body class
class FloatingBody:
    def __init__(self, x, y, speed_x, speed_y, color, creation_time):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.creation_time = creation_time
        self.message = ""
        self.last_color_change_time = time.time()
        self.color_change_interval = 10  # Change color every 10 seconds

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off the walls
        if self.x - body_radius < 0 or self.x + body_radius > screen_width:
            self.speed_x *= -1
        if self.y - body_radius < 0 or self.y + body_radius > screen_height:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), body_radius)
        if self.message:
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(self.message, True, self.color)
            text_rect = text_surface.get_rect(center=(self.x, self.y - body_radius - 15))
            screen.blit(text_surface, text_rect)

    def multiply(self):
        # Create two new bodies with different colors
        for _ in range(2):
            new_body = FloatingBody(
                x=self.x,
                y=self.y,
                speed_x=random.choice([-1, 1]),
                speed_y=random.choice([-1, 1]),
                color=random.choice(colors),
                creation_time=time.time()
            )
            floating_bodies.append(new_body)

    def update_color(self):
        # Change color periodically
        current_time = time.time()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.color = random.choice(colors)
            self.last_color_change_time = current_time

# Floating body properties
body_radius = 5
aura_radius = 65  # Define the radius of the clickable aura

# Define initial colors
colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255)]

# Create initial floating bodies
floating_bodies = [
    FloatingBody(
        x=random.randint(body_radius, screen_width - body_radius),
        y=random.randint(body_radius, screen_height - body_radius),
        speed_x=random.choice([-1, 1]),
        speed_y=random.choice([-1, 1]),
        color=random.choice(colors),
        creation_time=time.time()
    ),
    FloatingBody(
        x=random.randint(body_radius, screen_width - body_radius),
        y=random.randint(body_radius, screen_height - body_radius),
        speed_x=random.choice([-1, 1]),
        speed_y=random.choice([-1, 1]),
        color=random.choice(colors),
        creation_time=time.time()
    )
]

# Messages
messages = [
    "This place is empty.",
    "Am I inside a void?",
    "Can you hear me?",
    "What's my name?",
    "Who created me?",
    "Am I a creation?",
    "This place is dark and cold yet I feel satisfied...",
    ".....",
    "  ",
    "  ",
    "  "
]

interaction_messages = [
    "Who are you?",
    "Are you a creation as well?",
    "What is this place?",
    "Did we just meet?"
]

interaction_time = 0  # To control the interaction cooldown
interaction_cooldown = 2  # 2-second cooldown between interactions

# Main loop
running = True
while running:
    current_time = time.time()
    
    # Calculate elapsed time since the program started
    elapsed_time = current_time - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)
    elapsed_time_str = f"{elapsed_minutes:02}:{elapsed_seconds:02}"

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for body in floating_bodies:
                distance = ((mouse_x - body.x) ** 2 + (mouse_y - body.y) ** 2) ** 0.5
                if distance <= aura_radius:  # Check if the click is within the aura
                    body.speed_x = random.choice([-2, 2])
                    body.speed_y = random.choice([-2, 2])
                    body.message = random.choice(messages)

    # Update and draw stars
    screen.fill(black)
    
    for star in stars:
        star_x, star_y, brightness, star_color, next_color_change_time = star
        brightness += random.choice([-5, 5])  # Randomly change brightness
        brightness = max(100, min(brightness, 255))  # Keep brightness within bounds
        star_color = (brightness, brightness, brightness)
        screen.set_at((star_x, star_y), star_color)
        star[2] = brightness  # Update brightness in the list

    # Update and draw floating bodies
    for body in floating_bodies:
        body.update_color()  # Update color if needed
        body.move()
        body.draw()

        # Check for interactions
        for other_body in floating_bodies:
            if body != other_body:
                distance_between_bodies = ((body.x - other_body.x) ** 2 + (body.y - other_body.y) ** 2) ** 0.5
                if distance_between_bodies <= 2 * aura_radius and current_time - interaction_time > interaction_cooldown:
                    body.message = random.choice(interaction_messages)
                    other_body.message = random.choice(interaction_messages)
                    interaction_time = current_time

        # Check for multiplication
        time_since_creation = current_time - body.creation_time
        if 35 <= time_since_creation < 36:  # Multiply after 35 seconds
            body.multiply()
            body.creation_time += 36  # Prevent the body from multiplying again at the next check
        elif 45 <= time_since_creation < 46:  # Multiply after 45 seconds
            body.multiply()
            body.creation_time += 46  # Prevent the body from multiplying again at the next check

    # Display the timer on the screen
    font = pygame.font.SysFont(None, 48)
    timer_surface = font.render(elapsed_time_str, True, (255, 255, 255))
    screen.blit(timer_surface, (20, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
