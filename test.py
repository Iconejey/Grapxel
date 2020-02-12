def f(x): return x**3 - 2*x**2 + 3*x - 16

print([(y if (y:=f(a)) % 4 == 0 else 0) for a in range(10)])