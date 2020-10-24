import pygame
from functions import *
from MyPlayer import Player

def main():
    pygame.init()  # Inicia o jogo
    running = True  # Define se o jogo continua rodando
    pre_game = True  # Variável que define se mostra o menu
    game = False  # Variável que define se mostra o jogo
    blocks = []  # Lista em que serão armazenados os blocos que aparecem na tela
    pygame.display.set_caption("Teste")  # Título do jogo
    screen = pygame.display.set_mode((600, 480))  # Tamanho da tela
    bg_pos = intro(screen)  # Mostra a introdução
    # [mode, char] = menu(screen, bg_pos)  # Mostra o menu
    while running:
        if pre_game:
            [mode, char] = menu(screen, bg_pos)  # Função que mostra o menu
            if mode:
                player = Player(char)  # Inicia o personagem 
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
                pre_game = False
                game = True
            else:  # Caso se feche o programa no menu, a função retorna "", e isso indica que o resto do programa não deve ser rodado
                running = False
        if game:
                pygame.time.delay(20) # Um pequeno delay para conseguir equilibrar a ações do jogador
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Caso clique no botão de fechar, ele para de rodar
                        running = False
                    if event.type == pygame.KEYDOWN:  # Caso clique numa tecla...
                        if event.key == pygame.K_UP or event.key == pygame.K_SPACE: # ...checa se é para cima ou espaço...
                            if player.lives > 0:  # ...e se tiver mais de 0 vidas...
                                player.jump()  # ...ele pula.
                    if player.state == "dead":  # Se o personagem tiver caido ou sem vidas...
                        if event.type == pygame.MOUSEBUTTONDOWN:  #  ... quando clicar com o botão do mouse...
                            pos_mouse = pygame.mouse.get_pos()  # ... Checa a posição, e se tiver dentro
                            # da área de um dos botões, executa a função desse botão
                            if 110 < pos_mouse[0] < 210 and 300 < pos_mouse[1] < 340:  # Botão de reiniciar
                                blocks = []  # Zera os blocos
                                blocks.append(first_block(mode))  # Trás o primeiro bloco (que é maior que os demais)
                                # Reseta o estado e as vidas do personagem
                                player.state = "still"
                                player.lives = 3
                                player.player_y = player.original_y
                            elif 400 < pos_mouse[0] < 500 and 300 < pos_mouse[1] < 340:  # Botão de sair
                                running = False
                if player.state == "dead" or player.state == "falling":  # Caso o personagem tenha morrido
                    paralax(screen, background, background_pos, 0)  # Executa a função que movimenta o plano de fundo
                    # Com velocidade 0, apenas para manter a posição do cenáio
                    for i in range(len(blocks)):
                        blocks[i].show_static(screen)  # Mostra uma versão estática dos blocos
                    if player.state == "falling":  # Caso esteja caindo, vai diminuindo a posição do personagem no eixo y
                        # E só depois dele sair da tela, que mostra o menu
                        player.player_y += 6
                        player.show(screen, blocks)
                    else:
                        screen.blit(player.char_sprite, (player.player_x, player.player_y))  # Mostra o sprite do personagem, onde ele morreu
                        defeated_menu(screen)  # Mostra o menu de derrota
                else:
                    paralax(screen, background, background_pos) # Executa a função que movimenta o plano de fundo
                    show_hearts(screen, player.lives)  # Executa a função que mostra os corações, que representam as vidas do personagem
                    # Mostra cada bloco
                    for i in range(len(blocks)):
                        blocks[i].show(screen)
                        if blocks[i].num_blocks > 2 and blocks[i].obst_pos and blocks[i].obst_pos[3]:
                            # Checa se houve colisão do personagem com os obstáculos
                            blocks[i].check_obst(player)
                    player.show(screen, blocks)  # Mostra o personagem
                    if blocks:
                        if blocks[len(blocks) - 1].create_other:  # Cria outro bloco
                            block = Block(mode)
                            blocks.append(block)
                        if blocks[0].delete:  # Deleta o primeiro bloco se ele já tiver saído da tela
                            del blocks[0]
                    player.check_fall(blocks) # Checa se o jogador caiu
                pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
