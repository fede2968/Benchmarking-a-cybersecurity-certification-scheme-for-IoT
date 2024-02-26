import json
import pandas as pd

# Function to load JSON data from file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to create a DataFrame from the benchmark data
def create_dataframe_with_config(data):
    rows = []
    for d in data:
        # Extracting the config from the name string
        config = d['params']['config']
        max_val = d['stats']['max']
        mean = d['stats']['mean']
        min_val = d['stats']['min']
        stddev = d['stats']['stddev']
        rows.append([config, max_val, stddev, mean, stddev, min_val, stddev])
    return pd.DataFrame(rows, columns=['SETTING', 'AVG_WORST', 'STD_WORST', 'AVG_AVG', 'STD_AVG', 'AVG_BEST', 'STD_BEST'])

# Load the JSON data
file_path = '.benchmarks/Darwin-CPython-3.9-64bit/0001_risultati_benchmark.json.json'  # Replace with your JSON file path
benchmark_data = load_json_data(file_path)

# Extracting 'execute' and 'explore' groups
execute_data = [d for d in benchmark_data['benchmarks'] if d['group'] == 'execute']
explore_data = [d for d in benchmark_data['benchmarks'] if d['group'] == 'explore']

# Creating DataFrames with config as SETTING
execute_df_with_config = create_dataframe_with_config(execute_data)
explore_df_with_config = create_dataframe_with_config(explore_data)

# Save the DataFrames to CSV files
execute_csv_with_config_path = 'execute_benchmark_results_with_config.csv'
explore_csv_with_config_path = 'explore_benchmark_results_with_config.csv'

execute_df_with_config.to_csv(execute_csv_with_config_path, index=False)
explore_df_with_config.to_csv(explore_csv_with_config_path, index=False)
