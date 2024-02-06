
#%%
from skimage import io
from matplotlib import pyplot as plt
from skimage.morphology import disk
from skimage.filters.rank import entropy
from skimage.filters import threshold_otsu
import numpy as np
import glob
#%%
# storing scratch area collected over time
path = "scratch_images/*.*"
scratch_area_data = []

#%%
for image_path in glob.glob(path):
    img = io.imread(image_path)
    # applying entropy to segment based to texture
    entropy_img = entropy(img,disk(10))
    # get threshold value and create a binary segmented image
    threshold_val = threshold_otsu(entropy_img)
    segmented_img = entropy_img > threshold_val
    # quantify the scratch area and print
    scratch_area_percentage = (np.sum(segmented_img == False)/segmented_img.size)*100
    scratch_area_data.append(scratch_area_percentage)
#%%
# lets plot the result
time_data = [i for i in range(len(scratch_area_data))]
plt.plot(time_data,scratch_area_data,'-o')
plt.show()
