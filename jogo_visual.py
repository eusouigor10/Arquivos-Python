import pygame
from pygame.locals import *
from sys import exit
import os

pygame.init()

largura = 500
altura = 650

#criamos a tela do jogo
tela = pygame.display.set_mode((largura, altura)) 
pygame.display.set_caption('Jogo Visual') 

#carregamento da imagem de fundo
diretorio_do_script = os.path.dirname(os.path.abspath(__file__)) 

imagemFundo = 'CAMPO.png' #aqui eu defini o nome da imagem pra eu poder usar depois

caminho_completo_imagem = os.path.join(diretorio_do_script, imagemFundo) 

fundo = None 
try:
    fundo = pygame.image.load(caminho_completo_imagem).convert() 
    if fundo.get_size() != (largura, altura): 
        fundo = pygame.transform.scale(fundo, (largura, altura)) 

except pygame.error as e:
    print(
        f"ERRO: Não foi possível carregar a imagem de fundo em: {caminho_completo_imagem}")
    print(
        f"Verifique se o arquivo '{imagemFundo}' está na mesma pasta do script.")
    fundo = None

while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit()
            exit()

    if fundo: 
        tela.blit(fundo, (0, 0)) 
    else: 
        tela.fill((0, 0, 0)) 

    pygame.display.update() 
