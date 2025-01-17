import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

def load_routines(file_path):
    """
    Load routines from a file.

    Args:
        file_path (str): Path to the file containing routines.

    Returns:
        list: A list of routines, where each routine is a list of integers.
    """
    with open(file_path, 'r') as f:
        data = f.readlines()
    routines = [list(map(int, line.strip().split())) for line in data]
    return routines

def load_device_dict(file_path):
    """
    Load device dictionary from a Python file.

    Args:
        file_path (str): Path to the Python file containing the device dictionary.

    Returns:
        dict: A dictionary mapping device names to device IDs.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("dictionary", file_path)
    dictionary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dictionary)
    return dictionary.device_dict

def analyze_absence_patterns(routines, device_dict, country):
    """
    Analyze absence patterns based on device usage.

    Args:
        routines (list): List of routines, where each routine is a list of device IDs.
        device_dict (dict): Dictionary mapping device names to device IDs.
        country (str): Name of the country for which the analysis is performed.

    Returns:
        None
    """
    id_to_device = {v: k for k, v in device_dict.items()}

    # Flatten routines into a dataframe with hourly usage
    routine_data = []
    for hour, routine in enumerate(routines):
        for device in routine:
            routine_data.append((hour % 24, device))

    df = pd.DataFrame(routine_data, columns=["hour", "device_id"])

    # Replace device IDs with device names
    df["device"] = df["device_id"].map(id_to_device)

    # Focus on devices indicative of presence that do not operate continuously
    presence_devices = ["Light", "MotionSensor", "SmartPlug", "PresenceSensor", "Television"]
    df = df[df["device"].isin(presence_devices)]

    # Count usage by hour
    hourly_usage = df.groupby("hour").size().reset_index(name="usage")

    # Identify absence hours as those with significantly lower usage
    mean_usage = hourly_usage["usage"].mean()
    std_usage = hourly_usage["usage"].std()
    absence_hours = hourly_usage[hourly_usage["usage"] < mean_usage - std_usage]["hour"].tolist()

    # Plot absence patterns
    plt.figure(figsize=(12, 6))
    plt.bar(hourly_usage["hour"], hourly_usage["usage"], color="blue", alpha=0.7)
    plt.axhline(mean_usage - std_usage, color="red", linestyle="--", label="Absence Threshold")
    plt.title(f"Absence Patterns Based on Device Usage in {country}")
    plt.xlabel("Hour")
    plt.ylabel("Usage Count")
    plt.xticks(range(24))
    plt.legend()
    plt.tight_layout()

    # Save the plot
    if not os.path.exists('result'):
        os.makedirs('result')
    if not os.path.exists('result/absence-patterns/'):
        os.makedirs('result/absence-patterns/')
    plt.savefig(f"result/absence-patterns/absence-patterns-{country}.png")

    print(f"Absence hours for {country}: {absence_hours}")

# List of countries and their corresponding data files
countries = {
    "France": {"routines_file": "fr/routine_device_corpus.txt", "dict_file": "fr/dictionary.py"},
    "Korea": {"routines_file": "kr/routine_device_corpus.txt", "dict_file": "kr/dictionary.py"},
    "USA": {"routines_file": "us/routine_device_corpus.txt", "dict_file": "us/dictionary.py"},
    "Spain": {"routines_file": "sp/routine_device_corpus.txt", "dict_file": "sp/dictionary.py"}
}

# Process each country
for country, files in countries.items():
    print(f"Processing data for {country}...")
    routines_file = files["routines_file"]
    dict_file = files["dict_file"]

    if os.path.exists(routines_file) and os.path.exists(dict_file):
        routines = load_routines(routines_file)
        device_dict = load_device_dict(dict_file)
        analyze_absence_patterns(routines, device_dict, country)
    else:
        print(f"Data files for {country} are missing.")

print("Analysis complete! Absence pattern graphs saved in the 'result' folder.")