from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

T = 100
gamma = 0.2

x = np.linspace(0,T,num=T-1)
df = pd.read_csv('Hacondom.csv')
y0 = df.iloc[:,0].divide(10000)
y1 = df.iloc[:,1].divide(10000)
y2 = df.iloc[:,2].divide(10000)
y3 = df.iloc[:,3].divide(10000)
plt.title('N = 10000, alpha = 85%, beta = 20%, Condom use')
plt.xlabel('t')
plt.ylabel('Fraction of Compartments')
plt.plot(x,y0)
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)
plt.legend(['S', 'I', 'V', 'R'])
plt.show()
