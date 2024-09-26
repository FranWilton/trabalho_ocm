import numpy as np
import time
from itertools import combinations, product, permutations
import cProfile
import os
import heapq
import random
from collections import deque
import math

import random
from itertools import combinations


class BinPackingData:
    """
    Classe para representar os dados do problema do bin packing.
    """
    def __init__(self, file_path, probl):
        self.file_path = file_path
        self.capacidade = 0          # Capacidade do bin
        self.num_itens = 0           # Número de itens
        self.num_caixas = 0          # Número de bins na solução melhor conhecida atual
        self.pesos = []              # valores referentes a cada item
        self.probl = probl          # Problema a ser resolvido
        self.linha_encontrados = 0  # Número da linha com o início do problema

    def leitura(self):
        """
        Identifica e define os atributos da classe a partir do arquivo.
        """
        with open(self.file_path, 'r') as file:
            linhas = file.readlines()

            for i, linha in enumerate(linhas):
                if f"u120_{self.probl}" in linha.strip():
                    self.linha_encontrados = i
                    break

            self.capacidade, self.num_itens, self.num_caixas = map(
                int, linhas[self.linha_encontrados + 1].strip().split())

            for i in range(self.linha_encontrados + 2, self.linha_encontrados + 2 + self.num_itens):
                self.pesos.append(int(linhas[i].strip()))


class Metodos(BinPackingData):
    def __init__(self, plbm):
        super().__init__(plbm.file_path, plbm.probl)
        self.num_itens = plbm.num_itens
        self.capacidade = plbm.capacidade
        self.pesos = plbm.pesos
        self.bin_ale = []
        self.bin_gls = []


    def distribuir_itens(self, itens, capacidade_bin):
        """
        Distribui os itens em bins com capacidade máxima.
        """

        bins = []

        bins = []

        for item in itens:
            colocado = False

            for bin_atual in bins:
                if sum(bin_atual) + item <= capacidade_bin:
                    bin_atual.append(item)
                    colocado = True
                    break
            if not colocado:
                bins.append([item])

        return bins



    def little_inst(self, itens, capacidade_bin):
        """
        Executa permutação nos objetos e escolhe a melhor solução em um número menor de itens.
        """
        melhor_solucao = []
        menor_num_bins = float('inf')

        for permutacao in permutations(itens):
            bins_atual = self.distribuir_itens(permutacao, capacidade_bin)
            num_bins = len(bins_atual)

            if num_bins < menor_num_bins:
                menor_num_bins = num_bins
                melhor_solucao = bins_atual

        return melhor_solucao



    def cont_ale(self):
        """
        Constrói uma solução inicial aleatória, com base no embaralhamento dos itens.
        """
        pesos_ale = self.pesos[:]
        random.shuffle(pesos_ale)
        bin_ale = []
        sublista_atual = []

        for num in pesos_ale:
            if sum(sublista_atual) + num > self.capacidade:
                if sublista_atual:  # Adiciona a sublista atual somente se não estiver vazia
                    bin_ale.append(sublista_atual)
                sublista_atual = [num]  # Inicia uma nova sublista com o item atual
            else:
                sublista_atual.append(num)

        if sublista_atual:  
            bin_ale.append(sublista_atual)

        # Remove bins vazios, se houver
        bin_ale = [bin for bin in bin_ale if bin]

        return bin_ale


    def cons_guloso(self):
        """
        Constrói uma solução inicial usando um método guloso, ordenando os itens
        em ordem crescente e alocando os itens dentro dos bins.
        """
        vetor_ordem = sorted(self.pesos)

        bin_gls = []
        bin_atual = []

        for num in vetor_ordem:
            if sum(bin_atual) + num > self.capacidade:
                bin_gls.append(bin_atual)
                bin_atual = [num]
            else:
                bin_atual.append(num)

        if bin_atual:
            bin_gls.append(bin_atual)

        return bin_gls

    def cons_guloso_dec(self):
        """
        Constrói uma solução inicial usando um método guloso em ordem decrescente.
        """
        vetor_ordem = sorted(self.pesos, reverse=True)
        bin_gls = []

        for num in vetor_ordem:
            alocado = False
            for bin in bin_gls:
                if sum(bin) + num <= self.capacidade:
                    bin.append(num)
                    alocado = True
                    break
            if not alocado:
                bin_gls.append([num])

        return bin_gls

    def busca_local(self, solucao_inicial):
        """
        Busca local para melhorar a solução, buscando em cada item de todos os bins 
        alocar em outro bin sem ultrapassar a capacidade.
        """
        melhor_solucao = solucao_inicial[:]
        melhor_num_bins = len(melhor_solucao)

        for _ in range(100):
            for idx_bin_origem, bin_origem in enumerate(melhor_solucao):
                for idx_item, item in enumerate(bin_origem):
                    for idx_bin_destino, bin_destino in enumerate(melhor_solucao):
                        if idx_bin_origem != idx_bin_destino and sum(bin_destino) + item <= self.capacidade:
                            bin_origem.remove(item)
                            bin_destino.append(item)

                            if not bin_origem:
                                melhor_solucao.remove(bin_origem)

                            break

            novo_num_bins = len(melhor_solucao)
            if novo_num_bins < melhor_num_bins:
                melhor_num_bins = novo_num_bins
            else:
                break

        return melhor_solucao

    def vnd(self, sol_inicial):
      """
      Busca trocar elementos entre os bins, sobre o critério de a soma dos 
      quadrados dos pesos dos itens seja maior.
      """
      
      vetores = sol_inicial.copy()
      capacidade = self.capacidade

      for i in range(0, len(vetores), 2):
            
          if i + 1 < len(vetores):
            """
            Verifique se existe um vetor no índice i + 1
            """
                
            copy_a = vetores[i].copy()
            copy_b = vetores[i + 1].copy()

            min_a = min(vetores[i])
            min_b = min(vetores[i + 1])

            copy_a.remove(min_a)
            copy_b.remove(min_b)

            copy_a.append(min_b)
            copy_b.append(min_a)

            if sum(copy_a) <= capacidade and sum(copy_b) <= capacidade:
                 soma_01 = sum([x**2 for x in vetores[i]])
                 soma_02 = sum([x**2 for x in vetores[i + 1]])
                 soma_03 = sum([x**2 for x in copy_a])
                 soma_04 = sum([x**2 for x in copy_b])

                 if soma_01 + soma_02 < soma_03 + soma_04:
                     vetores[i] = copy_a
                     vetores[i + 1] = copy_b

      return vetores

    def random_multistart(self, iteracoes=100):
        """
        Esta função executa o método Random Multi-Start, 
        gerando várias soluções iniciais aleatórias, otimizando cada uma 
        com uma busca local e selecionando a melhor solução global
        """
        melhor_solucao_global = None

        for i in range(iteracoes):
            solucao_inicial = self.cont_ale()

            solucao_otimizada = self.busca_local(solucao_inicial)

            if melhor_solucao_global is None or len(solucao_otimizada) < len(melhor_solucao_global):
                melhor_solucao_global = solucao_otimizada

        return melhor_solucao_global

    def iterated_local_search(self, iteracoes=100):
      """
      Gera uma solução inicial aleatória, otimiza-a com busca local, e, 
      em cada iteração, aplica uma perturbação à melhor solução atual. 
      Após perturbar, aplica novamente a busca local e atualiza a melhor 
      solução se a nova for superior.
      """
      solucao_inicial = self.cont_ale()
      melhor_solucao_global = self.busca_local(solucao_inicial)

      for _ in range(iteracoes):
          solucao_perturbada = self.perturbar(melhor_solucao_global)
          solucao_otimizada = self.busca_local(solucao_perturbada)

          if len(solucao_otimizada) < len(melhor_solucao_global):
              melhor_solucao_global = solucao_otimizada

      return melhor_solucao_global

    def perturbar(self, solucao):
        """
        Perturba a solução existente. A perturbação pode ser feita movendo um item
        de um bin para outro, garantindo que o bin de destino tenha capacidade suficiente.
        """
        if len(solucao) <= 1:
            return solucao  # Sem perturbação possível

        # Escolhe aleatoriamente um bin e um item dentro dele
        bin_index = random.randint(0, len(solucao) - 1)
        
        if len(solucao[bin_index]) == 0:
            return solucao 

        item_index = random.randint(0, len(solucao[bin_index]) - 1)
        item = solucao[bin_index][item_index]

        capacidade = self.capacidade

        # Tenta encontrar um novo bin que tenha espaço para o item, com um limite de tentativas
        for _ in range(len(solucao)): 
            novo_bin_index = random.randint(0, len(solucao) - 1)
            
            if novo_bin_index != bin_index and (sum(solucao[novo_bin_index]) + item <= capacidade):
                solucao[bin_index].remove(item)
                solucao[novo_bin_index].append(item)
                return solucao  

        # Se não encontrou um bin válido, retorna a solução original
        return solucao




    def variable_neighborhood_search(self, iteracoes=100):
        """
        O algoritmo perturba a solução atual, aplica busca local e alterna entre vizinhanças 
        para encontrar a melhor solução possível.
        """

        solucao_inicial = self.cont_ale()
        melhor_solucao_global = self.busca_local(solucao_inicial)

        # Define as vizinhanças
        vizinhancas = [self.vizinhanca_1, self.vizinhanca_2] 
        k = 0  # Índice da vizinhança

        for _ in range(iteracoes):
            # Perturba a solução atual
            solucao_perturbada = self.perturbar(melhor_solucao_global)

            solucao_otimizada = self.busca_local(solucao_perturbada)

            if len(solucao_otimizada) < len(melhor_solucao_global):
                melhor_solucao_global = solucao_otimizada
                k = 0  # Reinicia a vizinhança se encontrar uma nova melhor solução
                
            else:
                # Aumenta a vizinhança
                k = min(k + 1, len(vizinhancas) - 1)  # Garante que k não exceda o número de vizinhanças

            solucao_otimizada = vizinhancas[k](melhor_solucao_global)  # Chama a função da vizinhança

        return melhor_solucao_global


    def vizinhanca_1(self, solucao):
        """
        Troca de itens entre dois bins.
        """
        # Implementa uma troca simples de itens entre bins
        if len(solucao) < 2:
            return solucao  

        bin1_index = random.randint(0, len(solucao) - 1)
        bin2_index = random.randint(0, len(solucao) - 1)

        if bin1_index == bin2_index or not solucao[bin1_index] or not solucao[bin2_index]:
            return solucao  # Se os bins são os mesmos ou vazios, não faz nada

        item1 = random.choice(solucao[bin1_index])
        item2 = random.choice(solucao[bin2_index])

        solucao[bin1_index].remove(item1)
        solucao[bin2_index].remove(item2)
        solucao[bin1_index].append(item2)
        solucao[bin2_index].append(item1)

        return solucao

    def vizinhanca_2(self, solucao):
        """
        Remove um item de um bin e adiciona a outro.
        """

        if len(solucao) < 2:
            return solucao  # Não é possível mover se houver menos de 2 bins

        bin_index = random.randint(0, len(solucao) - 1)

        if not solucao[bin_index]:  # Se o bin estiver vazio, não faz nada
            return solucao

        item = random.choice(solucao[bin_index])
        solucao[bin_index].remove(item)

        # Tenta adicionar o item a um bin diferente
        novo_bin_index = bin_index
        while novo_bin_index == bin_index:
            novo_bin_index = random.randint(0, len(solucao) - 1)

        solucao[novo_bin_index].append(item)

        return solucao



    def simulated_annealing(self, temperatura_inicial=1000, taxa_resfriamento=0.99, iteracoes_por_temperatura=100):
        """
        Inicia com uma solução aleatória e itera, perturbando-a para encontrar 
        novas soluções. Se a nova solução for melhor, é aceita; caso contrário, 
        pode ser aceita com uma probabilidade baseada na temperatura atual. 
        A temperatura diminui a cada iteração até atingir um limite, retornando 
        a melhor solução encontrada.
        """
        # Gera uma solução inicial aleatória
        solucao_atual = self.cont_ale()
        melhor_solucao_global = self.busca_local(solucao_atual)

        temperatura = temperatura_inicial

        while temperatura > 1:
            for _ in range(iteracoes_por_temperatura):
                solucao_nova = self.perturbar(solucao_atual)

                custo_atual = len(solucao_atual)
                custo_novo = len(solucao_nova)

                if custo_novo < custo_atual:
                    solucao_atual = solucao_nova
                else:
                    probabilidade = math.exp((custo_atual - custo_novo) / temperatura)
                    if random.random() < probabilidade:
                        solucao_atual = solucao_nova

                if custo_novo < len(melhor_solucao_global):
                    melhor_solucao_global = solucao_nova

            # Resfriamento
            temperatura *= taxa_resfriamento

        return melhor_solucao_global

    def tabu_search(self, iteracoes=100, tamanho_tabu=100):
        """
        Começa com uma solução aleatória e itera, gerando vizinhos e avaliando 
        seus custos. Soluções já exploradas são armazenadas em uma lista tabu 
        para evitar repetições. A melhor solução encontrada é atualizada ao 
        longo das iterações, e a lista tabu é mantida dentro de um tamanho 
        máximo. Retorna a melhor solução final.
        """
        solucao_atual = self.cont_ale()
        melhor_solucao_global = self.busca_local(solucao_atual)

        lista_tabu = []

        for _ in range(iteracoes):
            melhor_vizinho = None
            melhor_custo_vizinho = float('inf')

            vizinho_1 = self.vizinhanca_1(solucao_atual)
            vizinho_2 = self.vizinhanca_2(solucao_atual)
            vizinhos = [vizinho_1, vizinho_2]

            for vizinho in vizinhos:
                # Remove bins vazios do vizinho
                vizinho_sem_vazios = [bin for bin in vizinho if bin]  

                custo_vizinho = len(vizinho_sem_vazios)

                # Verifica se o vizinho está na lista tabu
                if vizinho_sem_vazios not in lista_tabu and custo_vizinho < melhor_custo_vizinho:
                    melhor_custo_vizinho = custo_vizinho
                    melhor_vizinho = vizinho_sem_vazios

            if melhor_vizinho is not None:
                solucao_atual = melhor_vizinho

                if len(solucao_atual) < len(melhor_solucao_global):
                    melhor_solucao_global = solucao_atual

                lista_tabu.append(solucao_atual)

                # Mantém a lista tabu com o tamanho máximo
                if len(lista_tabu) > tamanho_tabu:
                    lista_tabu.pop(0)  # Remove a solução mais antiga

        return melhor_solucao_global



    def grasp(self, iteracoes=100):
        """
        Em cada iteração, constrói uma solução inicial usando uma abordagem 
        gulosa aleatória e aplica busca local para otimização. A melhor solução 
        global é atualizada conforme novas soluções otimizadas são encontradas. 
        """

        melhor_solucao_global = None

        for _ in range(iteracoes):
            # Constrói uma solução inicial aleatória gulosa
            solucao_inicial = self.cons_guloso_dec() #mudar aqui

            # Aplica a busca local na solução inicial
            solucao_otimizada = self.busca_local(solucao_inicial)

            if melhor_solucao_global is None or len(solucao_otimizada) < len(melhor_solucao_global):
                melhor_solucao_global = solucao_otimizada

        return melhor_solucao_global



    def mostrar_informacoes(self, lista, constante):
        """
        Mostra informações sobre a lista de com a solução.
        """
        for vetor in lista:
            soma_vetor = sum(vetor)
            espaco_livre = constante - soma_vetor
            print(f"O vetor {vetor} resultou em soma {soma_vetor} e espaço livre de {espaco_livre}.")


problema01 = BinPackingData('/informacoes_pacotes.txt', probl="00")
problema01.leitura()
problema02 = BinPackingData('informacoes_pacotes.txt', probl="01")
problema02.leitura()
problema03 = BinPackingData('informacoes_pacotes.txt', probl="02")
problema03.leitura()

#metodo = Metodos(problema01)
#metodo = Metodos(problema02)
metodo = Metodos(problema03)

solucao_inicial_ale = metodo.cont_ale()
solucao_inicial_gul = metodo.cons_guloso()
solucao_inicial_gd = metodo.cons_guloso_dec()
solucao_otimizada = metodo.busca_local(solucao_inicial_ale)
busca_local_vnd = metodo.vnd(solucao_otimizada)
solucao_random_multistart = metodo.random_multistart()
solucao_Iiterated_local_search = metodo.iterated_local_search()
solucao_variable_neighborhood_search = metodo.variable_neighborhood_search()
solucao_simulated_annealing = metodo.simulated_annealing()
solucao_tabu_search = metodo.tabu_search()
solucao_grasp = metodo.grasp()

print("Solução inicial aleatória:  ", len(solucao_inicial_ale))
print("Solução gulosa:             ", len(solucao_inicial_gul))
print("Solução gulosa decrescente: ", len(solucao_inicial_gd))
print("Solução busca local:        ", len(solucao_otimizada))
print("Solução por VND:            ", len(busca_local_vnd))

# ALGORITMOS DE OTIMIZAÇÃO
print("Solução random multistart:  ", len(solucao_random_multistart))
print("Solução iterated local:     ", len(solucao_Iiterated_local_search))
print("Solução VNS:                ", len(solucao_variable_neighborhood_search))
print("Solução simulated annealing:", len(solucao_simulated_annealing))
print("Solução tabu search:        ", len(solucao_tabu_search))
print("Solução GRASP:              ", len(solucao_grasp))

#MOTRAS RESULTADO DA ALOCAÇÃO DO ITENS
#metodo.mostrar_informacoes(solucao_inicial_ale, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_inicial_gul, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_inicial_gd, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_otimizada, problema01.capacidade)
#metodo.mostrar_informacoes(busca_local_vnd, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_random_multistart, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_Iiterated_local_search, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_variable_neighborhood_search, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_simulated_annealing, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_tabu_search, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_grasp, problema01.capacidade)
