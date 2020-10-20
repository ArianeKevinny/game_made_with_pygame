import pygame
import math
from Blocks import Block
from PIL import Image

frames = {"galinha": 0, "pinguim": 0, "homem": 0, "mulher": 0}


# Cria um retângulo com um certo nível trasnparência
def transp_rec(width, height, color, trasnparency):
    m = pygame.Surface((width, height))  # Cria um retângulo
    m.set_alpha(trasnparency)  # Adiciona a transparência nele
    m.fill(color)  # Adiciona a trasnparência nele
    return m


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
def paralax(screen, background, background_pos):
    # A função cria dois papeis de paredes, que vão alternando, quando o primeiro sai da tela, ele é
    # reposicionado atrás do segundo
    screen.blit(background, background_pos[1])
    screen.blit(background, background_pos[2])
    background_pos[1][0] += 1
    background_pos[2][0] += 1
    if background_pos[1][0] == background_pos[0]:
        background_pos.pop(1)
        background_pos.append([-background_pos[0], 0])


# Código que eu peguei no stackoverflow para conseguir executar gifs, separando-os em frames

def insert_gif(path, x_scale=0, y_scale=0):
    def pil_to_game(img):
        format = "RGBA"
        data = img.tobytes("raw", format)
        return pygame.image.fromstring(data, img.size, format)

    def get_gif_frame(img, frame):
        format = "RGBA"
        img.seek(frame)
        return img.convert(format)

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
def button(screen, text, x_button, y_button):
    smallfont = pygame.font.SysFont('Corbel', 35)  # Define a fonte
    text = smallfont.render(text, True, (0, 0, 0))  # Cria o texto
    pygame.draw.rect(screen, (0, 0, 0), [x_button - 2, y_button - 2, 104, 44])  # Cria um retângulo preto
    # para servir de contorno
    pygame.draw.rect(screen, (255, 51, 51), [x_button, y_button, 100, 40])  # Cria o retângulo que será o
    # botão
    text_width = text.get_width()
    posX_test = 50 - math.ceil(text_width / 2) # Posiciona o texto centralizado no botão
    screen.blit(text, (x_button + posX_test, y_button + 2))  # Mostra o texto


# Faz o menu
def menu(screen):
    clock = pygame.time.Clock()
    text_char = ""
    b = True
    mode = ""
    char = ""
    inicio = True
    choose_character = False
    mediumfont = pygame.font.SysFont('cambria', 35)
    background = pygame.image.load("img/menu.png")
    background = pygame.transform.scale(background, (853, 480))
    background_pos = [853, [0, 0], [-853, 0]]
    m = transp_rec(500, 400, (230, 239, 255), 125)  # Retângulo usado no menu
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
                        pos_char = (95, 195)
                        char_selection = transp_rec(70, 70, (255, 0, 0), 80)
                    elif 200 < pos_mouse[0] < 250 and 200 < pos_mouse[1] < 260:
                        mode = "ice"
                        char = "pinguim"
                        pos_char = (195, 195)
                        char_selection = transp_rec(60, 70, (255, 0, 0), 80)
                    elif 310 < pos_mouse[0] < 370 and 140 < pos_mouse[1] < 260:
                        mode = "city"
                        char = "homem"
                        pos_char = (305, 135)
                        char_selection = transp_rec(70, 130, (255, 0, 0), 80)
                    elif 420 < pos_mouse[0] < 510 and 140 < pos_mouse[1] < 260:
                        mode = "forest"
                        char = "mulher"
                        pos_char = (415, 135)
                        char_selection = transp_rec(110, 130, (255, 0, 0), 80)
                    if char:
                        if 250 < pos_mouse[0] < 350 and 370 < pos_mouse[1] < 410:
                            b = False
        paralax(screen, background, background_pos)  # Executa o paralax
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
                screen.blit(char_selection, pos_char)
            # Mostra os 4 personagens em movimento
            # A função utilizada retorna frame por frame, e mostra ele na tela
            frame_galinha = insert_gif("animações/galinha.gif", 55, 60)
            screen.blit(frame_galinha, (100, 200))
            frame_pinguim = insert_gif("animações/pinguim.gif", 49, 60)
            screen.blit(frame_pinguim, (200, 200))
            frame_homem = insert_gif("animações/homem.gif", 54, 120)
            screen.blit(frame_homem, (310, 140))
            frame_mulher = insert_gif("animações/mulher.gif", 107, 120)
            screen.blit(frame_mulher, (420, 140))
            mediumfont = pygame.font.SysFont('cambria', 35)
            text = mediumfont.render('Escolha seu persongem', True, (0, 0, 0))
            shadow = mediumfont.render('Escolha seu persongem', True, (153, 153, 153))
            screen.blit(shadow, (115, 52))
            screen.blit(text, (112, 50))
            clock.tick(10)
        pygame.display.update()
    return mode, char  # A função retorna o modo do jogo e o personagem escolhido
