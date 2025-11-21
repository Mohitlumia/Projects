import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

def loop(x,r,t=1):
	while t <= 20:
		x = r*x*(1-x)
		t +=1
		y = round(x,5)
		yield y

lis_b = list(loop(0.4,2.6))

x_b=list(range(1,21))
y_b=lis_b

plt.plot(x_b,y_b,"bo-",linewidth="1",)

plt.title('Title')
plt.xlabel('Xaxis')
plt.ylabel('Yaxis')

plt.grid(True,color='k')

plt.show()