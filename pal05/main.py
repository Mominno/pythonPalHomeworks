import sys
import math
from collections import deque


def get_input():

    desired_dna_sequence = sys.stdin.readline()
    desired_dna_sequence = ''.join(e for e in desired_dna_sequence if e.isalnum())
    line = sys.stdin.readline()
    N, D = line.split(" ")
    costs_of_basic_units = []
    basic_units = []
    for i in range(int(N)):
        cost = int(sys.stdin.readline())
        costs_of_basic_units.append(cost)
        unit = sys.stdin.readline()
        unit = ''.join(e for e in unit if e.isalnum())
        basic_units.append(unit)

    return basic_units, costs_of_basic_units, desired_dna_sequence, int(D)


def get_candidates(basic_unit, desired_dna_sequence, max_del, unit_cost):

    max_index = len(desired_dna_sequence) - 1
    candidates = []

    # start from every character
    for start_index in range(len(desired_dna_sequence)):
        current_index = start_index
        deletions = 0
        for char in basic_unit:
            if current_index >= max_index:
                deletions += 1
                current_index
            if char == desired_dna_sequence[current_index]:
                current_index += 1
            else:
                deletions += 1
            # check if result is valid
        if deletions <= max_del and deletions != len(basic_unit):
            # doesnt matter maybe?
            #if current_index < max_index:
            current_index -= 1

            candidate = (deletions + unit_cost, start_index, current_index)
            candidates.append(candidate)

            while deletions < max_del and start_index-current_index !=0:
                deletions +=1
                current_index -= 1
                candidate = (deletions + unit_cost, start_index, current_index)
                candidates.append(candidate)


    return candidates


def create_minimum_cost_plan(candidate_list, basic_units, desired_dna_sequence):
    #print(desired_dna_sequence)
    #print("=================")
    s = [i for i in range(len(desired_dna_sequence))]
    str_indices = ''.join(map(str, s))
    #print(str_indices)
    max_index = len(desired_dna_sequence) -1
    for unit_list, basic_unit in zip(candidate_list, basic_units):
        print("{}: {}".format(basic_unit, unit_list))
    keys = [i for i in range(len(desired_dna_sequence))]
    dict_by_start = dict.fromkeys(keys)
    record = dict.fromkeys(keys)
    for key in dict_by_start:
        dict_by_start[key] = []
        record[key] = math.inf
    for unit_list in candidate_list:
        for unit in unit_list:
            start_index = unit[1]
            dict_by_start[start_index].append(unit)

    queue = deque()
    #print(dict_by_start)
    for cand in dict_by_start[0]:
        queue.append(cand+(1,))
    result = []

    while queue:
        cand = queue.popleft()
        #print(len(queue))
        print(cand)
        if cand[0] < record[cand[2]]:
            record[cand[2]] = cand[0]
        elif cand[0] > record[cand[2]]:
            continue
        if result:
            if result[0][0] < cand[0]:
                continue
        elif cand[2] == max_index:
            result.append(cand)
        else:
            next_index = cand[2] + 1
            if next_index in dict_by_start:
                for possible_extension in dict_by_start[next_index]:
                    extension = (cand[0]+possible_extension[0],cand[1],possible_extension[2],cand[3]+1)
                    queue.append(extension)
    #print(result)
    min_cost = math.inf
    min_piece = math.inf

    for res in result:
        if res[0] < min_cost:
            min_cost = res[0]
            min_piece = res[3]
        elif res[0] == min_cost and res[3] < min_piece:
            min_piece = res[3]

    return min_cost, min_piece


def solve_ge(basic_units, unit_costs, desired_sequence, max_del):
    candidate_list = []

    for basic_unit, unit_cost in zip(basic_units,unit_costs):
        unit_candidates = get_candidates(basic_unit, desired_dna_sequence, max_del, unit_cost)
        candidate_list.append(unit_candidates)

    return create_minimum_cost_plan(candidate_list, basic_units, desired_dna_sequence)


if __name__ == "__main__":
    basic_units, costs_of_basic_units, desired_dna_sequence, D = get_input()
    cost, pieces = solve_ge(basic_units, costs_of_basic_units, desired_dna_sequence, D)
    print("{} {}".format(cost, pieces))