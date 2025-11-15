# RecSys_EquityAlgorithm

## Descrição geral
Sistemas de recomendação utilizam-se de dados de interações dos usuários para modelar e prever suas preferências. Uma vez que estes dados não são experimentais, eles normalmente apresentam vieses que geram injustiças nas recomendações.
Tentamos, aqui, implementar as métricas e o algoritmo apresentados pelos pesquisadores **Santos e Comarela (2024)** - artigo disponível em https://sol.sbc.org.br/index.php/wics/article/view/29506 - para avaliar e tentar amenizar a injustiça de recomendações geradas por três algoritmos diferentes em quatro cenários em que os usuários estão divididos de acordo com alguma característica que os une.

A implementação segue um paradigma "ingênuo" no sentido de não utilizar estratégias mais sofisticadas para a clusterização dos usuários e de não adotar otimizações sutis ao algoritmo descrito no artigo. **Portanto, os resultados podem variar se outra implementação for desenvolvida**.

## Cenários considerados
O algoritmo foi testado para cada algoritmo e divisão dos usuários descritos abaixo.

Algoritmos:
  
