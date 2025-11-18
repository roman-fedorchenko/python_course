import matplotlib.pyplot as plt
import numpy as np
import json
import os
# потрібно для коректного шляху до файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'passengers.json')
# Читання даних з JSON файлу
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        passengers_data = json.load(f)
# Якщо файл не знайдено, використовуються вбудовані дані
except FileNotFoundError:
    print("File not found, using built-in data.")
    passengers_data = [
        {"weight_kg": 20.5}, {"weight_kg": 4.0}, {"weight_kg": 15.0},
        {"weight_kg": 32.0}, {"weight_kg": 3.5}, {"weight_kg": 26.5},
        {"weight_kg": 12.0}, {"weight_kg": 45.0}, {"weight_kg": 10.0},
        {"weight_kg": 25.0}
    ]
# Підрахунок кількості пасажирів у кожній категорії ваги багажу
count_less_5 = sum(1 for p in passengers_data if p['weight_kg'] < 5)
count_between_5_25 = sum(1 for p in passengers_data if 5 <= p['weight_kg'] <= 25)
count_more_25 = sum(1 for p in passengers_data if p['weight_kg'] > 25)
# Побудова кругової діаграми
data = [count_less_5, count_between_5_25, count_more_25]
ingredients = ["< 5 kg", "5-25 kg", "> 25 kg"]
fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} pas.)"

wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
    textprops=dict(color="w"),
    colors=['#4CAF50', '#FFC107', '#F44336']) 

ax.legend(wedges, ingredients,
    title="Weight categories",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=10, weight="bold")

ax.set_title("Distribution of passengers by baggage weight")

plt.show()