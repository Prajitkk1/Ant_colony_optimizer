# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 09:45:57 2023

@author: ADAMS-LAB
"""
from scipy.stats.qmc import LatinHypercube
import numpy as np
import copy
import random
import math

class ACO_optimizer:
    def __init__(self, cities,locations,n_iter=10, n_ants = 50):
        self.cities = cities
        self.no_cities = len(cities)
        self.distances = self.calculate_distances(locations)
        self.locations = locations
        self.alpha = 1
        self.beta = 5
        self.Q = 100
        self.evap = 0.5
        self.n_ants = n_ants
        self.init_pheromone = 10e-6
        self.n_iter = n_iter
        self.best_distance = float('inf')
        self.convergence = []
        self.pheromones = np.ones_like(self.distances) * self.init_pheromone
        
    def calculate_distance(self, value1, value2):
        return math.sqrt(math.pow(value2[0] - value1[0], 2) + math.pow(value2[1] - value1[1], 2))
    
    def calculate_distances(self, coordinates):
        n = len(coordinates)
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                distances[i, j] = distances[j, i] = self.calculate_distance(coordinates[i], coordinates[j])
        self.distances = distances
        return self.distances
    
    def route_construction(self):
        all_paths = []
        all_distances = []
        for k in range(self.n_ants):
            path = []
            random_city = random.choice(self.cities)
            path.append(random_city)
            available_cities = copy.deepcopy(self.cities)
            available_cities.remove(random_city)
            current_city = random_city
            while len(path) < self.no_cities:
                numerators = []
                for city in available_cities:
                    i = self.cities.index(city)
                    j = self.cities.index(current_city)
                    numerator = (self.pheromones[j, i] ** self.alpha) * ((1 / self.distances[j, i]) ** self.beta)
                    numerators.append(numerator)
                denominator = sum(numerators)
                probability = [i/denominator for i in numerators]
                next_city = random.choices(available_cities, weights=probability)[0]
                path.append(next_city)
                available_cities.remove(next_city)
                current_city = next_city
            path.append(random_city)    
            current_distance = sum(self.distances[self.cities.index(path[i - 1]), self.cities.index(path[i])] for i in range(len(path)))
            if current_distance<self.best_distance:
                self.best_distance = current_distance
                path_new = []
                for i in path:
                    path_new.append(self.cities.index(i))
                self.best_path = path_new
            all_distances.append(current_distance)
            all_paths.append(path)
        self.convergence.append(self.best_distance)
        return all_paths, all_distances

                

    
    def pheromone_update(self, all_paths, all_distances):
        delta_pheromones = np.zeros_like(self.pheromones)
        for i, path in enumerate(all_paths):
            for j in range(1, len(path)):
                city_idx1 = self.cities.index(path[j - 1])
                city_idx2 = self.cities.index(path[j])
                delta_pheromones[city_idx1, city_idx2] += self.Q / all_distances[i]
    
        self.pheromones = (1 - self.evap) * self.pheromones + delta_pheromones
    
    def optimize(self, n_iter=100):
        for i in range(n_iter):
            a,b = self.route_construction()
            self.pheromone_update(a,b)
        return self.best_distance, self.best_path, self.convergence