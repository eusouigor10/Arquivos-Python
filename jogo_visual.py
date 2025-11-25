import pygame
from pygame.locals import *
import os
import time


class JogoVisual:

    def __init__(self, grafo, largura=500, altura=650):
        pygame.init()

        self.grafo = grafo
        self.largura = largura
        self.altura = altura

        self.CELULA_LARGURA = largura // grafo.colunas
        self.CELULA_ALTURA = altura // grafo.linhas

        # Inverter matriz para o visual
        self.inv = lambda i: (self.grafo.linhas - 1) - i

        self.VERDE_CAMINHO = (0, 255, 0, 120)

        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Parking Puzzle - Visual")

        self.clock = pygame.time.Clock()

        self.carregar_imagens()

        self.agente_selecionado = None
        self.caminho_verde = []   # novo

    def carregar_imagens(self):  # Carregar imagens, se existirem na pasta do projeto
        dir = os.path.dirname(os.path.abspath(__file__))

        def load(name):
            path = os.path.join(dir, name)
            try:
                return pygame.image.load(path).convert_alpha()
            except:
                return None

        self.img_fundo = load("rodovia.png")
        self.img_cone = load("CONE.png")
        self.img_dest = load("destino.png")
        self.img_carro = load("agente.png")

    def desenhar_fundo(self):  # Desenhar fundo ou preencher branco, se não houver imagem
        if self.img_fundo:
            fundo = pygame.transform.scale(
                self.img_fundo, (self.largura, self.altura))
            self.tela.blit(fundo, (0, 0))
        else:
            self.tela.fill((255, 255, 255))

    # Desenhar área de saída ou preencher branco, se não houver imagem
    def desenhar_saida(self):
        y = 0
        h = self.CELULA_ALTURA

        if self.img_dest:
            dst = pygame.transform.scale(self.img_dest, (self.largura, h))
            self.tela.blit(dst, (0, 0))
        else:
            pygame.draw.rect(self.tela, (255, 255, 255),
                             (0, y, self.largura, h))

    # Desenhar área de início (transparente azul claro)
    def desenhar_area_inicio(self):
        y = self.inv(4) * self.CELULA_ALTURA
        h = 5 * self.CELULA_ALTURA

        s = pygame.Surface((self.largura, h), pygame.SRCALPHA)
        s.fill((150, 200, 255, 90))
        self.tela.blit(s, (0, y))

    # Desenhar obstáculos (cones) ou preencher vermelho, se não houver imagem
    def desenhar_obstaculos(self):
        for i in range(self.grafo.linhas):
            for j in range(self.grafo.colunas):

                v = self.grafo.matriz[i][j]
                if v.obstaculo:

                    iv = self.inv(i)
                    x = j * self.CELULA_LARGURA
                    y = iv * self.CELULA_ALTURA

                    if self.img_cone:
                        cone = pygame.transform.scale(self.img_cone,
                                                      (self.CELULA_LARGURA, self.CELULA_ALTURA))
                        self.tela.blit(cone, (x, y))
                    else:
                        pygame.draw.rect(self.tela, (200, 0, 0),
                                         (x, y, self.CELULA_LARGURA, self.CELULA_ALTURA))

    def desenhar_caminho_verde(self):  # Desenhar caminho em verde transparente
        if not self.caminho_verde:
            return

        for (i, j) in self.caminho_verde:
            iv = self.inv(i)
            x = j * self.CELULA_LARGURA
            y = iv * self.CELULA_ALTURA

            s = pygame.Surface(
                (self.CELULA_LARGURA, self.CELULA_ALTURA), pygame.SRCALPHA)
            s.fill(self.VERDE_CAMINHO)
            self.tela.blit(s, (x, y))

    # Desenhar agentes (carros) ou preencher azul, se não houver imagem
    def desenhar_agentes(self):
        for agente in self.grafo.agentes:

            (i1, j1), (i2, j2) = agente.posicoes

            iv1 = self.inv(i1)
            iv2 = self.inv(i2)

            min_i = min(iv1, iv2)
            max_i = max(iv1, iv2)
            min_j = min(j1, j2)
            max_j = max(j1, j2)

            x = min_j * self.CELULA_LARGURA
            y = min_i * self.CELULA_ALTURA
            w = (max_j - min_j + 1) * self.CELULA_LARGURA
            h = (max_i - min_i + 1) * self.CELULA_ALTURA

            if self.img_carro:  # Desenhar carro com imagem, rotacionando se necessário
                img = self.img_carro
                if h > w:
                    img = pygame.transform.rotate(img, -90)

                carro = pygame.transform.scale(img, (w, h))
                self.tela.blit(carro, (x, y))

            else:
                pygame.draw.rect(self.tela, (0, 0, 255), (x, y, w, h))

    # Detectar clique em um agente, retornando o agente clicado
    def detectar_clique(self, pos):
        mx, my = pos

        for agente in self.grafo.agentes:
            (i1, j1), (i2, j2) = agente.posicoes

            iv1 = self.inv(i1)
            iv2 = self.inv(i2)

            min_i = min(iv1, iv2)
            max_i = max(iv1, iv2)
            min_j = min(j1, j2)
            max_j = max(j1, j2)

            x = min_j * self.CELULA_LARGURA
            y = min_i * self.CELULA_ALTURA
            w = (max_j - min_j + 1) * self.CELULA_LARGURA
            h = (max_i - min_i + 1) * self.CELULA_ALTURA

            rect = pygame.Rect(x, y, w, h)

            if rect.collidepoint((mx, my)):
                return agente

        return None

    # Animar movimento do agente ao longo do caminho encontrado
    def animar_movimento(self, agente):
        caminho, _, _ = self.grafo.caminho_agente(agente)

        if not caminho:
            print("Sem caminho possível!")
            return

        for passo in caminho:

            agente.posicoes = (passo, agente.posicoes[0])

            self.atualizar_tela()
            pygame.time.delay(120)

        if agente in self.grafo.agentes:
            self.grafo.agentes.remove(agente)

    def atualizar_tela(self):  # Atualizar tela desenhando todos os elementos
        self.desenhar_fundo()
        self.desenhar_saida()
        self.desenhar_area_inicio()
        self.desenhar_obstaculos()
        self.desenhar_caminho_verde()
        self.desenhar_agentes()

        pygame.display.update()

    def executar(self):  # Loop principal do jogo, tratando eventos e atualizando a tela

        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

                # ...
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                agente = self.detectar_clique(e.pos)

                if agente:
                    # 1. Tenta calcular o caminho para o agente clicado
                    resultado = None
                    if not self.grafo.isPreso(agente):
                        resultado = self.grafo.caminho_agente(agente)

                    caminho = resultado[0] if resultado is not None else None

                    # 2. Lógica de clique
                    if self.agente_selecionado == agente:

                        if caminho:  # Se houver caminho calculado anteriormente
                            self.animar_movimento(agente)  # Passa o caminho
                            self.caminho_verde = []
                            self.agente_selecionado = None
                        else:
                            print("Agente preso ou sem caminho possível!")
                            self.caminho_verde = []
                    else:
                        # Seleciona o agente e mostra o caminho (se houver)
                        self.agente_selecionado = agente
                        if caminho:
                            self.caminho_verde = caminho
                        else:
                            self.caminho_verde = []
                            print("Agente preso ou sem caminho possível!")
                            # Não precisa do 'return' aqui, a tela será atualizada
# ...

            self.atualizar_tela()
            self.clock.tick(60)


if __name__ == "__main__":  # Executa o jogo visual se o arquivo for executado diretamente
    from grafo import Grafo

    grafo = Grafo()
    grafo.adicionar_agente_automaticamente()

    jogo = JogoVisual(grafo)
    jogo.executar()
