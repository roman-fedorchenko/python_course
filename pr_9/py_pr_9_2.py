import json
import os
# потрібно для коректного шляху до файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'passengers.json')
# Створення JSON файлу з даними пасажирів
passengers_data = [
    {"surname": "Petrenko", "items_count": 3, "weight_kg": 20.5},
    {"surname": "Ivanov",   "items_count": 1, "weight_kg": 4.0},
    {"surname": "Sydorenko","items_count": 2, "weight_kg": 15.0},
    {"surname": "Kovalenko","items_count": 4, "weight_kg": 32.0},
    {"surname": "Bondar",   "items_count": 1, "weight_kg": 3.5},
    {"surname": "Tkachenko","items_count": 3, "weight_kg": 26.5},
    {"surname": "Shevchenko","items_count": 2, "weight_kg": 12.0},
    {"surname": "Melnyk",   "items_count": 5, "weight_kg": 45.0},
    {"surname": "Boyko",    "items_count": 1, "weight_kg": 10.0},
    {"surname": "Moroz",    "items_count": 2, "weight_kg": 25.0}
]
# Запис даних у JSON файл
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(passengers_data, f, ensure_ascii=False, indent=4)
    print(f"The JSON file has been successfully created: {file_path}")
except Exception as e:
    print(f"Error writing a file: {e}")

try:
# Читання даних з JSON файлу
    with open(file_path, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)

    passengers_with_many_items = []
    count_less_5 = 0
    count_between_5_25 = 0
    count_more_25 = 0
# Аналіз даних
    for passenger in loaded_data:
        surname = passenger['surname']
        items = passenger['items_count']
        weight = passenger['weight_kg']

        if items > 2:
            passengers_with_many_items.append(surname)

        if weight < 5:
            count_less_5 += 1
        elif 5 <= weight <= 25:
            count_between_5_25 += 1
        elif weight > 25:
            count_more_25 += 1
# Виведення результатів аналізу
    print("ANALYSIS RESULTS:")    
    print("\nа) Passengers who have more than two items:")
    if passengers_with_many_items:
        print(", ".join(passengers_with_many_items))
    else:
        print("There are no such passengers.")

    print("\nб) Baggage weight statistics:")
    print(f"   - Less than 5 kg:       {count_less_5} passengers")
    print(f"   - From 5 to 25 kg:   {count_between_5_25} passengers")
    print(f"   - More than 25 kg:     {count_more_25} passengers")
except FileNotFoundError:
    print("Error: JSON file not found.")
except Exception as e:
    print(f"An error occurred during processing: {e}")