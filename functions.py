import pygame
import math
from Blocks import Block
from PIL import Image

frames = {"galinha": 0, "pinguim": 0, "homem": 0, "mulher": 0}


# Cria um retângulo com um certo nível trasnparência
def transp_rec(screen, width, height, color, trasnparency):
    m = pygame.Surface((width, height))
    m.set_alpha(trasnparency)
    m.fill(color)
    screen.blit(m, (60, 50))
    return m


# Faz o primeiro bloco, que tem um tamanho maior que a maioria
def first_block(mode):
    b = Block(mode)
    b.num_blocks = 25
    b.pos_t = []
    b.pos_b = []
    for i in range(b.num_blocks):
        b.pos_t.append([i * 32, 408])
        b.pos_b.append([i * 32, 444])
    return b


# Faz o efeito em que o cenário também se move dando uma sensação de movimento
def paralax(screen, background, background_pos):
    screen.blit(background, background_pos[1])
    screen.blit(background, background_pos[2])
    background_pos[1][0] += 1
    background_pos[2][0] += 1
    if background_pos[1][0] == background_pos[0]:
        background_pos.pop(1)
        background_pos.append([-background_pos[0], 0])


# Código que eu pegue no stackoverflow para conseguir executar gifs, separando-os em frames
def pil_to_game(img):
    format = "RGBA"
    data = img.tobytes("raw", format)
    return pygame.image.fromstring(data, img.size, format)


def get_gif_frame(img, frame):
    format = "RGBA"
    img.seek(frame)
    return img.convert(format)


def insert_gif(screen, path, x_frame, y_frame):
    gif_img = Image.open(path)
    if "galinha" in path:
        gif_name = "galinha"
        x_scale = 55
        y_scale = 60
    elif "pinguim" in path:
        gif_name = "pinguim"
        x_scale = 49
        y_scale = 60
    elif "homem" in path:
        gif_name = "homem"
        x_scale = 54
        y_scale = 120
    elif "mulher" in path:
        gif_name = "mulher"
        x_scale = 107
        y_scale = 120
    frame = pil_to_game(get_gif_frame(gif_img, frames[gif_name]))
    frame = pygame.transform.scale(frame, (x_scale, y_scale))
    screen.blit(frame, (x_frame, y_frame))
    frames[gif_name] = (frames[gif_name] + 1) % gif_img.n_frames


# Cria um botão (Com tamanho fixo)
def button(screen, text, x_button, y_button):
    smallfont = pygame.font.SysFont('Corbel', 35)
    text = smallfont.render(text, True, (0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0), [x_button - 2, y_button - 2, 104, 44])
    pygame.draw.rect(screen, (255, 51, 51), [x_button, y_button, 100, 40])
    text_width = text.get_width()
    posX_test = 50 - math.ceil(text_width / 2)
    screen.blit(text, (x_button + posX_test, y_button + 2))


# Faz o menu
def menu(screen):
    clock = pygame.time.Clock()
    text_char = ""
    b = True
    inicio = True
    choose_character = False
    mediumfont = pygame.font.SysFont('cambria', 35)
    background = pygame.image.load("img/menu.png")
    background = pygame.transform.scale(background, (853, 480))
    background_pos = [853, [0, 0], [-853, 0]]
    m = transp_rec(screen, 500, 400, (230, 239, 255), 125)
    while b:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                b = False
                mode = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inicio:
                    if 250 < pos_mouse[0] < 350 and 250 < pos_mouse[1] < 290:
                        inicio = False
                        choose_character = True
                    if 250 < pos_mouse[0] < 350 and 310 < pos_mouse[1] < 350:
                        b = False
                elif choose_character:
                    if 100 < pos_mouse[0] < 160 and 200 < pos_mouse[1] < 260:
                        text_char = mediumfont.render('Você escolheu a galinha', True, (0, 0, 0))
                        text_char_shadow = mediumfont.render('Você escolheu a galinha', True, (153, 153, 153))
                        mode = "forest"
                        pos_char = (95, 195)
                        char_selection = transp_rec(screen, 70, 70, (255, 0, 0), 80)
                    elif 200 < pos_mouse[0] < 250 and 200 < pos_mouse[1] < 260:
                        text_char = mediumfont.render('Você escolheu o pinguim', True, (0, 0, 0))
                        text_char_shadow = mediumfont.render('Você escolheu o pinguim', True, (153, 153, 153))
                        mode = "ice"
                        pos_char = (195, 195)
                        char_selection = transp_rec(screen, 60, 70, (255, 0, 0), 80)
                    elif 310 < pos_mouse[0] < 370 and 140 < pos_mouse[1] < 260:
                        text_char = mediumfont.render('Você escolheu o homem', True, (0, 0, 0))
                        text_char_shadow = mediumfont.render('Você escolheu o homem', True, (153, 153, 153))
                        mode = "city"
                        pos_char = (305, 135)
                        char_selection = transp_rec(screen, 70, 130, (255, 0, 0), 80)
                    elif 420 < pos_mouse[0] < 510 and 140 < pos_mouse[1] < 260:
                        text_char = mediumfont.render('Você escolheu a mulher', True, (0, 0, 0))
                        text_char_shadow = mediumfont.render('Você escolheu a mulher', True, (153, 153, 153))
                        mode = "forest"
                        pos_char = (415, 135)
                        char_selection = transp_rec(screen, 110, 130, (255, 0, 0), 80)
                    if text_char:
                        if 250 < pos_mouse[0] < 350 and 370 < pos_mouse[1] < 410:
                            b = False
        paralax(screen, background, background_pos)
        screen.blit(m, (60, 50))
        if inicio:
            button(screen, "Jogar", 250, 250)
            button(screen, "Sair", 250, 310)
        elif choose_character:
            if text_char:
                screen.blit(text_char_shadow, (102, 302))
                screen.blit(text_char, (100, 300))
                button(screen, "Iniciar", 250, 370)
                screen.blit(char_selection, pos_char)
            insert_gif(screen, "animações/galinha.gif", 100, 200)
            insert_gif(screen, "animações/pinguim.gif", 200, 200)
            insert_gif(screen, "animações/homem.gif", 310, 140)
            insert_gif(screen, "animações/mulher.gif", 420, 140)
            mediumfont = pygame.font.SysFont('cambria', 35)
            text = mediumfont.render('Escolha seu persongem', True, (0, 0, 0))
            shadow = mediumfont.render('Escolha seu persongem', True, (153, 153, 153))
            screen.blit(shadow, (114, 52))
            screen.blit(text, (112, 50))
            clock.tick(10)
        pygame.display.update()
        pos_mouse = pygame.mouse.get_pos()
    return mode
