import pygame

try:
    pygame.init()
except:
    print("O pygame não funfou")
    
largura = 640
comprimento = 480

pygame.display.set_mode((largura, comprimento))
pygame.display.set_caption("Game")

n_sair = True

while n_sair:
    for event in pygame.event.get( ):
        print(event) #mostra tudo que está acontecendo na tela no promt (XXX)
        if event.type == pygame.QUIT:
            #Colocar Pergunta "Deseja sair?"
            n_sair = False
    pygame.display.update()

pygame.quit()
