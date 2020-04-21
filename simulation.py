from person import Person
from epidemic import Epidemic
from partner import Partner
import write

import random

class Simulation:
    def __init__(self, N, T, people, partner_nwk, alpha, beta, gamma, phi, filename, groups_of=3):
        self.N = N
        self.groups_of = groups_of
        self.people = people   # List of people objects
        self.partner_nwk = partner_nwk
        self.groups = None
        self.T = T
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.phi = phi
        self.filename = filename

    def __call__(self):
        FILENAME_STATES = ''
        epidemic = Epidemic(self.alpha, self.beta, self.gamma, self.phi, self.people, self.partner_nwk)
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
        return self.partner_nwk
