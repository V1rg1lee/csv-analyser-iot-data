import os
import pandas as pd
import matplotlib.pyplot as plt

def load_routines(file_path):
    """Load routines from a file
    Args:
        file_path (str): Path to the file
    Returns:
        list: List of routines    
    """
    with open(file_path, 'r') as f:
        data = f.readlines()
    routines = [list(map(int, line.strip().split())) for line in data]
    return routines

def load_device_dict(file_path):
    """Load device dictionary from a file
    Args:
        file_path (str): Path to the file
    Returns:
        dict: Device dictionary
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("dictionary", file_path)
    dictionary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dictionary)
    return dictionary.device_dict

def analyze_routines(routines, country, device_dict):
    """Analyze routines and create a plot
    Args:
        routines (list): List of routines
        country (str): Country name
        device_dict (dict): Device dictionary
    Returns:
        list: List of devices sorted by usage count
    """
    id_to_device = {v: k for k, v in device_dict.items()}
    device_counts = {}
    for routine in routines:
        for device in routine:
            device_name = id_to_device.get(device, "Unknown")
            if device_name not in ["Unknown", "None"]: 
                device_counts[device_name] = device_counts.get(device_name, 0) + 1

    # Sort devices by usage count
    sorted_devices = sorted(device_counts.items(), key=lambda x: x[1], reverse=True)
    top_devices = dict(sorted_devices[:10])

    plt.figure(figsize=(10, 6))
    plt.bar(top_devices.keys(), top_devices.values())
    plt.title(f"Top 10 devices used in {country}")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Number of uses")
    plt.xlabel("Devices")
    plt.tight_layout()

    # Save the plot as a PNG file
    result_dir = 'result/top-ten'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    plt.savefig(f'{result_dir}/top-10-device-{country}.png')
    plt.close()

    return sorted_devices

# List of countries and their routine files
countries = {
    "France": "data/fr/routine_device_corpus.txt",
    "Korea": "data/kr/routine_device_corpus.txt",
    "USA": "data/us/routine_device_corpus.txt",
    "Spain": "data/sp/routine_device_corpus.txt"
}

dicts = {
    "France": "data/fr/dictionary.py",
    "Korea": "data/kr/dictionary.py",
    "USA": "data/us/dictionary.py",
    "Spain": "data/sp/dictionary.py"
}

# Analyze routines for each country
for country, file_path in countries.items():
    if os.path.exists(file_path):
        print(f"Analyzing routines for {country}:")
        routines = load_routines(file_path)
        device_dict = load_device_dict(dicts[country])
        analyze_routines(routines, country, device_dict)
    else:
        print(f"File not found for {country}: {file_path}")

print("Analysis complete! Results are saved in the 'result' folder if the analysis was successful.")