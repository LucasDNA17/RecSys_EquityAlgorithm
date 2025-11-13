import numpy as np

class SocialMeasures:

  def __init__(self, all_users_ratings, predictions_matrix, groups):
    self.all_users_ratings = all_users_ratings
    self.predictions_matrix = predictions_matrix
    self.groups = groups
    self.all_mean_rate_differences = None
    self.all_IndividualLosses = None
    self.individual_unfairness = None
    self.all_groupLosses = None
    self.group_unfairness = None

  def all(self):
    self.get_all_mean_rate_differences()
    self.get_allIndividualLosses()
    self.IndividualUnfairness()
    self.get_allGroupLosses()
    self.GroupUnfairness()


  def __mean_rate_difference__(self, userId):
    user_rating_map = self.all_users_ratings[userId]
    predictions_vector = self.predictions_matrix[userId - 1]
    differences = []
    for itemId in user_rating_map.keys():
      difference = user_rating_map[itemId] - predictions_vector[itemId - 1]
      differences.append(difference)

    return np.mean(differences)

  def get_all_mean_rate_differences(self):
    if self.all_mean_rate_differences is None:
      all_mean_rate_differences = {}
      for userId in self.all_users_ratings.keys():
        all_mean_rate_differences[userId] = self.__mean_rate_difference__(userId)

      self.all_mean_rate_differences = all_mean_rate_differences

    return all_mean_rate_differences


  def __IndividualLoss__(self, userId, predictions_vector):
    user_rating_map = self.all_users_ratings[userId]

    if len(user_rating_map) == 0: return 0

    squared_differences = 0
    for itemId in user_rating_map.keys():
      rating, prediction = user_rating_map[itemId], predictions_vector[itemId - 1]
      squared_differences += (rating - prediction)**2

    return squared_differences/len(user_rating_map)


  def get_allIndividualLosses(self):
    if self.all_IndividualLosses is None:
      all_IndividualLosses = {}
      for userId in self.all_users_ratings.keys():
        loss = self.__IndividualLoss__(userId, self.predictions_matrix[userId - 1])
        all_IndividualLosses[userId] = loss

      self.all_IndividualLosses = all_IndividualLosses

    return self.all_IndividualLosses


  def IndividualUnfairness(self):
    if self.individual_unfairness is None:
      all_individualLosses = self.get_allIndividualLosses()
      n_users = len(all_individualLosses)

      squared_differences = 0
      for i in range(1, n_users + 1):
        for j in range(i + 1, n_users + 1):
          squared_differences += (all_individualLosses[i] - all_individualLosses[j])**2

      individual_unfairness = squared_differences/(n_users**2)
      self.individual_unfairness = individual_unfairness

    return self.individual_unfairness


  def __GroupLoss__(self, groupId):
    group = self.groups[groupId]
    if len(group) == 0: return 0

    squared_differences = 0
    for userId in group:
      ratings = self.all_users_ratings[userId]
      for itemId in ratings.keys():
        squared_differences += (ratings[itemId] - self.predictions_matrix[userId - 1][itemId - 1])**2

    return squared_differences/len(group)


  def get_allGroupLosses(self):
    if self.all_groupLosses is None:
      all_GroupLosses = {}
      for i in range(len(self.groups)):
        loss = self.__GroupLoss__(i)
        all_GroupLosses[i] = loss

      self.all_groupLosses = all_GroupLosses

    return self.all_groupLosses


  def GroupUnfairness(self):
    if self.group_unfairness is None:
      all_groupLosses = self.get_allGroupLosses()
      n_groups = len(all_groupLosses)

      squared_differences = 0
      for i in range(n_groups):
        for j in range(i + 1, n_groups):
          squared_differences += (all_groupLosses[i] - all_groupLosses[j])**2

      group_unfairness = squared_differences/(n_groups**2)
      self.group_unfairness = group_unfairness

    return self.group_unfairness