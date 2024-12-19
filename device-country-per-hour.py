import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_routines(file_path):
    """
    Load routines from a given file.

    Args:
        file_path (str): The path to the file containing the routines.

    Returns:
        list: A list of routines, each routine being a list of integers.
    """
    with open(file_path, 'r') as f:
        data = f.readlines()
    routines = [list(map(int, line.strip().split())) for line in data]
    return routines

def load_device_dict(file_path):
    """
    Load the device dictionary from a given file.

    Args:
        file_path (str): The path to the file containing the device dictionary.

    Returns:
        dict: A dictionary where keys are device names and values are their IDs.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("dictionary", file_path)
    dictionary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dictionary)
    return dictionary.device_dict

def analyze_hourly_usage_by_device(routines, device_dict, country):
    """
    Analyze hourly average usage by device and country.

    Args:
        routines (list): A list of routines, each routine being a list of integers representing device IDs.
        device_dict (dict): A dictionary where keys are device names and values are their IDs.
        country (str): The name of the country for which the analysis is performed.

    Returns:
        None
    """
    id_to_device = {v: k for k, v in device_dict.items()}

    # Convert routines into a dataframe
    routine_data = []
    for hour, routine in enumerate(routines):
        for device in routine:
            routine_data.append((hour % 24, device))

    df = pd.DataFrame(routine_data, columns=["hour", "device_id"])

    # Replace device IDs with device names
    df["device"] = df["device_id"].map(id_to_device)

    # Group by device and hour to calculate average usage
    hourly_usage = df.groupby(["device", "hour"]).size().reset_index(name="usage")

    # Plot for each device
    output_dir = f'result/device-country/{country}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for device in hourly_usage["device"].unique():
        device_data = hourly_usage[hourly_usage["device"] == device]
        plt.figure(figsize=(10, 6))
        plt.bar(device_data["hour"], device_data["usage"], color="blue", alpha=0.7)
        plt.title(f"Hourly Usage for {device} in {country}")
        plt.xlabel("Hour")
        plt.ylabel("Usage Count")
        plt.xticks(range(24))
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{device}-{country}-hour.png')
        plt.close()

# List of countries and their corresponding data files
countries = {
    "France": {"routines_file": "data/fr/routine_device_corpus.txt", "dict_file": "data/fr/dictionary.py"},
    "Korea": {"routines_file": "data/kr/routine_device_corpus.txt", "dict_file": "data/kr/dictionary.py"},
    "USA": {"routines_file": "data/us/routine_device_corpus.txt", "dict_file": "data/us/dictionary.py"},
    "Spain": {"routines_file": "data/sp/routine_device_corpus.txt", "dict_file": "data/sp/dictionary.py"}
}

# Process each country
for country, files in countries.items():
    print(f"Processing data for {country}...")
    routines_file = files["routines_file"]
    dict_file = files["dict_file"]

    if os.path.exists(routines_file) and os.path.exists(dict_file):
        routines = load_routines(routines_file)
        device_dict = load_device_dict(dict_file)
        analyze_hourly_usage_by_device(routines, device_dict, country)
    else:
        print(f"Data files for {country} are missing.")

print("Analysis complete! Graphs saved in the 'result/device-country' folder.")
