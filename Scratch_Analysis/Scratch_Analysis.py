
#%%
from skimage import io
from matplotlib import pyplot as plt
from skimage.morphology import disk
from skimage.filters.rank import entropy
from skimage.filters import threshold_otsu

#%%
def segment_img(img):
    img = io.imread(image_path)
    # applying entropy to segment based to texture
    entropy_img = entropy(img,disk(10))
    # get threshold value and create a binary segmented image
    threshold_val = threshold_otsu(entropy_img)
    segmented_img = entropy_img > threshold_val
    return segmented_img

#%%
import glob
import numpy as np

# storing scratch area collected over time
scratch_area_data = []
path = "scratch_images/*.*"

for image_path in glob.glob(path):
    segmented_img = segment_img(image_path)
    # quantify the scratch area and print
    scratch_area_percentage = (np.sum(segmented_img == False)/segmented_img.size)*100
    scratch_area_data.append(scratch_area_percentage)

#%%
# lets plot the result
time_data = np.array([i for i in range(len(scratch_area_data))])

# applying linear regression
from scipy.stats import linregress
slop, intercept, *rest = linregress(time_data, scratch_area_data)

plt.plot(time_data,scratch_area_data,'bo')
plt.plot(time_data, (slop*time_data)+ intercept,label=f'y = {round(slop,2)}x + {round(intercept,2)}')
plt.xlabel('Days')
plt.ylabel('Scratch Area')
plt.title("Scratch Analysis")
plt.legend()  
plt.show()
