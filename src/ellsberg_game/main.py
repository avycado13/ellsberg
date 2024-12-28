import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Pentagon Papers: A Game of Conscience")
clock = pygame.time.Clock()

# Sound effects (you would need to add your own .wav files)
pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
photocopy_sound = pygame.mixer.Sound("photocopy.wav")
alert_sound = pygame.mixer.Sound("alert.wav")

# Main character (Daniel Ellsberg)
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 5

# Guard class for AI behavior
class Guard(pygame.sprite.Sprite):
    def __init__(self, start_pos, patrol_points):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=start_pos)
        self.patrol_points = patrol_points
        self.current_point = 0
        self.speed = 2
        self.state = "patrolling"
        self.detection_zone = pygame.Rect(self.rect.x, self.rect.y, 100, 50)  # Simple detection zone

    def update(self):
        if self.state == "patrolling":
            target_point = self.patrol_points[self.current_point]
            if self.rect.x < target_point[0]:
                self.rect.x += self.speed
            elif self.rect.x > target_point[0]:
                self.rect.x -= self.speed

            if self.rect.y < target_point[1]:
                self.rect.y += self.speed
            elif self.rect.y > target_point[1]:
                self.rect.y -= self.speed

            if self.rect.topleft == target_point:
                self.current_point = (self.current_point + 1) % len(self.patrol_points)
                
            self.detection_zone = pygame.Rect(self.rect.x, self.rect.y, 100, 50)
        # More states (suspicious, alert) can be added here

# Create guards
guards = pygame.sprite.Group()
guards.add(Guard(start_pos=(100, 100), patrol_points=[(100, 100), (300, 100), (300, 300), (100, 300)]))

# Puzzle: Finding the Key (for Level 1)
key_found = False
drawer_unlocked = False
key_location = random.choice([(50, 50), (150, 150), (250, 250)])  # Randomize key location

# Placeholder for different game states
game_state = "Level 1: The Decision"

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Update player position based on key presses
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Update guards
    guards.update()

    # Collision detection with guards
    for guard in guards:
        if guard.detection_zone.collidepoint(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2):
            alert_sound.play()
            print("Alert! You've been detected.")
            running = False

    # Puzzle: Finding the Key (Level 1)
    if game_state == "Level 1: The Decision":
        if not key_found:
            key_rect = pygame.Rect(key_location[0], key_location[1], 20, 20)
            if key_rect.collidepoint(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2):
                key_found = True
                print("Key found!")
        else:
            if player_pos[0] < 100 and player_pos[1] < 100:
                drawer_unlocked = True
                print("Drawer unlocked, documents found!")
                game_state = "Level 2: The Copying Process"

    # Puzzle: Photocopying without Detection (Level 2)
    if game_state == "Level 2: The Copying Process":
        if keys[pygame.K_SPACE]:
            photocopy_sound.play()
            print("Photocopying papers...")
            # Check for guard proximity
            for guard in guards:
                if guard.detection_zone.collidepoint(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2):
                    alert_sound.play()
                    print("Alert! You've been detected.")
                    running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw guards
    guards.draw(screen)

    # Draw the key if not found
    if not key_found:
        pygame.draw.rect(screen, (0, 255, 0), key_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# End of game
pygame.quit()
