'''
Test code
'''
import os
from datetime import datetime
# os.system('py main.py 100 5 0.1 0.2 0.0001 0.999 -f sample_data run')
N = 10000
T = 100

argument = 'py main.py {} {} 0.85 0.2 0.05 0.0001 -f HaCondom'.format(N, T)
os.system(argument)

# 'py main.py {} {} {} 0.8 0.2 0.01 -f data_alpha{}_{} run'
