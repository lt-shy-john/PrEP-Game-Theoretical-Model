from person import Person
from epidemic import Epidemic
from partner import Partner
import write

import random

class Simulation:
    def __init__(self, N, T, people, partner_nwk, alpha, beta, gamma, phi, filename, alpha_V, alpha_T, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2, groups_of=3):
        self.N = N
        self.groups_of = groups_of
        self.people = people   # List of people objects
        self.partner_nwk = partner_nwk
        self.groups = None
        self.T = T
        self.alpha = alpha
        self.alpha_V = alpha_V
        self.alpha_T = alpha_T
        self.beta = beta
        self.beta_SS = beta_SS
        self.beta_II = beta_II
        self.beta_RR = beta_RR
        self.beta_VV = beta_VV
        self.beta_IR = beta_IR
        self.beta_SR = beta_SR
        self.beta_SV = beta_SV
        self.beta_PI = beta_PI
        self.beta_IV = beta_IV
        self.beta_RV = beta_RV
        self.beta_SI2 = beta_SI2
        self.beta_II2 = beta_II2
        self.beta_RI2 = beta_RI2
        self.beta_VI2 = beta_VI2
        self.beta_condom = beta_condom
        self.gamma = gamma
        self.phi = phi
        self.filename = filename

        self.modes = {}

    def load_modes(self,modes):
        '''Load mode objects into epidemic class, as defined in the main code.

        parameters
        ----------

        modes - dict:
            Keys are integer mode code with the corresponding mode objects
        '''
        self.modes = modes

    def __call__(self, modes=None):
        FILENAME_STATES = ''
        epidemic = Epidemic(self.alpha, self.beta, self.gamma, self.phi, self.people, self.partner_nwk)
        epidemic.set_other_alpha_param(self.alpha_V, self.alpha_T)
        epidemic.set_other_beta_param(self.beta_SS, self.beta_II, self.beta_RR, self.beta_VV, self.beta_IR, self.beta_SR, self.beta_SV, self.beta_PI, self.beta_IV, self.beta_RV, self.beta_condom, self.beta_SI2, self.beta_II2, self.beta_RI2, self.beta_VI2)
        epidemic.load_modes(self.modes)
        print('beta = {}, alpha = {}, gamma = {}, phi = {}'.format(epidemic.infection, epidemic.vaccinated, epidemic.recover, epidemic.resus))
        epidemic.set_epidemic(1)
        print('=========== t = 0 ============\n')
        print('N = {}'.format(len(self.people)))
        print('S = {}, I = {}, V = {}, R = {}'.format(epidemic.S, epidemic.I, epidemic.V, epidemic.R))
        for t in range(self.T):
            print('=========== t = {} ============\n'.format(t+1))
            print('N = {}'.format(len(self.people)))
            print('S = {}, I = {}, V = {}, R = {}'.format(epidemic.S, epidemic.I, epidemic.V, epidemic.R))
            epidemic.next(self.filename)

        print('\n=========== Result ============\n')
        print('There are {} people infected.'.format(epidemic.I))
        print('There are {} people vaccinated.'.format(epidemic.V))
        print()
        if self.filename != '':
            print('Data stored in \'{}.csv\''.format(self.filename))
        print('Relationship topology is ready for view.\n')
        print('')

        # Return any data
        return self.partner_nwk
