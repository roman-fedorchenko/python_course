print("Variant 20 of practic 4. Task 1")
print("Given a one-dimensional array of N real elements. Find the minimum negative element.")
n=-1
while not n>0:
    n = int(input("Enter N (>0): "))
mass = [float(input(f"Enter element {i+1}: ")) for i in range(n)]

negatives = [x for x in mass if x < 0]
print("Minimum negative element:", min(negatives) if negatives else "No negative elements.")