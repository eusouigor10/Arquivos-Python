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
        self.caminho_verde = []

        self.pontos = 0
        self.fonte = pygame.font.SysFont("arial", 32, True)

        self.mensagem_temp = ""
        self.mensagem_tempo = 0

    def carregar_imagens(self):
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

    def desenhar_fundo(self):
        if self.img_fundo:
            fundo = pygame.transform.scale(
                self.img_fundo, (self.largura, self.altura))
            self.tela.blit(fundo, (0, 0))
        else:
            self.tela.fill((255, 255, 255))

    def desenhar_saida(self):
        y = 0
        h = self.CELULA_ALTURA
        if self.img_dest:
            dst = pygame.transform.scale(self.img_dest, (self.largura, h))
            self.tela.blit(dst, (0, 0))
        else:
            pygame.draw.rect(self.tela, (255, 255, 255),
                             (0, y, self.largura, h))

    def desenhar_area_inicio(self):
        y = self.inv(4) * self.CELULA_ALTURA
        h = 5 * self.CELULA_ALTURA
        s = pygame.Surface((self.largura, h), pygame.SRCALPHA)
        s.fill((150, 200, 255, 90))
        self.tela.blit(s, (0, y))

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

    def desenhar_caminho_verde(self):
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

            if self.img_carro:
                img = self.img_carro
                if h > w:
                    img = pygame.transform.rotate(img, -90)
                carro = pygame.transform.scale(img, (w, h))
                self.tela.blit(carro, (x, y))
            else:
                pygame.draw.rect(self.tela, (0, 0, 255), (x, y, w, h))

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

    def animar_movimento(self, agente):
        caminho, _, chegou = self.grafo.caminho_agente(agente)

        if not caminho:
            print("Sem caminho possível!")
            return

        for passo in caminho:
            agente.posicoes = (passo, agente.posicoes[0])
            self.atualizar_tela()
            pygame.time.delay(80)  # delay para visualização

        if agente in self.grafo.agentes:
            self.grafo.agentes.remove(agente)

        if chegou:
            self.pontos += 2
            self.mensagem_temp = "Chegou ao destino! +2 pontos"
            self.mensagem_tempo = 120

        self.grafo.resetar_obstaculos()

    def desenhar_pontuacao(self):
        txt = self.fonte.render(f"Pontos: {self.pontos}", True, (66, 245, 239))
        y_pontos = self.altura - txt.get_height() - 10

        self.tela.blit(txt, (10, y_pontos))

        if self.mensagem_temp:
            txt2 = self.fonte.render(self.mensagem_temp, True, (66, 245, 239))
            self.tela.blit(txt2, (self.largura // 2 -
                           txt2.get_width() // 2, 40))

            self.mensagem_tempo -= 1
            if self.mensagem_tempo <= 0:
                self.mensagem_temp = ""

    def atualizar_tela(self):
        self.desenhar_fundo()
        self.desenhar_saida()
        self.desenhar_area_inicio()
        self.desenhar_obstaculos()
        self.desenhar_caminho_verde()
        self.desenhar_agentes()
        self.desenhar_pontuacao()

        pygame.display.update()

    def executar(self):

        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    agente = self.detectar_clique(e.pos)

                    if agente:
                        # tenta calcular caminho
                        resultado = None
                        if not self.grafo.isPreso(agente):
                            resultado = self.grafo.caminho_agente(agente)

                        caminho = resultado[0] if resultado else None

                        # SE CLICOU NO MESMO AGENTE
                        if self.agente_selecionado == agente:

                            if caminho:
                                self.animar_movimento(agente)
                                self.caminho_verde = []
                                self.agente_selecionado = None
                            else:
                                # PERDE PONTOS
                                self.pontos -= 3
                                #self.mensagem_temp = "Carro preso! -3 pontos"
                                self.mensagem_tempo = 90

                                #print("Agente preso!")
                                self.caminho_verde = []

                        else:
                            # Seleciona o agente e mostra caminho
                            self.agente_selecionado = agente
                            if caminho:
                                self.caminho_verde = caminho
                            else:
                                self.pontos -= 3
                                self.mensagem_temp = "Carro preso! -3 pontos"
                                self.mensagem_tempo = 90

                                self.caminho_verde = []

            self.atualizar_tela()
            self.clock.tick(60)


if __name__ == "__main__":
    from grafo import Grafo

    grafo = Grafo()
    grafo.adicionar_agente_automaticamente()

    jogo = JogoVisual(grafo)
    jogo.executar()
