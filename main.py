import pygame
import random
import sys


# screen size
WIDTH = 1000
HEIGHT = 562

# files
BG_COLOR = (27, 27, 27)
WHITE = (255, 255, 255)
FONT = 'assets/font/NerkoOne-Regular.ttf'
BUBBLES = ['assets/img/bubble1.png', 'assets/img/bubble2.png', 'assets/img/bubble3.png', 'assets/img/bubble4.png']
BUBBLE_SONG = 'assets/audio/pop.ogg'
CURSOR = 'assets/img/cursor.png'

#points
POINTS = 0
RECORD = 0

GAME_TIME = 1200
TIMER = GAME_TIME 

#game state
GAME_PAUSED = True
CLOSE = False

class Bubble(pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y) -> None:
    super().__init__()
    self.image = pygame.image.load(BUBBLES[random.randrange(len(BUBBLES))]).convert_alpha()
    self.image = pygame.transform.scale(self.image, (100, 100))
    self.rect = self.image.get_rect()
    self.rect.center = [pos_x, pos_y]

class CatCursor(pygame.sprite.Sprite):
  def __init__(self) -> None:
    super().__init__()
    self.image = pygame.image.load(CURSOR).convert_alpha()
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.sound = pygame.mixer.Sound(BUBBLE_SONG)
    self.rect = self.image.get_rect()

  def update(self):
    self.rect.center = pygame.mouse.get_pos()

  def shoot(self):
    global POINTS

    collisions = pygame.sprite.spritecollide(cursor, bubbles_group, False)
    for collision in collisions:
      self.sound.play()
      POINTS += 1
      collision.kill()
      bubble = Bubble(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
      bubbles_group.add(bubble)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Soap Bubbles')

clock = pygame.time.Clock()

fontTitle = pygame.font.Font(FONT, 60)
font = pygame.font.Font(FONT, 25)

bubbles_group = pygame.sprite.Group()
for i in range(20):
  bubble = Bubble(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
  bubbles_group.add(bubble)

cursor = CatCursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)

while not CLOSE:
  if not GAME_PAUSED:
    pygame.mouse.set_visible(False)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          GAME_PAUSED = not GAME_PAUSED
      if event.type == pygame.MOUSEBUTTONDOWN:
        cursor.shoot()

    screen.fill(BG_COLOR)
    bubbles_group.draw(screen)
    cursor_group.draw(screen)
    cursor_group.update()

    score = font.render(f"Pontos: {POINTS}", True, WHITE)
    time = font.render(f"Tempo: {TIMER/60:.1f}", True, WHITE)

    screen.blit(score, (30, 30))
    screen.blit(time, (30, 70))

    TIMER -= 1
    if TIMER < 0:
      TIMER = GAME_TIME
      if POINTS > RECORD:
        RECORD = POINTS
      GAME_PAUSED = not GAME_PAUSED
        # POINTS = 0

  else:
    screen.fill(BG_COLOR)
    pygame.mouse.set_visible(True)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          GAME_PAUSED = not GAME_PAUSED
          if TIMER == GAME_TIME:
            POINTS = 0


    title = fontTitle.render(f"Soap Bubbles", True, WHITE)
    pause = font.render(f"Pressione ESPAÇO para jogar", True, (200, 141, 180))
    description = font.render(f"Estoure o maior numero de bolhas que conseguir", True, WHITE)
    record = font.render(f"Recorde: {RECORD}", True, WHITE)
    score = font.render(f"Pontos: {POINTS}",True, WHITE)

    screen.blit(title, title.get_rect(center = (WIDTH/2, HEIGHT/2-50)))
    screen.blit(description, description.get_rect(center = (WIDTH/2, HEIGHT/2+15)))
    screen.blit(pause, pause.get_rect(center = (WIDTH/2, HEIGHT/3*2)))
    screen.blit(score, (30, 30))
    screen.blit(record, (30, 70))
  
  pygame.display.flip()
  clock.tick(60)