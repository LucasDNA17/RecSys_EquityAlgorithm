import pandas as pd
import surprise as sp
from SocialMeasures import SocialMeasures
from EquityAlgorithm import EquityAlgorithm


class Test:
  def __init__(self, df, rec_model, groups):
    self.df = df
    self.max_rating = self.df['rating'].max()
    self.min_rating = self.df['rating'].min()
    self.n_users = self.df['userId'].max()
    self.n_items = self.df['itemId'].max()
    self.rec_model = rec_model
    self.groups = groups
    self.predictions_matrix = None
    self.equity_algorithm = None
    self.users_ratings = None

  def __get_predictions_matrix__(self):
    if self.predictions_matrix is None:
      reader = sp.Reader(rating_scale=(self.min_rating, self.max_rating))
      data_surprise = sp.Dataset.load_from_df(df, reader=reader)
      trainset_surprise = data_surprise.build_full_trainset()
      self.rec_model.fit(trainset_surprise)

      predictions_matrix = np.zeros((self.n_users, self.n_items))
      for userId in self.df['userId'].unique():
        for itemId in self.df['itemId'].unique():
          prediction = self.rec_model.predict(userId, itemId).est
          predictions_matrix[userId - 1][itemId - 1] = prediction

      self.predictions_matrix = predictions_matrix

    return self.predictions_matrix


  def __get_user_rating_map__(self, userId):
    ratings = self.df.loc[self.df['userId']==userId, ['itemId', 'rating']]
    ratings_map = {}

    for row in ratings.itertuples():
      itemId, rating = row.itemId, row.rating
      ratings_map[itemId] = rating

    return ratings_map


  def __get_all_users_ratings__(self):
    if self.users_ratings is None:
      all_users_ratings = {}
      for userId in self.df['userId'].unique():
        all_users_ratings[userId] = self.__get_user_rating_map__(userId)

      self.users_ratings = all_users_ratings

    return self.users_ratings


  def run(self, range_h):
    self.__get_all_users_ratings__()
    self.__get_predictions_matrix__()
    initial_social_measures = SocialMeasures(self.users_ratings, self.predictions_matrix, self.groups)
    initial_social_measures.all()
    social_measures_h = {}

    for h in range_h:
      algo = EquityAlgorithm(self.users_ratings, self.predictions_matrix, self.min_rating, self.max_rating, self.groups, h=h)
      algo.run()
      social_measures_h[h] = algo.social_metrics_after


    return initial_social_measures, social_measures_h