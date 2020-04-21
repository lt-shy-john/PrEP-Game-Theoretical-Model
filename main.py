# Import libraries
import sys


# Import class files
from person import Person
from simulation import Simulation
import mode
from partner import Partner

'''
Main code

- cmd functions
- main loop
'''
def setting(N, T, alpha, beta, gamma, phi):
    info = input('Information about the parameters? [y/n] ').lower()
    print()
    if info == 'y':
        info_summ()
    print('Leave blank if not changing the value(s).')
    N_temp = input('N >>> ')
    N = set_correct_para(N_temp, N, pos=True)
    T_temp = input('T >>> ')
    T = set_correct_para(T_temp, T, pos=True)
    alpha_temp = input('alpha >>> ')
    alpha = set_correct_epi_para(alpha_temp, alpha)
    beta_temp = input('beta >>> ')
    beta = set_correct_epi_para(beta_temp, beta)
    gamma_temp = input('gamma >>> ')
    gamma = set_correct_epi_para(gamma_temp, gamma)
    phi_temp = input('phi >>> ')
    phi = set_correct_epi_para(phi_temp, phi)
    population = Person.make_population(N)
    return N, T, alpha, beta, gamma, phi

def summary():
    print('N: {}'.format(N))
    print('T: {}'.format(T))
    print('===== SIR Rate =====')
    print('alpha: {}'.format(alpha))
    print('beta: {}'.format(beta))
    print('gamma: {}'.format(gamma))
    print('phi: {}'.format(phi))
    print()
    info = input('Information about the parameters? [y/n] ').lower()
    if info == 'y':
        info_summ()

def show_nwk():
    try:
        partner_nwk.show_nwk()
    except NameError:
        print('Topology will be generated after the first run.')
        pass

def info_summ():
    print('N - Number of simulated agents.')
    print('T - Time steps/ period of simulation.')
    print('Alpha - Adoption of vaccination/ PrEP (willingness).')
    print('Beta - Infection rate.')
    print('Gamma - Recovery rate.')
    print('Phi - Protection wear off rate.')

def help():
    print('RUN/ START - Start the simulation.')
    print('SETTING - Reset simulation settings.')
    print('MODE - Change mode settings.')
    print('SUMMARY - Print the simulation parameters.')
    print('QUIT/ Q - Quit the software.')

def correct_para(p, pos=False):
    '''
    Convert the parameters into integers.

    Parameters
    p -- input.
    - pos: If the parameter is positive number.
    '''
    try:
        p_num = int(p)
        if pos == True and p_num < 1:
            p_num = 1
        return p_num
    except ValueError:
        p_num = 1
        return p_num

def set_correct_para(p, P, pos=False):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_para(p, pos=False)

def correct_epi_para(p):
    '''
    Convert epidemic parameters into floats.

    Parameters
    - p: Epidemic rate, positive decimal less than 1.
    '''
    try:
        p_num = float(p)
        if p_num < 0 or p_num > 1:
            p_num = 0
            print('Please check your inputs and change them in SETTING.')
        return p_num
    except ValueError:
        p_num = 0
        print('Please check your inputs and change them in SETTING.')
        return p_num

def set_correct_epi_para(p, P):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_epi_para(p)

def set_mode():
    cmd = ''
    while cmd != 'y':
        print('Select the following options:')
        print('01: Living in city/ suburb. [{}]'.format(mode01.flag))
        print('02: Visit GP/ Sex clinic []')
        print('03: Age groups (elder/ young) []')
        print('04: Add cost of PrEP []')
        print('05: Edit partner network')
        print('06: Risk compensation (%) []')
        print('21: Partner negotiates for sex []')
        print('22: Inflexible to taking PrEP []')
        print('23: Contrary to social groups []')
        print('31: Include on demand PrEP. []')
        print('Input number codes to change the options.')
        mode_input = input('> ')
        mode_settings(mode_input)
        cmd = input('Return to main menu? [y/n]')

def mode_settings(cmd):
    cmd = cmd.split(' ')
    print(cmd)
    if len(cmd) > 0:
        for i in range(len(cmd)):
            if cmd[i] == '01':
                mode01()
            if cmd[i] == '05':
                mode05()
            elif cmd[i] == '31':
                mode31()



def export(filename):
    print('Coming soon')

print('  ======================================  \n\n')
print('  Agent Based Modelling: PrEP SIRP Model  \n\n')
print('  ======================================  ')
print()
if len(sys.argv) == 1:
    N = input('Number of people (N): ')
    N = correct_para(N, pos=True)
    T = input('Simulation time (T): ')
    T = correct_para(T)
    alpha = input('Adoption rate (alpha): ')
    alpha = correct_epi_para(alpha)
    beta = input('Infection rate (beta): ')
    beta = correct_epi_para(beta)
    gamma = input('Recovery rate (gamma): ')
    gamma = correct_epi_para(gamma)
    phi = input('Rate to resuscept (phi): ')
    phi = correct_epi_para(phi)
elif len(sys.argv) > 1:
    print('Using pre-defined inputs. ')
    try:
        N = correct_para(sys.argv[1], pos=True)
        T = correct_para(sys.argv[2])
        alpha = correct_epi_para(sys.argv[3])
        beta = correct_epi_para(sys.argv[4])
        gamma = correct_epi_para(sys.argv[5])
        phi = correct_epi_para(sys.argv[6])
    except:
        print('Exception encountered. Leaving program...')
        print('Usage: python3 main.py [N] [T] [alpha] [beta] [gamma] [phi] ...\n       [-m modes] [-f filename] [run]\n')
        quit()
print()

'''
Set initial variables
'''

population = Person.make_population(N)
partner_nwk = Partner(population)
filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.
mode01 = mode.Mode01(population)
mode05 = mode.Mode05(population, partner_nwk)
mode31 = mode.Mode31(population)

'''
Express mode

Loads the settings prior to the run. Optional keyword 'run' to run the simulation automatically.
'''
# Check file name to export
for i in range(len(sys.argv)):
    if sys.argv[i] == '-f' and sys.argv[i+1] != 'run':
        filename = sys.argv[i+1]
    elif sys.argv[i] == '-f' and sys.argv[i+1] == 'run':
        print('"Run" is not a valid file name to export.')
        quit()

if sys.argv[-1] == 'run':
    print('===== Simulation Running =====')
    current_run = Simulation(population, T, population, partner_nwk, alpha, beta, gamma, phi, filename)
    current_run()
    print('=====  Simulation Ended  =====')
    print('\nSee you!')
    quit()

'''
Normal mode
'''

while True:
    cmd = input('>>> ').lower()
    if cmd == 'setting':
        N, T, alpha, beta, gamma, phi = setting(N, T, alpha, beta, gamma, phi)
        population = Person.make_population(N)
    elif cmd == 'summary':
        summary()
    elif cmd == 'look':
        show_nwk()
    elif cmd == 'help':
        help()
    elif cmd == 'start' or cmd == 'run':
        print('===== Simulation Running =====')
        current_run = Simulation(population, T, population, partner_nwk, alpha, beta, gamma, phi, filename)
        current_run()
        print('=====  Simulation Ended  =====')
    elif cmd == 'mode':
        set_mode()
    elif cmd == 'export':
        filename = input('File name: ')
    elif cmd == 'thank you':
        print('==== Thank you ====')
    elif cmd == 'quit' or cmd == 'q':
        print('See you!')
        quit()
    else:
        print('Invalid input. Please check your command again.')
    print('')
