import pygame
from pygame.locals import *
from sys import exit

pygame.init()

#configurações da tela
largura = 1000
altura = 600
x = 0
y = 0
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('TRABALHO GRAFOS')
clock = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 50, False, False)
pontos = 0

#loop infinito do jogo
while True:
    clock.tick(10) #frames por segundo do jogo
    #preenchimento da tela para apagar o resto dos objetos que se moveram
    tela.fill((0,0,0))
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (255,255,255))
    #loop de iterações para cada evento que ocorrer
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                x = x - 5
            if event.key == K_d:
                x = x + 5
            if event.key == K_s:
                y = y + 5
            if event.key == K_w: 
                y = y - 5

    if pygame.key.get_pressed()[K_a]:
        x = x - 5 
    if pygame.key.get_pressed()[K_d]:
        x = x + 5 
    if pygame.key.get_pressed()[K_s]:
        y = y + 5 
    if pygame.key.get_pressed()[K_w]:
        y = y - 5         
    
    ret_vermelho = pygame.draw.rect(tela, (255,0,0), (100,100,100,100))
    ret_verde = pygame.draw.rect(tela, (0,255,0), (x,y,100,100))

    if ret_vermelho.colliderect(ret_verde):
        pontos = pontos + 1
    
    tela.blit(texto_formatado, (450, 40))

    #verificação para ver se o retângulo sumiu da tela
    '''if y >= altura:
    #    y = 0
    #y = y + 1 #incremento da posição do retângulo
    atualização da tela'''
    pygame.display.update()
