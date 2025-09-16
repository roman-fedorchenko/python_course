print("Variant 20 of practic 1. Task 3")
n=-1
while not 1<=n<=9:
    n=int(input("Enter a number: "))
for i in range(1, n + 1):
    print("  " * (n - i), end="")
    for num in range(1, i + 1):
        print(num, end=" ")
    print()
for i in range(n, 0, -1):
    print("  "*(n-1), end="")
    for j in range(i, 0, -1):
        print(j, end=" ")
    print()