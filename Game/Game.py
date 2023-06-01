import pygame
from pygame.locals import *


screen = pygame.display.set_mode((640, 640))

class BaseBullet:
    def __init__(self, x: float, y: float, damage: int, side: str, name: str, speed: float, spacing: float):
        self.damage = damage
        image = pygame.image.load(name)
        match side:
            case "left":
                self.x = x - spacing
                self.y = y
                self.image = pygame.transform.rotate(image,-90)
                self.rect = self.image.get_rect()
            case "right":
                self.x = x + spacing
                self.y = y
                self.image = pygame.transform.rotate(image,90)
                self.rect = self.image.get_rect()
            case "up":
                self.y = y - spacing
                self.x = x
                self.image = image
                self.rect = self.image.get_rect()
            case "down":
                self.y = y + spacing
                self.x = x
                self.image = pygame.transform.rotate(image,180)
                self.rect = self.image.get_rect()
        self.side = side
        self.speed = speed
        self._iscollided = None
    def shoot(self) -> None:
        match self.side:
            case "left":
                while not self._iscollided:
                    self.x -= self.speed
                    self.rect.x -= self.speed
                    self.update()
            case "right":
                while not self._iscollided:
                    self.x += self.speed
                    self.rect.x += self.speed
                    self.update()
            case "up":
                while not self._iscollided:
                    self.y -= self.speed
                    self.rect.y -= self.speed
                    self.update()
            case "down":
                while not self._iscollided:
                    self.y += self.speed
                    self.rect.y += self.speed
                    self.update()
    def _is_collision_enemy(self, other) -> bool:
        return self.rect.colliderect(other.rect)
    def update(self):
        screen.blit(self.image, (self.rect.centerx, self.rect.centery))

class BaseTank:
    def __init__(self, x: float, y: float, hp: int, damage: int, firerate: float, spacing: float, speed: int, bullet_speed:float, name: str = "BaseTank.png"):
        self.x = x
        self.y = y
        self._original_image = pygame.image.load(name)
        self.image = self._original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = hp
        self.damage = damage
        self.firerate = firerate
        self.spacing = spacing
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.name = name
        self.side: str = None
        self.delta_time = 0
        self.name_of_bullet: str = "BaseBullet.jpg"

    def moving(self, side) -> None:
        match side:
            case "left":
                self.image = pygame.transform.rotate(self._original_image, -180)
                self.rect = self.image.get_rect()
            case "right":
                self.image = pygame.transform.rotate(self._original_image, 0)
                self.rect = self.image.get_rect()
            case "up":
                self.image = pygame.transform.rotate(self._original_image, 90)
                self.rect = self.image.get_rect()
            case "down":
                self.image = pygame.transform.rotate(self._original_image, -90)
                self.rect = self.image.get_rect()
    def shoot(self) -> None:
        if self.delta_time >= self.firerate:
            bullet = BaseBullet(self.x, self.y, self.damage, self.side, self.name_of_bullet, 50, 2)
            self.delta_time = 0
            bullet.shoot()
        else:
            while self.delta_time <= self.firerate:
                    self.delta_time += pygame.time.get_ticks()
    def move(self) -> None:
        match self.side:
            case "left":
                self.moving("left")

            case "right":
                self.moving("right")
            case "up":
                self.moving("up")
            case "down":
                self.moving("down")


pygame.init()
clock = pygame.time.Clock()

tank = BaseTank(480, 480, 100, 10, 10, 20, 3, 1.5, "BaseTankAllies.jpg")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                tank.shoot()

            if event.key == K_w:
                tank.moving("up")
            elif event.key == K_a:
                tank.moving("left")
            elif event.key == K_d:
                tank.moving("right")
            elif event.key == K_s:
                tank.moving("down")

    screen.fill((0, 0, 0))
    screen.blit(tank.image, (tank.rect.centerx, tank.rect.centery))
    pygame.display.flip()
    clock.tick(60)