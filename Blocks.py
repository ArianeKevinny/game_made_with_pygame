import pygame
import random


class Block:
    num_blocks = 0  # Indica o número de blocos no conjunto de blocos
    create_other = False  # Indica se pode criar outro conjunto de blocos
    delete = False  # Indica se pode deletar o conjunto de blocos
    blocks_made = [0, [5, 10, 15]]
    have_star = False
    def __init__(self, mode):
        self.pos_t = []
        self.pos_b = []
        type_obst = []
        self.obst_pos = []
        self.mode = mode  # Representa o tipo de blocos, background e obstáculos
        self.blocks_made[0] += 1
        # De acordo com o modo, os obstáculos se alteram
        if mode == "ice":
            type_obst = ["ice rock", "snowman", "sign"]
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
        y_top = 400  # Altura que são gerados os blocos no topo
        y_bottom = 440  # Altura que são gerados os blocos no topo
        self.num_blocks = random.randint(2, 8)  # Escolhe aleatoriamente o número de blocos que o conjunto terá
        if self.num_blocks >= 4:
            obst_num = random.randint(2, self.num_blocks - 2)  # Indica o bloco que vai ficar o obstáculo
            obst_ind = random.randint(0, len(type_obst)-1)  # Indica o índice do obstáculo na lista dos obstáculos
            self.obst = pygame.image.load("img/obst/"+type_obst[obst_ind]+".png")  # Representa a imagem do obstáculo
        if self.blocks_made[0] in self.blocks_made[1]:
            star_num = random.randint(0, self.num_blocks - 1)
            if self.num_blocks >= 4:
                while star_num == obst_num:
                    star_num = random.randint(0, self.num_blocks - 1)
            self.star = pygame.image.load("img/star.png")
            self.have_star = True
        for i in range(0, self.num_blocks):  # Insere as posições dos blocos dentro de uma lista
            # Obs: Os blocos sempre surgem da borda direita da tela
            self.pos_t.append([600 + (i * 40), y_top])
            self.pos_b.append([600 + (i * 40), y_bottom])
            if self.num_blocks > 4 and i == obst_num:  # Insere a posição do obstáculo
                self.obst_pos = [type_obst[obst_ind], 600 + (i * 40), y_top - self.obst.get_height(), 1]
                if type_obst[obst_ind] == "cannon":
                    self.pos_cannonball = []
                elif type_obst[obst_ind] == "bee":
                    self.obst_pos.append(-0.5)
            if self.have_star and i == star_num:
                self.star_pos = [600 + (i * 40), y_top - 10 - self.star.get_height()]

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
            if self.pos_snow[i][0] >= 610 or self.pos_snow[i][1] >= 490:
                self.pos_snow.pop(i)
                # ... e adiciona outro no lugar
                self.pos_snow.append([random.randint(0, 590), random.randint(0, 590)])
            i += 1  # É o contador que permite que todos os flocos sejam movidos

    def check_obst(self, player):
        """Checa se houve colisão do personagem com algum obstáculo"""
        x_player = 0
        x_obst = 0
        y_player = 0
        y_obst = 0
        # Checa se o personagem se chocou com um obstáculo
        if self.obst_pos[0] != "cannon":
            # O canhão não é um obstáculo em si, mas suas bolas são
            x_player = self.obst_pos[1] < player.player_x < self.obst_pos[1] + self.obst.get_width()
            y_player = self.obst_pos[2] < player.player_y < self.obst_pos[2] + self.obst.get_height()
            x_obst = player.player_x < self.obst_pos[1] < player.player_x + player.char_sprite.get_width()
            y_obst = player.player_y < self.obst_pos[2] < player.player_y + player.char_sprite.get_height()
        else:
            if self.pos_cannonball:
                x_player = self.pos_cannonball[0] < player.player_x < self.pos_cannonball[0] + 27
                y_player = self.pos_cannonball[1] < player.player_x < self.pos_cannonball[1] + 27
                x_obst = player.player_x < self.pos_cannonball[0] < player.player_x + player.char_sprite.get_width()
                y_obst = player.player_y < self.pos_cannonball[1] < player.player_y + player.char_sprite.get_height()
        # Caso coincida nos dois casos, tira uma vida do personagem
        if (x_player or x_obst) and (y_player or y_obst):
            self.obst_pos[3] = 0
            player.lives -= 1


    def check_star(self, player):
        """Checa se houve colisão do personagem com algum obstáculo"""
        x_player = 0
        x_star = 0
        y_player = 0
        y_star = 0
        # Checa se o personagem se chocou com um obstáculo
        x_player = self.star_pos[0] < player.player_x < self.star_pos[0] + self.star.get_width()
        y_player = self.star_pos[1] < player.player_y < self.star_pos[1] + self.star.get_height()
        x_star = player.player_x < self.star_pos[0] < player.player_x + player.char_sprite.get_width()
        y_star = player.player_y < self.star_pos[1] < player.player_y + player.char_sprite.get_height()
        if (x_player or x_star) and (y_player or y_star):
            self.have_star = False
            player.num_stars += 1

    def show(self, screen):
        # A abelha se movimenta mais rápido que o resto dos dos obstáculos
        # Depois tenho que implementar a abelha subir e descer
        if self.obst_pos and self.obst_pos[0] == "bee":
            screen.blit(self.obst, (self.obst_pos[1], self.obst_pos[2]))
            self.obst_pos[1] -= random.randint(5, 10)
            if self.obst_pos[1] > -10:
                if self.obst_pos[2] > 380:
                    self.obst_pos[3] = - random.random()
                elif self.obst_pos[2] < 330:
                    self.obst_pos[3] = random.random()
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
            self.pos_t[i] = [self.pos_t[i][0] - 4, self.pos_t[i][1]]
            self.pos_b[i] = [self.pos_b[i][0] - 4, self.pos_b[i][1]]
            #if self.mode == "ice":  # Caso o modo seja de neve, irá nevar
            #    self.snowing(screen)
            # Movimenta o obstáculo
            if self.obst_pos and self.obst_pos[1] == self.pos_t[i][0] + 4 and self.obst_pos[0] != "bee":
                screen.blit(self.obst, (self.obst_pos[1], self.obst_pos[2]))
                self.obst_pos[1] -= 4
                if self.obst_pos[0] == "cannon":  # Especifica o comportamento da bola que ele atira
                    if not self.pos_cannonball and self.obst_pos[1] <= 640 - self.obst.get_width():
                        self.pos_cannonball = [self.obst_pos[1] - 20, self.obst_pos[2]]
                    if self.pos_cannonball:
                        cannonball = pygame.image.load("img/obst/cannonball.png")
                        screen.blit(cannonball, (self.pos_cannonball[0], self.pos_cannonball[1]))
                        self.pos_cannonball[0] -= 8
            if self.have_star and self.star_pos[0] == self.pos_t[i][0] + 4:
                screen.blit(self.star, (self.star_pos[0], self.star_pos[1]))
                self.star_pos[0] -= 4
            if i == self.num_blocks - 1:
                # A distância de um conjunto de blocos para outro é de 80px
                # Caso chegue essa distância, ele permite criar outro conjunto de blocos
                if self.pos_t[i][0] <= 500:
                    self.create_other = True
                # Quando o conjunto de blocos sai da tela, então permite deletar o conjunto de blocos
                if self.pos_t[i][0] <= -40:
                    self.delete = True

    def show_static(self, screen):
        # Mostra os blocos de forma estática na posição que estavam quando o personagem morreu
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
        if 5 >= self.num_blocks > 2:
            screen.blit(self.obst, (self.obst_pos[1], self.obst_pos[2]))
