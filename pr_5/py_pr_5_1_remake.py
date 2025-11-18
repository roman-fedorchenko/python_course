import random

def generate_passengers(n):
    return {
        f"passenger{i}": [round(random.uniform(23, 27), 1) for _ in range(random.randint(1, 5))]
        for i in range(1, n + 1)
    }

def analyze_passengers(passengers):
    
    print(f"{'Passenger':<15} | {'Count':<5} | {'Total weight':<10} | {'Things'}")
    print("-" * 60)
    
    all_weights = []
    
    for name, weights in passengers.items():
        total_weight = sum(weights)
        count = len(weights)
        all_weights.extend(weights)
        print(f"{name:<15} | {count:<5} | {total_weight:<10.1f} | {weights}")
    #А
    print("-" * 60)
    count_many_items = sum(1 for w in passengers.values() if len(w) > 2)
    print(f"а) Пpassengers with more than 2 items: {count_many_items}")
    #Б
    count_single_light = sum(1 for w in passengers.values() if len(w) == 1 and w[0] < 25)
    print(f"б) Passengers with only 1 item weighing less than 25 kg: {count_single_light}")
    #В
    if not all_weights:
        print("в) It is impossible to calculate the average (data is not available).")
        return

    avg_weight = sum(all_weights) / len(all_weights)
    print(f"   [The average weight of one thing: {avg_weight:.2f} kg]")

    matching_passengers = [
        name for name, weights in passengers.items()
        if all(abs(w - avg_weight) <= 0.5 for w in weights)
    ]

    if matching_passengers:
        print(f"в) Passengers, where the weight of each item is ≈ average:")
        print("   " + ", ".join(matching_passengers))
    else:
        print("в) No such passengers were found.")

if __name__ == "__main__":
    print("Variant 20 of practic 5. Task 1 (Optimized)\n")
    data = generate_passengers(10)
    analyze_passengers(data)