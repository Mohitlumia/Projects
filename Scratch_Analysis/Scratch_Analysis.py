
#%%
from skimage import io
from matplotlib import pyplot as plt
from skimage.morphology import disk
from skimage.filters.rank import entropy
#%%
path = "scratch_images/Scratch0.jpg"
img = io.imread(path)
# applying entropy to segment based to texture
entropy_img = entropy(img,disk(10))
#%%
plt.imshow(entropy_img,cmap="gray")
