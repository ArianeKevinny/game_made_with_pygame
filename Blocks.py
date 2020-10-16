import pygame
import random


class Block:
    num_blocks = 0  # Indica o número de blocos no conjunto de blocos
    create_other = False  # Indica se pode criar outro conjunto de blocos
    delete = False  # Indica se pode deletar o conjunto de blocos

    def __init__(self, mode):
        self.pos_t = []
        self.pos_b = []
        type_obst = []
        self.mode = mode  # Representa o tipo de blocos, background e obstáculos
        # De acordo com o modo, os obstáculos se alteram
        if mode == "ice":
            type_obst = ["ice rock", "snowman"]
            self.pos_snow = []  # Lista com a posição dos flocos de neve
            # Cria 80 flocos de neve em posições aleatórias
            for j in range(80):
                self.pos_snow.append([random.randint(0, 620), random.randint(0, 620)])
        elif mode == "forest":
            type_obst = ["bee", "stump", "rock"]
        elif mode == "city":
            type_obst = ["spike", "hydrant", "cannon"]
        # Carrega todos os tipos de blocos necessários
        self.t_left = pygame.image.load("img/" + mode + "/t_left.png")
        self.t_right = pygame.image.load("img/" + mode + "/t_right.png")
        self.t_middle = pygame.image.load("img/" + mode + "/t_middle.png")
        self.t_single = pygame.image.load("img/" + mode + "/t_single.png")
        self.b_left = pygame.image.load("img/" + mode + "/b_left.png")
        self.b_right = pygame.image.load("img/" + mode + "/b_right.png")
        self.b_middle = pygame.image.load("img/" + mode + "/b_middle.png")
        self.b_single = pygame.image.load("img/" + mode + "/b_single.png")
        y_top = 408  # Altura que são gerados os blocos no topo
        y_bottom = 444  # Altura que são gerados os blocos no topo
        self.num_blocks = random.randint(1, 5)  # Escolhe aleatoriamente o número de blocos que o conjunto terá
        if self.num_blocks > 2:
            obst_num = random.randint(1, self.num_blocks - 2)  # Indica o bloco que vai ficar o obstáculo
            obst_ind = random.randint(0, len(type_obst)-1)  # Indica o índice do obstáculo na lista dos obstáculos
            self.obst = pygame.image.load("img/obst/"+type_obst[obst_ind]+".png")  # Representa a imagem do obstáculo
        for i in range(0, self.num_blocks):  # Insere as posições dos blocos dentro de uma lista
            # Obs: Os blocos sempre surgem da borda direita da tela
            self.pos_t.append([640 + (i * 36), y_top])
            self.pos_b.append([640 + (i * 36), y_bottom])
            if self.num_blocks > 2 and i == obst_num:  # Insere a posição do obstáculo
                self.obst_pos = [type_obst[obst_ind], 640 + (i * 32), y_top - self.obst.get_height()]
                if type_obst[obst_ind] == "cannon":
                    self.pos_cannonball = []
                elif type_obst[obst_ind] == "bee":
                    self.obst_pos.append(-0.5)

    def snowing(self, screen):
        # Função simula o efeito de novo
        # Apenas na fase do pinguim
        snowflake = pygame.image.load("img/snowflake.png")  # Imagem do floco de neve
        i = 0
        while i != len(self.pos_snow):  # Atualiza a posição dos flocos 1 por 1
            screen.blit(snowflake, (self.pos_snow[i][0], self.pos_snow[i][1]))
            self.pos_snow[i][0] += 0.3  # Velocidade vertical
            self.pos_snow[i][1] += 0.2  # Velocidade horizontal
            # Deleta um floco depois que ele saiu da tela ...
            if self.pos_snow[i][0] >= 650 or self.pos_snow[i][1] >= 490:
                self.pos_snow.pop(i)
                # ... e adiciona outro no lugar
                self.pos_snow.append([random.randint(0, 620), random.randint(0, 620)])
            i += 1  # É o contador que permite que todos os flocos sejam movidos

    def show(self, screen):
        # A abelha se movimenta mais rápido que o resto dos dos obstáculos
        # Depois tenho que implementar a abelha subir e descer
        print(self.num_blocks)
        if self.num_blocks > 2 and self.obst_pos[0] == "bee":
            screen.blit(self.obst, (self.obst_pos[1], self.obst_pos[2]))
            self.obst_pos[1] -= 2
            if self.obst_pos[2] > 380:
                self.obst_pos[3] = -0.5
            elif self.obst_pos[2] < 330:
                self.obst_pos[3] = 0.5
            self.obst_pos[2] += self.obst_pos[3]
        # Mostra todos o blocos
        for i in range(self.num_blocks):
            if i == 0 and self.num_blocks > 1:
                screen.blit(self.t_left, self.pos_t[i])
                screen.blit(self.b_left, self.pos_b[i])
            elif i == len(self.pos_t) - 1 and self.num_blocks > 1:
                screen.blit(self.t_right, self.pos_t[i])
                screen.blit(self.b_right, self.pos_b[i])
            elif self.num_blocks == 1:
                screen.blit(self.t_single, self.pos_t[i])
                screen.blit(self.b_single, self.pos_b[i])
            else:
                screen.blit(self.t_middle, self.pos_t[i])
                screen.blit(self.b_middle, self.pos_b[i])
            # Velocidade de 1px
            self.pos_t[i] = [self.pos_t[i][0] - 1, self.pos_t[i][1]]
            self.pos_b[i] = [self.pos_b[i][0] - 1, self.pos_b[i][1]]
            if self.mode == "ice":  # Caso o modo seja de neve, irá nevar
                self.snowing(screen)
            # Movimenta o obstáculo
            if self.num_blocks > 2 and self.obst_pos[1] == self.pos_t[i][0] + 1 and self.obst_pos[0] != "bee":
                screen.blit(self.obst, (self.obst_pos[1], self.obst_pos[2]))
                self.obst_pos[1] -= 1
                if self.obst_pos[0] == "cannon":  # Especifica o comportamento da bola que ele atira
                    if not self.pos_cannonball and self.obst_pos[1] <= 640 - self.obst.get_width():
                        self.pos_cannonball = [self.obst_pos[1] - 20, self.obst_pos[2]]
                    if self.pos_cannonball:
                        cannonball = pygame.image.load("img/obst/cannonball.png")
                        screen.blit(cannonball, (self.pos_cannonball[0], self.pos_cannonball[1]))
                        self.pos_cannonball[0] -= 3
            if i == self.num_blocks - 1:
                # A distância de um conjunto de blocos para outro é de 80px
                # Caso chegue essa distância, ele permite criar outro conjunto de blocos
                if self.pos_t[i][0] <= 560:
                    self.create_other = True
                # Quando o conjunto de blocos sai da tela, então permite deletar o conjunto de blocos
                if self.pos_t[i][0] <= -40:
                    self.delete = True
