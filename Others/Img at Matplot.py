import cv2
import matplotlib.pyplot as plt

location = '/storage/emulated/0/Pictures/Screenshots/Screenshot_20200422-170826.jpg'

cv2image = cv2.imread(location)#, cv2.IMREAD_GRAYSCALE)
matimage = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)

plt.imshow(matimage)#, cmap = 'gray', interpolation = 'bicubic')
# gray because matplotlib use rgb and cv2 use brg color
plt.show()