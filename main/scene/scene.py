import pygame, random
from .utils import SceneBase, half_of, draw_rounded_rect


class SampleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((255, 255, 255))


class MainScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen
        self.player = pygame.transform.scale(pygame.image.load('./images/player.png'), (80, 80))

        self.player_loc = (half_of(self.screen.get_width()) - 40, self.screen.get_height() - 100)
        self.bullets_shot = {}
        self.enemies = {}
        self.round_num = 0
        self.score = 0

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.player_loc = (event.pos[0] - 40, event.pos[1] - 40)
            #hold down mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                while True:
                    num = random.randint(1, 999999)
                    if num in self.bullets_shot:
                        pass
                    else:
                        self.bullets_shot[num] = {
                            "instance": self.CreateBullet(0),
                            "loc": (self.player_loc[0] + 30, self.player_loc[1]),
                            "eval": 0
                        }
                        break


    def Update(self):
        pass

    def Render(self, screen):
        print(self.score)
        screen.fill((255, 255, 255))
        self.RoundRender()

        screen.blit(self.player, (self.player_loc))

        for enemy in self.enemies:
            screen.blit(self.enemies[enemy]["instance"], self.enemies[enemy]["loc"])
            if self.enemies[enemy]["cooldown"] > 0:
                self.enemies[enemy]["cooldown"] -= 1
            else:
                while True:
                    num = random.randint(1, 999999)
                    if num in self.bullets_shot:
                        pass
                    else:
                        self.bullets_shot[num] = {
                            "instance": self.CreateBullet(1),
                            "loc": (self.enemies[enemy]["loc"][0] + 30, self.enemies[enemy]["loc"][1]),
                            "eval": 1
                        }
                        break
                self.enemies[enemy]["cooldown"] = self.enemies[enemy]["originalcd"]

        for item in self.bullets_shot:
            screen.blit(self.bullets_shot[item]['instance'], self.bullets_shot[item]['loc'])

        enemies_copy = self.enemies.copy()
        for enemy2 in self.enemies:
            for item2 in self.bullets_shot:
                if int(self.bullets_shot[item2]["loc"][0]) in range(int(self.enemies[enemy2]["loc"][0]), int(self.enemies[enemy2]["loc"][0] + 80)):
                    if int(self.bullets_shot[item2]["loc"][1]) in range(int(self.enemies[enemy2]["loc"][1]), int(self.enemies[enemy2]["loc"][1] + 80)):
                        if self.bullets_shot[item2]["eval"] == 0:
                            del enemies_copy[enemy2]
                            self.score += 1
        self.enemies = enemies_copy

        for item2 in self.bullets_shot:
            if int(self.bullets_shot[item2]["loc"][0]) in range(int(self.player_loc[0]), int(self.player_loc[0] + 80)):
                if int(self.bullets_shot[item2]["loc"][1]) in range(int(self.player_loc[1]), int(self.player_loc[1] + 80)):
                    if self.bullets_shot[item2]["eval"] == 1:
                        exit('You died')

        bullets_shot_copy = self.bullets_shot.copy()
        for item1 in self.bullets_shot:
            if self.bullets_shot[item1]["loc"][1] > self.screen.get_height() or self.bullets_shot[item1]["loc"][1] < 0:
                del bullets_shot_copy[item1]
            else:
                if self.bullets_shot[item1]["eval"] == 0:
                    self.bullets_shot[item1]["loc"] = (self.bullets_shot[item1]["loc"][0], self.bullets_shot[item1]["loc"][1] - 5)
                if self.bullets_shot[item1]["eval"] == 1:
                    self.bullets_shot[item1]["loc"] = (self.bullets_shot[item1]["loc"][0], self.bullets_shot[item1]["loc"][1] + 1.75)
        self.bullets_shot = bullets_shot_copy

        for enemy1 in self.enemies:
            self.enemies[enemy1]["loc"] = (self.enemies[enemy1]["loc"][0] + random.randint(-2, 2), self.enemies[enemy1]["loc"][1] + 0.4)


    def CreateEnemy(self):
        return pygame.transform.scale(pygame.image.load('./images/enemy.png'), (80, 80))

    def CreateBullet(self, eval: int):
        if eval not in [0, 1]: return
        if eval == [0, 1][0]: return pygame.transform.scale(pygame.image.load('./images/bullet.png'), (20, 20))  # Player
        if eval == [0, 1][1]: return pygame.transform.rotate(pygame.transform.scale(pygame.image.load('./images/bullet.png'), (20, 20)), 180)

    def RoundRender(self):
        if len(self.enemies.keys()) > 0:
            return
        else:
            self.round_num += 1

        if self.round_num in [1, 2, 3]:
            for i in range(0, self.round_num * 3):
                self.enemies[i] = {
                    "instance": self.CreateEnemy(),
                    "loc": (random.randint(80, self.screen.get_width()-80), 0),
                    "originalcd": 500,
                    "cooldown": 0
                }
        else:
            for i in range(0, self.round_num * random.randint(3, 7)):
                self.enemies[i] = {
                    "instance": self.CreateEnemy(),
                    "loc": (random.randint(80, self.screen.get_width() - 80), 0),
                    "originalcd": 150,
                    "cooldown": 0
                }