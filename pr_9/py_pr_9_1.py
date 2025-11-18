import pandas as pd
import os
# потрібно для коректного шляху до файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data.csv')
# Спроба відкрити файл
try:
    print(f"Try to open file: {file_path}")
    data = pd.read_csv(file_path)
    print("File successfully opened.")
# Відфільтрувати дані для потрібного показника
    target_indicator = 'Inflation, consumer prices (annual %)'
    data_inf = data[data['Series Name'] == target_indicator].copy()

    result = []
# Аналіз даних за кожен рік
    for year in range(2010, 2020):
        col_name = f"{year} [YR{year}]"
# Перевірка наявності стовпця для року
        if col_name in data_inf.columns:
            series_numeric = pd.to_numeric(data_inf[col_name], errors='coerce')
# Знаходження максимуму та мінімуму
            max_idx = series_numeric.idxmax() 
            max_val = series_numeric.max()
            if pd.notna(max_idx):
                max_country = data_inf.loc[max_idx, 'Country Name']
            else:
                max_country = "No Data"
            min_idx = series_numeric.idxmin()
            min_val = series_numeric.min()
            if pd.notna(min_idx):
                min_country = data_inf.loc[min_idx, 'Country Name']
            else:
                min_country = "No Data"
# Збереження результатів
            result.append({
                'Year': year,
                'Max Country': max_country,
                'Max Value': max_val,   
                'Min Country': min_country,
                'Min Value': min_val
            })
# Виведення результатів
    result_data = pd.DataFrame(result)
    print("\nResults:")
    print(result_data)
# Збереження результатів у новий CSV файл
    output_path = os.path.join(script_dir, 'output.csv')
    result_data.to_csv(output_path, index=False)
    print(f"\nResult into file {output_path}")
# Обробка помилок при відкритті файлу
except FileNotFoundError:
    print("\nError:")
    print(f"The file was not found at the address:\n{file_path}")
except Exception as e:
    print(f"\nAn unexpected error occurred:\n{e}")