from matplotlib import pyplot as plt
import pandas as pd

i = 0   # counter
N = 100
x = []
y1 = []
y2 = []
while i < 21:
    filename = 'data_beta{}_{}hr.csv'.format(i*5/100,'2020-04-08')
    df = pd.read_csv(filename)
    x.append(i*5/100)
    y1.append(df.iloc[-1,1]/N)
    y2.append(df.iloc[-1,2]/N)
    i += 1
plt.title('N = 100, T = 500')
plt.xlabel('Beta')
plt.ylabel('Fraction of infected/ vaccinated population (I)')
plt.plot(x,y1)
plt.plot(x,y2)
plt.show()
