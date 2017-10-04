#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import itertools
import time
import numpy as np
import numpy.linalg as LA
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def edge_length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def cycle_length(cycle, points):
    return sum(edge_length(points[cycle[i - 1]], points[cycle[i]]) for i in range(len(cycle)))


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    point_count = int(lines[0])

    points = []
    for i in range(1, point_count+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # trivial solution
    # visit the points in the order they appear in the file
    # obj, opt, solution = trivial(points)

    # greedy solution (nearest neighbor)
    # starts from 0, add nearest neighbor to the cycle at each step
    # generally acceptable, but can be arbitrarily bad
    # obj, opt, solution = greedy(points)

    # 2-opt solution
    obj, opt, solution = two_opt(points)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def trivial(points):
    cycle = range(len(points))
    return cycle_length(cycle, points), 0, list(cycle)


def greedy(points):
    point_count = len(points)
    coords = np.array([(point.x, point.y) for point in points])
    cycle = [0]
    candidates = set(range(1, point_count))
    while candidates:
        curr_point = cycle[-1]
        nearest_neighbor = None
        nearest_dist = np.inf
        for neighbor in candidates:
            if LA.norm(coords[curr_point] - coords[neighbor]) < nearest_dist:
                nearest_neighbor = neighbor
                nearest_dist = LA.norm(coords[curr_point] - coords[neighbor])
        cycle.append(nearest_neighbor)
        candidates.remove(nearest_neighbor)
    return cycle_length(cycle, points), 0, cycle


def swap(cycle, length, start, end, points):
    new_cycle = cycle[:start] + cycle[start:end + 1][::-1] + cycle[end + 1:]
    new_length = length - \
                 (edge_length(points[cycle[start - 1]], points[cycle[start]]) +
                  edge_length(points[cycle[end]], points[cycle[(end + 1) % len(cycle)]])) + \
                 (edge_length(points[new_cycle[start - 1]], points[new_cycle[start]]) +
                  edge_length(points[new_cycle[end]], points[new_cycle[(end + 1) % len(cycle)]]))
    return new_cycle, new_length


def two_opt(points):
    point_count = len(points)
    best_length, _, best_cycle = greedy(points)
    improved = True
    t = time.clock()
    while improved:
        improved = False
        for start, end in itertools.combinations(range(point_count), 2):
            curr_cycle, curr_length = swap(best_cycle, best_length, start, end, points)
            if curr_length < best_length:
                best_cycle = curr_cycle
                best_length = curr_length
                improved = True
                break
        if time.clock() - t >= 4 * 3600 + 59 * 60:
            improved = False
    return cycle_length(best_cycle, points), 0, best_cycle


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

