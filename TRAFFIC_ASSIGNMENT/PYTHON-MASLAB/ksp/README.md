# KSP v1.43

## DESCRIPTION
O K Shortest Loopless Paths (KSP) é um algoritmo proposto por Yen [[1]](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.17.11.712) capaz de encontrar os K caminhos mais curtos entre dois nodos de um dado grafo.

A única dependência do script é o pacote [py-expression-eval](https://github.com/AxiaCore/py-expression-eval), utilizado na interpretação dos arquivos de grafo.

## USAGE
		python KSP.py [-h] -f FILE -k K [-l OD_LIST] [-n FLOW]

Or:

		./KSP.py [-h] -f FILE -k K [-l OD_LIST] [-n FLOW]
```
arguments:
	-h, --help	show this help message and exit.
	-f FILE		the graph file.
	-k K		number of shortest paths to find.
	-l OD_LIST	list of OD-pairs, in the format 'O|D;O|D;[and so on]', 
			where O are valid origin nodes, and D are valid destination nodes.
	-n FLOW		number of vehicles (flow) to consider when computing the links' costs.
```

## Exemplo 1
Obter os 4 caminhos mais curtos para todos os pares OD da rede OW (assumindo que o arquivo da rede está no mesmo diretório do script KSP.py). No terminal, a partir do diretório do KSP, ao digitar:

		python KSP.py -f OW.net -k 4
obtém-se:

		ksptable = [
			[ # A|L flow
				['A-C', 'C-G', 'G-J', 'J-I', 'I-L'], # cost 28.0
				['A-C', 'C-G', 'G-J', 'J-L'], # cost 29.0
				['A-C', 'C-F', 'F-I', 'I-L'], # cost 31.0
				['A-C', 'C-D', 'D-G', 'G-J', 'J-I', 'I-L'] # cost 33.0
			],
			[ # A|M flow
				['A-C', 'C-D', 'D-H', 'H-K', 'K-M'], # cost 26.0
				['A-C', 'C-G', 'G-J', 'J-K', 'K-M'], # cost 28.0
				['A-C', 'C-G', 'G-H', 'H-K', 'K-M'], # cost 28.0
				['A-D', 'D-H', 'H-K', 'K-M'] # cost 29.0
			],
			[ # B|L flow
				['B-D', 'D-G', 'G-J', 'J-I', 'I-L'], # cost 32.0
				['B-D', 'D-G', 'G-J', 'J-L'], # cost 33.0
				['B-A', 'A-C', 'C-G', 'G-J', 'J-I', 'I-L'], # cost 35.0
				['B-A', 'A-C', 'C-G', 'G-J', 'J-L'] # cost 36.0
			],
			[ # B|M flow
				['B-E', 'E-H', 'H-K', 'K-M'], # cost 23.0
				['B-D', 'D-H', 'H-K', 'K-M'], # cost 25.0
				['B-D', 'D-E', 'E-H', 'H-K', 'K-M'], # cost 30.0
				['B-E', 'E-D', 'D-H', 'H-K', 'K-M'] # cost 32.0
			]
		]
		
## Exemplo 2
Obter os 4 caminhos mais curtos apenas para o par AL da rede OW (assumindo que o arquivo da rede está no mesmo diretório do script KSP.py). No terminal, a partir do diretório do KSP, ao digitar:

		python KSP.py -f OW.net -l 'A|L' -k 4
obtém-se:

		ksptable = [
			[ # A|L flow
				['A-C', 'C-G', 'G-J', 'J-I', 'I-L'], # cost 28.0
				['A-C', 'C-G', 'G-J', 'J-L'], # cost 29.0
				['A-C', 'C-F', 'F-I', 'I-L'], # cost 31.0
				['A-C', 'C-D', 'D-G', 'G-J', 'J-I', 'I-L'] # cost 33.0
			]
		]

## Instruções para chamar o KSP a partir de outros programas
Para chamar o KSP a partir de outros programas escritos em Python, basta importar o KSP e chamá-lo da seguinte forma:

		import KSP

		routes = KSP.getKRoutesNetFile(graph_file, origin, destination, K)
Onde:

graph_file é o caminho do arquivo de rede (string);

origin é o nodo de origem (string);

destination é o nodo de destino (string);

K é a quantidade de caminhos mais curtos desejados (int).

A função acima lê o arquivo de rede e gera as k rotas para o par OD fornecido. Para calcular para mais pares OD, basta chamar a função novamente. No entanto, note que construir a rede a partir do arquivo para cada par OD é ineficiente. Logo, pode-se construir a rede separadamente e então chamar uma variante da função acima que recebe as listas já processadas de nós, arestas e pares OD:

		import KSP

		V, E, OD = KSP.generateGraph(graph_file)

		for od in OD:
		    origin, destination = od.split('|')
		    routes = KSP.getKRoutes(V, E, origin, destination, K)
O resultado do algoritmo (em ambos os casos) é uma lista dupla, onde cada posição corresponde a uma tupla <caminho, custo>. Considerando os exemplos anteriores (com a rede OW), a saída para o par AL com K=4 seria a seguinte:

		[  [['A-C', 'C-G', 'G-J', 'J-I', 'I-L'], 28.0], 
		   [['A-C', 'C-G', 'G-J', 'J-L'], 29.0], 
		   [['A-C', 'C-F', 'F-I', 'I-L'], 31.0], 
		   [['A-C', 'C-D', 'D-G', 'G-J', 'J-I', 'I-L'], 33.0]   ]
Um exemplo detalhado do KSP para esta finalidade está disponível no arquivo de exemplo ksp_calling_example.py, contido no mesmo diretório do algoritmo.

## Links externos
[Explicação simplificada do algoritmo KSP na Wikipedia (em inglês)](https://en.wikipedia.org/wiki/Yen%27s_algorithm)


## GRAPH FILE FORMATTING INSTRUCTIONS

See [[2]](https://github.com/maslab-ufrgs/network_description_syntax) for complete instructions.

## REFERENCES:

1. Yen, J.Y.: [Finding the k shortest loopless paths in a network.](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.17.11.712) Management Science 17(11) (1971) 712-716.

2. https://github.com/maslab-ufrgs/transportation_networks.

## AUTHOR

Created in February 10, 2014, by Gabriel de Oliveira Ramos <goramos@inf.ufrgs.br>.
