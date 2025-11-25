# Descrição da Jogabilidade do Jogo

A jogabilidade foi definida das seguintes maneiras:

- Objetivo do jogo: chegar com todos os carros até a linha de chegada, evitando selecionar algum carro preso. A cada carro que chega ao final, pontos são somados e, a cada carro preso selecionado, pontos são perdidos;
- Obstáculos são adicionados de maneira aleatória seguindo o padrão de uma linha com obstáculos e uma linha sem, desde o fim da área de início até a linha de chegada, com 2 posições livres sorteadas por linha de obstáculos a cada inicialização do jogo;
- As adjacências de cada vértice são dadas pelos vértices à esquerda, à direita, acima e abaixo;
- Os agentes são adicionados na inicialização do jogo na área destinada a eles, na parte inferior do tabuleiro do jogo. Essa adição ocorre de forma aleatória, considerando um número consideravelmente grande de possíveis agentes;
- Os agentes presos são aqueles que não possuem possibilidade de movimentação e nem seus adjacentes permitem que o mesmo se movimente;
- Os agentes se movimentam até a linha de chegada sempre considerando o menor caminho possível calculado pelo algoritmo de Dijkstra;
- A cada movimentação de um agente, as rotas dos outros agentes são recalculadas para sempre procurar o menor caminho;
- As bibliotecas importadas foram a do Pygame para a criação do jogo visual, a biblioteca Math para a constante infinita utilizada no algoritmo de Dijkstra e também a biblioteca que permite o uso da fila de prioridades, também utilizada em Dijkstra.
