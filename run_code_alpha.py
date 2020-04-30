'''
Sweep through different lifestyle rates (alpha)
'''
import os
from datetime import datetime
# os.system('py main.py 100 5 0.1 0.2 0.0001 0.999 -f sample_data run')
N = 100
T = 100
i = 0   # counter
while i < 21:
    argument = 'py main.py {} {} {} 0.2 0.05 0.01 -f data_alpha{}_{} run'.format(N, T, i*5/100, i*5, datetime.today().strftime('%Y%m%d'))
    os.system(argument)
    i += 1
# 'py main.py {} {} {} 0.8 0.2 0.01 -f data_alpha{}_{} run'
