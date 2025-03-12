import os
from circle import area

radius = float(os.getenv('RADIUS', 1.0))  # По умолчанию радиус 1, если переменная не задана
circle_area = area(radius)
print(f"The area of the circle is: {circle_area}")