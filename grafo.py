import random

class Vertice:
    def __init__(self):
        self.lista_adj = []
        self.distancia = 0
        self.obstaculo = False
        self.destino = False

class Grafo:

    def __init__(self, linhas=20,colunas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []
        self.cria_matriz()

    #criação da matriz
    def cria_matriz(self):
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                v = Vertice()
                linha.append(v)
            self.matriz.append(linha)

    #criação dos obstáculos
    def criacao_obstaculos(self):
        vetor = [0,1,2,3,4,5,6,7,8,9]
        for i in range(6,20):
            if i % 2 == 0: #apenas em linhas pares
                sorteados = random.sample(vetor, 2)
                for j in range(10):
                    if j != sorteados[0] and j != sorteados[1]:
                        v = self.matriz[i][j]
                        v.obstaculo = True
    
    #definição da linha de destinos
    def destinos(self):
        for j in range(10):
            self.matriz[19][j].destino = True
    
    #preenchimento das listas de adjacências
    def preenchimento_matriz(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                v = self.matriz[i][j]
                if v.obstaculo != True:
                    if i - 1 >= 0 and self.matriz[i - 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i - 1][j])
                    if j - 1 >= 0 and self.matriz[i][j - 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j - 1])
                    if i + 1 < self.linhas and self.matriz[i + 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i + 1][j])
                    if j + 1 < self.colunas and self.matriz[i][j + 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j + 1])