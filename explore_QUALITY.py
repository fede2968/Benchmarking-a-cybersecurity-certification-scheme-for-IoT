import itertools as itr
import random
import dataset_generator
import csv
import pandas as pd

COUNTER = 0
COUNTER_TOTAL = 0
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
    global COUNTER_TOTAL
    N = N + J
    for i in range(-N, N+1):  
        if i == 0:
            continue
        neighbor_value = value_att_old + i
        neighbor_score = old_score + i
        if neighbor_value >= 0:  
            attribute_changes.append((neighbor_value, neighbor_score))
            COUNTER_TOTAL+=1
            

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
    
    neighbors_list_total = subexplore(neighbors_dict, new_system, old_score - actual_score)

    if not neighbors_list_total:
        return explore(old_score, actual_score, new_system, old_system, N, J + 2, recursion_depth + 1, max_recursion_depth)
    
    return random.choice(neighbors_list_total) if len(neighbors_list_total) > 1 else neighbors_list_total

def subexplore(neighbors_dict, new_system, difference_score):
    global COUNTER
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
    #print (temp_list)
    return list_to_return if list_to_return else [temp_list]

def execute(new_system, t):
    global COUNTER 
    

    if len(t) == 1 and isinstance(t[0], list):
        t = t[0]
        COUNTER += 1  
    #print("TEST = ",t)
    for combo in t:
        (combo_value, combo_score), (list_index, tuple_index) = combo
        COUNTER += 1  
        if new_system[list_index][tuple_index][1] == 0 and new_system[list_index][tuple_index][0] == combo_value:
            new_system[list_index][tuple_index] = (combo_value, combo_score)
            
    return new_system

def calculate_total_score(system):
    return sum(score for sublist in system for _, score in sublist)


def custom_sort_key(setting_str):
    """
    Convert setting string to a tuple and return it for sorting.
    Handle potential empty or malformed strings.
    """
    try:
        return tuple(map(int, setting_str.strip("()").split(',')))
    except ValueError:
        return float('inf')  

def create_and_sort_csv(COUNTER_TOTAL, COUNTER, n_micro, n_att, file_path, specific_order):
    tot = COUNTER/COUNTER_TOTAL
    rounded_number = round(tot, 7)
    data_formatted = f"{n_micro, n_att}    {rounded_number}    {COUNTER}         {COUNTER_TOTAL} "

    with open(file_path, mode='a', newline='') as file:
        file.seek(0, 2) 
        if file.tell() == 0:
            file.write("SETTING EXEC/TOTAL EXECUTED     TOTAL   \n")
        file.write(data_formatted + "\n")

    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=' ')
        headers = next(reader)
        data = [row for row in reader if row] 

    order_dict = {v: i for i, v in enumerate(specific_order)}
    data.sort(key=lambda row: order_dict.get(custom_sort_key(row[0].strip()), float('inf')))

    with open(file_path, 'w', newline='') as file:
        file.write(" ".join(headers) + "\n")
        for row in data:
            file.write(" ".join(row) + "\n")


def max_exec_total(csv_file_path, settings):
    """
    Modifica per calcolare e ritornare il valore totale per ogni configurazione.
    """
    data = pd.read_csv(csv_file_path, header=None, sep='\s+', skiprows=1)

    data['SETTING'] = data[0] + ' ' + data[1]

    data = data.drop(columns=[0, 1])

    data.columns = ['EXEC/TOTAL', 'EXECUTED', 'TOTAL', 'SETTING']

    with open("quality_for_setting", 'a', newline='') as file:
        if file.tell() == 0:
            file.write("SETTING EXECUTED_AVG_PERC(%)   EXECUTED_STD_PERC(%)    TOTAL   EXECUTED_AVG  EXECUTED_STD   \n")

        for s in settings:
            filtered_data = data[data['SETTING'] == str(s)]
            max_exec_total_value = round(filtered_data['EXEC/TOTAL'].mean(), 2)
            std_dev = round(filtered_data['EXEC/TOTAL'].std(), 5)
            std_percentual = round(std_dev * 100, 5)
            max_percentual = round(max_exec_total_value * 100, 4) 
            total_max = filtered_data["TOTAL"].max()  

            line = f"{str(s):<15}{max_percentual:>10}{std_percentual:>20}{total_max:>15}{max_exec_total_value:>15}{std_dev:>15}\n"
            file.write(line)


              
def export_settings(system):
    with open("settings.csv", 'a', newline='') as file:
        for s in system:
            c = s["config"]
            gp = s["grouped_properties"]
            mn = s["micro_new"]
            s_o = s["score"]
            s_n = s["score_new"]
            config_str = ','.join(map(str, c)) 
            gp_str = str(gp)  
            mn_str = str(mn) 
            line = f"{config_str:<15}{gp_str:>10}{mn_str:>20}{s_o:>10}{s_n:>15}\n"
            file.write(line)



def main():
    new_system_2 = []
    setting = [(3, 3), (10, 10), (3, 10), (10, 3), (30, 30), (20, 20), (20, 30), (30, 20), (100, 100), (50, 50), (100, 50), (50, 100)]
    system = dataset_generator.main(setting)
    export_settings(system)
    global COUNTER_TOTAL
    global COUNTER
    total = []
    for s in system:
        for i in range (1,5):
            old_score = s["score"]
            actual_score = s["score_new"]
            new_system = s["micro_new"]
            old_system = s["grouped_properties"]
            t = []
            new_system_2 = []
            
            N = 5
            J = 1
            max_attempts = 100

            t = explore(old_score, actual_score, new_system, old_system, N, J)
        
            new_system_2 = execute(new_system, t)
            actual_score = calculate_total_score(new_system_2)
            
            while old_score > actual_score and max_attempts > 0 and t != [[]]:
                t = explore(old_score, actual_score, new_system_2, old_system, N, J)
                print(t)
                new_system_2 = execute(new_system_2, t)
                actual_score = calculate_total_score(new_system_2)
                max_attempts -= 1
            
            print("sistema vecchio ", old_system)
            print("sistema nuovo ", new_system)
            print("score nuovo ", actual_score)
            print(COUNTER, COUNTER_TOTAL)
            create_and_sort_csv(COUNTER_TOTAL, COUNTER, s["num_micro_properties"], s["num_attributes"], "output.csv", dataset_generator.setting)
            COUNTER = 0
            COUNTER_TOTAL = 1

    max_exec_total("output.csv", setting)

if __name__ == "__main__":
    main()
