'''
Sweep through different infection rates (beta)
'''
import os
from datetime import datetime
# os.system('py main.py 100 5 0.1 0.2 0.0001 0.999 -f sample_data run')
N = 100000
T = 500
i = 0   # counter
while i < 21:
    argument = 'py main.py {} {} 0.1 {} 0.001 0.0001 -f data_beta{}_{} run'.format(N, T, i*5/100, i*5/100, datetime.today().strftime('%Y%m%d'))
    os.system(argument)
    i += 1
