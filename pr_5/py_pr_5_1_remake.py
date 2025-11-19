import random
print("Variant 20 of practic 5. Task 1")
passengers = {}
n = 10

for i in range(1, n + 1): 
    weight = [] 
    length = random.randint(1, 5)
    for j in range(length):
        w = round(random.uniform(23, 27), 1)  
        weight.append(w)
    passengers["passenger" + str(i)] = weight

for name, weights in passengers.items():
    print(f"{name}: {weights} (всього речей: {len(weights)}, сумарна вага: {sum(weights):.1f} кг)")

# завдання А
#a=sum(1 for name, weights in passengers.items() if  len(weights)> 2)
a = 0
for name, weight in passengers.items():
    if len(weight) > 2:
        a += 1
print("а) Пасажирів з більше ніж 2 речами:", a)

# завдання Б
#b=sum(1 for name, weights in passengers.items() if  len(weights)==1 and weights[0]<25)
b=0
for name, weight in passengers.items():
    if len(weight) == 1 and weight[0] < 25:
        b += 1
print("б) Пасажирів, у яких тільки 1 річ масою менше 25:", b)

# завдання В
#all_weights = [w for weights in passengers.values() for w in weights]
all_weights = []
for weights in passengers.values():
    for w in weights:
        all_weights.append(w)
avg_weight = sum(all_weights) / len(all_weights)

#matching_passengers = [name for name, weights in passengers.items() if all(abs(w - avg_weight) <= 0.5 for w in weights)]
matching_passengers = []
for name, weights in passengers.items():
    all_within_range = True
    for w in weights:
        if abs(w - avg_weight) > 0.5:
            all_within_range = False
            break
    if all_within_range:
        matching_passengers.append(name)

if matching_passengers:
    print(f"в) Номери багажів, де вага речей ≈ середній ({avg_weight:.2f} кг):")
    for p in matching_passengers:
        print("   ", p)
else:
    print(f"в) Немає багажів, де вага речей відрізняється від середньої ({avg_weight:.2f} кг) не більше ніж на 0.5 кг.")