# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 13:24:55 2023

@author: ADAMS-LAB
"""
path = [1, 49, 32, 45, 19, 41, 8, 9, 10, 43, 33, 51, 11, 52, 14, 13, 47, 26, 27, 28, 12, 25, 4, 6, 15, 5, 24, 48, 38, 37, 40, 39, 36, 35, 34, 44, 46, 16, 29, 50, 20, 23, 30, 2, 7, 42, 21, 17, 3, 18, 31, 22, 1]



from ACO_optimizer import ACO_optimizer
def read_coordinates_from_file(file_path):
    coordinates = []
    city_ids = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("EOF"):
                break
            elif not line.startswith(("NAME", "TYPE", "COMMENT", "DIMENSION", "EDGE_WEIGHT_TYPE", "NODE_COORD_SECTION")):
                city_id, x, y = line.strip().split()
                coordinates.append((float(x), float(y)))
                city_ids.append(city_id)
    return coordinates,city_ids

file_path = "5672785.txt"
coordinates, city_ids = read_coordinates_from_file(file_path)
# print(coordinates)
# print(city_ids)


path = path

import matplotlib.pyplot as plt


path_coordinates = [coordinates[int(city)-1] for city in path]


for i in range(len(path_coordinates) - 1):
    x1, y1 = path_coordinates[i]
    x2, y2 = path_coordinates[i + 1]
    plt.plot([x1, x2], [y1, y2], '-o')


for idx, (x, y) in enumerate(path_coordinates[:-1]):
    plt.annotate(idx, (x, y), fontsize=12, ha='right')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('optim')
plt.grid()
plt.show()
