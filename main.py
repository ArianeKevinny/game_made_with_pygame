import pygame
from functions import *
from MyPlayer import Player

blocks = []  # Lista em que serão armazenados os blocos que aparecem na tela
pos_heart = [(), (), ()]


def main():
    pygame.init()  # Inicia o jogo
    running = True
    pygame.display.set_caption("Teste")  # Título do jogo
    screen = pygame.display.set_mode((600, 480))  # Tamanho da tela
    bg_pos = intro(screen)
    [mode, char] = menu(screen, bg_pos)  # Mostra o menu
    if mode == "":
        running = False
    else:
        player = Player(char)
        # Os papéis de parede possuem diferentes tamanhos, então é preciso adaptar o tamanho para cada um deles
        if mode == "city":
            background_pos = [816, [0, 0], [-816, 0]]
        elif mode == "forest":
            background_pos = [1440, [0, 0], [-1440, 0]]
        elif mode == "ice":
            background_pos = [853, [0, 0], [-853, 0]]
        background = pygame.image.load("img/"+mode+"/background.png")  # Carrega o papel de parede
        background = pygame.transform.scale(background, (background_pos[0], 480))  # Adequa para caber na tela
        blocks.append(first_block(mode))  # O primeiro bloco é maior que a maioria
    while running:
        pygame.time.delay(20) # Um pequeno delay para conseguir equilibrar a ações do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE: # Quando aperta para cima ou
                    # espaço o personagem pula
                    if player.lives > 0:
                        player.jump()
        paralax(screen, background, background_pos)
        show_hearts(screen, player.lives)
        for i in range(len(blocks)):
            if player.state == "falling" or player.lives == 0:
                blocks[i].show_static(screen) # Quando o personagem morre, mostra uma imagem estática
            else:
                blocks[i].show(screen)
                if blocks[i].num_blocks > 2 and blocks[i].obst_pos and blocks[i].obst_pos[3]:
                    # Checa se houve colisão do personagem com os obstáculos
                    blocks[i].check_obst(player)
        player.show(screen, blocks)  # Mostra o jogador
        if player.state != "falling":  # Caso o jogador não esteja caindo...
            # ... executa as funções normais dos blocos, como destruir e criar mais
            if blocks:
                if blocks[len(blocks) - 1].create_other:
                    block = Block(mode)
                    blocks.append(block)
                if blocks[0].delete:
                    del blocks[0]
            player.check_fall(blocks) # Checa se o jogador caiu
        if player.state == "falling" and player.player_y < 480:
            player.player_y += 6  # 80 + player.char_sprite.get_height()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
