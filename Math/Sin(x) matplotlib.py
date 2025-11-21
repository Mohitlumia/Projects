import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

xaxis=np.linspace(0,np.pi*2,100)
yaxis=np.sin(xaxis)

xfill=np.linspace(0,np.pi,100)
yfill=np.sin(xfill)

xfill2=np.linspace(np.pi,np.pi*2,100)
yfill2=np.sin(-xfill)

plt.plot(xaxis,yaxis,"k")
P=plt.fill(xfill,yfill,"c")
N=plt.fill(xfill2,yfill2,"r")

plt.title('Sin(X)')
plt.xlabel('Xaxis')
plt.ylabel('Yaxis')

plt.legend((P[0],N[0]),('Positive','Negative'))

plt.grid(True,color='k')

plt.show()