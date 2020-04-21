from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

T = 500

x = np.linspace(0,T,num=T-1)
df = pd.read_csv('data_beta0.8_2020-04-08hr.csv')
y1 = df.iloc[:,1]
y2 = df.iloc[:,2]
plt.title('N = 100, T = 500, beta = 80%')
plt.xlabel('t')
plt.ylabel('Fraction of infected/ vaccinated population (I)')
plt.plot(x,y1)
plt.plot(x,y2)
plt.show()
