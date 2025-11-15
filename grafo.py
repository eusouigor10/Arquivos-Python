import random
import heapq
import math

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
    
    def reconstruir_caminho(self, destino, predecessores): #o objetivo da função é criar uma lista que representa o caminho percorrido
        caminho = [] 
        atual = destino #atual começa sendo o último

        while atual != None: #enquanto não chega ao fim do dicionário de predecessores
            caminho.append(atual) #coloca o vértice na lista de caminhos
            atual = predecessores[atual] #atualiza o vértice para seu predecessor
        caminho.reverse() #após completar a lista, inverte ela para ficar do primeiro ao último
        return caminho
    
    def dijkstra(self, fonte): #o objetivo da função é retornar o caminho mais curto da fonte até algum vértice da linha de destinos
        #fonte deve ser passado como uma tupla
        fonte_posicao_i, fonte_posicao_j = fonte
        inicio = self.matriz[fonte_posicao_i][fonte_posicao_j]

        #criação de dicionário de distâncias e de predecessores
        ditancias = {}
        predecessores = {}

        #inicialização (initialize-single-source)
        for i in range(self.linhas):
            for j in range(self.colunas):
                ditancias[(i, j)] = math.inf
                predecessores[(i, j)] = None

        ditancias[(fonte_posicao_i)(fonte_posicao_j)] = 0 #coloca a distância do vértice fonte como 0
        heap = [] #cria a fila de prioridades vazia, que vai considerar a distância (primeiro valor) como prioridade
        heapq.heappush(heap, (0, (fonte_posicao_i, fonte_posicao_j))) #insere na fila de prioridades uma tupla com a distância e as coordenadas da fonte

        while heap: #enquanto a fila de prioridades não estiver vazia
            distancia_atual, (i, j) = heapq.heappop(heap) #armazena na distancia_atual e na tupla de posições um elemento retirado da fila de prioridades
            v = self.matriz[i][j]

            if v.destino == True: #caso chegue na linha de destinos, já retorna
                return self.reconstruir_caminho((i, j), predecessores)
            
            for vizinho in v.lista_adj: #explora os vizinhos do vértice
                nova_posicao_i, nova_posicao_j = vizinho.linha, vizinho.coluna
                nova_distancia = distancia_atual + 1 #incrementa a distância
                #relaxamento
                if nova_distancia < ditancias[(nova_posicao_i, nova_posicao_j)]: #caso a nova distância seja menor que a distância atual, atualiza a distância e o pai
                    ditancias[(nova_posicao_i, nova_posicao_j)] = nova_distancia
                    predecessores[(nova_posicao_i, nova_posicao_j)] = (i, j)
                    heapq.heappush(heap, (nova_distancia, (nova_posicao_i, nova_posicao_j)))

        return None #retorna vazio caso não exista caminho
        
                
            
