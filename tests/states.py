import pandas as pd
import numpy as np
import surprise as sp
from uszipcode import SearchEngine
from Test import Test


#Criação do dataframe
#É necessário baixar ml-100k no link https://files.grouplens.org/datasets/movielens/ml-100k.zip
df = pd.read_csv('./ml-100k/u.data', sep='\t', header=None)
df.columns = ['userId', 'itemId', 'rating', 'timestamp']
df.drop('timestamp', axis=1, inplace=True)
df.head()

#Lendo as informações dos zipcodes dos usuários
users_information = pd.read_csv('./ml-100k/u.user', sep='|', header=None)
users_information.columns = ['userId', 'age', 'gender', 'occupation', 'zipCode']
users_information.drop(columns=['age', 'gender', 'occupation'], inplace=True)

engine = SearchEngine()
#Função para obter o estado de um usuário a partir do zipcode
def get_state(userId):
    zipcode = users_information.loc[users_information['userId']==userId, 'zipCode'].iloc[0]
    search = engine.by_zipcode(zipcode)
    if search is None:
        return None
    return search.state

#Lista de abreviações dos estados
us_state_abbreviations = [
    "AE", "AL", "AK", "AP", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

#Obtenção dos estados para cada usuário
states = {abbreviation : [] for abbreviation in us_state_abbreviations}
little_group = []
for userId in users_information['userId'].unique():
  state = get_state(userId)
  if state is not None:
    states[state].append(userId)
  else:
    little_group.append(userId)

#Divisão dos usuários em grupos
#Estados com menos de 50 usuários são agrupados em apenas um grupo
#para reduzir o consumo de memória RAM
delimiter = 50
for state in states.keys():
  if len(states[state]) < delimiter:
    little_group.extend(states[state])

#Criação da lista de grupos
groups = [states[state] for state in states.keys() if len(states[state]) >= delimiter]
groups.append(little_group)


#Teste com três algoritmos de recomendação diferentes: KNN, SVD e NMF
#Range de h: 1 - 4
KNNBasic_algo = sp.KNNBasic()
SVD_algo = sp.SVD()
NMF_algo = sp.NMF()
results = {}

range_h = list(range(1, 5))

Test_KNN = Test(df, KNNBasic_algo, groups)
initial_measures, results['KNN'] = Test_KNN.run(range_h)

Test_SVD = Test(df, SVD_algo, groups)
_, results['SVD'] = Test_SVD.run(range_h)

Test_NMF = Test(df, NMF_algo, groups)
_, results['NMF'] = Test_NMF.run(range_h)