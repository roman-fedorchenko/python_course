print("Variant 20 of practic 2. Task 1")
task=-1
n=-1
while not 1<=task<=2:
    task=int(input("Choise the task 1 or 2 : "))
if task==1:
    print("Task 1")
    print("Z=(m^0.5-n^0.5)/m")
    m=-1
    while not 0<= m:
        m=float(input("Input m (m>=0): "))
    while not 0<= n:
        n=float(input("Input n (n>=0): "))
    print("Z=", (m**0.5-n**0.5)/m)
elif task==2:
    print("Task 2")
    while not n>0:
        n=int(input("Input your natural n (n>=0): "))
    mass=[]
    for i in range(1,n):
         if(n%i==0):
             mass.append(i)
    if sum(mass)==n:
         print(n, "is perfect number")
         print("Divisors of", n, "are:", mass)
    else:
         print(n, "is not perfect number")