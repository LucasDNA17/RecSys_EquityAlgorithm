import pandas as pd
import surprise as sp
from Test import Test


#Criação do dataframe
#É necessário baixar ml-100k no link https://files.grouplens.org/datasets/movielens/ml-100k.zip
df = pd.read_csv('./ml-100k/u.data', sep='\t', header=None)
df.columns = ['userId', 'itemId', 'rating', 'timestamp']
df.drop('timestamp', axis=1, inplace=True)
df.head()

#Lendo as informações de idade dos usuários
users_information = pd.read_csv('./ml-100k/u.user', sep='|', header=None)
users_information.columns = ['userId', 'age', 'gender', 'occupation', 'zipCode']
users_information.drop(columns=['gender', 'occupation', 'zipCode'], inplace=True)

#Diminuição do tamanho do dataframe caso não se tenha a licensa Guropi
#Os resultados obtidos em 'results' NÃO fizeram esta limitação
size_limit = 100 #Limite de usuários para h = 2
df = df.loc[df['userId'] <= size_limit, ['userId', 'itemId', 'rating']]
users_information = users_information.loc[users_information['userId'] <= size_limit, ['userId', 'age']]


#Dividindo os usuários de acordo com suas idades
group_children = list((users_information.loc[users_information['age'] < 12, ['userId']])['userId'].unique())
group_teenager = list((users_information.loc[(users_information['age'] >= 12) & (users_information['age'] <18), ['userId']])['userId'].unique())
group_adult = list((users_information.loc[(users_information['age'] >= 18) & (users_information['age'] < 60), ['userId']])['userId'].unique())
group_elder = list((users_information.loc[users_information['age'] >= 60, ['userId']])['userId'].unique())
groups = [group_children, group_teenager, group_adult, group_elder]


#Teste com três algoritmos de recomendação diferentes: KNN, SVD e NMF
#Range de h: 1 - 2  --- nos testes reais, feitos com a licença gurobi, o range era 1 - 4
KNNBasic_algo = sp.KNNBasic()
SVD_algo = sp.SVD()
NMF_algo = sp.NMF()
results = {}

range_h = list(range(1, 3))

Test_KNN = Test(df, KNNBasic_algo, groups)
initial_measures, results['KNN'] = Test_KNN.run(range_h)

Test_SVD = Test(df, SVD_algo, groups)
_, results['SVD'] = Test_SVD.run(range_h)

Test_NMF = Test(df, NMF_algo, groups)
_, results['NMF'] = Test_NMF.run(range_h)


print(f"\nInitial Measures: ")
initial_measures.print()

print(f"\n")
h = 2
algo = 'SVD'
print(f"{algo} measures with h = {h}: ")
results[algo][h].print()
