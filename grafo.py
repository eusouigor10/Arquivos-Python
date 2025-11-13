import random

class Vertice:
    def __init__(self):
        self.lista_adj = []
        self.distancia = 0
        self.obstaculo = False
        self.destino = False
        self.linha = None
        self.coluna = None


class Agente:
    def __init__(self, grafo, posicao_1, posicao_2, direcao):
        self.grafo = grafo
        self.posicoes = (posicao_1, posicao_2)
        self.direcao = direcao

class Grafo:

    def __init__(self, linhas=20,colunas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []
        self.agentes = []
        self.cria_matriz()
        self.criacao_obstaculos()
        self.destinos()
        self.preenchimento_matriz()
        self.direcoes = ['esq', 'dir']
        self.lista_linhas_agentes = [0, 1, 2, 3, 4]
        self.lista_colunas_agentes = [0, 1, 2, 3, 4,5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    #criação da matriz
    def cria_matriz(self):
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                v = Vertice()
                v.linha = i
                v.coluna = j
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
                if v.obstaculo != True: #se não for obstáculo, verifica os limites da matriz e adiciona na lista de adj.
                    if i - 1 >= 0 and self.matriz[i - 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i - 1][j])
                    if j - 1 >= 0 and self.matriz[i][j - 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j - 1])
                    if i + 1 < self.linhas and self.matriz[i + 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i + 1][j])
                    if j + 1 < self.colunas and self.matriz[i][j + 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j + 1])
    
    def adicionar_agente(self, i1, j1, i2, j2):
        #verifica área da matriz
        if i1 >= 0 and i1 <= 4 and i2 >= 0 and i2 <= 4:
            if j1 >= 0 and j1 <= 9 and j2 >= 0 and j2 <= 9:
                #verifica adjacência das duas posições que compõem o agente
                if self.matriz[i1][j1] in self.matriz[i2][j2].lista_adj:
                    #verifica se tem por onde andar
                    if not self.isPreso(i1, j1, i2, j2):
                        ocupado = False #verifica sobreposição
                        for agente in self.agentes:
                            if (i1, j1) in agente.posicoes or (i2, j2) in agente.posicoes:
                                ocupado = True
                                break
                        if not ocupado: #caso não haja sobreposição
                            if i2 > i1: #caso esteja na vertical
                                direcao = 'cima'
                            else: #caso esteja na horizontal
                                direcao = random.choice(self.direcoes)
                                self.agentes.append(Agente(self, (i1, j1), (i2, j2), direcao))
                                return True
        return False
                        
    def adicionar_agente_automaticamente(self):
        cont_sucesso = 0 #contador de vizinhos adicionados
        cont_iteracoes = 0
        while cont_sucesso < 20 and cont_iteracoes < 1000: #20 é o número máximo de agentes possível
            i1 = random.choice(self.lista_linhas_agentes) #escolhe uma posição aleatória dentro da área
            j1 = random.choice(self.lista_colunas_agentes)#de agentes
            possiveis_vizinhos = []
            if i1 - 1 >= 0:
                possiveis_vizinhos.append((i1 - 1, j1)) #verifica os limites da matriz e adiciona 
            if i1 + 1 <= 4:                             #a tupla de possíveis vizinhos
                possiveis_vizinhos.append((i1 + 1, j1))
            if j1 - 1 >= 0:
                possiveis_vizinhos.append((i1, j1 - 1))
            if j1 + 1 <= 9:
                possiveis_vizinhos.append((i1, j1 + 1))
            posicao_escolhida = (random.choice(possiveis_vizinhos)) #escolhe um vizinho aletório
            i2, j2 = posicao_escolhida                              #e adiciona 
            cont_iteracoes += 1
            if self.adicionar_agente(i1, j1, i2, j2) == True:
                cont_sucesso += 1
    
    def isPreso(self, i1, j1, i2, j2):
        v1 = self.matriz[i1][j1]
        v2 = self.matriz[i2][j2]
        
        adjacentes = v1.lista_adj + v2.lista_adj #soma as adjacências
        ocupado = False

        for adjacente in adjacentes: #verifica se algum adjacente tem a mesma posição de algum agente 
            ocupado = False
            for agente in self.agentes:
                if (adjacente.linha, adjacente.coluna) in agente.posicoes:
                    ocupado = True
                    break
            if ocupado == False:
                return False #se se manteve desocupado, há espaço para andar
        
        return True
        
                
            
