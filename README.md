# Problema de Bin Packing

Este projeto implementa uma solução para o problema de **Bin Packing** utilizando diversas abordagens de otimização. O objetivo é distribuir um conjunto de itens em bins de capacidade fixa, minimizando o número total de bins utilizados.

## Estrutura do Código

### Classes

- **BinPackingData**: Classe responsável por ler e armazenar os dados do problema a partir de um arquivo. Contém métodos para inicializar os parâmetros do problema, como capacidade do bin, número de itens e pesos dos itens.

- **Metodos**: Herda de `BinPackingData` e implementa várias estratégias de alocação e otimização:
  - `distribuir_itens`: Distribui itens em bins respeitando a capacidade máxima.
  - `little_inst`: Gera permutações dos itens para encontrar a melhor solução para um número reduzido de itens.
  - `cont_ale`: Constrói uma solução inicial aleatória.
  - `cons_guloso` e `cons_guloso_dec`: Constrói soluções iniciais usando abordagens gulosas (crescentes e decrescentes).
  - `busca_local`: Melhora uma solução existente buscando alocação de itens entre bins.
  - Métodos de busca e otimização:
    - `random_multistart`
    - `iterated_local_search`
    - `variable_neighborhood_search`
    - `simulated_annealing`
    - `tabu_search`
    - `grasp`

### Execução

1. **Leitura de Dados**: Instâncias do problema são criadas e os dados são lidos de um arquivo específico.
2. **Geração de Soluções**: Várias soluções são geradas usando os métodos implementados:
   - Soluções iniciais aleatórias e gulosas.
   - Aplicação de algoritmos de otimização.
3. **Exibição de Resultados**: O código imprime o número de bins utilizados para cada solução gerada.

### Exemplos de Uso

Para usar o código, instanciar a classe `BinPackingData` com o caminho para o arquivo de dados e o problema desejado. Em seguida, criar uma instância da classe `Metodos` e chamar os métodos para gerar e otimizar as soluções.

```python
problema = BinPackingData('caminho/para/arquivo.txt', probl="00")
problema.leitura()
metodo = Metodos(problema)
solucao_inicial = metodo.cont_ale()
solucao_otimizada = metodo.busca_local(solucao_inicial)
solucao_random_multistart = metodo.random_multistart()

# Apresentação dos resultado(Quantidade de bins usados)
print("Solução inicial aleatória:  ", len(solucao_inicial_ale))
print("Solução busca local:        ", len(solucao_otimizada))
print("Solução random multistart:  ", len(solucao_random_multistart))

#Ver a solução das alocação dos itens nos bins
metodo.mostrar_informacoes(solucao_inicial_ale, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_otimizada, problema01.capacidade)
#metodo.mostrar_informacoes(solucao_random_multistart, problema01.capacidade)
