import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# потрібно для коректного шляху до файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data.csv')
# Читання даних з CSV файлу
try:
    df = pd.read_csv(file_path)
    year_cols = [col for col in df.columns if 'YR' in col]
    years_clean = [col.split(' ')[0] for col in year_cols]
# Функція для отримання даних певної країни
    def get_country_data(country_name):
        row = df[df['Country Name'] == country_name]
        if row.empty:
            return None
        data = row[year_cols].values.flatten()
        return pd.to_numeric(data, errors='coerce')
# Задання країн для лінійного графіка
    country1 = 'Ukraine'
    country2 = 'United States'

    y1 = get_country_data(country1)
    y2 = get_country_data(country2)

    if y1 is not None and y2 is not None:
        plt.figure(figsize=(10, 6))
# Побудова лінійних графіків
        plt.plot(years_clean, y1, label=country1, color="blue", marker='o', linewidth=2)
        plt.plot(years_clean, y2, label=country2, color="red", marker='s', linewidth=2)
# Додавання підписів та легенди
        plt.title('Inflation, consumer prices (annual %)', fontsize=15)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Inflation (%)', fontsize=12)
        plt.legend()
        plt.grid(True)
# Відображення графіка
        print(f"Schedule for {country1} and {country2} created.")
        plt.show()
# Обробка випадку, якщо країна не знайдена
# Користувач вводить країну для стовпчикової діаграми
    else:
        print(f"Error: No data found for {country1} or {country2}")

    print("\nBuilding a bar chart")
    user_country = input("Enter the name of the country (in English, e.g. Poland): ").strip()
    
    y_user = get_country_data(user_country)

    if y_user is not None:
        plt.figure(figsize=(10, 6))

        plt.bar(years_clean, y_user, color='green', alpha=0.7, label=user_country)

        plt.title(f'Inflation Dynamics: {user_country}', fontsize=15)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Inflation (%)', fontsize=12)
        plt.legend()
        plt.grid(axis='y')
        
        print(f"Chart for {user_country} created.")
        plt.show()
    else:
        print(f"Country '{user_country}' was not found in the file. Check the spelling.")

except FileNotFoundError:
    print(f"Error: File. '{file_path}' not found.")
except Exception as e:
    print(f"An error has occurred: {e}")