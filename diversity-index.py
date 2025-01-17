import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def load_routines(file_path):
    """
    Load routines from the provided file
    Args:
        file_path (str): The path to the file containing routines data.
    Returns:
        list: A list of routines, where each routine is a list of device IDs.
    """
    with open(file_path, 'r') as f:
        data = f.readlines()
    routines = [list(map(int, line.strip().split())) for line in data]
    return routines

def load_device_dict(file_path):
    """
    Load the device dictionary from the provided file.
    Args:
        file_path (str): The path to the file containing the device dictionary.
    Returns:
        dict: A dictionary mapping device names to their corresponding IDs.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("dictionary", file_path)
    dictionary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dictionary)
    return dictionary.device_dict

def calculate_diversity_index(routines, device_dict):
    """
    Calculate the diversity index based on device usage.
    Args:
        routines (list): A list of routines, where each routine is a list of device IDs.
        device_dict (dict): A dictionary mapping device names to their corresponding IDs.
    Returns:
        float: The diversity index calculated as the number of unique devices divided by the total usage.
    """
    id_to_device = {v: k for k, v in device_dict.items()}

    # Flatten routines into a single list of device IDs
    device_usage = [device for routine in routines for device in routine]

    # Map device IDs to device names
    device_names = [id_to_device.get(device, "Unknown") for device in device_usage]

    # Count occurrences of each device
    device_counts = Counter(device_names)

    # Calculate diversity index
    total_usage = sum(device_counts.values())
    diversity_index = len(device_counts) / total_usage if total_usage > 0 else 0

    return diversity_index

# List of countries and their corresponding data files
countries = {
    "France": {"routines_file": "fr/routine_device_corpus.txt", "dict_file": "fr/dictionary.py"},
    "Korea": {"routines_file": "kr/routine_device_corpus.txt", "dict_file": "kr/dictionary.py"},
    "USA": {"routines_file": "us/routine_device_corpus.txt", "dict_file": "us/dictionary.py"},
    "Spain": {"routines_file": "sp/routine_device_corpus.txt", "dict_file": "sp/dictionary.py"}
}

# Calculate diversity indices for all countries
diversity_indices = {}

for country, files in countries.items():
    print(f"Processing data for {country}...")
    routines_file = files["routines_file"]
    dict_file = files["dict_file"]

    if os.path.exists(routines_file) and os.path.exists(dict_file):
        routines = load_routines(routines_file)
        device_dict = load_device_dict(dict_file)
        diversity_index = calculate_diversity_index(routines, device_dict)
        diversity_indices[country] = diversity_index
    else:
        print(f"Data files for {country} are missing.")

# Plot the diversity indices
plt.figure(figsize=(10, 6))
countries_list = list(diversity_indices.keys())
indices = list(diversity_indices.values())
plt.bar(countries_list, indices, color="purple", alpha=0.7)
plt.title("Device Usage Diversity Index by Country")
plt.xlabel("Country")
plt.ylabel("Diversity Index")
plt.tight_layout()

# Save the plot
if not os.path.exists('result'):
    os.makedirs('result')
if not os.path.exists('result/diversity-index'):
    os.makedirs('result/diversity-index')
plt.savefig('result/diversity-index/diversity-index-by-country.png')

print("Analysis complete! Diversity index graph saved as 'result/diversity-index/diversity-index-by-country.png'.")