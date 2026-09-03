import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FROG OF THE FLY")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 48)

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

explosion_start = 0
explosion_delay = 1000
particles = []

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
                explosion_start = pygame.time.get_ticks()

    if game_state == "exploding":
        time_since_explosion = pygame.time.get_ticks() - explosion_start

        # Frode pulserer før katastrofen
        if (time_since_explosion // 100) % 2 == 0:
            frog_radius += 1

        if time_since_explosion >= explosion_delay:
            game_state = "game_over"

            # Frode blir til biologisk konfetti
            for _ in range(80):
                particles.append(
                    {
                        "x": frog_x,
                        "y": frog_y,
                        "dx": random.uniform(-6, 6),
                        "dy": random.uniform(-6, 6),
                        "radius": random.randint(3, 8),
                        "color": random.choice(
                            [
                                (180, 0, 0),
                                (220, 20, 20),
                                (100, 0, 0),
                                (40, 160, 60),
                            ]
                        ),
                    }
                )

    if game_state == "game_over":
        for particle in particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.15

    # Bakgrunn
    screen.fill((120, 190, 120))

    # Fredrik tha Flue
    pygame.draw.circle(screen, (30, 30, 30), (fly_x, fly_y), fly_radius)
    pygame.draw.circle(screen, (220, 220, 220), (fly_x - 7, fly_y - 6), 5)
    pygame.draw.circle(screen, (220, 220, 220), (fly_x + 7, fly_y - 6), 5)

    # Frode tha Frosk
    if game_state != "game_over":
        pygame.draw.circle(screen, (40, 160, 60), (frog_x, frog_y), frog_radius)

        # Øyne
        pygame.draw.circle(screen, (255, 255, 255), (frog_x - 15, frog_y - 20), 10)
        pygame.draw.circle(screen, (255, 255, 255), (frog_x + 15, frog_y - 20), 10)

        # Pupiller
        pygame.draw.circle(screen, (0, 0, 0), (frog_x - 15, frog_y - 20), 4)
        pygame.draw.circle(screen, (0, 0, 0), (frog_x + 15, frog_y - 20), 4)

    # Blod og gørr
    if game_state == "game_over":
        for particle in particles:
            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                particle["radius"],
            )

        game_over_text = game_over_font.render(
            "Sorry. Frode overspiste og sprakk.",
            True,
            (30, 30, 30),
        )

        game_over_text2 = game_over_font.render(
            "GAME OVER",
            True,
            (180, 0, 0),
        )

        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        text2_rect = game_over_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

        screen.blit(game_over_text, text_rect)
        screen.blit(game_over_text2, text2_rect)

    # Score
    score_text = font.render(f"Fluer spist: {score}", True, (30, 30, 30))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()