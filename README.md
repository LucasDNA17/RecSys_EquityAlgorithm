# RecSys_EquityAlgorithm

## Descrição geral
Sistemas de recomendação utilizam-se de dados de interações dos usuários para modelar e prever suas preferências. Uma vez que estes dados não são experimentais, eles normalmente apresentam vieses que geram injustiças nas recomendações.
Tentamos, aqui, implementar as métricas e o algoritmo apresentados pelos pesquisadores **Santos e Comarela (2024)** - artigo disponível em https://sol.sbc.org.br/index.php/wics/article/view/29506 - para avaliar e tentar amenizar a injustiça de recomendações geradas por três algoritmos diferentes em quatro cenários em que os usuários estão divididos de acordo com alguma característica que os une.
A base de dados utilizada para os testes foi a [MovieLens-100k](https://grouplens.org/datasets/movielens/100k/).

A implementação segue um paradigma "ingênuo" no sentido de não utilizar estratégias mais sofisticadas para a clusterização dos usuários e de não adotar otimizações sutis ao algoritmo descrito no artigo. **Portanto, os resultados podem variar se outra implementação for desenvolvida**.

## Cenários considerados
O algoritmo de equidade foi testado para cada algoritmo de recomendação e divisão dos usuários descritos abaixo.

Algoritmos:

	* KNN
	* SVD
	* NMF

Grupos de usuários:

	+ Gêneros: gêneros feminino e masculino;
	+ Idade: crianças (idade menor do que 12 anos); adolescentes (idade maior ou igual a 12 e menor do que 18 anos); adulto (idade maior ou igual a 18 e menor do que 60 anos); idoso (idade maior do que 60 anos)
	+ Estado: estado de origem dos Estados Unidos. Estados com menos de 50 usuários foram agrupados em um grupo, chamado de "Rest". Os estados que formaram grupos próprios são: CA, IL, MN, NY, TX.
	+ Popularidade: os usuários foram ordenados em ordem decrescente de popularidade média de itens interagidos, sendo que a popularidade de um item é a sua quantidade de interações. O primeiro terço dos usuários são os do tipo "blockbuster"; o segundo do tipo "diversificado"; e o terceiro do tipo "nichado".
  
