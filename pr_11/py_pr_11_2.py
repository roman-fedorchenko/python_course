import pandas as pd
import matplotlib.pyplot as plt
import os

# Налаштування стилю графіків
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

# Вказуємо назву вашого файлу
# Використовуємо Path join для надійності шляху
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, 'data_2.csv') 

try:
    # 1. Завантаження даних
    df_velo = pd.read_csv(filename, encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')

    # --- ОЧИЩЕННЯ ДАНИХ ---
    if 'Unnamed: 1' in df_velo.columns:
        df_velo = df_velo.drop(columns=['Unnamed: 1'])

    # Видаляємо колонки, які містять лише нулі/NaN (щоб не плутати користувача)
    df_clean = df_velo.dropna(axis=1, how='all')

    # 2. Агрегація даних по місяцях
    # resample('M') гарантує, що ми матимемо 12 точок даних (по одній за місяць)
    monthly_data = df_clean.resample('M').sum()
    
    # 3. Вибір доріжки для графіку
    # Беремо найпопулярнішу доріжку за рік для більш наочного графіку
    most_popular_path = monthly_data.sum().idxmax()
    path_to_plot = most_popular_path
    
    # 4. Побудова графіку (Bar Chart)
    monthly_data[path_to_plot].plot(kind='bar', color='teal', width=0.8)
    
    plt.title(f'Динаміка відвідування велодоріжки: {path_to_plot} (2010)', fontsize=15)
    plt.xlabel('Місяць')
    plt.ylabel('Кількість велосипедистів')
    
    # --- ВИПРАВЛЕННЯ (ПІДТВЕРДЖЕННЯ) ---
    # Цей блок гарантує, що кожен місяць буде позначено на осі Х
    month_names_abbr = [d.strftime('%b') for d in monthly_data.index]
    plt.xticks(
        range(len(month_names_abbr)), # Позиції від 0 до 11
        month_names_abbr,            # Підписи 'Jan', 'Feb', ...
        rotation=45
    )
    
    plt.tight_layout()
    plt.show()

    # Попередні розрахунки, які вимагала умова:
    total_cyclists = df_clean.sum().sum()
    print(f"\nЗагальна кількість велосипедистів за 2010 рік: {int(total_cyclists)}")

except FileNotFoundError:
    print(f"ПОМИЛКА: Файл '{filename}' не знайдено.")
except Exception as e:
    print(f"Виникла помилка: {e}")