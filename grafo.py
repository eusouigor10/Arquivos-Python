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
        self.caminho = None


class Grafo:

    def __init__(self, linhas=20, colunas=10):
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
        self.lista_colunas_agentes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # criação da matriz
    def cria_matriz(self):
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                v = Vertice()
                v.linha = i
                v.coluna = j
                linha.append(v)
            self.matriz.append(linha)

    # criação dos obstáculos
    def criacao_obstaculos(self):
        vetor = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(6, 20):
            if i % 2 == 0:  # apenas em linhas pares
                sorteados = random.sample(vetor, 2)
                for j in range(10):
                    if j != sorteados[0] and j != sorteados[1]:
                        v = self.matriz[i][j]
                        v.obstaculo = True

    # definição da linha de destinos
    def destinos(self):
        for j in range(10):
            self.matriz[19][j].destino = True

    # preenchimento das listas de adjacências
    def preenchimento_matriz(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                v = self.matriz[i][j]
                # se não for obstáculo, verifica os limites da matriz e adiciona na lista de adj.
                if v.obstaculo != True:
                    if i - 1 >= 0 and self.matriz[i - 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i - 1][j])
                    if j - 1 >= 0 and self.matriz[i][j - 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j - 1])
                    if i + 1 < self.linhas and self.matriz[i + 1][j].obstaculo == False:
                        v.lista_adj.append(self.matriz[i + 1][j])
                    if j + 1 < self.colunas and self.matriz[i][j + 1].obstaculo == False:
                        v.lista_adj.append(self.matriz[i][j + 1])

    def adicionar_agente(self, i1, j1, i2, j2):
        agente_a_ser_adicionado = Agente(self, (i1, j1), (i2, j2), None)
        # verifica área da matriz
        if i1 >= 0 and i1 <= 4 and i2 >= 0 and i2 <= 4:
            if j1 >= 0 and j1 <= 9 and j2 >= 0 and j2 <= 9:
                # verifica adjacência das duas posições que compõem o agente
                if self.matriz[i1][j1] in self.matriz[i2][j2].lista_adj:
                    # verifica se tem por onde andar
                    if not self.isPreso(agente_a_ser_adicionado):
                        ocupado = False  # verifica sobreposição
                        for agente in self.agentes:
                            if (i1, j1) in agente.posicoes or (i2, j2) in agente.posicoes:
                                ocupado = True
                                break
                        if not ocupado:  # caso não haja sobreposição
                            if i2 > i1:  # caso esteja na vertical
                                direcao = 'cima'
                            else:  # caso esteja na horizontal
                                direcao = random.choice(self.direcoes)
                            self.agentes.append(
                                Agente(self, (i1, j1), (i2, j2), direcao))
                            return True
        return False

    def adicionar_agente_automaticamente(self):
        cont_sucesso = 0  # contador de vizinhos adicionados
        cont_iteracoes = 0
        while cont_sucesso <= 40 and cont_iteracoes < 1000:  # 20 é o número máximo de agentes possível
            # escolhe uma posição aleatória dentro da área
            i1 = random.choice(self.lista_linhas_agentes)
            j1 = random.choice(self.lista_colunas_agentes)  # de agentes
            possiveis_vizinhos = []
            if i1 - 1 >= 0:
                # verifica os limites da matriz e adiciona
                possiveis_vizinhos.append((i1 - 1, j1))
            if i1 + 1 <= 4:  # a tupla de possíveis vizinhos
                possiveis_vizinhos.append((i1 + 1, j1))
            if j1 - 1 >= 0:
                possiveis_vizinhos.append((i1, j1 - 1))
            if j1 + 1 <= 9:
                possiveis_vizinhos.append((i1, j1 + 1))
            # escolhe um vizinho aletório
            posicao_escolhida = (random.choice(possiveis_vizinhos))
            i2, j2 = posicao_escolhida  # e adiciona
            cont_iteracoes += 1
            if self.adicionar_agente(i1, j1, i2, j2) == True:
                cont_sucesso += 1

    def isPreso(self, agente):
        frente, tras = agente.posicoes
        i1, j1 = frente
        i2, j2 = tras

        v1 = self.matriz[i1][j1]
        v2 = self.matriz[i2][j2]

        adjacentes = v1.lista_adj + v2.lista_adj

        for adj in adjacentes:
            pos = (adj.linha, adj.coluna)

            # não pode se mover para uma posição ocupada por qualquer outro agente
            ocupado = False
            for outro in self.agentes:
                if outro is agente:
                    continue
                if pos in outro.posicoes:
                    ocupado = True
                    break

            if not ocupado:
                return False  # achou um caminho disponível

        return True  # todos adjacentes bloqueados

    # o objetivo da função é criar uma lista que representa o caminho percorrido
    def reconstruir_caminho(self, destino, predecessores):
        caminho = []
        atual = destino  # atual começa sendo o último

        while atual != None:  # enquanto não chega ao fim do dicionário de predecessores
            caminho.append(atual)  # coloca o vértice na lista de caminhos
            # atualiza o vértice para seu predecessor
            atual = predecessores[atual]
        caminho.reverse()  # após completar a lista, inverte ela para ficar do primeiro ao último
        return caminho

    def dijkstra(self, fonte, agente_atual=None):
        fonte_posicao_i, fonte_posicao_j = fonte

        distancias = {}
        predecessores = {}

        # inicialização
        for i in range(self.linhas):
            for j in range(self.colunas):
                distancias[(i, j)] = math.inf
                predecessores[(i, j)] = None

        distancias[(fonte_posicao_i, fonte_posicao_j)] = 0
        heap = []
        heapq.heappush(heap, (0, (fonte_posicao_i, fonte_posicao_j)))

        while heap:
            distancia_atual, (i, j) = heapq.heappop(heap)

            if distancia_atual > distancias[(i, j)]:
                continue

            v = self.matriz[i][j]

            # Se chegou ao destino, termina
            if v.destino:
                return self.reconstruir_caminho((i, j), predecessores)

            for vizinho in v.lista_adj:
                nova_posicao_i = vizinho.linha
                nova_posicao_j = vizinho.coluna
                pos = (nova_posicao_i, nova_posicao_j)

                # tratar outros agentes como obstáculos
                ocupado = False
                for outro in self.agentes:
                    if outro is agente_atual:
                        continue  # o próprio agente não conta como obstáculo
                    if pos in outro.posicoes:
                        ocupado = True
                        break

                if ocupado:
                    continue  # ignora essa célula como se fosse obstáculo

                nova_distancia = distancia_atual + 1

                # Relaxamento
                if nova_distancia < distancias[(nova_posicao_i, nova_posicao_j)]:
                    distancias[(nova_posicao_i, nova_posicao_j)
                               ] = nova_distancia
                    predecessores[(nova_posicao_i, nova_posicao_j)] = (i, j)
                    heapq.heappush(
                        heap, (nova_distancia, (nova_posicao_i, nova_posicao_j)))

        return None

    # essa função retorna o caminho mais curto entre os dois das duas posições do agente
    def caminho_agente(self, agente):
        p1 = agente.posicoes[0]
        p2 = agente.posicoes[1]
        caminho1 = self.dijkstra(p1, agente_atual=agente)
        caminho2 = self.dijkstra(p2, agente_atual=agente)
        if caminho1 == None:
            return caminho2
        if caminho2 == None:
            return caminho1

        if len(caminho1) <= len(caminho2):
            return caminho1, p1, p2
        else:
            return caminho2, p2, p1

    def movimentacao_agente(self, agente):

        # se ainda não tem caminho calculado (primeira interação de cada agente), calcula uma vez
        if agente.caminho is None or len(agente.caminho) <= 1:
            caminho, posicao_frente, posicao_tras = self.caminho_agente(agente)
            agente.caminho = caminho

        caminho = agente.caminho

        # se o caminho acabou
        if len(caminho) <= 1 or caminho is None:
            return False

        # remove posição atual (frente) e segue para a próxima
        caminho.pop(0)

        nova_frente = caminho[0]
        nova_tras = agente.posicoes[0]

        # atualiza as posições do agente (sensação de movimento)
        agente.posicoes = (nova_frente, nova_tras)

        # depois de mover este agente, atualizar caminhos dos outros
        for outro in self.agentes:
            if outro is not agente:
                outro.caminho = None

        return True
