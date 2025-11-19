import pygame
from pygame.locals import *
from sys import exit
import os
from grafo import Grafo

pygame.init()

largura = 500
altura = 650

# Cores
PRETO = (0, 0, 0)
CINZA_ESCURO = (50, 50, 50)
VERMELHO_ESCURO = (139, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 150, 0)

grafo_jogo = Grafo()

linhas_matriz = grafo_jogo.linhas    # 20
colunas_matriz = grafo_jogo.colunas  # 10

CELULA_LARGURA = largura // colunas_matriz  # 500 // 10 = 50
CELULA_ALTURA_INT = altura // linhas_matriz    # 650 // 20 = 32

# criamos a tela do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo Visual')

diretorio_do_script = os.path.dirname(os.path.abspath(__file__))

# criando a variavel imagemFundo para carregar a imagem de fundo
imagemFundo = 'rodovia.png'
caminho_completo_imagem_fundo = os.path.join(diretorio_do_script, imagemFundo)
fundo = None
try:
    fundo = pygame.image.load(caminho_completo_imagem_fundo).convert()
    fundo = pygame.transform.scale(fundo, (largura, altura))
except pygame.error as e:
    fundo = None

# criando a variavel imagem_cone para carregar a imagem do cone
imagem_cone = 'CONE.png'
caminho_completo_imagem_cone = os.path.join(diretorio_do_script, imagem_cone)
cone_img = None
try:
    cone_img_original = pygame.image.load(
        caminho_completo_imagem_cone).convert_alpha()
    cone_img = pygame.transform.scale(
        cone_img_original, (CELULA_LARGURA, CELULA_ALTURA_INT))
except pygame.error as e:
    cone_img = None

imagemDestino = 'destino.png'
caminho_completo_imagem_destino = os.path.join(
    diretorio_do_script, imagemDestino)
destino_img = None
try:
    destino_img_original = pygame.image.load(
        caminho_completo_imagem_destino).convert_alpha()
    destino_img = pygame.transform.scale(
        destino_img_original, (largura, CELULA_ALTURA_INT))
except pygame.error as e:
    destino_img = None


def desenha_obstaculos(tela, grafo, cone_img):
    OFFSET_DESENHO = 5

    for i in range(grafo.linhas):
        for j in range(grafo.colunas):
            vertice = grafo.matriz[i][j]

            if vertice.obstaculo:
                i_deslocada = i - OFFSET_DESENHO

                # Desenha apenas se a linha deslocada for visível e não for a linha 0
                if 0 < i_deslocada < grafo.linhas:

                    x = j * CELULA_LARGURA
                    y = i_deslocada * CELULA_ALTURA_INT

                    if cone_img:
                        tela.blit(cone_img, (x, y))
                    else:
                        cor_obstaculo = VERMELHO_ESCURO
                        w = CELULA_LARGURA
                        h = CELULA_ALTURA_INT
                        pygame.draw.rect(tela, cor_obstaculo, (x, y, w, h))


def desenha_destino(tela, grafo):
    i_destino = grafo.linhas - 20
    y = i_destino * CELULA_ALTURA_INT

    if destino_img:
        tela.blit(destino_img, (0, y))
    else:
        cor_destino = BRANCO
        w = largura
        h = CELULA_ALTURA_INT
        pygame.draw.rect(tela, cor_destino, (0, y, w, h))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(BRANCO)

    desenha_destino(tela, grafo_jogo)

    desenha_obstaculos(tela, grafo_jogo, cone_img)

    pygame.display.update()
