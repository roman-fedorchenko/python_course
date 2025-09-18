from f import f
print("Variant 20 of practic 2. Task 2")
n=-1
while not (n>0):
    n=int(input("Input your natural n (n>=0): "))
    mass, p = f(n)
    if p:
        print(n," is a perfect number")
        print("Divisors of", n, "are:", mass)
    else:
        print(n," is not a perfect number")