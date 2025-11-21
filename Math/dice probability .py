import numpy as np

r = np.random.random(20000)

r = r*6 + 1

print((np.floor(r) == 1).mean())
print((np.floor(r) == 2).mean())
print((np.floor(r) == 3).mean())
print((np.floor(r) == 4).mean())
print((np.floor(r) == 5).mean())
print((np.floor(r) == 6).mean())
