def f(n):
    mass = []
    for i in range(1, n):
        if n % i == 0:
            mass.append(i)
    p = sum(mass) == n
    return mass, p


