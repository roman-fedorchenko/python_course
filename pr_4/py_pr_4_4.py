print("Variant 20 of practic 4. Task 4")
n=-1
while not n>0:
    n = int(input("Enter N (>0): "))
mass = [int(input(f"Enter element {i+1}: ")) for i in range(n)]

mass = [0 if x < 0 else x for x in mass]
print("Mass:", mass)