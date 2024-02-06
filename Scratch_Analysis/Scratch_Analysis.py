
#%%
from skimage import io
from matplotlib import pyplot as plt

#%%
path = "scratch_images/Scratch0.jpg"
img = io.imread(path)

#%%
plt.imshow(img,cmap="gray")
