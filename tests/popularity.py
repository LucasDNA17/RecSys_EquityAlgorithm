import pandas as pd
import surprise as sp
from Test import Test


#Criação do dataframe
df = pd.read_csv('./ml-100k/u.data', sep='\t', header=None)
df.columns = ['userId', 'itemId', 'rating', 'timestamp']
df.drop('timestamp', axis=1, inplace=True)
df.head()

#Diminuição do tamanho do dataframe caso não se tenha a licensa Guropi
#Os resultados obtidos em 'results' NÃO fizeram esta limitação
size_limit = 40 #Limite de usuários para h = 5
df = df.loc[df['userId'] <= size_limit, ['userId', 'itemId', 'rating']]

#Função para obter a popularidade (número de interações) de um item
def get_item_popularity(itemId):
  return df.loc[df['itemId']==itemId].shape[0]

#Função para obter a popularidade média da lista de interações de um usuário
def get_user_mean_popularity(userId):
    user_items = df.loc[df['userId']==userId, 'itemId']
    user_items['popularity'] = user_items.apply(get_item_popularity)
    mean_popularity = user_items['popularity'].mean()
    return mean_popularity


#Ordena os usuários em ordem decrescente de popularidade
users_sorted_popularity = list(df['userId'].unique())
users_sorted_popularity.sort(key=get_user_mean_popularity, reverse=True)

#Divide os usuários em três grupos:
#Primeiro terço: blockbuster - usuários que vêem itens populares
#Segundo terço: diversified - usuários que vêem itens diversificados
#Terceiro terço: niched - usuários que vêem itens nichados
n_users = len(users_sorted_popularity)
first_third = int(n_users/3)
second_third = int(2*n_users/3)

blockbuster = users_sorted_popularity[:first_third]
diversed = users_sorted_popularity[first_third:second_third]
niched = users_sorted_popularity[second_third:]

groups = [blockbuster, diversed, niched]

#Teste com três algoritmos de recomendação diferentes: KNN, SVD e NMF
#Range de h: 1 - 5
KNNBasic_algo = sp.KNNBasic()
SVD_algo = sp.SVD()
NMF_algo = sp.NMF()
results = {}

range_h = list(range(1, 6))

Test_KNN = Test(df, KNNBasic_algo, groups)
initial_measures, results['KNN'] = Test_KNN.run(range_h)

Test_SVD = Test(df, SVD_algo, groups)
_, results['SVD'] = Test_SVD.run(range_h)

Test_NMF = Test(df, NMF_algo, groups)
_, results['NMF'] = Test_NMF.run(range_h)

print(f"\nInitial Measures: ")
initial_measures.print()

print(f"\n")
h = 5
algo = 'KNN'
print(f"{algo} measures with h = {h}: ")
results[algo][h].print()