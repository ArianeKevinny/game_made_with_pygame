import pygame
import random

class Block:
    num = 0
    pos_top = []
    pos_bottom = []
    create_other = False
    delete = False
    snowflake = pygame.image.load("img/snowflake.png")
    pos_snow = []

    def __init__(self, mode):
        self.mode = mode
        self.t_left = pygame.image.load("img/" + mode + "/t_left.png")
        self.t_right = pygame.image.load("img/" + mode + "/t_right.png")
        self.t_middle = pygame.image.load("img/" + mode + "/t_middle.png")
        self.t_single = pygame.image.load("img/" + mode + "/t_single.png")
        self.b_left = pygame.image.load("img/" + mode + "/b_left.png")
        self.b_right = pygame.image.load("img/" + mode + "/b_right.png")
        self.b_middle = pygame.image.load("img/" + mode + "/b_middle.png")
        self.b_single = pygame.image.load("img/" + mode + "/b_single.png")

        y_top = 408
        y_bottom = 444
        p_top = []
        p_bottom = []
        self.num = random.randint(1, 5)
        for i in range(self.num):
            p_top.append([640 + i * 32, y_top])
            p_bottom.append([640 + i * 32, y_bottom])
        self.pos_top = p_top
        self.pos_bottom = p_bottom

    def snowing(self, screen):
        rem = []
        if not self.pos_snow:
            for i in range(60):
                self.pos_snow.append([random.randint(0, 620), random.randint(0, 620)])
        for i in range(len(self.pos_snow)):
            screen.blit(self.snowflake, (self.pos_snow[i][0], self.pos_snow[i][1]))
            self.pos_snow[i] = [self.pos_snow[i][0]+0.3, self.pos_snow[i][1] + 0.1]
            if self.pos_snow[i][0] > 320 and len(self.pos_snow) < 55:
                self.pos_snow.append([random.randint(0, 620), random.randint(0, 620)])
            if self.pos_snow[i][1] > 650 or self.pos_snow[i][0] > 650:
                rem.append(i)
                self.pos_snow.append([random.randint(0, 620), random.randint(0, 620)])
        for i in rem:
            self.pos_snow.pop(i)

    def show(self, screen):
        n = len(self.pos_top)
        for i in range(n):
            if i == 0 and n > 1:
                screen.blit(self.t_left, self.pos_top[i])
                screen.blit(self.b_left, self.pos_bottom[i])
            elif i == len(self.pos_top) - 1 and n > 1:
                screen.blit(self.t_right, self.pos_top[i])
                screen.blit(self.b_right, self.pos_bottom[i])
            elif n == 1:
                screen.blit(self.t_single, self.pos_top[i])
                screen.blit(self.b_single, self.pos_bottom[i])
            else:
                screen.blit(self.t_middle, self.pos_top[i])
                screen.blit(self.b_middle, self.pos_bottom[i])
            self.pos_top[i] = [self.pos_top[i][0] - 1, self.pos_top[i][1]]
            self.pos_bottom[i] = [self.pos_bottom[i][0] - 1, self.pos_bottom[i][1]]
            if self.mode == "ice":
                self.snowing(screen)
            if i == self.num - 1:
                if self.pos_top[i][0] <= 560:
                    self.create_other = True
                if self.pos_top[i][0] <= -40:
                    self.delete = True