
#%%
from skimage import io
from matplotlib import pyplot as plt
from skimage.morphology import disk
from skimage.filters.rank import entropy
from skimage.filters import threshold_otsu
import numpy as np
#%%
path = "scratch_images/Scratch0.jpg"
img = io.imread(path)
# applying entropy to segment based to texture
entropy_img = entropy(img,disk(10))
#%%
# get threshold value and create a binary segmented image
threshold_val = threshold_otsu(entropy_img)
segmented_img = entropy_img > threshold_val
#%%
# quantify the scratch area and print
scratch_area_percentage = (np.sum(segmented_img == False)/segmented_img.size)*100
print(scratch_area_percentage)
#%%
plt.imshow(segmented_img,cmap="gray")