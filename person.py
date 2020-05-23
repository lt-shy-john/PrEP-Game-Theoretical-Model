'''
Model Opinion Dynamics and separate them into groups of 3
'''

import random

class Person:
    id = 0 # Initial population

    def __init__(self, personality = 0):
        Person.id += 1  # Name of the person.
        self.id = Person.id
        self.opinion = 1 #random.choices([0, 1], weights = [2, 8], k = 1)[0]
        self.meta_opinion = None

        self.location = 0
        '''
        0 - City
        1 - Suburb
        2 - Rural
        '''

        self.occupation = 0
        '''
        0 - Not specified
        1 - Sex worker
        '''

        self.wealth = 1000
        self.d_GP = 0
        self.d_sc = None

        self.group_no = None
        '''
        Personality:
        0 - Normal
        1 - Inflexible
        2 - Balancer
        '''
        self.personality = personality

        self.suceptible = 0 #int(round(random.uniform(0, 1), 0))   # 0 means without disease, 1 means infected
        self.reinfected = 0
        self.vaccinated = 0   # Assume all 0 (None of them took vaccine).
        self.recovered = 0  # 0 means not in R compartment, 1 is.

        self.last_sex = 0  # Last time the person has sex.
        self.sex_history = []
        self.is_casual = False
        self.infection_clock = 0

        self.treatment = 0
        self.treatment_warning = None  # When 3, goes back to I2.

        self.condom_group = None  # Check mode 06 for information.
        self.risk_compensation = 1
        self.condom_history = []

        self.on_demand = None  # See Mode31 class for more information.
        self.mated_marker = None

    def make_population(N):
        population = []
        for i in range(N):
            population.append(Person())
        return population

    def swap_opinion(self):
        if self.opinion == 0:
            self.opinion = 1
        else:
            self.opinion = 0
