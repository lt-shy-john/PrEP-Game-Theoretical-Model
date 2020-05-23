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
def setting(N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2):
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
    cmd = input('Other parameters? [y/n]')
    if cmd == 'y':
        setting_other(N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T)
    population = Person.make_population(N)
    return N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T

def setting_other(N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T):
    print('Adoption parameters \n')
    alpha_V_temp = input('PrEP: ')
    alpha_V = set_correct_epi_para(alpha_V_temp, alpha_V)
    alpha_T_temp = input('Treatment: ')
    alpha_T = set_correct_epi_para(alpha_T_temp, alpha_T)
    print('Transmission parameters \n')
    beta_SS_temp = input('SS: ')
    beta_SS = set_correct_epi_para(beta_SS_temp, beta_SS)
    beta_II_temp = input('II: ')
    beta_II = set_correct_epi_para(beta_II_temp, beta_II)
    beta_RR_temp = input('RR: ')
    beta_RR = set_correct_epi_para(beta_RR_temp, beta_RR)
    beta_VV_temp = input('VV: ')
    beta_VV = set_correct_epi_para(beta_VV_temp, beta_VV)
    beta_IR_temp = input('IR: ')
    beta_IR = set_correct_epi_para(beta_IR_temp, beta_IR)
    beta_SR_temp = input('SR: ')
    beta_SR = set_correct_epi_para(beta_IR_temp, beta_SR)
    beta_SV_temp = input('SV: ')
    beta_SV = set_correct_epi_para(beta_IR_temp, beta_SV)
    beta_PI_temp = input('PI: ')
    beta_PI = set_correct_epi_para(beta_PI_temp, beta_PI)
    beta_IV_temp = input('IR: ')
    beta_IV = set_correct_epi_para(beta_IV_temp, beta_IV)
    beta_SI2_temp = input('beta_SI2: ')
    beta_SI2 = set_correct_epi_para(beta_SI2_temp, beta_SI2)
    beta_II2_temp = input('beta_II2: ')
    beta_II2 = set_correct_epi_para(beta_II2_temp, bebeta_II2ta_PI)
    beta_RI2_temp = input('beta_RI2: ')
    beta_RI2 = set_correct_epi_para(beta_RI2_temp, beta_RI2)
    beta_VI2_temp = input('beta_VI2: ')
    beta_VI2 = set_correct_epi_para(beta_VI2_temp, beta_VI2)
    print('Wear-off parameters \n')
    phi_V_temp = input('PrEP: ')
    phi_V = set_correct_epi_para(phi_V_temp, phi_V)
    phi_T_temp = input('Treatment: ')
    phi_T = set_correct_epi_para(phi_T_temp, phi_T)
    return N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T

def summary():
    print('N: {}'.format(N))
    print('T: {}'.format(T))
    print('===== SIR Rate =====')
    print('alpha: {}'.format(alpha))
    print('beta: {}'.format(beta))
    print('gamma: {}'.format(gamma))
    print('phi: {}'.format(phi))
    cmd = input('Show other epidemic paremeters? [y/n] ')
    if cmd == 'y':
        print('alpha_V = {}'.format(alpha_V))
        print('alpha_T = {}'.format(alpha_T))
        print('beta_SS = {}'.format(beta_SS))
        print('beta_II = {}'.format(beta_II))
        print('beta_RR = {}'.format(beta_RR))
        print('beta_VV = {}'.format(beta_VV))
        print('beta_IR = {}'.format(beta_IR))
        print('beta_SR = {}'.format(beta_SR))
        print('beta_SV = {}'.format(beta_SV))
        print('beta_PI = {}'.format(beta_PI))
        print('beta_IV = {}'.format(beta_IV))
        print('beta_RV = {}'.format(beta_IV))
        print('beta_condom = {}'.format(beta_condom))
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
    print('SETTING - Set simulation settings.')
    print('OTHER SETTING - Set auxillary simulation parameters.')
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

def set_mode(mode):
    cmd = ''
    while cmd != 'y':
        print('Select the following options:')
        print('01: Living in city/ suburb/ rural [{}]'.format(mode01.flag))
        print('02: Visit GP/ Sex clinic [{}]'.format(mode02.flag))
        print('03: Age groups (elder/ young) []')
        print('04: Casual sex []')
        print('05: Edit partner network')
        print('06: Risk compensation (%) [{}]'.format(mode06.flag))
        print('07: Include sex workers []')
        print('10: Add cost of PrEP []')
        print('21: Partner negotiates for sex [{}]'.format(mode21.flag))
        print('22: Stubbon to take PrEP []')
        print('23: Stubbon to against PrEP []')
        print('24: Contrary to social groups []')
        print('31: Include on demand PrEP. [{}]'.format(mode31.flag))
        print('32: Population on demand PrEP had planned sex. []')
        print('41: Moral hazard of PrEP []')
        print('42: Moral hazard of treatment []')
        print('Input number codes to change the options.')
        mode_input = input('> ')
        mode = mode_settings(mode_input, mode)
        cmd = input('Return to main menu? [y/n] ')
    return mode

def mode_settings(cmd, mode=None):
    cmd = cmd.split(' ')
    print(cmd)
    if len(cmd) > 0:
        for i in range(len(cmd)):
            try:
                int(cmd[i])
            except ValueError:
                print('Wrong data type for mode, please check your inputs.')
                continue
            if int(cmd[i]) == 1:
                mode01()
                if mode01.flag == 'X':
                    mode[1] = mode01
                else:
                    mode.pop(1)
            elif int(cmd[i]) == 2:
                mode02.set_proportion()
                mode02()
                if mode02.flag == 'X':
                    mode[2] = mode02
                else:
                    mode.pop(2)
            elif int(cmd[i]) == 4:
                mode04()
                if mode04.flag == 'X':
                    mode[4] = mode04
                else:
                    mode.pop(4)
            elif int(cmd[i]) == 5:
                mode05()
                if mode05.flag == 'X':
                    mode[5] = mode05
                else:
                    mode.pop(5)
            elif int(cmd[i]) == 6:
                mode06()
                if mode06.flag == 'X':
                    mode[6] = mode06
                else:
                    mode.pop(6)
            elif int(cmd[i]) == 21:
                mode21()
                if mode21.flag == 'X':
                    mode[21] = mode21
                else:
                    mode.pop(21)
            elif int(cmd[i]) == 31:
                mode31()
                if mode31.flag == 'X':
                    mode[31] = mode31
                else:
                    mode.pop(31)
    return mode

def mode_settings_express(cmd):
    return mode

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
alpha_V = alpha
alpha_T = alpha
beta_SS = 0.0
beta_II = 0.0
beta_RR = 0.01
beta_VV = 0.0
beta_IR = 0.01
beta_SR = 0.01
beta_SV = 0.01
beta_PI = 0.01
beta_IV = 0.01
beta_RV = 0.01
beta_condom = 0.000001
beta_SI2 = beta
beta_II2 = 0.0
beta_RI2 = beta_IR
beta_VI2 = beta_IV
phi_V = phi
phi_T = 0.95

population = Person.make_population(N)
partner_nwk = Partner(population)
filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.
mode01 = mode.Mode01(population, partner_nwk)
mode02 = mode.Mode02(population)
mode05 = mode.Mode05(population, partner_nwk)
mode06 = mode.Mode06(population, partner_nwk)
mode21 = mode.Mode21(population, partner_nwk)
mode31 = mode.Mode31(population)
modes = {}

'''
Express mode

Loads the settings prior to the run. Optional keyword 'run' to run the simulation automatically.
'''
# Check if mode exists
for i in range(len(sys.argv)):
    try:
        if sys.argv[-1] == '-m':
            raise ValueError
    except ValueError:
        print('No mode codes provided. Please check your inputs.')
        quit()

    if sys.argv[i] == '-m' and sys.argv[i+1] != 'run':
        modes = mode_settings_express(mode_cmd)
    elif sys.argv[i] == '-m' and sys.argv[i+1] != 'run':
        print('"Run" is not a valid mode code.')
        quit()

# Check file name to export
for i in range(len(sys.argv)):
    try:
        if sys.argv[-1] == '-f':
            raise ValueError
    except ValueError:
        print('No file name provided. Please check your inputs.')
        quit()

    if sys.argv[i] == '-f' and sys.argv[i+1] != 'run':
        filename = sys.argv[i+1]
    elif sys.argv[i] == '-f' and sys.argv[i+1] == 'run':
        print('"Run" is not a valid file name for export.')
        quit()

if sys.argv[-1] == 'run':
    print('===== Simulation Running =====')
    current_run = Simulation(population, T, population, partner_nwk, alpha, beta, gamma, phi, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2)
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
        N, T, alpha, beta, gamma, phi, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T = setting(N, T, alpha, beta, gamma, phi)
        population = Person.make_population(N)
    elif cmd == 'other setting':
        print('Leave blank if not changing the value(s).')
        N, T, alpha, beta, gamma, phi, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, phi_V, phi_T = setting_other()
    elif cmd == 'summary':
        summary()
    elif cmd == 'look':
        show_nwk()
    elif cmd == 'help':
        help()
    elif cmd == 'start' or cmd == 'run':
        print('===== Simulation Running =====')
        current_run = Simulation(population, T, population, partner_nwk, alpha, beta, gamma, phi, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2)
        # Load modes
        current_run.load_modes(modes)
        if len(modes) > 0:
            print('\nMode objects loaded.\n')
        # Run
        current_run()
        print('=====  Simulation Ended  =====')
    elif cmd == 'mode':
        modes = set_mode(modes)
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
