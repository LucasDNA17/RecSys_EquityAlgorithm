
import numpy as np
from SocialMeasures import SocialMeasures
import gurobipy as gp


class EquityAlgorithm:

  def __init__(self, all_users_ratings, predictions_matrix, min_rate, max_rate, groups, h=10):
    self.all_users_ratings = all_users_ratings
    self.min_rate = min_rate
    self.max_rate = max_rate
    self.groups = groups
    self.n_items = predictions_matrix.shape[1]
    self.n_users = predictions_matrix.shape[0]
    self.set_predictions_matrix(predictions_matrix)
    self.set_groups(groups)
    self.set_h_parameter(h)
    self.social_metrics_before = SocialMeasures(all_users_ratings, predictions_matrix, groups)
    self.social_metrics_after = None

  def set_predictions_matrix(self, predictions_matrix):
    if predictions_matrix.shape != (self.n_users, self.n_items):
      raise TypeError(f"Shape mismatch: matrix should be {self.predictions_matrix.shape} instead of {predictions_matrix.shape}")

    elif not ((predictions_matrix >= self.min_rate) & (predictions_matrix <= self.max_rate)).all():
      raise ValueError(f"Prediction values should be between {self.min_rate} and {self.max_rate}")

    else:
      self.predictions_matrix = predictions_matrix
      self.social_metrics_before = SocialMeasures(self.all_users_ratings, self.predictions_matrix, self.groups)
      self.social_metrics_after = None


  def set_h_parameter(self, h):
    if not isinstance(h, int) or h <= 0:
      raise TypeError(f"h should be a positive integer")

    else:
      self.h = h
      self.social_metrics_after = None


  def set_groups(self, groups):
    if not isinstance(groups, list):
      raise TypeError(f"Groups should be a list of lists")

    for group in groups:
      if not isinstance(group, list):
        raise TypeError(f"Groups should be a list of lists")

    groups_sets = [set(group) for group in groups]
    if len(set.intersection(*groups_sets)) > 0:
      raise ValueError(f"Groups should not have any common elements")

    union = set.union(*groups_sets)
    if(union != set(range(1, self.n_users + 1))):
      raise ValueError(f"Groups must contain every userId in the range 1 - {self.n_users + 1}")

    else:
      self.groups = groups
      self.social_metrics_before = SocialMeasures(self.all_users_ratings, self.predictions_matrix, self.groups)
      self.social_metrics_after = None


  def __generate_random_variations__(self, all_ratings_mean_differences):
    n_users, n_items = self.predictions_matrix.shape[0], self.predictions_matrix.shape[1]
    altered_predictions_matrix = self.predictions_matrix.copy()
    for i in range(n_users):
      lim = all_ratings_mean_differences[i + 1]/(self.max_rate - self.min_rate)

      if lim >= 0:
        altered_predictions_matrix[i] += np.random.uniform(0, lim, size=n_items)
      else:
        altered_predictions_matrix[i] += np.random.uniform(lim, 0, size=n_items)

    altered_predictions_matrix = altered_predictions_matrix.clip(self.min_rate, self.max_rate)
    return altered_predictions_matrix


  def __Z_matrix__(self, matrices):
    Z = np.zeros((len(self.all_users_ratings), len(matrices)))

    for j in range(len(matrices)):
      social_measures = SocialMeasures(self.all_users_ratings, matrices[j], self.groups)
      individual_losses = social_measures.get_allIndividualLosses()
      for userId in self.all_users_ratings.keys():
        Z[userId - 1][j] = individual_losses[userId]

    return Z


  def optimization_algorithm(self, list_matrices, Z):

    with gp.Model() as model:

      all_users = [i for i in range(Z.shape[0])]
      all_matrices = [i for i in range(len(list_matrices))]
      h = len(all_matrices)
      n_users = Z.shape[0]
      n_itens = (list_matrices[0]).shape[1]

      w = model.addVars(all_users, all_matrices, vtype=gp.GRB.BINARY, name='W')

      group_losses = [gp.quicksum(w[i - 1, j]*Z[i - 1][j] for i in group for j in range(h))/len(group) for group in self.groups]

      avg_loss = gp.quicksum(group_losses)/len(self.groups)
      model.setObjective(gp.quicksum((loss - avg_loss)**2 for loss in group_losses), gp.GRB.MINIMIZE)

      model.addConstrs((w.sum(user, '*') == 1 for user in all_users), "OneRecommendationPerUser")
      model.optimize()

      X_optimized = np.zeros((n_users, n_itens))
      for user in all_users:
        for matrice in range(h):
          if w[user, matrice].X > 0.5:  # Se a recomendação foi escolhida para o usuário
            X_optimized[user - 1] = list_matrices[matrice][user - 1]

      return X_optimized


  def run(self):
    self.social_metrics_before.all()
    all_mean_rate_differences = self.social_metrics_before.all_mean_rate_differences
    all_individualLosses = self.social_metrics_before.all_IndividualLosses

    altered_matrices = [self.__generate_random_variations__(all_mean_rate_differences) for i in range(self.h)]
    Z = self.__Z_matrix__(altered_matrices)

    X_optimized = self.optimization_algorithm(altered_matrices, Z)
    self.social_metrics_after = SocialMeasures(self.all_users_ratings, X_optimized, self.groups)
    self.social_metrics_after.all()

    return X_optimized