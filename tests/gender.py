import pandas as pd
import surprise as sp
import numpy as np
from Test import Test


#Criação do dataframe
#É necessário baixar ml-100k no link https://files.grouplens.org/datasets/movielens/ml-100k.zip
df = pd.read_csv('./ml-100k/u.data', sep='\t', header=None)
df.columns = ['userId', 'itemId', 'rating', 'timestamp']
df.drop('timestamp', axis=1, inplace=True)
df.head()

#Lendo as informações de gênero dos usuários
users_information = pd.read_csv('./ml-100k/u.user', sep='|', header=None)
users_information.columns = ['userId', 'age', 'gender', 'occupation', 'zipCode']
users_information.drop(columns=['age', 'occupation', 'zipCode'], inplace=True)

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