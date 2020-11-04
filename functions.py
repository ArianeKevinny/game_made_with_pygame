import pygame
import math
from Blocks import Block
from PIL import Image
import sys

frames = {"galinha": 0, "pinguim": 0, "homem": 0, "mulher": 0}
pos_heart = [(20, 10), (80, 10), (140, 10)]
pos_star = [(420, 10), (480, 10), (540, 10)]


# Cria um retângulo com um certo nível trasnparência
def transp_rec(width, height, color, transparency):
    m = pygame.Surface((width, height))  # Cria um retângulo
    m.set_alpha(transparency)  # Adiciona a transparência nele
    m.fill(color)  # Adiciona a transparência nele
    return m


# Mostra o número de vidas, utilizando corações
def show_hearts_stars(screen, player):
    heart = pygame.image.load("img/heart.png")
    star = pygame.image.load("img/big star.png")
    for i in range(0, player.lives):
        screen.blit(heart, pos_heart[i])
    for i in range(player.num_stars):
        screen.blit(star, pos_star[i])


# Faz o primeiro bloco, que tem um tamanho maior que a maioria
def first_block(mode):
    # Cria um bloco
    b = Block(mode)
    # Muda as propriedades dele para que ele possua mais blocos que os outros blocos poderiam ter
    b.num_blocks = 25
    b.obst_pos = []
    b.pos_t = []
    b.pos_b = []
    for i in range(b.num_blocks):
        b.pos_t.append([i * 40, 400])
        b.pos_b.append([i * 40, 440])
    return b


# Faz o efeito em que o cenário também se move dando uma sensação de movimento
def paralax(screen, background, background_pos, speed=1):
    # A função cria dois papeis de paredes, que vão alternando, quando o primeiro sai da tela, ele é
    # reposicionado atrás do segundo
    screen.blit(background, background_pos[1])
    screen.blit(background, background_pos[2])
    if speed:
        background_pos[1][0] += speed
        background_pos[2][0] += speed
        if speed > 0:
            if background_pos[1][0] == (speed * math.ceil(background_pos[0]/speed)):
                background_pos.pop(1)
                background_pos.append([-background_pos[0], 0])
        else:
            if background_pos[1][0] == -1*(speed * math.ceil(background_pos[0]/speed)):
                background_pos.pop(1)
                background_pos.append([background_pos[0], 0])


# Código que eu peguei no stackoverflow para conseguir executar gifs, separando-os em frames

def insert_gif(path, x_scale=0, y_scale=0):
    def pil_to_game(img):
        data = img.tobytes("raw", "RGBA")
        return pygame.image.fromstring(data, img.size, "RGBA")

    def get_gif_frame(img, frame):
        img.seek(frame)
        return img.convert("RGBA")

    gif_img = Image.open(path)
    gif_name = ""
    if "galinha" in path:
        gif_name = "galinha"
    elif "pinguim" in path:
        gif_name = "pinguim"
    elif "homem" in path:
        gif_name = "homem"
    elif "mulher" in path:
        gif_name = "mulher"
    frame = pil_to_game(get_gif_frame(gif_img, frames[gif_name]))
    if x_scale and y_scale:
        frame = pygame.transform.scale(frame, (x_scale, y_scale))
    frames[gif_name] = (frames[gif_name] + 1) % gif_img.n_frames
    return frame


# Cria um botão (Com tamanho fixo)
def button(screen, text, x_button, y_button, font_size=35):
    smallfont = pygame.font.SysFont('Corbel', font_size)  # Define a fonte
    text = smallfont.render(text, True, (0, 0, 0))  # Cria o texto
    pygame.draw.rect(screen, (0, 0, 0), [x_button - 2, y_button - 2, 104, 44])  # Cria um retângulo preto
    # para servir de contorno
    pygame.draw.rect(screen, (255, 51, 51), [x_button, y_button, 100, 40])  # Cria o retângulo que será o
    # botão
    text_width = text.get_width()
    posy_text = 20 - math.ceil(font_size / 2)
    posx_text = 50 - math.ceil(text_width / 2)  # Posiciona o texto centralizado no botão
    screen.blit(text, (x_button + posx_text, y_button + posy_text))  # Mostra o texto


# Faz a intro
def intro(screen):
    CLOCK = pygame.time.Clock()
    bg = pygame.image.load("img/intro.png").convert()
    bg_pos = [853, [0, 0], [853, 0]]
    bgWidth, bgHeight = bg.get_rect().size
    running = True
    stageWidth = bgWidth * 2
    stagePosX = 0
    menu_transparency = 0
    startScrollingPosX = 300
    circleRadius = 25
    circlePosX = circleRadius
    playerPosX = circleRadius
    playerPosY = 400
    playerVelocityX = 0

    mulher = [pygame.image.load('animacoes/mulher/mulher1.png'), pygame.image.load('animacoes/mulher/mulher2.png'),
              pygame.image.load('animacoes/mulher/mulher3.png'),
              pygame.image.load('animacoes/mulher/mulher4.png'), pygame.image.load('animacoes/mulher/mulher5.png'),
              pygame.image.load('animacoes/mulher/mulher6.png'),
              pygame.image.load('animacoes/mulher/mulher7.png'), pygame.image.load('animacoes/mulher/mulher8.png')]
    walkcounter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.time.delay(65)
        if playerPosX > stageWidth - circleRadius + 5:  # se o jogador sai pelo limite da direita
            paralax(screen, bg, bg_pos, 0)
            menu = transp_rec(500, 400, (230, 239, 255), menu_transparency)
            screen.blit(menu, (60, 50))
            menu_transparency += 5
            if menu_transparency == 125:
                running = False
        else:
            paralax(screen, bg, bg_pos, -8)
            if walkcounter + 1 >= 8:
                walkcounter = 0
            playerPosX += 20
            walkcounter += 1
            if playerPosX < circleRadius: playerPosX = circleRadius
            if playerPosX < startScrollingPosX:
                circlePosX = playerPosX
            elif playerPosX > stageWidth - startScrollingPosX:
                circlePosX = playerPosX - stageWidth + 600
            else:
                circlePosX = startScrollingPosX
                stagePosX += -playerVelocityX

            rel_x = stagePosX % bgWidth
            # screen.blit(bg, (rel_x - bgWidth, 0))
            screen.blit(mulher[walkcounter], (circlePosX - 38, playerPosY - 200))
        pygame.display.update()
        CLOCK.tick(500)
    return bg_pos


# Faz o menu
def menu(screen, background_pos):
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



