# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 12:52:10 2023

@author: ADAMS-LAB
"""

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
all_distances = []
for kk in range(10):
    opt = ACO_optimizer(city_ids, coordinates)
    distance, path, convergence_history = opt.optimize(100)
    all_distances.append(distance)
    
    
    import matplotlib.pyplot as plt
    
    
    path_coordinates = [coordinates[int(city)] for city in path]
    
    
    for i in range(len(path_coordinates) - 1):
        x1, y1 = path_coordinates[i]
        x2, y2 = path_coordinates[i + 1]
        plt.plot([x1, x2], [y1, y2], '-o')
    
    
    for idx, (x, y) in enumerate(path_coordinates[:-1]):
        plt.annotate(idx, (x, y), fontsize=12, ha='right')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Final Path _ run ' + str(kk))
    plt.grid()
    plt.show()
    plt.plot([x for x in convergence_history])
    plt.xlabel("iterations")
    plt.ylabel("distance")
    plt.title("aco_"+str(kk))
    # plt.savefig("aco.png")
    plt.show()
