import os
import pandas as pd
import matplotlib.pyplot as plt

# Dictionnary to map device names to IDs
device_dict = {
    'AirConditioner': 0,
    'AirPurifier': 1,
    'Blind': 2,
    'Camera': 3,
    'ClothingCareMachine': 4,
    'Computer': 5,
    'ContactSensor': 6,
    'CurbPowerMeter': 7,
    'Dishwasher': 8,
    'Dryer': 9,
    'Elevator': 10,
    'Fan': 11,
    'GarageDoor': 12,
    'Light': 13,
    'Microwave': 14,
    'MotionSensor': 15,
    'NetworkAudio': 16,
    'None': 17,
    'Other': 18,
    'Oven': 19,
    'PresenceSensor': 20,
    'Projector': 21,
    'Refrigerator': 22,
    'RemoteController': 23,
    'RobotCleaner': 24,
    'Siren': 25,
    'SmartLock': 26,
    'SmartPlug': 27,
    'Switch': 28,
    'Television': 29,
    'Thermostat': 30,
    'Washer': 31,
    'WaterValve': 32
}

# Map device IDs to names
id_to_device = {v: k for k, v in device_dict.items()}

# Function to load routines from a file
def load_routines(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()
    routines = [list(map(int, line.strip().split())) for line in data]
    return routines

# Analyze routines for a given country
def analyze_routines(routines, country):
    device_counts = {}
    for routine in routines:
        for device in routine:
            device_name = id_to_device.get(device, "Unknown")
            device_counts[device_name] = device_counts.get(device_name, 0) + 1

    # Sort devices by usage count
    sorted_devices = sorted(device_counts.items(), key=lambda x: x[1], reverse=True)
    top_devices = dict(sorted_devices[:10])

    plt.figure(figsize=(10, 6))
    plt.bar(top_devices.keys(), top_devices.values())
    plt.title(f"Top 10 appareils utilisés en {country}")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Nombre d'utilisations")
    plt.xlabel("Appareils")
    plt.tight_layout()
    plt.show()

    return sorted_devices

# List of countries and their routine files
countries = {
    "France": "data/fr/routine_device_corpus.txt",
    "Korea": "data/kr/routine_device_corpus.txt",
    "USA": "data/us/routine_device_corpus.txt",
    "Spain": "data/sp/routine_device_corpus.txt"
}

# Analyze routines for each country
for country, file_path in countries.items():
    if os.path.exists(file_path):
        print(f"Analyse des routines pour {country}:")
        routines = load_routines(file_path)
        analyze_routines(routines, country)
    else:
        print(f"Fichier non trouvé pour {country}: {file_path}")
