import collections
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
import math
from lexicographic import solve_linear_problem
from secondObjective import solve_linear_problem2
from secondObjective import solve_proportional_robust_controller_placement_integral
np.set_printoptions(threshold=sys.maxsize)

def twoNodesAttacked():
    # Define the nodes
    sa_nodes = {
        1: {'sa_node_y': 32.45, 'sa_node_x': -99.739998, 'sa_node_label': 'Abilene'},
        2: {'sa_node_y': 42.6699982, 'sa_node_x': -73.8000029, 'sa_node_label': 'Albany'},
        3: {'sa_node_y': 35.119977, 'sa_node_x': -106.61997, 'sa_node_label': 'Albuquerque'},
        4: {'sa_node_y': 33.7599982, 'sa_node_x': -84.4199987, 'sa_node_label': 'Atlanta'},
        5: {'sa_node_y': 30.3099988, 'sa_node_x': -97.7500018, 'sa_node_label': 'Austin'},
        6: {'sa_node_y': 39.2999992, 'sa_node_x': -76.6100008, 'sa_node_label': 'Baltimore'},
        7: {'sa_node_y': 30.4499996, 'sa_node_x': -91.1299968, 'sa_node_label': 'Baton_Rouge'},
        8: {'sa_node_y': 45.79000104, 'sa_node_x': -108.5400006, 'sa_node_label': 'Billings'},
        9: {'sa_node_y': 33.5299985, 'sa_node_x': -86.8000029, 'sa_node_label': 'Birmingham'},
        10: {'sa_node_y': 46.81000154, 'sa_node_x': -100.7699965, 'sa_node_label': 'Bismarck'},
        11: {'sa_node_y': 42.3400005, 'sa_node_x': -71.0199959, 'sa_node_label': 'Bostons'},
        12: {'sa_node_y': 42.8899993, 'sa_node_x': -78.860001, 'sa_node_label': 'Buffalo'},
        13: {'sa_node_y': 32.7900008, 'sa_node_x': -79.9899982, 'sa_node_label': 'Charleston'},
        14: {'sa_node_y': 35.2, 'sa_node_x': -80.83, 'sa_node_label': 'Charlotte'},
        15: {'sa_node_y': 41.839997, 'sa_node_x': -87.680001, 'sa_node_label': 'Chicago'},
        16: {'sa_node_y': 39.1399991, 'sa_node_x': -84.5100027, 'sa_node_label': 'Cincinnati'},
        17: {'sa_node_y': 41.4799992, 'sa_node_x': -81.6800014, 'sa_node_label': 'Cleveland'},
        18: {'sa_node_y': 39.990002, 'sa_node_x': -82.989997, 'sa_node_label': 'Columbus'},
        19: {'sa_node_y': 32.79, 'sa_node_x': -96.77, 'sa_node_label': 'Dallas'},
        20: {'sa_node_y': 39.77000271, 'sa_node_x': -104.8700036, 'sa_node_label': 'Denver'},
        21: {'sa_node_y': 42.3800019, 'sa_node_x': -83.0999998, 'sa_node_label': 'Detroit'},
        22: {'sa_node_y': 31.84981, 'sa_node_x': -106.4396, 'sa_node_label': 'El_Paso'},
        23: {'sa_node_y': 36.7800007, 'sa_node_x': -119.790002, 'sa_node_label': 'Fresno'},
        24: {'sa_node_y': 36.0800024, 'sa_node_x': -79.8300018, 'sa_node_label': 'Greensboro'},
        25: {'sa_node_y': 41.7700004, 'sa_node_x': -72.6800003, 'sa_node_label': 'Hartford'},
        26: {'sa_node_y': 29.77, 'sa_node_x': -95.39, 'sa_node_label': 'Houston'},
        27: {'sa_node_y': 30.330003, 'sa_node_x': -81.660002, 'sa_node_label': 'Jacksonville'},
        28: {'sa_node_y': 39.1199992, 'sa_node_x': -94.7300038, 'sa_node_label': 'Kansas_City'},
        29: {'sa_node_y': 36.20999, 'sa_node_x': -115.2199, 'sa_node_label': 'Las_Vegas'},
        30: {'sa_node_y': 34.72, 'sa_node_x': -92.35, 'sa_node_label': 'Little_Rock'},
        31: {'sa_node_y': 40.5899999, 'sa_node_x': -73.6699993, 'sa_node_label': 'Long_Island'},
        32: {'sa_node_y': 34.110001, 'sa_node_x': -118.410002, 'sa_node_label': 'Los_Angeles'},
        33: {'sa_node_y': 38.2200009, 'sa_node_x': -85.7399979, 'sa_node_label': 'Louisville'},
        34: {'sa_node_y': 35.110001, 'sa_node_x': -90.010004, 'sa_node_label': 'Memphis'},
        35: {'sa_node_y': 25.7800006, 'sa_node_x': -80.2099997, 'sa_node_label': 'Miami'},
        36: {'sa_node_y': 43.0600013, 'sa_node_x': -87.9700005, 'sa_node_label': 'Milwaukee'},
        37: {'sa_node_y': 44.9599988, 'sa_node_x': -93.2699973, 'sa_node_label': 'Minneapolis'},
        38: {'sa_node_y': 36.1699984, 'sa_node_x': -86.7799989, 'sa_node_label': 'Nashville'},
        39: {'sa_node_y': 30.07, 'sa_node_x': -89.93, 'sa_node_label': 'New_Orleans'},
        40: {'sa_node_y': 40.6699983, 'sa_node_x': -73.9400035, 'sa_node_label': 'New_York'},
        41: {'sa_node_y': 40.7200012, 'sa_node_x': -74.1699986, 'sa_node_label': 'Newark'},
        42: {'sa_node_y': 36.9199982, 'sa_node_x': -76.2399978, 'sa_node_label': 'Norfolk'},
        43: {'sa_node_y': 37.77000071, 'sa_node_x': -122.2200016, 'sa_node_label': 'Oakland'},
        44: {'sa_node_y': 35.4700015, 'sa_node_x': -97.5100028, 'sa_node_label': 'Oklahoma_City'},
        45: {'sa_node_y': 41.2599984, 'sa_node_x': -96.0100022, 'sa_node_label': 'Omaha'},
        46: {'sa_node_y': 28.4999994, 'sa_node_x': -81.370003, 'sa_node_label': 'Orlando'},
        47: {'sa_node_y': 40.0099985, 'sa_node_x': -75.1299964, 'sa_node_label': 'Philadelphia'},
        48: {'sa_node_y': 33.54000058, 'sa_node_x': -112.0699996, 'sa_node_label': 'Phoenix'},
        49: {'sa_node_y': 40.3, 'sa_node_x': -80.13, 'sa_node_label': 'Pittsburgh'},
        50: {'sa_node_y': 45.54000072, 'sa_node_x': -122.6600035, 'sa_node_label': 'Portland'},
        51: {'sa_node_y': 41.82, 'sa_node_x': -71.42, 'sa_node_label': 'Providence'},
        52: {'sa_node_y': 35.8199995, 'sa_node_x': -78.6600034, 'sa_node_label': 'Raleigh'},
        53: {'sa_node_y': 37.5299986, 'sa_node_x': -77.4700015, 'sa_node_label': 'Richmond'},
        54: {'sa_node_y': 43.1699985, 'sa_node_x': -77.620003, 'sa_node_label': 'Rochester'},
        55: {'sa_node_y': 38.56999946, 'sa_node_x': -121.4700016, 'sa_node_label': 'Sacramento'},
        56: {'sa_node_y': 40.77999863, 'sa_node_x': -111.9300007, 'sa_node_label': 'Salt_Lake_City'},
        57: {'sa_node_y': 29.459997, 'sa_node_x': -98.510002, 'sa_node_label': 'San_Antonio'},
        58: {'sa_node_y': 32.8100017, 'sa_node_x': -117.139999, 'sa_node_label': 'San_Diego'},
        59: {'sa_node_y': 37.65999942, 'sa_node_x': -122.4199987, 'sa_node_label': 'San_Francisco'},
        60: {'sa_node_y': 37.29999947, 'sa_node_x': -121.8499985, 'sa_node_label': 'San_Jose'},
        61: {'sa_node_y': 34.43000021, 'sa_node_x': -119.7200014, 'sa_node_label': 'Santa_Barbara'},
        62: {'sa_node_y': 41.4, 'sa_node_x': -75.67, 'sa_node_label': 'Scranton'},
        63: {'sa_node_y': 47.61999916, 'sa_node_x': -122.3499985, 'sa_node_label': 'Seattle'},
        64: {'sa_node_y': 47.66999805, 'sa_node_x': -117.4100038, 'sa_node_label': 'Spokane'},
        65: {'sa_node_y': 39.5, 'sa_node_x': -89.4, 'sa_node_label': 'Springfield'},
        66: {'sa_node_y': 38.64, 'sa_node_x': -90.24, 'sa_node_label': 'St_Louis'},
        67: {'sa_node_y': 43.040001, 'sa_node_x': -76.1399993, 'sa_node_label': 'Syracuse'},
        68: {'sa_node_y': 30.46, 'sa_node_x': -84.28, 'sa_node_label': 'Tallahassee'},
        69: {'sa_node_y': 27.9599988, 'sa_node_x': -82.4800035, 'sa_node_label': 'Tampa'},
        70: {'sa_node_y': 41.659997, 'sa_node_x': -83.58, 'sa_node_label': 'Toledo'},
        71: {'sa_node_y': 32.2, 'sa_node_x': -110.89, 'sa_node_label': 'Tucson'},
        72: {'sa_node_y': 36.13, 'sa_node_x': -95.92, 'sa_node_label': 'Tulsa'},
        73: {'sa_node_y': 38.9100003, 'sa_node_x': -77.0199965, 'sa_node_label': 'Washington_DC'},
        74: {'sa_node_y': 26.7499997, 'sa_node_x': -80.1299975, 'sa_node_label': 'West_Palm_Beach'},
        75: {'sa_node_y': 39.7400018, 'sa_node_x': -75.5299989, 'sa_node_label': 'Wilmington'}
    }
    # Nodes Of Kristi - Europe
    # sa_nodes = {
    #     1: {'sa_node_y': 52.52, 'sa_node_x': 13.4, 'sa_node_label': 'Berlin'},
    #     2: {'sa_node_y': 38.12, 'sa_node_x': 13.35, 'sa_node_label': 'Palermo'},
    #     3: {'sa_node_y': 37.38, 'sa_node_x': -5.98, 'sa_node_label': 'Seville'},
    #     4: {'sa_node_y': 50.05, 'sa_node_x': 19.95, 'sa_node_label': 'Cracow'},
    #     5: {'sa_node_y': 48.58, 'sa_node_x': 7.77, 'sa_node_label': 'Strasbourg'},
    #     6: {'sa_node_y': 48.87, 'sa_node_x': 2.33, 'sa_node_label': 'Paris'},
    #     7: {'sa_node_y': 52.25, 'sa_node_x': 21, 'sa_node_label': 'Warsaw'},
    #     8: {'sa_node_y': 44.83, 'sa_node_x': 20.5, 'sa_node_label': 'Belgrade'},
    #     9: {'sa_node_y': 45.47, 'sa_node_x': 9.17, 'sa_node_label': 'Milan'},
    #     10: {'sa_node_y': 48.22, 'sa_node_x': 16.37, 'sa_node_label': 'Vienna'},
    #     11: {'sa_node_y': 52.47, 'sa_node_x': -1.88, 'sa_node_label': 'Birmingham'},
    #     12: {'sa_node_y': 47.5, 'sa_node_x': 19.08, 'sa_node_label': 'Budapest'},
    #     13: {'sa_node_y': 50.08, 'sa_node_x': 14.43, 'sa_node_label': 'Prague'},
    #     14: {'sa_node_y': 59.33, 'sa_node_x': 18.05, 'sa_node_label': 'Stockholm'},
    #     15: {'sa_node_y': 38.73, 'sa_node_x': -9.13, 'sa_node_label': 'Lisbon'},
    #     16: {'sa_node_y': 40.42, 'sa_node_x': -3.72, 'sa_node_label': 'Madrid'},
    #     17: {'sa_node_y': 60.17, 'sa_node_x': 24.97, 'sa_node_label': 'Helsinki'},
    #     18: {'sa_node_y': 55.72, 'sa_node_x': 12.57, 'sa_node_label': 'Copenhagen'},
    #     19: {'sa_node_y': 47.38, 'sa_node_x': 8.55, 'sa_node_label': 'Zurich'},
    #     20: {'sa_node_y': 59.93, 'sa_node_x': 10.75, 'sa_node_label': 'Oslo'},
    #     21: {'sa_node_y': 43.3, 'sa_node_x': 5.37, 'sa_node_label': 'Marseille'},
    #     22: {'sa_node_y': 50.1, 'sa_node_x': 8.67, 'sa_node_label': 'Frankfurt'},
    #     23: {'sa_node_y': 41.88, 'sa_node_x': 12.5, 'sa_node_label': 'Rome'},
    #     24: {'sa_node_y': 53.55, 'sa_node_x': 10.02, 'sa_node_label': 'Hamburg'},
    #     25: {'sa_node_y': 38, 'sa_node_x': 23.73, 'sa_node_label': 'Athens'},
    #     26: {'sa_node_y': 44.85, 'sa_node_x': -0.57, 'sa_node_label': 'Bordeaux'},
    #     27: {'sa_node_y': 41.37, 'sa_node_x': 2.18, 'sa_node_label': 'Barcelona'},
    #     28: {'sa_node_y': 45.73, 'sa_node_x': 4.83, 'sa_node_label': 'Lyon'},
    #     29: {'sa_node_y': 51.5, 'sa_node_x': -0.17, 'sa_node_label': 'London'},
    #     30: {'sa_node_y': 51.23, 'sa_node_x': 6.78, 'sa_node_label': 'Dusseldorf'},
    #     31: {'sa_node_y': 45.83, 'sa_node_x': 16.02, 'sa_node_label': 'Zagreb'},
    #     32: {'sa_node_y': 42.75, 'sa_node_x': 23.33, 'sa_node_label': 'Sofia'},
    #     33: {'sa_node_y': 52.35, 'sa_node_x': 4.9, 'sa_node_label': 'Amsterdam'},
    #     34: {'sa_node_y': 53.33, 'sa_node_x': -6.25, 'sa_node_label': 'Dublin'},
    #     35: {'sa_node_y': 50.83, 'sa_node_x': 4.35, 'sa_node_label': 'Brussels'},
    #     36: {'sa_node_y': 48.13, 'sa_node_x': 11.57, 'sa_node_label': 'Munich'},
    #     37: {'sa_node_y': 55.85, 'sa_node_x': -4.25, 'sa_node_label': 'Glasgow'},

    # }



    # sa_nodes = {
    #     1: {'sa_node_y': 15, 'sa_node_x': -20, 'sa_node_label': 'A'},
    #     2: {'sa_node_y': 25, 'sa_node_x': -10, 'sa_node_label': 'B'},
    #     3: {'sa_node_y': 8, 'sa_node_x': -10, 'sa_node_label': 'C'},
    #     4: {'sa_node_y': 5, 'sa_node_x': 0, 'sa_node_label': 'D'},
    #     5: {'sa_node_y': 15, 'sa_node_x': 0, 'sa_node_label': 'E'},
    #     6: {'sa_node_y': 8, 'sa_node_x': 10, 'sa_node_label': 'F'},
    #     7: {'sa_node_y': 15, 'sa_node_x': 20, 'sa_node_label': 'G'},
    #     8: {'sa_node_y': 25, 'sa_node_x': 10, 'sa_node_label': 'H'},
    # }

    sa_links = [
        (19, 1, {'sa_link_length': 336.9509334}),
        (22, 1, {'sa_link_length': 761.2090776}),
        (11, 2, {'sa_link_length': 277.0649613}),
        (67, 2, {'sa_link_length': 234.2212201}),
        (19, 3, {'sa_link_length': 1133.443119}),
        (20, 3, {'sa_link_length': 647.7371779}),
        (22, 3, {'sa_link_length': 436.9494668}),
        (29, 3, {'sa_link_length': 943.5364333}),
        (9, 4, {'sa_link_length': 266.2280948}),
        (14, 4, {'sa_link_length': 439.2379644}),
        (27, 4, {'sa_link_length': 554.1108875}),
        (26, 5, {'sa_link_length': 282.0488176}),
        (57, 5, {'sa_link_length': 143.5525064}),
        (47, 6, {'sa_link_length': 179.1949651}),
        (49, 6, {'sa_link_length': 384.8187539}),
        (73, 6, {'sa_link_length': 67.17947405}),
        (26, 7, {'sa_link_length': 500.1517957}),
        (39, 7, {'sa_link_length': 147.3504058}),
        (10, 8, {'sa_link_length': 729.0170987}),
        (20, 8, {'sa_link_length': 880.041712}),
        (64, 8, {'sa_link_length': 848.8579799}),
        (47, 6, {'sa_link_length': 179.1949651}),
        (49, 6, {'sa_link_length': 384.8187539}),
        (73, 6, {'sa_link_length': 67.17947405}),
        (26, 7, {'sa_link_length': 500.1517957}),
        (39, 7, {'sa_link_length': 147.3504058}),
        (10, 8, {'sa_link_length': 729.0170987}),
        (20, 8, {'sa_link_length': 880.041712}),
        (64, 8, {'sa_link_length': 848.8579799}),
        (38, 9, {'sa_link_length': 352.382908}),
        (39, 9, {'sa_link_length': 582.4644304}),
        (37, 10, {'sa_link_length': 738.9401642}),
        (51, 11, {'sa_link_length': 79.92293577}),
        (17, 12, {'sa_link_length': 336.4337393}),
        (54, 12, {'sa_link_length': 126.6263824}),
        (27, 13, {'sa_link_length': 379.311106}),
        (52, 13, {'sa_link_length': 430.1818131}),
        (24, 14, {'sa_link_length': 159.8834469}),
        (21, 15, {'sa_link_length': 459.1452686}),
        (36, 15, {'sa_link_length': 165.3264805}),
        (65, 15, {'sa_link_length': 357.5730073}),
        (18, 16, {'sa_link_length': 193.2153767}),
        (33, 16, {'sa_link_length': 177.4925816}),
        (73, 16, {'sa_link_length': 777.0507392}),
        (18, 17, {'sa_link_length': 238.9630572}),
        (70, 17, {'sa_link_length': 191.2436294}),
        (49, 18, {'sa_link_length': 294.7135669}),
        (26, 19, {'sa_link_length': 432.7312491}),
        (30, 19, {'sa_link_length': 553.9582807}),
        (44, 19, {'sa_link_length': 366.9361351}),
        (45, 20, {'sa_link_length': 920.3373588}),
        (56, 20, {'sa_link_length': 731.2717231}),
        (70, 21, {'sa_link_length': 107.2436957}),
        (57, 22, {'sa_link_length': 964.4531908}),
        (71, 22, {'sa_link_length': 505.7485307}),
        (29, 23, {'sa_link_length': 496.1990407}),
        (32, 23, {'sa_link_length': 386.6707817}),
        (43, 23, {'sa_link_length': 289.9410618}),
        (33, 24, {'sa_link_length': 690.4091794}),
        (52, 24, {'sa_link_length': 131.0972102}),
        (53, 24, {'sa_link_length': 317.8965469}),
        (31, 25, {'sa_link_length': 186.2707622}),
        (51, 25, {'sa_link_length': 125.5599482}),
        (46, 27, {'sa_link_length': 246.5770348}),
        (45, 28, {'sa_link_length': 314.0322058}),
        (66, 28, {'sa_link_length': 470.8657976}),
        (72, 28, {'sa_link_length': 418.4383844}),
        (48, 29, {'sa_link_length': 495.9003239}),
        (56, 29, {'sa_link_length': 700.0051286}),
        (34, 30, {'sa_link_length': 261.3433471}),
        (40, 31, {'sa_link_length': 29.36152283}),
        (58, 32, {'sa_link_length': 223.8445086}),
        (61, 32, {'sa_link_length': 150.6766134}),
        (38, 33, {'sa_link_length': 295.1182142}),
        (66, 33, {'sa_link_length': 473.8016755}),
        (38, 34, {'sa_link_length': 377.8363294}),
        (69, 35, {'sa_link_length': 397.1149107}),
        (74, 35, {'sa_link_length': 129.8250315}),
        (37, 36, {'sa_link_length': 568.3338475}),
        (45, 37, {'sa_link_length': 561.3270039}),
        (68, 39, {'sa_link_length': 653.3593336}),
        (41, 40, {'sa_link_length': 24.21353477}),
        (62, 40, {'sa_link_length': 199.5750874}),
        (75, 40, {'sa_link_length': 204.1516726}),
        (47, 41, {'sa_link_length': 136.0604521}),
        (52, 42, {'sa_link_length': 298.6558234}),
        (75, 42, {'sa_link_length': 383.6690534}),
        (55, 43, {'sa_link_length': 132.6490217}),
        (56, 43, {'sa_link_length': 1135.717402}),
        (59, 43, {'sa_link_length': 25.71991716}),
        (72, 44, {'sa_link_length': 193.3587768}),
        (74, 46, {'sa_link_length': 275.7928548}),
        (62, 47, {'sa_link_length': 193.4089904}),
        (58, 48, {'sa_link_length': 574.6750816}),
        (71, 48, {'sa_link_length': 222.4582756}),
        (62, 49, {'sa_link_length': 473.5653806}),
        (55, 50, {'sa_link_length': 937.7404056}),
        (56, 50, {'sa_link_length': 1221.189289}),
        (63, 50, {'sa_link_length': 279.0817311}),
        (73, 53, {'sa_link_length': 190.1446685}),
        (67, 54, {'sa_link_length': 145.265921}),
        (60, 59, {'sa_link_length': 77.16267231}),
        (61, 60, {'sa_link_length': 446.9898708}),
        (67, 62, {'sa_link_length': 223.7750822}),
        (64, 63, {'sa_link_length': 444.2069519}),
        (66, 65, {'sa_link_length': 144.0599684}),
        (69, 68, {'sa_link_length': 394.0942686})
    ]
    
    # Kristi's Links - Europe
    # sa_links = [    
    #     (1, 7, {'sa_link_length': 516.43}),
    #     (1, 13, {'sa_link_length': 280.6}),  
    #     (1, 36, {'sa_link_length': 505.09}),   
    #     (1, 18, {'sa_link_length': 359.9}),    
    #     (1, 24, {'sa_link_length': 253.33}),
    #     (2, 25, {'sa_link_length': 908.4}),
    #     (2, 23, {'sa_link_length': 424.31}),
    #     (3, 15, {'sa_link_length': 313.98}),
    #     (3, 27, {'sa_link_length': 829.37}),
    #     (4, 7, {'sa_link_length': 255.35}),
    #     (4, 12, {'sa_link_length': 290.62}),
    #     (5, 6, {'sa_link_length': 400.25}),
    #     (5, 22, {'sa_link_length': 181.15}),
    #     (5, 19, {'sa_link_length': 145.52}),
    #     (6, 28, {'sa_link_length': 396.74}),
    #     (6, 29, {'sa_link_length': 342.31}),
    #     (6, 35, {'sa_link_length': 261.65}),
    #     (6, 26, {'sa_link_length': 498.33}),
    #     (7, 17, {'sa_link_length': 913.83}),
    #     (8, 32, {'sa_link_length': 324.14}),
    #     (8, 31, {'sa_link_length': 367.38}),
    #     (8, 12, {'sa_link_length': 316.38}),
    #     (9, 23, {'sa_link_length': 480.6}),
    #     (9, 36, {'sa_link_length': 347.6}),
    #     (9, 19, {'sa_link_length': 217.63}),
    #     (10, 31, {'sa_link_length':267.08}),
    #     (10, 13, {'sa_link_length': 250.35}),
    #     (10, 36, {'sa_link_length': 356.01}),
    #     (11, 29, {'sa_link_length': 159.2}),
    #     (11, 37, {'sa_link_length': 406.22}),
    #     (12, 13, {'sa_link_length': 445.21}),
    #     (14, 17, {'sa_link_length': 398.53}), 
    #     (14, 18, {'sa_link_length': 517.52}), 
    #     (15, 16, {'sa_link_length': 500.2}), 
    #     (15, 29, {'sa_link_length': 1581.72}), 
    #     (16, 27, {'sa_link_length': 506.93}),
    #     (16, 26, {'sa_link_length': 555.81}), 
    #     (17, 20, {'sa_link_length': 788.32}),
    #     (18, 20, {'sa_link_length': 480.33}), 
    #     (19, 28, {'sa_link_length': 338.43}), 
    #     (21, 28, {'sa_link_length': 273.57}),
    #     (21, 23, {'sa_link_length': 604.45}),
    #     (21, 27, {'sa_link_length': 338.79}),
    #     (21, 26, {'sa_link_length': 504.7}),
    #     (22, 30, {'sa_link_length': 183.11}),
    #     (22, 36, {'sa_link_length': 304.15}), 
    #     (22, 24, {'sa_link_length': 394.66}), 
    #     (23, 31, {'sa_link_length': 521.96}), 
    #     (24, 33, {'sa_link_length': 367.96}), 
    #     (25, 32, {'sa_link_length': 529.26}), 
    #     (25, 31, {'sa_link_length': 1078.24}), 
    #     (29, 33, {'sa_link_length': 360.2}), 
    #     (29, 34, {'sa_link_length': 459.63}), 
    #     (30, 35, {'sa_link_length': 175.65}),
    #     (33, 35, {'sa_link_length': 173.23}),
    #     (33, 37, {'sa_link_length': 711.44}),
    #     (34, 37, {'sa_link_length': 308.39}),
    #     ]
    
    # sa_links = [
    #     (3, 1, {'sa_link_length': 10}),
    #     (2, 1, {'sa_link_length': 761.2090776}),
    #     (3, 2, {'sa_link_length': 277.0649613}),
    #     (4, 2, {'sa_link_length': 234.2212201}),
    #     (5, 2, {'sa_link_length': 1133.443119}),
    #     (4, 3, {'sa_link_length': 647.7371779}),
    #     (5, 4, {'sa_link_length': 436.9494668}),
    #     (6, 4, {'sa_link_length': 943.5364333}),
    #     (7, 4, {'sa_link_length': 266.2280948}),
    #     (8, 4, {'sa_link_length': 439.2379644}),
    #     (8, 5, {'sa_link_length': 554.1108875}),
    #     (7, 6, {'sa_link_length': 282.0488176}),
    #     (7, 8, {'sa_link_length': 143.5525064})
    # ]


    # Create graph
    G = nx.Graph()

    # Add nodes to the graph
    for node_id, node_attrs in sa_nodes.items():
        G.add_node(node_id, **node_attrs)

    # Add links to the graph
    for link in sa_links:
        node_a, node_b, link_attrs = link
        G.add_edge(node_a, node_b, **link_attrs)

    # Draw the graph
    pos = {node: (attrs['sa_node_x'], attrs['sa_node_y']) for node, attrs in sa_nodes.items()}
    labels = {node: attrs['sa_node_label'] for node, attrs in sa_nodes.items()}
    fig = plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, labels=labels)
    # plt.show()



    '''# initialize adjacency matrix
    adj_matrix = np.zeros((n_nodes, n_nodes))
    print(len(adj_matrix))

    np.set_printoptions(threshold=sys.maxsize)'''
    '''for edge in G.edges():
        node1 = edge[0]
        node2 = edge[1]
        adj_matrix[node1][node2] = 1
        adj_matrix[node2][node1] = 1'''
    '''
    # fill adjacency matrix based on edges in sa_links
    for edge in sa_links:
        node1 = edge[0]
        node2 = edge[1]
        node1_idx = list(sa_nodes.keys()).index(node1)
        node2_idx = list(sa_nodes.keys()).index(node2)
        adj_matrix[node1_idx][node2_idx] = 1
        adj_matrix[node2_idx][node1_idx] = 1

    print(adj_matrix)'''


    adj_matrix = nx.adjacency_matrix(G).todense()
    adj_matrixOriginal = nx.adjacency_matrix(G)
    ##print(adj_matrix)
    ##print(adj_matrixOriginal)

    #controller_nodes=[4,75]
    controller_nodes=  [1,1,1,11]
    '''# Add 5 random controllers to the graph
    num_controllers = 5
    controller_nodes = random.sample(list(G.nodes), num_controllers)
    for node in controller_nodes:
        G.nodes[node]['controller'] = True


    '''

    sa_attack_nodes = {
        1:{15, 38, 39, 66},
        2:{7, 15, 38, 66},
        3:{15, 34, 39, 66},
        4:{15, 19, 28, 39},
        5:{7, 15, 34, 66},
        6:{15, 30, 39, 66},
        7:{15, 26, 38, 66},
        8:{15, 19, 39, 66},
        9:{15, 26, 34, 66},
        10:{7, 15, 30, 66},
        11:{7, 15, 19, 28},
        12:{19, 28, 36, 39}
    }
 
 
    # sa_attack_nodes = {
    #     1:{1, 6, 12, 21, 22, 29},
    #     2:{1, 6, 12, 15, 21, 22},
    #     3:{1, 6, 12, 21, 22, 33},
    #     4:{1, 6, 9, 12, 21, 22},
    #     5:{1, 4, 6, 21, 22, 29},
    #     6:{1, 4, 6, 15, 21, 22},
    #     7:{1, 4, 6, 9, 21, 22},
    #     8:{1, 4, 6, 21, 22, 33},
    #     9:{1, 6, 12, 19, 21, 22},
    #     10:{1, 6, 7, 9, 21, 22},
    #     11:{1, 6, 7, 21, 22, 29},
    #     12:{1, 4, 6, 19,21,22}}
    
    sa_attack_nodes = {
        1: {15, 19, 22, 24, 33, 40},
        2: {15, 19, 22, 24, 33, 75},
        3: {15, 19, 22, 33, 53, 75},
        4: {15, 19, 22, 33, 42, 53},
        5: {15, 19, 22, 33, 42, 73},
        6: {15, 19, 22, 33, 52, 73},
        7: {15, 19, 22, 33, 40, 53},
        8: {15, 19, 22, 33, 52, 53},
        9: {15, 19, 22, 24, 33, 42},
        10: {15, 19, 22, 33, 73, 75},
        11: {15, 19, 22, 24, 33, 52},
        12: {15, 19, 22, 33, 40, 73},
        13: {64, 65, 41, 12, 47, 22, 59},
        14: {33, 36, 4, 74, 17},
        15: {1, 35, 4, 70, 19},
        16: {65, 9, 68, 23},
        17: {64, 5, 12, 57, 62},
        18: {3, 41, 9, 47, 18},
        19: {37, 7, 9, 44, 54},
        20: {34, 72, 17, 51, 57, 62},
        21: {68, 70, 41, 48, 50, 19, 22},
        22: {3, 41, 12, 56, 58},
        23: {65, 67, 14, 15, 54, 61} }
    
    # sa_attack_nodes = {
    #     1:{4, 5, 6},
    #     2:{2, 5, 7},
    #     3:{2, 4, 6}
    # }
    # sa_attack_nodes = {
    #     1 : {17, 19, 20, 22, 24, 27, 33, 37, 39, 40, 50, 67},
    #     2 : {10, 17, 19, 20, 22, 24, 27, 33, 39, 40, 50, 67},
    #     3 : {17, 19, 20, 22, 24, 27, 33, 37, 39, 40, 50, 62},
    #     4 : {17, 19, 20, 22, 24, 27, 33, 37, 39, 40, 63, 67},
    #     5 : {15, 17, 19, 20, 22, 24, 27, 33, 39, 40, 50, 67},
    #     6 : {4, 17, 19, 20, 22, 33, 37, 39, 40, 50, 52, 67},
    #     7 : {15, 18, 19, 20, 22, 24, 27, 33, 39, 40, 50, 67},
    #     8 : {8, 17, 19, 20, 22, 24, 27, 33, 39, 40, 50, 67},
    #     9 : {17, 19, 20, 22, 24, 27, 28, 33, 39, 40, 50, 67},
    #     10 : {10, 17, 19, 20, 22, 24, 27, 33, 39, 40, 50, 62},
    #     11 : {15, 19, 22, 24, 27, 29, 33, 39, 40, 43, 45, 67},
    #     12 : {17, 19, 20, 22, 24, 27, 28, 33, 39, 40,63,67}}
    # sa_attack_nodes = {
    # 1 : {17, 19, 20, 24, 27, 33, 39, 40, 50, 67},
    # 2 : {17, 19, 20, 22, 24, 27, 33, 39, 40, 63},
    # 3 : {17, 19, 20, 22, 24, 33, 39, 40, 63, 67},
    # 4 : {17, 19, 20, 22, 24, 27, 33, 40, 63, 67},
    # 5 : {17, 19, 20, 22, 24, 27, 33, 39, 40, 64},
    # 6 : {17, 19, 20, 22, 24, 33, 39, 40, 50, 67},
    # 7 : {7, 19, 20, 22, 24, 27, 33, 40, 50, 67},
    # 8 : {17, 19, 20, 22, 24, 27, 33, 39, 40, 50},
    # 9 : {17, 19, 20, 22, 24, 27, 33, 40, 64, 67},
    # 10 : {17, 19, 20, 22, 24, 33, 39, 40, 64, 67},
    # 11 : {15, 19, 22, 24, 27, 33, 39, 40, 45, 67},
    # 12 : {19, 20, 22, 24, 27, 33, 39, 40,50,70},
    # 13 : {40, 20, 5},
    # 14 : {65, 66, 34, 14, 19},
    # 15 : {66, 44, 46, 19, 24, 28, 29},
    # 16 : {35, 74, 46, 54, 27},
    # 17 : {1, 70, 38, 53, 27, 63},
    # 18 : {69, 5, 14},
    # 19 : {33, 2, 11, 18, 19},
    # 20 : {3, 5, 7, 51, 24, 26, 27},
    # 21 : {32, 5, 15, 48, 50, 52, 62},
    # 22 : {42, 43, 21, 54, 63},
    # 23 : {71, 40, 73, 12, 18} }
    # Generate 12 random attacks
    # sa_attack_nodes = {
    #     1:{1, 6, 9, 12, 15, 17, 21, 22, 31, 33},
        # 2:{1, 6, 9, 12, 17, 21, 22, 29, 31, 33},
        # 3:{1, 6, 9, 10, 12, 15, 17, 21, 22, 33},
        # 4:{1, 6, 8, 9, 10, 15, 17, 21, 22, 33},
        # 5:{1, 6, 7, 8, 9, 10, 15, 21, 22, 33},
        # 6:{1, 6, 7, 9, 12, 15, 21, 22, 31, 33},
        # 7:{1, 6, 9, 12, 17, 21, 22, 29, 31, 37},
        # 8:{1, 6, 8, 9, 10, 17, 21, 22, 29, 33},
        # 9:{1, 6, 9, 10, 12, 17, 21, 22, 29, 33},
        # 10:{1, 6, 7, 8, 9, 10, 21, 22, 29, 33},
        # 11:{1, 6, 7, 9, 12, 21, 22, 29, 31, 33},
        # 12:{1, 6, 9, 12, 15, 21, 22, 25,31,33}}
    # }
    sa_attack_nodes = {
        1 : {17, 19, 20, 22, 24, 33, 42, 63},
        2 : {17, 19, 20, 22, 33, 52, 53, 63},
        3 : {17, 19, 20, 22, 24, 33, 42, 50},
        4 : {17, 19, 20, 22, 24, 33, 42, 64},
        5 : {17, 19, 20, 22, 33, 42, 53, 63},
        6 : {17, 19, 20, 22, 33, 50, 52, 53},
        7 : {17, 19, 20, 22, 24, 33, 52, 63},
        8 : {17, 19, 20, 22, 24, 33, 63, 75},
        9 : {17, 19, 20, 22, 33, 52, 53, 64},
        10 : {17, 19, 20, 22, 33, 52, 63, 73},
        11 : {19, 22, 24, 28, 37, 38, 40, 67},
        12 : {17, 19, 20, 22, 33, 42,50,53},    
        13 : {64, 65, 41, 12, 47, 22, 59},
        14 : {33, 36, 4, 74, 17},
        15 : {1, 35, 4, 70, 19},
        16 : {65, 9, 68, 23},
        17 : {64, 5, 12, 57, 62},
        18 : {3, 41, 9, 47, 18},
        19 : {37, 7, 9, 44, 54},
        20 : {34, 72, 17, 51, 57, 62},
        21 : {68, 70, 41, 48, 50, 19, 22},
        22 : {3, 41, 12, 56, 58},
        23 : {65, 67, 14, 15, 54, 61}  
        }

    sa_attack_nodes = {
        1 : {3, 43, 13, 14, 50, 57, 27, 29},
        2 : {64, 1, 33, 70, 40, 73, 72, 15},
        3 : {32, 33, 8, 44, 48, 21, 58, 63},
        4 : {64, 34, 67, 36, 5, 73, 43, 15},
        5 : {68, 4, 39, 16, 19, 20, 56, 30},
        6 : {56, 4, 6, 39, 44, 18, 24, 26},
        7 : {64, 34, 7, 39, 10, 11, 14, 56},
        8 : {3, 4, 71, 10, 17, 55, 26, 28},
        9 : {66, 3, 8, 44, 13, 17, 19, 60},
        10 : {8, 11, 12, 45, 13, 19, 55, 56},
        11 : {67, 68, 6, 39, 70, 53, 56, 62},
        12 : {1, 34, 5, 73, 48, 52, 54, 57},
        13 : {2, 36, 41, 17, 21, 55, 24, 31},
        14 : {2, 34, 44, 21, 23, 56, 57, 61},
        15 : {32, 8, 72, 74, 11, 48, 16, 62},
        16 : {4, 37, 36, 7, 72, 73, 13, 51},
        17 : {34, 35, 71, 60, 54, 58, 27, 28},
        18 : {32, 34, 14, 15, 49, 19, 59, 60},
        19 : {33, 1, 67, 10, 11, 47, 27, 62},
        20 : {69, 46, 48, 16, 53, 54, 58, 30},
        21 : {70, 8, 73, 40, 43, 16, 53, 58},
        22 : {1, 67, 40, 42, 13, 46, 56, 63},
        23 : {36, 4, 8, 41, 20, 55, 59, 61},
        24 : {5, 7, 48, 17, 20, 57, 59, 60},
        25 : {4, 36, 7, 44, 50, 22, 26, 62},
        26 : {34, 3, 67, 38, 7, 14, 21, 58},
        27 : {37, 6, 40, 10, 48, 53, 55, 25},
        28 : {32, 65, 5, 7, 42, 11, 16, 23},
        29 : {66, 35, 68, 5, 41, 12, 52, 30},
        30 : {32, 67, 35, 7, 41, 42, 14, 21},
        31 : {33, 38, 73, 12, 45, 47, 22, 59},
        32 : {35, 5, 39, 10, 22, 25, 26, 30},
        33 : {35, 68, 72, 12, 23, 57, 59, 61},
        34 : {40, 74, 10, 42, 13, 46, 14, 58},
        35 : {34, 7, 71, 39, 11, 12, 50, 25},
        36 : {69, 8, 10, 12, 14, 16, 60, 61},
        37 : {72, 46, 47, 14, 48, 21, 63, 31},
        38 : {32, 69, 44, 48, 18, 19, 20, 30},
        39 : {69, 71, 14, 48, 49, 51, 52, 54},
        40 : {5, 74, 13, 46, 53, 24, 29, 30},
        41 : {32, 37, 40, 10, 43, 48, 23, 56},
        42 : {2, 70, 44, 45, 47, 19, 20, 28},
        43 : {33, 71, 41, 13, 46, 17, 18, 57},
        44 : {37, 47, 17, 19, 52, 25, 26, 30},
        45 : {35, 37, 74, 12, 19, 52, 25, 59},
        46 : {1, 74, 42, 45, 14, 24, 28, 31},
        47 : {66, 3, 46, 16, 49, 24, 62, 31},
        48 : {39, 8, 42, 74, 15, 51, 20, 21},
        49 : {33, 1, 43, 50, 19, 51, 56, 30},
        50 : {66, 6, 40, 11, 13, 49, 60, 61},
        51 : {70, 71, 73, 74, 44, 48, 22, 30},
        52 : {64, 65, 8, 49, 50, 20, 54, 62},
        53 : {32, 33, 49, 51, 20, 26, 28, 61},
        54 : {64, 33, 66, 69, 71, 8, 49, 28},
        55 : {33, 67, 10, 43, 44, 13, 53, 56},
        56 : {34, 66, 37, 9, 10, 15, 49, 58},
        57 : {6, 74, 11, 43, 46, 49, 27, 28},
        58 : {4, 71, 9, 14, 48, 55, 28, 62},
        59 : {35, 43, 44, 11, 19, 23, 24, 31},
        60 : {64, 67, 71, 10, 42, 14, 49, 24},
        61 : {66, 67, 71, 7, 74, 48, 52, 61},
        62 : {1, 8, 73, 9, 44, 51, 23, 60},
        63 : {39, 71, 10, 22, 59, 60, 29, 63},
        64 : {67, 37, 7, 73, 42, 12, 61, 29},
        65 : {33, 7, 72, 45, 13, 26, 27, 29},
        66 : {36, 68, 37, 11, 12, 49, 19, 23},
        67 : {4, 37, 39, 7, 47, 18, 51, 58},
        68 : {68, 5, 71, 8, 49, 54, 25, 58},
        69 : {35, 38, 6, 42, 12, 17, 18, 23},
        70 : {32, 68, 37, 42, 17, 19, 22, 55},
        71 : {1, 2, 68, 37, 42, 43, 27, 30},
        72 : {64, 1, 9, 10, 47, 22, 25, 30},
        73 : {32, 2, 41, 11, 46, 55, 24, 25},
        74 : {2, 35, 6, 14, 15, 21, 54, 56},
        75 : {64, 4, 69, 9, 43, 20, 23, 25},
        76 : {67, 71, 43, 44, 14, 20, 22, 57},
        77 : {67, 12, 44, 49, 20, 52, 54, 60},
        78 : {5, 38, 13, 17, 20, 54, 58, 61},
        79 : {3, 5, 74, 17, 52, 23, 61, 63},
        80 : {67, 4, 37, 38, 41, 43, 52, 24},
        81 : {64, 10, 17, 55, 58, 27, 60, 30},
        82 : {35, 74, 13, 50, 51, 57, 60, 31},
        83 : {32, 34, 43, 12, 48, 49, 50, 21},
        84 : {4, 5, 6, 71, 41, 9, 74, 56},
        85 : {32, 34, 41, 74, 13, 46, 49, 54},
        86 : {4, 69, 37, 43, 48, 16, 20, 57},
        87 : {33, 66, 3, 38, 72, 19, 20, 26},
        88 : {66, 36, 37, 9, 47, 17, 28, 30},
        89 : {73, 43, 44, 16, 17, 18, 57, 62},
        90 : {1, 3, 9, 12, 48, 54, 25, 31},
        91 : {32, 67, 74, 49, 22, 59, 29, 31},
        92 : {7, 40, 10, 13, 18, 51, 58, 59},
        93 : {2, 35, 18, 53, 54, 22, 27, 31},
        94 : {6, 39, 10, 14, 49, 53, 24, 29},
        95 : {2, 35, 71, 41, 12, 18, 51, 31},
        96 : {33, 2, 68, 70, 7, 10, 48, 53},
        97 : {37, 69, 6, 7, 12, 48, 53, 55},
        98 : {64, 65, 71, 41, 73, 45, 17, 28},
        99 : {7, 9, 42, 11, 46, 21, 56, 63},
        100 : {1, 34, 39, 73, 15, 48, 26, 60}}

    # sizes_list = []
    # for i in range(1, 12):
    #     sizes_list.append(4)
    # for i in range(1, 101):
    #     random_size = 8 #random.randint(3,7)       
    #     random_nodes = set(random.sample(range(1, len(sa_nodes)), random_size))  # Replace range(1, 100) with your desired range of nodes
    #     sa_attack_nodes[i] = random_nodes
    #     sizes_list.append(len(random_nodes))
    # average_size = sum(sizes_list) / len(sizes_list)
    # average_size = len(sa_nodes) - average_size
    # Print the updated attack nodes
    for i, nodes in sa_attack_nodes.items():
        print(f"Attack {i}: {nodes}")
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(sa_attack_nodes.items(), columns=['Attack', 'Nodes'])

    # Save the DataFrame to an Excel file
    excel_filename = 'sa_attack_nodes1.csv'
    df.to_csv(excel_filename, index=False)

    print(f"Data has been saved to {excel_filename}")

    '''num_attacks = 1
    num_nodes = len(sa_nodes)
    sa_attack_nodes = {}
    k = 2

    #for i in range(1, num_attacks + 1):
    for i in range(1, len(sa_attack_nodes)):
        # Select a random subset of nodes for the current attack
        nodes = random.sample(range(1, num_nodes + 1), k)  # Change 4 to the desired number of nodes per attack
        sa_attack_nodes[i] = set(nodes)

    print(sa_attack_nodes)
    print('length os SA attack...:', len(sa_attack_nodes))'''


    # Create an ordered dictionary to store adjacency matrices in order
    adj_matrices = collections.OrderedDict()
    prob_adj_matricesss = collections.OrderedDict()
    prob_adj_matricesss1 = collections.OrderedDict()

    ###df12 = pd.DataFrame(adj_matrixOriginal)
    ###df12.to_csv('Conus-4-12_adj_matrixOriginal.csv', index=False)
    df12 = pd.DataFrame(adj_matrix)
    df12.to_csv('adj_matrixDenseOriginal.csv', index=False)

    # Create an empty DataFrame to store the connected nodes information
    #connected_nodes_df = pd.DataFrame(columns=['Controller', 'Connected Nodes'])
    # Select five random controllers
    #controller_nodes = random.sample(list(sa_nodes.keys()), 5)
    # print("Selected Controllers: ", controller_nodes)

    # Initialize list for connected nodes after attacks
    connected_nodes_list = []
    path_matrixes = []
    avarage_connections=[]
    nodes_number = []

    # Execute the attacks one by one
    for i, nodes in sa_attack_nodes.items():
        G1 = G.copy()
        # Remove the edges connected to the attacked nodes
        for node in nodes:
            if G1.has_node(node):
                edges = list(G1.edges(node))  # Get the edges connected to the node
                G1.remove_edges_from(edges)  # Remove the edges
                ##G1.remove_node(node)

        # Draw the new graph
        # print(f"Attacking nodes: {nodes}")
        # print(f"New graph after attack {i}")


        # pos = {node: (attrs['sa_node_x'], attrs['sa_node_y']) for node, attrs in sa_nodes.items()}
        # labels = {node: attrs['sa_node_label'] for node, attrs in sa_nodes.items()}
        # fig = plt.figure(figsize=(10, 7))
        # plt.suptitle(f"New graph after attack {i}")
        # nx.draw(G1, pos, with_labels=True, labels=labels)
        # plt.show()
        # get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(G1).todense()
        # print(np.shape(adj_matrix))
        adj_matrix1 = nx.adjacency_matrix(G1)
        adj=adj_matrix
        # print(f"-----------------------------------------------------------------------------------------")
        # Initialize an adjacency matrix with zeros
        path_matrix = np.zeros((len(sa_nodes), len(sa_nodes)))
        path_matrix_controller = np.zeros((len(sa_nodes), len(sa_nodes)))

        # Loop over all nodes as source and target
        for source in G1.nodes:
            if source in nodes:
               continue  # Skip calculations for attacked nodes
            for target in G1.nodes:
                if target in nodes:
                    continue  # Skip calculations for attacked nodes
                # Skip if the source and target are the same
                if source == target:
                    path_matrix[source-1, target-1] = 1
                # Check if a path exists between the source and target
                if nx.has_path(G1, source, target):
                    # Calculate the shortest path length
                    path_length = nx.dijkstra_path_length(G1, source, target)
                    # If the path length is 10 or less, mark with a 1 in the matrix
                    if path_length <= 1000000:
                        path_matrix[source-1, target-1] = 1




        '''path_matrix = adj_matrix
        for _ in range(75):
            path_matrix = np.dot(path_matrix, adj_matrix)'''
        # Now path_matrix has 1 where there is a path of length 10 or less, and 0 otherwise
        #print(path_matrix)
        path_matrixes.append(path_matrix)
        # Initialize the minimum count with a large value
        # plt.show()
        count = 0
        # Convert controller node indices to names
        #controller_names = [node_names[node] for node in controller_nodes]

        # Select rows where the index is in controller_names
        #
        # controller_paths_df = path_matrix.loc[controller_names]

        # Check connected components
        for no in range(len(sa_nodes)):
            for xo in range(len(controller_nodes)):
                ##print('kordinata',no,controller_nodes[xo]-1)
                ##print('vlera ne matrice',path_matrix[no, controller_nodes[xo]-1])
                if path_matrix[no, controller_nodes[xo]-1] ==1:
                    count = count+1
                    #print(path_matrix[no, controller_nodes[2]])
                    #print('count aktual',count)
                    break

        #print(count)
        avarage_connections.append(count)
        # print(f'Number of connected nodes after attack {i}:',count)
  

    # Create the DataFrame using the unique values from the list
    avarage_connections1 =avarage_connections
    total = sum(avarage_connections)
    total=total/len(avarage_connections)
    # print('Avarageeeeeeeeeeeee',total)
    size = len(path_matrix)
    sum_matrix_path= np.zeros((size, size))
    for matrix in path_matrixes:
        sum_matrix_path += matrix
    # print(f'sum matrix isssssssssss by gentiii{i}:',sum_matrix_path)
    # sum_matrix = np.sum(path_matrixes, axis=0)
    # print(f'sum matrix isssssssssss by Albaniiiiiiiii{i}:',sum_matrix)
    #sum_matrix= sum_matrix/num_attacks
    sum_matrix_path= sum_matrix_path/len(path_matrixes)
    connected_nodes_df = pd.DataFrame(connected_nodes_list)
    df23=pd.DataFrame(sum_matrix_path)
    # Get node names from the sa_nodes dictionary
    node_names = {index-1: attrs['sa_node_label'] for index, attrs in sa_nodes.items()}

    # Rename indices and columns
    df23.rename(index=node_names, columns=node_names, inplace=True)
    df23.to_csv('path10.csv', index=True)

    folder_name = 'ResultsControllers'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    base_filename = 'connected_nodes_K2__'
    file_number = 1
    filename = f'{folder_name}/{base_filename}{file_number}.csv'
    file_numberEx = 1
    filenameEx = f'{folder_name}/{base_filename}{file_number}.xlsx'

    while os.path.isfile(filename):
        file_number += 1
        filename = f'{folder_name}/{base_filename}{file_number}.csv'

    while os.path.isfile(filenameEx):
        file_numberEx += 1
        filenameEx = f'{folder_name}/{base_filename}{file_numberEx}.xlsx'

    connected_nodes_df.to_csv(filename, index=False)
    connected_nodes_df.to_excel(filenameEx, index=False)

    sum_matrix_path[sum_matrix_path == 1] = 0.9

        # Step 1: Create a new matrix with ones
    ones_matrix = np.ones_like(sum_matrix_path)
    # print('ikjo me duhet pet momentin nnnnnnnnnnnnnnnnnnnnnnnnnnn',sum_matrix_path)
    # Step 2: Subtract every element of sum_matrix1 from ones_matrix
    proportionalFairnessMatrix = ones_matrix - sum_matrix_path
    
    #proportionalFairnessMatrix[proportionalFairnessMatrix <= 0] = 0
    
    # Step 3: Calculate the logarithm of every element in new_matrix
    proportionalFairnessMatrix = np.log10(proportionalFairnessMatrix)
    non_zero_counts = np.count_nonzero(proportionalFairnessMatrix, axis=1)
    # print('non_zero_counts',non_zero_counts)
    # non_zero_counts = non_zero_counts/len(sa_nodes)
    
    print(np.shape(proportionalFairnessMatrix))
    print('Proportional Fairness Matrix:')
    #print(proportionalFairnessMatrix)
    df = pd.DataFrame(proportionalFairnessMatrix)
    df.to_csv('proportionalFairnessMatrix.csv', index=False)
    row_sums = np.sum(proportionalFairnessMatrix, axis=1)
    # for x in range(len(row_sums)):
    #     row_sums[x] = row_sums[x]*non_zero_counts[x]
    print('Row Sums:',row_sums)
    
    sorted_indices = np.argsort(row_sums)
    # sorted_indices = np.array(sorted_indices, dtype=np.int32)
    sorted_sums = row_sums[sorted_indices]
    for i, row_sum in zip(sorted_indices, sorted_sums):
        print(f"Node Index {i+1}: Node Sum = {row_sum}")

    data = {'Node Index': sorted_indices + 1, 'Node Sum': sorted_sums}
    df = pd.DataFrame(data)

    df.to_csv('ydsgugvisgvdivsidgvugi.csv', index=False)

    albanivl=pd.DataFrame(path_matrixes[0])
    albanivl.to_csv('albanivl.csv', index=False)
    print(len(path_matrixes))
    print(len(sa_nodes))
    length = len(sa_nodes)    
    N = list(range(length)) # Set of i values
    M = list(range(length)) # Set of j values
    K = len(controller_nodes)  # Value of K
    indexj =[]
    lambda1 = []
    solution = solve_linear_problem(N,M,K,sum_matrix_path)
    lambda1.append(solution["lambda1"])
    indexj.append(solution["optimal_j"])

    length = len(N)
    avarage_connections =[]
    for i in range(length-1):
        infoi = solve_linear_problem2(N,M,K,sum_matrix_path,lambda1, indexj,i+2)
        lambda1.append(infoi["lambda1"])
        indexj.append(infoi["optimal_j"])
    controllers = [i+1 for i, val in enumerate(infoi["x"]) if val == 1]
    print("this are controllersssssss:",controllers)

    # result = solve_proportional_robust_controller_placement_integral(N, sum_matrix_path, K, 2, M)


    for i, nodes in sa_attack_nodes.items():
        G1 = G.copy()
        # Remove the edges connected to the attacked nodes
        for node in nodes:
            if G1.has_node(node):
                edges = list(G1.edges(node))  # Get the edges connected to the node
                G1.remove_edges_from(edges)  # Remove the edges
                ##G1.remove_node(node)

        # Draw the new graph
        print(f"Attacking nodes: {nodes}")
        print(f"New graph after attack {i}")


        pos = {node: (attrs['sa_node_x'], attrs['sa_node_y']) for node, attrs in sa_nodes.items()}
        labels = {node: attrs['sa_node_label'] for node, attrs in sa_nodes.items()}
        fig = plt.figure(figsize=(10, 7))
        plt.suptitle(f"New graph after attack {i}")
        nx.draw(G1, pos, with_labels=True, labels=labels)
        # plt.show()
        # get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(G1).todense()
        print(np.shape(adj_matrix))
        adj_matrix1 = nx.adjacency_matrix(G1)
        adj=adj_matrix
        print(f"-----------------------------------------------------------------------------------------")
        # Initialize an adjacency matrix with zeros
        path_matrix = np.zeros((len(sa_nodes), len(sa_nodes)))
        path_matrix_controller = np.zeros((len(sa_nodes), len(sa_nodes)))

        # Loop over all nodes as source and target
        for source in G1.nodes:
            if source in nodes:
               continue  # Skip calculations for attacked nodes
            for target in G1.nodes:
                if target in nodes:
                    continue  # Skip calculations for attacked nodes
                # Skip if the source and target are the same
                if source == target:
                    path_matrix[source-1, target-1] = 1
                # Check if a path exists between the source and target
                if nx.has_path(G1, source, target):
                    # Calculate the shortest path length
                    path_length = nx.dijkstra_path_length(G1, source, target)
                    # If the path length is 10 or less, mark with a 1 in the matrix
                    if path_length <= 1000000:
                        path_matrix[source-1, target-1] = 1
                # Check connected components
                # Now path_matrix has 1 where there is a path of length 10 or less, and 0 otherwise
        #print(path_matrix)
        path_matrixes.append(path_matrix)
        # plt.show()
        min_count1 = float('inf')
        count = 0
        for no in range(len(sa_nodes)):
            for xo in range(len(controllers)):
                ##print('kordinata',no,controller_nodes[xo]-1)
                ##print('vlera ne matrice',path_matrix[no, controller_nodes[xo]-1])
                if path_matrix[no, controllers[xo]-1] ==1:
                    count = count+1
                    #print(path_matrix[no, controller_nodes[2]])
                    #print('count aktual',count)
                    break
        avarage_connections.append(count)
        print(f'Number of connected nodes after attack {i}:',count)

        min_count1 = min(avarage_connections) 


    print('Avarage conectiones vector:',avarage_connections)
    total = sum(avarage_connections)
    # print('totaliii',total)
    # print('gjatesiaaaaaa',len(avarage_connections))
    total=total/len(avarage_connections)
    total_12 = sum(avarage_connections[:12])
    total_12 = total_12 / 12
    print('Proportional Fairness Sorted Values:')
    for i, row_sum in zip(sorted_indices, sorted_sums):
        print(f"Node Index {i+1}: Node Sum = {row_sum}")
    print('Controllers:',controllers)
    print('Avarage perfiudnimtar',total)
    unique_values = set()  # Set to store unique values
    indexes = []  # List to store the unique indexes

    for i, row_sum in zip(sorted_indices, sorted_sums):
        if row_sum not in unique_values:
            unique_values.add(row_sum)
            indexes.append(i + 1)

    print(indexes)
    controllers2=[]
    for i in range(len(controllers)):
        controllers2.append(indexes[i])
    print(controllers2)
    avarage_connections = []
    for i, nodes in sa_attack_nodes.items():
        G1 = G.copy()
        # Remove the edges connected to the attacked nodes
        for node in nodes:
            if G1.has_node(node):
                edges = list(G1.edges(node))  # Get the edges connected to the node
                G1.remove_edges_from(edges)  # Remove the edges
                ##G1.remove_node(node)

        # Draw the new graph
        print(f"Attacking nodes: {nodes}")
        print(f"New graph after attack {i}")


        # pos = {node: (attrs['sa_node_x'], attrs['sa_node_y']) for node, attrs in sa_nodes.items()}
        # labels = {node: attrs['sa_node_label'] for node, attrs in sa_nodes.items()}
        # fig = plt.figure(figsize=(10, 7))
        # plt.suptitle(f"New graph after attack {i}")
        # nx.draw(G1, pos, with_labels=True, labels=labels)
        # plt.show()
        # get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(G1).todense()
        print(np.shape(adj_matrix))
        adj_matrix1 = nx.adjacency_matrix(G1)
        adj=adj_matrix
        print(f"-----------------------------------------------------------------------------------------")
        # Initialize an adjacency matrix with zeros
        path_matrix = np.zeros((len(sa_nodes), len(sa_nodes)))
        path_matrix_controller = np.zeros((len(sa_nodes), len(sa_nodes)))

        # Loop over all nodes as source and target
        for source in G1.nodes:
            if source in nodes:
               continue  # Skip calculations for attacked nodes
            for target in G1.nodes:
                if target in nodes:
                    continue  # Skip calculations for attacked nodes
                # Skip if the source and target are the same
                if source == target:
                    path_matrix[source-1, target-1] = 1
                # Check if a path exists between the source and target
                if nx.has_path(G1, source, target):
                    # Calculate the shortest path length
                    path_length = nx.dijkstra_path_length(G1, source, target)
                    # If the path length is 10 or less, mark with a 1 in the matrix
                    if path_length <= 1000000:
                        path_matrix[source-1, target-1] = 1
                # Check connected components
                # Now path_matrix has 1 where there is a path of length 10 or less, and 0 otherwise
        #print(path_matrix)
        path_matrixes.append(path_matrix)
        # plt.show()
        # Initialize the minimum count with a large value
        min_count = float('inf')
        count = 0
        for no in range(len(sa_nodes)):
            for xo in range(len(controllers2)):
                ##print('kordinata',no,controller_nodes[xo]-1)
                ##print('vlera ne matrice',path_matrix[no, controller_nodes[xo]-1])
                if path_matrix[no, controllers2[xo]-1] ==1:
                    count = count+1
                    #print(path_matrix[no, controller_nodes[2]])
                    #print('count aktual',count)
                    break
        avarage_connections.append(count)
        print(f'Number of connected nodes after attack {i}:',count)

        min_count = min(avarage_connections )

    # Print the lowest value of count
    print('Lowest value of count LF:', min_count1)
    print('Lowest value of count PF:',min_count )
    total2_12 = sum(avarage_connections[:12])
    total2_12 = total2_12 / 12
    total2 = sum(avarage_connections)
    # persentage1= total/average_size* 100

    # print('totaliii',total)
    # print('gjatesiaaaaaa',len(avarage_connections))
    total2=total2/len(avarage_connections)
    # persentage2= total2/average_size *100
    
    # print("Avarage vector Lexi:",avarage_connections1)
    print("Avarage Lexi:",total)
    # print("Lexicographic approach coverage:",total_12)
    print("Controllers proposed by Lexicographic approach:",controllers)
    # print("Persentage lexi and number of nodes:",persentage1 ,average_size)
    
    # print("Avarage vector PF:",avarage_connections)
    print("Avarage PF:",total2)
    # print("Proportional Fairness approach coverage:",total2_12)
    print("Controllers proposed by Proportional Fairness approach:",controllers2)
    # print("these are uniqe values:",unique_values)
    
    
    # print("Persentage PF and number of nodes:",persentage2,average_size)
    # if result:
    #     print("Optimal Solution:")
    #     for var, value in result.items():
    #         if value == 1.0:
    #             print(f"{var}: {value}")
    # else:
    #     print("No optimal solution found.")
        
    info = {
        "N": N,
        "M": M,
        "K": K,
        "pij": sum_matrix_path,
        "total": total,
        "matrix":path_matrixes,
        "sa_nodes":sa_nodes
    }
    return info

indexj =[]
lambda1 = []
info = twoNodesAttacked()
# # K = 4
# solution = solve_linear_problem(info["N"],info["M"],info["K"],info["pij"])
# lambda1.append(solution["lambda1"])
# indexj.append(solution["optimal_j"])

# length = len(info["N"])

# for i in range(5):
#     infoi = solve_linear_problem2(info["N"],info["M"],info["K"],info["pij"],lambda1, indexj,i+2)
#     lambda1.append(infoi["lambda1"])
#     indexj.append(infoi["optimal_j"])
# controllers = [i+1 for i, val in enumerate(infoi["x"]) if val == 1]
# # Print the solution
# print("Optimal Solution:")
# print("lambda1 =", solution["lambda1"])
# print("Controllers =", [i+1 for i, val in enumerate(solution["x"]) if val == 1])
# print("Optimal Solution for n iterations:")
# print("lambda1 =", infoi["lambda1"])
# print("Controllers =", [i+1 for i, val in enumerate(infoi["x"]) if val == 1])
# print(info["total"])
# controllers = [i+1 for i, val in enumerate(infoi["x"]) if val == 1]
# avarage_connections = []
# count = 0
# sa_nodes_length = len(info["sa_nodes"])
# matrixes = info["matrix"]
# # print("this is a matrixxxxxxxxxxxxxxx",matrixes[0])
# print("this is a matrixxxxxxxxxxxxxxx",sa_nodes_length)
# for no in range(sa_nodes_length):
#     for xo in range( len(controllers)):
#         ##print('kordinata',no,controller_nodes[xo]-1)
#         ##print('vlera ne matrice',path_matrix[no, controller_nodes[xo]-1])
#         if (matrixes[no][controllers[xo]-1] ==1).all():
#             count = count+1
#             #print(path_matrix[no, controller_nodes[2]])
#             #print('count aktual',count)
#             break
#     #print(count)
#     avarage_connections.append(count)
#     print(f'Number of connected nodes after attack {i}:',count)

# # Create the DataFrame using the unique values from the list
# total = sum(avarage_connections)
# total=total/len(avarage_connections)
# print('Avarageeeeeeeeeeeee',total)