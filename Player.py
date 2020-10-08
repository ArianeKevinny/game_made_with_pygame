import pygame
import random
from os import path

# Dados gerais do jogo.
largura_X = 600 # largura da tela
altura_Y = 480 # altura da tela
bloco = 60 # Tamanho de cada tile (tile é bloco) 
personagem_X = bloco
personagem_Y = int(bloco * 1.33)

branco = (255, 255, 255)
preto = (0, 0, 0)

img_dir = path.join(path.dirname(__file__), 'img')#chamar a pasta de imagens colocar o arquivo no mesmo local onde está a pasta img
animacoes_dir = path.join(path.dirname(__file__), 'animacoes')#chamar a pasta de animações
PLAYER_IMG = 'player_img'

#definir a volocidade y, de queda
velocidade_Y = 5
# Define a velocidade inicial no pulo
tamanho_PULO = quadrado
# Define a velocidade em x
velocidade_X = 5

# Modo do personagem
parado = 0
pulando = 1
caindo = 2

# Define os tipos de blocos
BLOCK = 0
EMPTY = -1

# um mapa 8 por 10, pq cada bloco é de 60, sem empty lugares vazio e block lugares bloqueados
mapa = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
]

def carregar_imagens(img_dir):
    imagens = {}
    ##nesse caso eu não upei nenhuma imagem
    imagens[PLAYER_IMG] = pygame.image.load(path.join(img_dir, '')).convert_alpha()
    imagens[BLOCK] = pygame.image.load(path.join(img_dir, '')).convert()
    return imagens

#parte do cenário que tá errado obviamente mas bora mudar
#depois importa a classe correta
class Tile(pygame.sprite.Sprite):
    def __init__(self, player_img, linha, coluna):
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do bloco.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do bloco.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o bloco
        self.rect.x = bloco * coluna
        self.rect.y = bloco * linha     

# Classe dos personagens
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, linha, coluna, blocks):
        pygame.sprite.Sprite.__init__(self)

        self.state = parado # Modo atual

        player_img = pygame.transform.scale(player_img, (personagem_X, persogame_Y)) # ajustar a imagem

        self.image = player_img # é uma imagem estatica, ainda não testei colocar um gif
        
        self.rect = self.image.get_rect() #esse rect é um objeto que guarda a posiçao do personagem

        self.blocks = blocks #guarda os blocos pra caso tenha algum objeto a frente

        # Posiciona o personagem
        self.rect.x = coluna * bloco
        self.rect.bottom = linha * bloco # essa linha é o índice do bloco abaixo do bonequinho

        self.speedx = 0
        self.speedy = 0

        ## Esse self ai é a imagem que fica relacionada ao rect pra movimemtar o personagem 

    def update(self):

        self.speedy += velocidade_Y

        if self.speedy > 0:
            self.state = caindo
            
        self.rect.y += self.speedy
        # Se encontrou algum coisa (direção Y)
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        for collision in collisions:
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                self.state = parado
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0
                self.state = parado

        self.rect.x += self.speedx
        # Se sair da janela do jogo pelas laterais
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= largura:
            self.rect.right = largura - 1
        # Se encontrou alguma coisa (direção X)
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        for collision in collisions:
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

    # fazer o personagem pular
    def jump(self):
        if self.state == parado:
            self.speedy -= tamanho_PULO
            self.state = pulando

def game_screen(screen):
    clock = pygame.time.Clock()
    imagens = carregar_imagens(img_dir)

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    player = Player(imagens[PLAYER_IMG], 12, 2, blocks)

    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            tile_type = mapa[linha][coluna]
            if tile_type == BLOCK:
                tile = Tile(assets[tile_type], linha, coluna)
                all_sprites.add(tile)
                blocks.add(tile)

    all_sprites.add(player)

    n_sair = 0
    sair = 1

    state = n_sair
    while state != sair:
        clock.tick(60)
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = sair
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx -= SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx -= SPEED_X

        all_sprites.update()
        screen.fill(BRANCO)
        all_sprites.draw(screen)
        pygame.display.flip()


# Main()
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Jogo (bora pensar em um nome melhor)")

try:
    game_screen(screen)
finally:
    pygame.quit()

