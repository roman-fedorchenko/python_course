import matplotlib.pyplot as plt
import numpy as np
# Визначення діапазону значень x та обчислення відповідних значень y
x = np.linspace(1, 10, 1000)
y = 5 * np.sin(x) * np.cos(x**2 + 1/x)**2
# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='5*sin(x)*cos(x^2+1/x)^2', color="green", linewidth=2)
# Додавання підписів та легенди
plt.title('Graph of a complex function', fontsize=15)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend()
plt.grid(True)
# Відображення графіка
plt.show()