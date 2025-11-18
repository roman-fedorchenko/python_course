import pandas as pd
import numpy as np
import random

# Перемінна для конторолю виводу
pr=8

# Генерація даних (як у Практичній №5)
def generate_data(n):
    data = []
    for i in range(1, n + 1):
# Генеруємо кількість речей (1-5) та їх вагу
        items_count = random.randint(1, 5)
        weights = [round(random.uniform(5, 20), 1) for _ in range(items_count)]
        total_weight = sum(weights) 
# Додаємо запис у список
        data.append({
            "Passenger": f"Pass_{i}",
            "Items_Count": items_count,
            "Total_Weight_kg": round(total_weight, 2),
            "Category": random.choice(["Economy", "Business", "VIP"]) # Додаткова характеристика
        })
    return data

# Створюємо DataFrame
raw_data = generate_data(20)
df = pd.DataFrame(raw_data)

print(f"1. Вміст DataFrame (перші {pr} рядки)")
print("-"*100)
print(df.head(pr))
print("-"*100)

print("\n2. Типи даних")
print("-"*100)
print(df.dtypes)
print("-"*100)

print("\n3. Розмірність (рядки, стовпці)")
print("-"*100)
print(df.shape)
print("-"*100)

print("\n4. Описова статистика")
print("-"*100)
print(df.describe())
print("-"*100)

# Додавання нових стовпців
df['Cost_Per_Kg'] = 50
df['Total_Cost_UAH'] = (df['Total_Weight_kg'] * df['Cost_Per_Kg']) + 100

print(f"\n5. Додано стовпець вартості (перші {pr} рядки)")
print("-"*100)
print(df[['Passenger', 'Total_Weight_kg', 'Total_Cost_UAH']].head(pr))
print("-"*100)

# Фільтрація даних за вартістю >2000
expensive_luggage = df[df['Total_Cost_UAH'] > 2000]
print(f"\n6. Фільтрація (вартість > 2000 грн): знайдено {len(expensive_luggage)} записів")
print("-"*100)
print(expensive_luggage)
print("-"*100)

# Сортування даниз за вагою
sorted_df = df.sort_values(by='Total_Weight_kg', ascending=False)
print("\n7. Топ-3 пасажири з найважчим багажем")
print("-"*100)
print(sorted_df.head(3))
print("-"*100)

# Групування та агрегація даних за категоріями
grouped = df.groupby('Category')['Total_Weight_kg'].mean()
print("\n8. Середня вага багажу по категоріях")
print("-"*100)
print(grouped)
print("-"*100)

# Додаткова агрегація
agg_stats = df.groupby('Category').agg({
    'Total_Cost_UAH': ['max', 'sum'],  # Максимальна та сумарна вартість
    'Passenger': 'count'            # Кількість пасажирів
})
print("\n9. Розширена статистика по категоріях")
print("-"*100)
print(agg_stats)
print("-"*100)