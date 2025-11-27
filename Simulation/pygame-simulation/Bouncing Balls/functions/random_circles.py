
import random
from objects.circles import Circles

def random_circles(num_circles = 5, width = 800, height = 600):
    circles_lis = []
    
    for _ in range(num_circles): # Create 50 circles with random attributes
        r = random.randint(15, 25)
        x = random.randint(r, width - r)
        y = random.randint(r, height - r)
        vx = random.randint(0, 1) / 5
        vy = random.randint(0, 1) / 5
        color = (
            random.randint(50, 200),
            random.randint(100, 150),
            random.randint(50, 100),
        )

        circles_lis.append(Circles(x, y, r, color, vx, vy))
    return circles_lis