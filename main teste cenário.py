from Blocks import Block
import pygame

blocks = [] # lista com todos os blocos
background = pygame.image.load("img/forest/background.png")
background_pos = [[0, 0], [-1440, 0]] # Posição do background, no caso da floresta, ainda vou implementar o do resto

def paralax(screen): # Faz o paralax (efeito em que o fundo move, mas o personagem não)
    screen.blit(background, background_pos[0])
    screen.blit(background, background_pos[1])
    background_pos[0][0] += 4
    background_pos[1][0] += 4
    if background_pos[0][0] == 1440:
        background_pos.pop(0)
        background_pos.append([-1440, 0])

def new_block(): # Cria um novo conjunto de blocos
    block = Block()
    blocks.append(block)

pygame.init()
running = True
pygame.display.set_caption("Teste")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((640, 480))
new_block()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    paralax(screen) # OBS: Ainda tá em fase de teste
    for i in range(len(blocks)):
        blocks[i].show(screen) # Mostra o conteúdo de cada bloco
    if blocks[len(blocks) - 1].create_other: # Permite que crie outro
        new_block()
    try:
        if blocks[0].delete: # Deleta o primeiro se ele já saiu da tela
            blocks.pop(0)
    except:
        pass
    pygame.display.update()
