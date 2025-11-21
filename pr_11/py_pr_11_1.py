import pandas as pd
import numpy as np
import random
#примітка: спрочатку створити словник, а потім вже dataframe
# Перемінна для конторолю виводу
pr=8

# Генерація даних
def generate_data_dict(n):
# Ініціалізуємо словник, де ключі — це майбутні колонки
    data = {
        "Passenger": [],
        "Items_Count": [],
        "Total_Weight_kg": [],
        "Category": []
    }
    
    for i in range(1, n + 1):
# Генеруємо дані (так само як і раніше)
        items_count = random.randint(1, 5)
        weights = [round(random.uniform(5, 20), 1) for _ in range(items_count)]
        total_weight = sum(weights)
        category = random.choice(["Economy", "Business", "VIP"])
# Додаємо дані у відповідні списки всередині словника
        data["Passenger"].append(f"Pass_{i}")
        data["Items_Count"].append(items_count)
        data["Total_Weight_kg"].append(round(total_weight, 2))
        data["Category"].append(category)
        
    return data

# Генеруємо словник
raw_data_dict = generate_data_dict(2000)

# Перевіримо, як виглядає словник (для наочності)
# print(raw_data_dict) 

# Створюємо DataFrame зі словника
df = pd.DataFrame(raw_data_dict)

print(f"1. DataFrame content (first {pr} rows)")
print("-"*100)
print(df.head(pr))
print("-"*100)

print("\n2. Data types")
print("-"*100)
print(df.dtypes)
print("-"*100)

print("\n3. Dimension (rows, columns)")
print("-"*100)
print(df.shape)
print("-"*100)

print("\n4. Descriptive statistics")
print("-"*100)
print(df.describe())
print("-"*100)

# Додавання нових стовпців
df['Cost_Per_Kg'] = 50
df['Total_Cost_UAH'] = (df['Total_Weight_kg'] * df['Cost_Per_Kg']) + 100

print(f"\n5. Added cost column (first {pr} rows)")
print("-"*100)
print(df[['Passenger', 'Total_Weight_kg', 'Total_Cost_UAH']].head(pr))
print("-"*100)

# Фільтрація даних за вартістю >2000
expensive_luggage = df[df['Total_Cost_UAH'] > 2000]
print(f"\n6. Filtering (cost > 2000 UAH): {len(expensive_luggage)} records found")
print("-"*100)
print(expensive_luggage)
print("-"*100)

# Сортування даниз за вагою
sorted_df = df.sort_values(by='Total_Weight_kg', ascending=False)
print("\n7. Top 3 passengers with the heaviest luggage")
print("-"*100)
print(sorted_df.head(3))
print("-"*100)

# Групування та агрегація даних за категоріями
grouped = df.groupby('Category')['Total_Weight_kg'].mean()
print("\n8. Average baggage weight by category")
print("-"*100)
print(grouped)
print("-"*100)

# Додаткова агрегація
agg_stats = df.groupby('Category').agg({
    'Total_Cost_UAH': ['max', 'sum'],   # Максимальна та сумарна вартість
    'Passenger': 'count'                # Кількість пасажирів
})
print("\n9. Advanced statistics by category")
print("-"*100)
print(agg_stats)
print("-"*100)