import random

from partner import Partner
import person
import write

class Epidemic:

    def __init__ (self, vaccinated, infection, recover, resus, people, partner_nwk):
        self.epidemic = 0   # Whether an epidemic occured or not.
        self.people = people
        try:
            if vaccinated >= 0 and vaccinated <= 1:
                self.vaccinated = vaccinated   # Probability to get vaccinated
            else:
                raise ValueError
            if infection >= 0 and infection <= 1:
                self.infection = infection
            else:
                raise ValueError
            if recover >= 0 and recover <= 1:
                self.recover = recover  # Recovery rate
            else:
                raise ValueError
            if resus >= 0 and resus <= 1:
                self.resus = resus
            else:
                raise ValueError

            # Customised infection rate
            self.infection_IR = 0.01
            self.infection_SR = 0.01
            self.infection_PI = 0.01
            self.infection_condom = 0.01

            self.urge_call_rate = 1/len(self.people)  # How often do one person has urge to make love with partner(s).

            self.S = len(self.people)
            self.I1 = 0
            self.I2 = 0
            self.I = self.I1 + self.I2
            self.V = 0
            self.R = 0
            self.Pro = 0
            self.Ag = 0
            self.dS = -self.vaccinated*self.S*self.Pro - (1-self.vaccinated)*self.infection*self.S*self.I*self.Pro - self.infection*self.S*self.I*self.Ag + self.recover*self.I + self.resus*self.V
            self.dI = (1-self.vaccinated)*self.infection*self.S*self.I*self.Pro + self.infection*self.S*self.I*self.Ag - self.recover*self.I
            self.dV = self.vaccinated*self.S*self.Pro - self.resus*self.V

            # Partner topology
            self.partner_nwk = partner_nwk

        except ValueError:
            print('Check your parameters if they are probabilities.')

    def get_states(self):
        '''
            Get number of people who are in S, I or V state.
        '''
        self.S = 0
        self.I = 0
        self.I1 = 0
        self.I2 = 0
        self.V = 0
        self.R = 0
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                self.V += 1
                continue
            elif self.people[i].suceptible == 1 and self.people[i].recovered == 0:
                self.I1 += 1
                continue
            elif self.people[i].reinfected == 1 and self.people[i].recovered == 0:
                self.I2 += 1
                continue
            elif self.people[i].recovered == 1:
                self.R += 1
                continue
            self.S += 1
        self.I = self.I1 + self.I2
        return self.S, self.I, self.I1, self.I2, self.V, self.R

    def set_epidemic(self, mode):
        '''
        Set either the environment to be disease-free or not.
        '''
        try:
            if mode > 1 or mode < 0:
                raise ValueError
        except ValueError:
            print('Mode must be either 1 or 0')
            pass
        if mode == 1:
            self.epidemic = 1
            Epidemic.start_epidemic(self)
        else:
            self.epidemic = 0
            Epidemic.kill_epidemic(self)

    def start_epidemic(self):
        '''
        Start an epidemic
        '''
        # Pick one person as infected
        # first_infected = random.randint(0,len(self.people)-1)
        # self.people[first_infected].suceptible = 1

        # Pick R_0 of people infected initially
        proportion = (self.infection/self.recover)/len(self.people)
        # print('R_0(%) = ', proportion)
        for i in range(len(self.people)):
            if random.uniform(0,1) <= proportion:
                self.people[i].suceptible = 1

    def kill_epidemic(self):
        for i in range(len(self.people)):
            self.people[i].suceptible = 0

    def set_pro_ag(self):
        '''
        Return the proportion of people who pro or against vaccination.
        '''
        pro = 0
        ag = 0
        for i in range(len(self.people)):
            if self.people[i].opinion == 1:
                pro += 1
            else:
                ag += 1
        self.Pro = pro/(len(self.people))
        self.Ag = ag/(len(self.people))
        ag = 0   # Resume temp variables
        pro = 0  # Resume temp variables

    def vaccinate(self):
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1:
                continue
            if self.people[i].opinion == 1 and random.uniform(0,1) <= self.vaccinated:
                self.people[i].vaccinated = 1

    def recovery(self):
        '''
        A person is recovered if they take medication. Still infected but no symptoms observed.
        '''
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                continue
            if self.people[i].suceptible == 1 and random.uniform(0,1) <= self.recover:
                self.people[i].recovered = 1

    def natural_transmission(self):
        if self.epidemic == 0:
            # If eradicated, then there are no external transmissions.
            return
        for i in range(len(self.people)):
            seed = random.randint(0,100)/100
            if seed < 1/(len(self.people))*self.infection:
                self.people[i].suceptible = 1

    def mate(self, pair):
        # Note: We are not assuming pair has 2 elements only. Will change var name to comp(onent).
        r = 0.5
        rI = 0.8
        if len(pair) > 1:
            i = random.randint(0,len(pair)-1)  # Who is making the request
            mu = 2
        else:
            return None
        for j in range(len(pair)):
            if i == j:
                continue # Skip the person is deciding
            # [Distrust, Abuse, Honour trust]
            m = 1
            Ej = [1,1,1]
            Mj = [-rI,self.infection*rI,(1-self.infection)*r]
            Kj = [m*(1-self.infection)*r,m*self.infection*rI,m*(1-self.infection)*r]
            max_utility = 0
            option = None
            for k in range(3):
                if Ej[k]+Mj[k]+Kj[k] > max_utility:
                    max_utility = Ej[k]+Mj[k]+Kj[k]
                    option = k
            if option == 0:
                return None
            # print(pair[j].id, max_utility, option)
            if option == 2 and (pair[i].suceptible == 1 and pair[i].recovered == 0) or (pair[i].reinfected == 1 and pair[i].recovered == 0):
                option = 1
            if option == 1 or option == 2:
                return option

    def infect(self):
        for i in range(len(self.partner_nwk.network)):
            if isinstance(self.partner_nwk.network[i][0], person.Person) == False or isinstance(self.partner_nwk.network[i][1], person.Person) == False:
                continue

            agree = self.mate(self.partner_nwk.network[i])
            if agree == None:
                return None

            # Infect (or not)
            if self.partner_nwk.network[i][0].suceptible == 1 and random.uniform(0,1) <= self.infection and self.partner_nwk.network[i][1].vaccinated == 0:
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].suceptible == 1 and random.uniform(0,1) <= self.infection and self.partner_nwk.network[i][0].vaccinated == 0:
                self.partner_nwk.network[i][0].suceptible = 1

    def infection_clock(self, i):
        if self.people[i].infection_clock == 30*6 and self.people[i].suceptible == 1:
            # Move to I2
            self.people[i].reinfected = 1
            self.people[i].recovered = 0
            self.people[i].infection_clock = 0
            return

        if self.people[i].infection_clock == 365*10 and self.people[i].reinfected == 1 and self.people[i].recovered == 0:
            # Back to I1 compartment
            self.people[i].reinfected = 0
            self.people[i].suceptible = 1
            self.people[i].recovered = 0
            self.people[i].infection_clock = 0

    def infected(self):
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1 or (self.people[i].reinfected == 1 and self.people[i].recovered == 0):
                self.people[i].infection_clock += 1
            else:
                self.people[i].infection_clock = 0

            self.infection_clock(i)


    def reinfect(self):
        '''
        Wear off of treatment.
        '''
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1 and  random.uniform(0,1) <= self.resus:
                if self.people[i].treatment_warning == None:
                    self.people[i].treatment_warning = 1
                else:
                    self.people[i].treatment_warning += 1
            elif self.people[i].suceptible == 1 and  random.uniform(0,1) > self.resus:
                self.people[i].treatment_warning = None

            # Check if eligible to be reinfected
            if self.people[i].treatment_warning == 3:
                self.people[i].recovered = 0
                self.people[i].reinfected = 1

    def wear_off(self):
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1 and random.uniform(0,1) <= self.resus:
                self.people[i].vaccinated = 0

    def __iter__(self):
        return self

    def next(self, filename):
        '''
        At each iteration, there will be:
        * Calculate S, I, V and proportion of pro and against vaccine.
        * Each person interacts with another.
        * Write the data files.

        Parameter:
        - filename: File name for csv output.
        '''

        self.get_states()
        self.set_pro_ag()
        self.natural_transmission()
        self.wear_off()
        self.recovery()
        self.infect()
        self.vaccinate()
        self.infected()
        self.reinfect()
        self.get_states()
        if filename != '':
            write.WriteStates(self, filename)
