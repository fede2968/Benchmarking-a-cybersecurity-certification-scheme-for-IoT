import itertools as itr
import random
import dataset_generator

def process_microproperties(new_microproperty, old_microproperty, N, J):
    """
    Extracts and processes values from microproperties for neighbor search.
    """
    extracted_values = []
    extracted_new_values = []
    final_neigh = []

    for i in range(len(new_microproperty)):
        new_value, new_score = new_microproperty[i]
        old_value, old_score = old_microproperty[i]

        if new_score == 0:
            extracted_new_values.append(new_value)
            extracted_values.append((old_value, old_score))

    for value, score in extracted_values:
        neighbors = neigh_of(value, score, N, J)
        final_neigh.append(neighbors)

    return extracted_values, extracted_new_values, final_neigh

def neigh_of(value_att_old, old_score, N, J):
    """
    Generates neighbor values based on attribute changes within specified limits.
    """
    neighbors = []
    attribute_changes = []

    N = N + J
    for i in range(-N, N+1):  # Modified to include negative range
        if i == 0:
            continue
        neighbor_value = value_att_old + i
        neighbor_score = old_score + i
        if neighbor_value >= 0:  # Ensuring neighbor value is non-negative
            attribute_changes.append((neighbor_value, neighbor_score))

    neighbors.append(attribute_changes)
    return neighbors

def compare_with_zero_score(neigh_blocks, new_system):
    zero_score_values = [val for val, score in new_system if score == 0]
    comparisons = []

    for block in neigh_blocks:
        for neigh in block[0]:
            if neigh[0] in zero_score_values:
                comparisons.append(neigh)
    
    return comparisons

def count_zero_score_elements(system):
    return sum(1 for sublist in system for _, score in sublist if score == 0)

def explore(old_score, actual_score, new_system, old_system, N, J, recursion_depth=0, max_recursion_depth=100):
    if recursion_depth > max_recursion_depth:
        return []

    neighbors_dict = []

    for i in range(len(new_system)):
        new_microproperty = new_system[i]
        old_microproperty = old_system[i]

        _, _, final_neigh = process_microproperties(new_microproperty, old_microproperty, N, J)
        comparisons = compare_with_zero_score(final_neigh, new_microproperty)
        
        neighbors_dict.extend(comparisons)
    
    zero_score_count = count_zero_score_elements(new_system)

    neighbors_list_total = subexplore(neighbors_dict, new_system, old_score - actual_score)


    if len(neighbors_dict) != zero_score_count:
        return explore(old_score, actual_score, new_system, old_system, N, J + 2, recursion_depth + 1, max_recursion_depth)
    
    if not neighbors_list_total:
        return explore(old_score, actual_score, new_system, old_system, N, J + 2, recursion_depth + 1, max_recursion_depth)
    
    return random.choice(neighbors_list_total) if len(neighbors_list_total) > 1 else neighbors_list_total

def subexplore(neighbors_dict, new_system, difference_score):
    list_to_return = []
    temp_list = []
    added_values = set()
    
    for i, new_microproperty in enumerate(new_system):
        for j, (new_value, new_score) in enumerate(new_microproperty):
            if new_score == 0 and new_value not in added_values:
                for neigh in neighbors_dict:
                    if neigh[0] == new_value:
                        temp_list.append(((new_value, neigh[1]), (i, j)))
                        added_values.add(new_value)
                        break

    for combo in temp_list:
        if combo[0][1] >= difference_score:
            return [combo]

    all_combinations = list(itr.chain.from_iterable(itr.combinations(temp_list, r) for r in range(1, len(temp_list) + 1)))

    for combination in all_combinations:
        if sum(item[0][1] for item in combination) >= difference_score:
            list_to_return.append([(item[0], item[1]) for item in combination])

    return list_to_return if list_to_return else [temp_list]

def execute(new_system, t):
    if len(t) == 1 and isinstance(t[0], list):
        t = t[0]

    for combo in t:
        (combo_value, combo_score), (list_index, tuple_index) = combo
        if new_system[list_index][tuple_index][1] == 0 and new_system[list_index][tuple_index][0] == combo_value:
            new_system[list_index][tuple_index] = (combo_value, combo_score)
    return new_system

def calculate_total_score(system):
    return sum(score for sublist in system for _, score in sublist)

def main():
    new_system_2 = []
   
    new_system, old_system, actual_score,  old_score = dataset_generator.main()

    print("score vecchio", old_score)
    
    N = 1
    J = 1
    max_attempts = 100

    t = explore(old_score, actual_score, new_system, old_system, N, J)
    print("sistema nuovo senza certificato ", new_system)
    new_system_2 = execute(new_system, t)
    actual_score = calculate_total_score(new_system_2)
    
    while old_score > actual_score and max_attempts > 0:
        t = explore(old_score, actual_score, new_system_2, old_system, N, J)
        #print(t)
        new_system_2 = execute(new_system_2, t)
        actual_score = calculate_total_score(new_system_2)
        max_attempts -= 1
   
    print("sistema nuovo ", new_system)
    print("score nuovo ", actual_score)
   

if __name__ == "__main__":
    main()
