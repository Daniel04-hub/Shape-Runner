import pygame
import asyncio
import random
from sys import exit

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "My Web Game"
FPS = 60

# Colors
BG_COLOR = (59, 122, 87) # Amazon Green-ish
WHITE = (255, 255, 255)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load Sounds Logic (Robust)
def load_sound_safe(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

coin_sound = load_sound_safe("assets/coin.wav")
hit_sound = load_sound_safe("assets/hit.wav")
gameover_sound = load_sound_safe("assets/gameover.wav")

def play_sound(sound):
    if sound:
        sound.play()

# --- Classes with Asset Fallback ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        except Exception as e:
            # print(f"Asset Error: {e}")
            self.image = pygame.Surface((32, 32))
            self.image.fill((50, 50, 255)) # Blue Square
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 50, 50)) # Red Square
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 32)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 32)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, walls):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 215, 0)) # Yellow Square
            pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)
        self.rect = self.image.get_rect()
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)
            if not pygame.sprite.spritecollideany(self, walls):
                break

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/wall.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill((128, 128, 128)) # Grey Square
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Main Game Loop (Async) ---
async def main():
    # Groups
    player_group = pygame.sprite.GroupSingle()
    player = Player()
    player_group.add(player)

    walls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Create Walls
    for i in range(20):
        w = Wall(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        walls.add(w)
    
    # Create Coins
    for i in range(20):
        c = Coin(walls)
        coins.add(c)

    # Create Enemies
    for i in range(5):
        e = Enemy()
        enemies.add(e)

    score = 0
    font = pygame.font.Font(None, 30) # Default font
    game_over = False

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                # Restart logic would go here
                pass

        if not game_over:
            # Updates
            player_group.update()
            enemies.update()

            # Coin Collection
            hits = pygame.sprite.spritecollide(player, coins, True)
            for coin in hits:
                score += 1
                play_sound(coin_sound)

            # Enemy Collision
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True
                play_sound(gameover_sound)

        # Draw
        screen.fill(BG_COLOR)
        walls.draw(screen)
        coins.draw(screen)
        enemies.draw(screen)
        player_group.draw(screen)

        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            go_surf = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(go_surf, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2))

        pygame.display.update()
        
        # Critical for Web: await sleep
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
