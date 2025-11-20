import pandas as pd
import surprise as sp
from Test import Test


#Criação do dataframe
df = pd.read_csv('./ml-100k/u.data', sep='\t', header=None)
df.columns = ['userId', 'itemId', 'rating', 'timestamp']
df.drop('timestamp', axis=1, inplace=True)
df.head()


#Lendo as informações de gênero dos usuários
users_information = pd.read_csv('./ml-100k/u.user', sep='|', header=None)
users_information.columns = ['userId', 'age', 'gender', 'occupation', 'zipCode']
users_information.drop(columns=['age', 'occupation', 'zipCode'], inplace=True)

#Diminuição do tamanho do dataframe caso não se tenha a licensa Guropi
#Os resultados obtidos em 'results' NÃO fizeram esta limitação
size_limit = 40 #Limite de usuários para h = 5
df = df.loc[df['userId'] <= size_limit, ['userId', 'itemId', 'rating']]
users_information = users_information.loc[users_information['userId'] <= size_limit, ['userId', 'gender']]


#Divisão dos grupos 
group_male = list(((users_information.loc[users_information['gender'] == 'M', ['userId']])['userId'].unique()))
group_female = list(((users_information.loc[users_information['gender'] == 'F', ['userId']])['userId'].unique()))
groups = [group_male, group_female]


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
algo = 'NMF'
print(f"{algo} measures with h = {h}: ")
results[algo][h].print()
