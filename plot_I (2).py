from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

N = 100
gamma = 0.2
data = []

x = np.multiply(np.linspace(0,1,num=21),100)
i = 0
while i < 21:
    filename = 'data_alpha{}_20200429.csv'.format(i*5)
    tmp = pd.read_csv(filename)
    data.append(np.divide(tmp.iloc[-1].to_numpy(),N))
    i += 1
#data_alpha0.6_20200427
# print(x)
data = pd.DataFrame(data, columns=['S', 'I', 'V', 'R'], index=x)
print(data)

y1 = data.iloc[:,1]
y2 = data.iloc[:,2]
y3 = data.iloc[:,3]
plt.title('N = 100, T = 100')
plt.xlabel('alpha (%)')
plt.ylabel('Fraction of infected/ vaccinated/ recovered population')
plt.plot(x,y1, label='I')
plt.plot(x,y2, label='V')
plt.plot(x,y3, label='R')
plt.legend(loc='upper right',bbox_to_anchor=(1, 0.5))
plt.show()
