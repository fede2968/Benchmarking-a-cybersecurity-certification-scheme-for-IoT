import numpy as np
import random
from dataclasses import dataclass
import pandas as pd

# DEFINE CONSTANTS
WORSEN = 1
IMPROVE = 2
BIG = 1
MINI = 2
N_CHANGE = 10
BIG_CHANGE_FACTOR = random.randint(5, 10)
MINI_CHANGE_FACTOR = random.randint(1, 4)

setting = [(3, 3), (10, 10), (3, 10), (10, 3), (30, 30), (20, 20), (20, 30), (30, 20), (100, 100), (50, 50), (100, 50), (50, 100)]
change_width_worsen = 0.25
change_width_improve = 0.75
worsen = 0.25
improve = 0.75
TEMP = []

@dataclass
class System:
    properties: list
    num_micro_properties: int
    num_attributes_per_micro: int

    def score(self):
        return sum(score for _, score in self.properties)

    def __repr__(self):
        grouped_properties = [self.properties[i:i + self.num_micro_properties] for i in range(0, len(self.properties), self.num_attributes_per_micro)]
        return f"System(properties={grouped_properties})"

    @staticmethod
    def create_system(micro_properties, num_micro, num_att):
        all_attributes = [attribute for property in micro_properties for attribute in property]
        return System(all_attributes, num_micro, num_att)

    def get_counts(self):
        return self.num_micro_properties, self.num_attributes_per_micro

def generate(setting):
    configuration = random.choice(setting)
    return configuration

def generate_attributes(n_attribute):
    return [(value := np.random.randint(1, 10), np.random.randint(value + 1, 15)) for _ in range(n_attribute)]

def define_microproperties(num_micro, num_att):
    micro_property = []
    for _ in range(num_micro):
        micro_property.append(generate_attributes(num_att))
    return micro_property


def generate_changes(n_micro, n_att):
    for change in range(N_CHANGE):
        values = [WORSEN, IMPROVE]
        valuesW = [BIG, MINI]
        probabilitiesW = [change_width_worsen, change_width_improve]
        probabilities = [worsen, improve]
        n_properties = np.random.randint(1, n_micro + 1)
        n_attribute = np.random.randint(1, n_att + 1)
        type_change = np.random.choice(values, p=probabilities)
        width_change = np.random.choice(valuesW, p=probabilitiesW)
    return n_properties, n_attribute, type_change, width_change

def apply_changes(micro_properties, type_change, n_properties, n_attributes):
    # Ensure each micro-property is only changed once
    selected_micro_properties_indices = random.sample(range(len(micro_properties)), min(n_properties, len(micro_properties)))

    for idx in selected_micro_properties_indices:
        micro = micro_properties[idx]
        selected_attribute = random.choice(range(len(micro)))
        value, _ = micro[selected_attribute]
        if type_change == IMPROVE:
            change_factor = random.randint(MINI_CHANGE_FACTOR, BIG_CHANGE_FACTOR)
            new_value = min(value + change_factor, 15)
        else:
            change_factor = random.randint(MINI_CHANGE_FACTOR, BIG_CHANGE_FACTOR)
            new_value = max(value - change_factor, 0)
        micro[selected_attribute] = (new_value, 0)

    return micro_properties




def main(setting):
    results = []
    for i in range(1,100):
        for config in setting:
            n_micro, n_att = config
            micro_old = define_microproperties(n_micro, n_att)
            sys = System.create_system(micro_old, n_micro, n_att)
            score = sys.score()

            n_properties_changed, n_attribute_changed, type_change, width_change = generate_changes(n_micro, n_att)
            micro_new = apply_changes(micro_old, type_change, n_properties_changed, n_attribute_changed)
            sys_t = System.create_system(micro_new, n_micro, n_att)
            score_new = sys_t.score()
            grouped_properties = [sys.properties[i:i+n_att] for i in range(0, len(sys.properties), n_att)]
            
            num_micro_properties, num_attributes = sys.get_counts()
            result = {
                "config": config,
                "grouped_properties": grouped_properties,
                "score_new": score_new,
                "score": score,
                "micro_new": micro_new,
                "num_micro_properties": num_micro_properties,
                "num_attributes": num_attributes
            }
            results.append(result)
    return results

if __name__ == "__main__":
    systems = main(setting)
    print(systems[0]["micro_new"])# Displaying the result of the first configuration for brevity
