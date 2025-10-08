print("Variant 20 of practic 4. Task 3")
n=-1
while not n>0:
    n = int(input("Enter N (>0): "))
mass = [input(f"Enter element {i + 1}: ") for i in range(n)]

mass_a = [x for x in mass if x.isalpha()]
mass_b = [x for x in mass if x.isdigit()]

print("Alphabetic elements:", mass_a)
print("Numeric elements:", mass_b)
