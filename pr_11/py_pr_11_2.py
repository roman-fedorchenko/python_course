import pandas as pd
import matplotlib.pyplot as plt
import os

# Налаштування стилю графіків
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

# Вказуємо назву вашого файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, 'data_2.csv') 

try:
    # 1. Завантаження та попередня обробка даних
    df_velo = pd.read_csv(filename, encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')
    
    if 'Unnamed: 1' in df_velo.columns:
        df_velo = df_velo.drop(columns=['Unnamed: 1'])
        
    df_clean = df_velo.dropna(axis=1, how='all')
    
    # Розрахунки, які потрібні для ВСІХ завдань
    monthly_data = df_clean.resample('M').sum()
    total_per_path = df_clean.sum().sort_values(ascending=False)
    total_cyclists = total_per_path.sum()

    print("ANALYSIS OF DATA ON THE USE OF CYCLING PATHS (2010)")

    # --- ЗАВДАННЯ 1: Загальна кількість велосипедистів ---
    print(f"\n1. Total number of cyclists in 2010: {int(total_cyclists)}")
    
    # --- ЗАВДАННЯ 2: Кількість велосипедистів на кожній доріжці ---
    print("\n2. Total number of cyclists on each cycle path:")
    print(total_per_path.to_string()) # Виводимо весь список

    # --- ЗАВДАННЯ 3: Найпопулярніший місяць для 3-х доріжок ---
    # Обираємо ТОП-3 найпопулярніші доріжки за обсягом трафіку
    top_3_paths = total_per_path.head(3).index

    print(f"\n3. The most popular month for selected tracks:")
    for path in top_3_paths:
        # idxmax знаходить дату з максимальним значенням
        best_month_idx = monthly_data[path].idxmax()
        best_month_name = best_month_idx.strftime('%B')
        count = monthly_data.loc[best_month_idx, path]
        print(f"Track '{path}': {best_month_name} ({int(count)} cyclists)")

    # --- ЗАВДАННЯ 4: Побудова графіку ---
    # Вибираємо найпопулярнішу доріжку для графіку
    most_popular_path = total_per_path.index[0]
    path_to_plot = most_popular_path
    
    monthly_data[path_to_plot].plot(kind='bar', color='teal', width=0.8)

    plt.title(f'Dynamics of bicycle path visits: {path_to_plot} (2010)', fontsize=15)
    plt.xlabel('Month')
    plt.ylabel('Number of cyclists')
    
    # Налаштування підписів по осі X
    month_names_abbr = [d.strftime('%b') for d in monthly_data.index]
    plt.xticks(
        range(len(month_names_abbr)),
        month_names_abbr,
        rotation=45
    )

    plt.tight_layout()
    plt.show()

# Обробка помилок
except FileNotFoundError:
    print(f"ERROR: File '{filename}' not found.")
except Exception as e:
    print(f"An error has occurred: {e}")