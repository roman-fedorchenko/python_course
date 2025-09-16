print("Variant 20 of practic 1. Task 1")
a=-1
b=-1
while not 1<=a<=100:
    a=int(input("Enter A in in range 1-100: "))
while not 1<=b<=100:
    b=int(input("Enter B in in range 1-100: "))
if(a>b):
    x=pow(a,2)-b
    print("X=a^2-b=",x)
elif(a==b):
    x=-a;
    print("X=-a=",x)
else:
    x=(a*b-1)/b
    print("X=(a*b-1)/b=",x)