import random

# Функція генерації початкових даних (для зручності)
def generate_passengers(n=10):
    data = {}
    for i in range(1, n + 1): 
        weight = [] 
        length = random.randint(1, 5)
        for j in range(length):
            w = round(random.uniform(23, 27), 1)  
            weight.append(w)
        data["passenger" + str(i)] = weight
    return data

# Виведення на екран всіх значень словника
def print_dictionary(data):
    print("\nCurrent dictionary content")
    if not data:
        print("The dictionary is empty.")
        return
    for name, weights in data.items():
        print(f"{name}: {weights} (total number of items: {len(weights)}, total weight: {sum(weights):.1f} kg)")

# Додавання нового запису
def add_record(data, name, weights):
    if name in data:
        print(f"\n[Error] Passenger '{name}' already exists in the database.")
    else:
        data[name] = weights
        print(f"\n[Info] Entry added: {name} -> {weights}")

# Видалення запису
def delete_record(data, name):
    if name in data:
        del data[name]
        print(f"\n[Info] Deleted entry: {name}")
    else:
        print(f"\n[Error] Passenger '{name}' not found, deletion impossible.")

# Перегляд вмісту за відсортованими ключами
def print_sorted_dictionary(data):
    print("\nGlossary (sorted by keywords)")
# Використовуємо функцію sorted() до ключів
    sorted_keys = sorted(data.keys())
    
    for key in sorted_keys:
        weights = data[key]
        print(f"{key}: {weights}")

# Розв’язання завдань варіанту (А, Б, В)
def solve_variant_tasks(data):
    print("\nAnalysis results (Option 20)")
    
    if not data:
        print("No data available for analysis.")
        return

    # Завдання А
    count_a = sum(1 for weights in data.values() if len(weights) > 2)
    print(f"а) Passengers with more than 2 items: {count_a}")

# Завдання Б
# Виправляємо логіку умови: len=1 та вага < 25
    count_b = sum(1 for weights in data.values() if len(weights) == 1 and weights[0] < 25)
    print(f"б) Passengers with only 1 item weighing less than 25 kg: {count_b}")

# Завдання В
    all_weights = [w for weights in data.values() for w in weights]
    
    if not all_weights:
        print("в) There are no items, so it is impossible to calculate the average weight.")
        return

    avg_weight = sum(all_weights) / len(all_weights)
    print(f"   (Average weight of one item: {avg_weight:.2f} kg)")

    matching_passengers = [
        name for name, weights in data.items()
        if all(abs(w - avg_weight) <= 0.5 for w in weights)
    ]

    if matching_passengers:
        print(f"в) Luggage numbers where the weight of items is approximately average (±0.5 kg):")
        for p in matching_passengers:
            print(f"   - {p}")
    else:
        print(f"в) No luggage where the weight of all items is close to average.")

# Основний блок виконання програми
if __name__ == "__main__":
    print("Variant 20 of practic 5. Task 1 (Functions)")
    
# Створення бази
    passengers = generate_passengers(10)
    
# Виведення
    print_dictionary(passengers)
    
# Додавання запису
    new_luggage = [24.5, 25.0]
    add_record(passengers, "passenger_NEW", new_luggage)
    
# Видалення запису (наприклад, passenger1)
    delete_record(passengers, "passenger1")
    
# Виведення відсортованого словника
    print_sorted_dictionary(passengers)
    
# Виконання завдань варіанту
    solve_variant_tasks(passengers)