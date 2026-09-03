import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FROG OF THE FLY")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

running = True
game_state = "playing"

# Vi lager Frode tha Frosk
frog_x = WIDTH // 2
frog_y = HEIGHT // 2
frog_radius = 30
frog_speed = 3

# Vi lager Fredrik tha Flue
fly_x = random.randint(30, WIDTH - 30)
fly_y = random.randint(30, HEIGHT - 30)
fly_radius = 8

score = 0

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spill-logikk
    if game_state == "playing":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            frog_x -= frog_speed

        if keys[pygame.K_RIGHT]:
            frog_x += frog_speed

        if keys[pygame.K_UP]:
            frog_y -= frog_speed

        if keys[pygame.K_DOWN]:
            frog_y += frog_speed

        # Pythagoras finner avstanden mellom Frode og Fredrik
        distance_x = frog_x - fly_x
        distance_y = frog_y - fly_y
        distance = (distance_x**2 + distance_y**2) ** 0.5

        # Frode spiser Fredrik
        if distance < frog_radius + fly_radius:
            score += 1
            frog_radius += 2

            # Fredrik reinkarneres et tilfeldig sted
            fly_x = random.randint(30, WIDTH - 30)
            fly_y = random.randint(30, HEIGHT - 30)

            # Frode har tatt ett måltid for mye
            if score >= 25:
                game_state = "exploding"

    # Bakgrunn
    screen.fill((120, 190, 120))

    # Fredrik tha Flue
    pygame.draw.circle(screen, (30, 30, 30), (fly_x, fly_y), fly_radius)
    pygame.draw.circle(screen, (220, 220, 220), (fly_x - 7, fly_y - 6), 5)
    pygame.draw.circle(screen, (220, 220, 220), (fly_x + 7, fly_y - 6), 5)

    # Frode tha Frosk
    pygame.draw.circle(screen, (40, 160, 60), (frog_x, frog_y), frog_radius)

    # Øyne
    pygame.draw.circle(screen, (255, 255, 255), (frog_x - 15, frog_y - 20), 10)
    pygame.draw.circle(screen, (255, 255, 255), (frog_x + 15, frog_y - 20), 10)

    # Pupiller
    pygame.draw.circle(screen, (0, 0, 0), (frog_x - 15, frog_y - 20), 4)
    pygame.draw.circle(screen, (0, 0, 0), (frog_x + 15, frog_y - 20), 4)

    # Score
    score_text = font.render(f"Fluer spist: {score}", True, (30, 30, 30))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()