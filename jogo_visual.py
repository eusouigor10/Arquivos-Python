import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 500
altura = 650

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo Visual')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    tela.fill((0, 0, 0))
    pygame.display.update()
