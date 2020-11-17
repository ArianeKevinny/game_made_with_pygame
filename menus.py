import pygame
from functions import *
# Faz o menu do início
def menu_beginning(screen, background_pos):
    clock = pygame.time.Clock()
    b = True
    mode = ""
    char = ""
    inicio = True
    choose_character = False
    mediumfont = pygame.font.SysFont('cambria', 35)
    background = pygame.image.load("img/menu.png")
    background = pygame.transform.scale(background, (853, 480))
    m = transp_rec(500, 400, (230, 239, 255), 125)  # Retângulo usado no menu
    pos_char = {"galinha": (95, 195), "pinguim": (195, 195), "homem": (305, 135), "mulher": (415, 135)}
    while b:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                b = False
                mode = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if inicio:
                    if 250 < pos_mouse[0] < 350 and 250 < pos_mouse[1] < 290:
                        inicio = False
                        choose_character = True
                    if 250 < pos_mouse[0] < 350 and 310 < pos_mouse[1] < 350:
                        b = False
                        mode = ""
                elif choose_character:
                    # Quando clica num personagem, é preciso fazer um retangulo transparente nele para
                    # indicar que ele foi escolhido
                    if 100 < pos_mouse[0] < 160 and 200 < pos_mouse[1] < 260:
                        mode = "forest"
                        char = "galinha"
                        char_selection = transp_rec(70, 70, (255, 0, 0), 80)
                    elif 200 < pos_mouse[0] < 250 and 200 < pos_mouse[1] < 260:
                        mode = "ice"
                        char = "pinguim"
                        char_selection = transp_rec(60, 70, (255, 0, 0), 80)
                    elif 310 < pos_mouse[0] < 370 and 140 < pos_mouse[1] < 260:
                        mode = "city"
                        char = "homem"
                        char_selection = transp_rec(70, 130, (255, 0, 0), 80)
                    elif 420 < pos_mouse[0] < 510 and 140 < pos_mouse[1] < 260:
                        mode = "forest"
                        char = "mulher"
                        char_selection = transp_rec(110, 130, (255, 0, 0), 80)
                    if char:
                        if 250 < pos_mouse[0] < 350 and 370 < pos_mouse[1] < 410:
                            b = False
        paralax(screen, background, background_pos, -1)  # Executa o paralax
        screen.blit(m, (60, 50))
        if inicio:
            # No início mostra apenas dois botões
            button(screen, "Jogar", 250, 250)
            button(screen, "Sair", 250, 310)
        elif choose_character:
            if char:
                # Depois de escolher um personagem, mostra um texto que indica o personagem escolhido e o
                # botão de iniciar
                if char in ["galinha", "mulher"]:
                    art = " a "
                else:
                    art = " o "
                text_char = mediumfont.render("Você escolheu"+art+char, True, (0, 0, 0))
                text_pos = 320 - math.ceil(text_char.get_width()/2)
                text_char_shadow = mediumfont.render("Você escolheu"+art+char, True, (153, 153, 153))
                screen.blit(text_char_shadow, (text_pos + 2, 302))
                screen.blit(text_char, (text_pos, 300))
                button(screen, "Iniciar", 250, 370)
                screen.blit(char_selection, pos_char[char])
            # Mostra os 4 personagens em movimento
            # A função utilizada retorna frame por frame, e mostra ele na tela
            frame_galinha = insert_gif("animacoes/galinha/galinha.gif", 55, 60)
            screen.blit(frame_galinha, (100, 200))
            frame_pinguim = insert_gif("animacoes/pinguim/pinguim.gif", 49, 60)
            screen.blit(frame_pinguim, (200, 200))
            frame_homem = insert_gif("animacoes/homem/homem.gif", 54, 120)
            screen.blit(frame_homem, (310, 140))
            frame_mulher = insert_gif("animacoes/mulher/mulher.gif", 89, 100)
            screen.blit(frame_mulher, (420, 160))
            mediumfont = pygame.font.SysFont('cambria', 35)
            text = mediumfont.render('Escolha seu persongem', True, (0, 0, 0))
            shadow = mediumfont.render('Escolha seu persongem', True, (153, 153, 153))
            screen.blit(shadow, (115, 52))
            screen.blit(text, (112, 50))
            clock.tick(10)
        pygame.display.update()
    return mode, char  # A função retorna o modo do jogo e o personagem escolhido

def defeated_menu(screen):
    font = pygame.font.SysFont('Arial', 80)  # Define a fonte
    text = font.render("Você perdeu!", True, (0, 0, 0))
    m = transp_rec(500, 400, (230, 239, 255), 100)
    screen.blit(m, (60, 50))
    screen.blit(text, (109, 100))
    button(screen, "Reiniciar", 110, 300, 26)
    button(screen, "Voltar ao menu", 265, 300, 15)
    button(screen, "Sair", 400, 300)

def advice_menu(screen, bg_pos):
    going = True
    background = pygame.image.load("img/menu.png")
    background = pygame.transform.scale(background, (853, 480))
    menu = transp_rec(400, 205, (255, 255, 255), 130)
    font = pygame.font.SysFont('Arial', 15)  # Define a fonte
    text = [font.render("O objetivo do jogo é coletar todas as estrelas no três niveis.", True, (0, 0, 0)),
            font.render("Para  pular aperte espaço ou seta para cima", True, (0, 0, 0)),
            font.render("Aperte qualquer tecla para iniciar o jogo...", True, (0, 0, 0))]
    pos = [(139, 158), (190, 233), (186, 308)]
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                going = False
        paralax(screen, background, bg_pos, -1)
        screen.blit(menu, (100, 138))
        for i in range(3):
            screen.blit(text[i], pos[i])
        pygame.display.update()

def next_level_menu(screen):
    tela = transp_rec(600, 480, (0, 0, 0), 125)
    font1 = pygame.font.SysFont('Arial', 30)
    font2 = pygame.font.SysFont('Arial', 15)
    text = [font1.render("Você coletou todas as estrelas.", True, (255, 255, 255)),
            font2.render("Aperte qualquer tecla para ir para a próxima fase.", True, (255, 255, 255))]
    screen.blit(tela, (0, 0))
    screen.blit(text[0], (300 - math.ceil(text[0].get_width()/2), 240 - math.ceil(text[0].get_height()/2)))
    screen.blit(text[1], (300 - math.ceil(text[1].get_width() / 2), 450))

def victory_screen(screen):
    tela = transp_rec(600, 480, (0, 0, 0), 125)
    font1 = pygame.font.SysFont('Arial', 84)
    font2 = pygame.font.SysFont('Arial', 15)
    text = [font1.render("Você venceu", True, (255, 255, 255)),
            font2.render("Aperte qualquer tecla para sair.", True, (255, 255, 255))]
    screen.blit(tela, (0, 0))
    screen.blit(text[0], (300 - math.ceil(text[0].get_width() / 2), 150))
    screen.blit(text[1], (300 - math.ceil(text[1].get_width() / 2), 450))