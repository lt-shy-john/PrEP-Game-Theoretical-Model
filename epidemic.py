import random

from partner import Partner
import person
import write

class Epidemic:

    def __init__ (self, vaccinated, infection, recover, resus, people, partner_nwk):
        '''Initial elements

        Attributes
        ----------

        epidemic - int
            Flag epidemic starts or ends.

        people - People
            Agents for simulation
        '''
        self.epidemic = 0   # Whether an epidemic occured or not.
        self.people = people
        self.mode = {}  # Dict of modes loaded. Values are mode objects

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

            # Customised lifestyle rate. Call set_other_alpha_param() to set values.
            self.alpha_V = self.vaccinated
            self.alpha_T = self.vaccinated

            # Customised infection rate
            self.infection_SS = 0.0
            self.infection_II = 0.0
            self.infection_II2 = 0.0
            self.infection_RR = 0.01
            self.infection_VV = 0.0
            self.infection_IR = 0.01
            self.infection_SR = 0.01
            self.infection_SV = 0.01
            self.infection_PI = 0.01
            self.infection_IV = 0.01
            self.infection_RV = 0.01
            self.infection_SI2 = self.infection
            self.infection_RI2 = 0.01
            self.infection_VI2 = 0.01
            self.infection_condom = 0.01
            self.check_beta()

            self.sex_rate = 1/len(self.people)  # How often do one person has urge to make love with partner(s).


            '''Compartment statics

            Number of agents within a compartment.

            Attributes
            ----------
            S: int
                Number of people not infected (susceptible).
            I1: int
                Number of people in the acute phase of HIV.
            I2: int
                Number of people in the chronic phase of HIV.
            I: int
                Sum of people in I1 and I2. Number of infected agents (excl. recovered).
            V: int
                Number of people taken PrEP
            R: int
                Number of people under taking treatment and not showing symptoms.
            Pro: int
                Number of agents willing to accept PrEP
            Ag: int
                Number of agents against of taking PrEP
            dS: int
                Difference of suceptible compartment at different times
            dI: int
                Difference of infected compartment at different times
            dV: int
                Difference of vaccinated (PrEP) compartment at different times
            '''
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

            '''Partner topology

            Attributes
            ----------

            partner_nwk: nx.graph
                Graph object showing sexual relationships of all agents.

            '''
            self.partner_nwk = partner_nwk

        except ValueError:
            print('Check your parameters if they are probabilities.')

    def set_other_alpha_param(self, alpha_V, alpha_T):
        self.alpha_V = alpha_V
        self.alpha_T = alpha_T

    def set_other_beta_param(self, beta_SS, beta_II, beta_RR, beta_VV, beta_IR, beta_SR, beta_SV, beta_PI, beta_IV, beta_RV, beta_condom, beta_SI2, beta_II2, beta_RI2, beta_VI2):
        self.infection_SS = beta_SS
        self.infection_II = beta_II
        self.infection_RR = beta_RR
        self.infection_VV = beta_VV
        self.infection_IR = beta_IR
        self.infection_SR = beta_SR
        self.infection_SV = beta_SV
        self.infection_PI = beta_PI
        self.infection_IV = beta_IV
        self.infection_RV = beta_RV
        self.infection_condom = beta_condom
        self.infection_SI2 = beta_SI2
        self.infection_II2 = beta_II2
        self.infection_RI2 = beta_RI2
        self.infection_VI2 = beta_VI2

        self.check_beta()

    def check_beta(self):
        beta_ls = [self.infection_SS, self.infection_II, self.infection_RR, self.infection_VV, self.infection_IR, self.infection_SR, self.infection_SV, self.infection_PI, self.infection_IV, self.infection_RV, self.infection_condom, self.infection_SI2, self.infection_II2, self.infection_RI2, self.infection_VI2]
        for beta_param in beta_ls:
            if beta_param > self.infection:
                beta_param = self.infection


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

    def load_modes(self, modes):
        self.mode.update(modes)

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

        # Resume temp variables
        ag = 0
        pro = 0

    def vaccinate(self):
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1:
                continue
            if self.people[i].opinion == 1 and random.uniform(0,1) <= self.alpha_V:
                self.people[i].vaccinated = 1

    def recovery(self):
        '''
        A person is recovered if they take medication. Still infected but no symptoms observed.
        '''
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                continue
            if self.people[i].infection_clock >= 30*6 and self.people[i].suceptible == 1 and random.uniform(0,1) <= self.recover:
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
            # Infect through sex network
            if isinstance(self.partner_nwk.network[i][0], person.Person) == False or isinstance(self.partner_nwk.network[i][1], person.Person) == False:
                continue

            agree = self.mate(self.partner_nwk.network[i])
            if agree == None:
                self.partner_nwk.network[i][0].sex_history.append(0)
                self.partner_nwk.network[i][1].sex_history.append(0)
                return None

            # Sex made, record
            self.partner_nwk.network[i][0].sex_history.append(1)
            self.partner_nwk.network[i][1].sex_history.append(1)

            if 6 in self.mode:
                self.mode[6].infect_condom_use(self.infection_condom, self.sex_rate)

            '''Infect (or not)
            '''
            # SS
            if self.partner_nwk.network[i][0].suceptible == 0 and self.partner_nwk.network[i][0].vaccinated == 0 and self.partner_nwk.network[i][1].suceptible == 0 and  self.partner_nwk.network[i][1].vaccinated == 0 and random.uniform(0,1) <= self.infection_SS:
                # print('SS: Beep*')
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].suceptible == 0 and self.partner_nwk.network[i][1].vaccinated == 0 and self.partner_nwk.network[i][0].suceptible == 0 and  self.partner_nwk.network[i][0].vaccinated == 0 and random.uniform(0,1) <= self.infection_SS:
                # print('SS: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1

            # SI
            if self.partner_nwk.network[i][1].suceptible == 1 and self.partner_nwk.network[i][0].suceptible == 0 and  self.partner_nwk.network[i][0].vaccinated == 0 and random.uniform(0,1) <= self.infection:
                # print('SI: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1

            # SR
            if self.partner_nwk.network[i][0].recovered == 1 and self.partner_nwk.network[i][1].suceptible == 0 and random.uniform(0,1) <= self.infection_SR:
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].recovered == 1 and self.partner_nwk.network[i][0].suceptible == 0 and random.uniform(0,1) <= self.infection_SR:
                # print('SR: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1

            # SV


            # II
            if self.partner_nwk.network[i][1].suceptible == 1 and self.partner_nwk.network[i][0].suceptible == 1 and random.uniform(0,1) <= self.infection_II:
                # print('II: Beep**')
                self.partner_nwk.network[i][0].suceptible = 1
                self.partner_nwk.network[i][1].suceptible = 1

            # IR
            if self.partner_nwk.network[i][1].suceptible == 1 and self.partner_nwk.network[i][0].recovered == 1 and random.uniform(0,1) <= self.infection_IR:
                # print('IR: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1
            elif self.partner_nwk.network[i][0].suceptible == 1 and self.partner_nwk.network[i][1].recovered == 1 and random.uniform(0,1) <= self.infection_IR:
                # print('IR: Beep**')
                self.partner_nwk.network[i][1].suceptible = 1

            # IV
            if self.partner_nwk.network[i][1].suceptible == 1 and self.partner_nwk.network[i][0].vaccinated == 1 and random.uniform(0,1) <= self.infection_IV:
                # print('IV: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1
            elif self.partner_nwk.network[i][0].suceptible == 1 and self.partner_nwk.network[i][1].vaccinated == 1 and random.uniform(0,1) <= self.infection_IV:
                # print('IV: Beep**')
                self.partner_nwk.network[i][1].suceptible = 1

            # RR
            if self.partner_nwk.network[i][1].recovered == 1 and self.partner_nwk.network[i][0].recovered == 1 and random.uniform(0,1) <= self.infection_RR:
                # print('RR: Beep*')
                self.partner_nwk.network[i][0].suceptible = 1
                self.partner_nwk.network[i][1].suceptible = 1

            # RV
            if self.partner_nwk.network[i][1].recovered == 1 and self.partner_nwk.network[i][0].vaccinated == 1 and random.uniform(0,1) <= self.infection_RV:
                # print('RV: Beep**')
                self.partner_nwk.network[i][0].suceptible = 1
            elif self.partner_nwk.network[i][0].recovered == 1 and self.partner_nwk.network[i][1].vaccinated == 1 and random.uniform(0,1) <= self.infection_RV:
                # print('RV: Beep*')
                self.partner_nwk.network[i][1].suceptible = 1

            # VV
            if self.partner_nwk.network[i][1].vaccinated == 1 and self.partner_nwk.network[i][0].vaccinated == 1 and random.uniform(0,1) <= self.infection_VV:
                self.partner_nwk.network[i][0].suceptible = 1
                self.partner_nwk.network[i][1].suceptible = 1

            # SI2
            if self.partner_nwk.network[i][0].reinfected == 1 and self.partner_nwk.network[i][1].suceptible == 0 and random.uniform(0,1) <= self.infection_SI2:
                # print('SI: Beep** Beep')
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].reinfected == 1 and self.partner_nwk.network[i][0].suceptible == 0 and random.uniform(0,1) <= self.infection_SI2:
                # print('SI: Beep* Beep**')
                self.partner_nwk.network[i][0].suceptible = 1
            # II2

            # RI2
            if self.partner_nwk.network[i][0].reinfected == 1 and self.partner_nwk.network[i][1].recovered == 1 and random.uniform(0,1) <= self.infection_RI2:
                # print('!!!')
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].reinfected == 1 and self.partner_nwk.network[i][0].recovered == 1 and random.uniform(0,1) <= self.infection_RI2:
                # print('!!!')
                self.partner_nwk.network[i][0].suceptible = 1

            # VI2
            if self.partner_nwk.network[i][0].reinfected == 1 and self.partner_nwk.network[i][1].vaccinated == 1 and random.uniform(0,1) <= self.infection_VI2:
                # print('?!?')
                self.partner_nwk.network[i][1].suceptible = 1
            elif self.partner_nwk.network[i][1].reinfected == 1 and self.partner_nwk.network[i][0].vaccinated == 1 and random.uniform(0,1) <= self.infection_VI2:
                # print('!?!')
                self.partner_nwk.network[i][0].suceptible = 1

    def casual_sex(self):
        if 4 in self.mode:
            person00, person01 = self.mode[4].casual_sex(self.people)

            '''Make sex with the person
            '''
            # SS
            if person00.suceptible == 0 and person00.vaccinated == 0 and person01.suceptible == 0 and  person01.vaccinated == 0 and random.uniform(0,1) <= self.infection_SS:
                # print('SS: Beep*')
                person01.suceptible = 1
            elif person01.suceptible == 0 and person01.vaccinated == 0 and person00.suceptible == 0 and  person00.vaccinated == 0 and random.uniform(0,1) <= self.infection_SS:
                # print('SS: Beep*')
                person00.suceptible = 1

            # SI
            if self.partner_nwk.network[i][1].suceptible == 1 and person00.suceptible == 0 and  person00.vaccinated == 0 and random.uniform(0,1) <= self.infection:
                # print('SI: Beep*')
                person00.suceptible = 1

            # SR
            if person00.recovered == 1 and person01suceptible == 0 and random.uniform(0,1) <= self.infection_SR:
                person01.suceptible = 1
            elif person01.recovered == 1 and person00.suceptible == 0 and random.uniform(0,1) <= self.infection_SR:
                # print('SR: Beep*')
                person00.suceptible = 1

            # SV


            # II
            if person01.suceptible == 1 and person00.suceptible == 1 and random.uniform(0,1) <= self.infection_II:
                # print('II: Beep**')
                person00.suceptible = 1
                person01.suceptible = 1

            # IR
            if person01.suceptible == 1 and person00.recovered == 1 and random.uniform(0,1) <= self.infection_IR:
                # print('IR: Beep*')
                person00.suceptible = 1
            elif person00.suceptible == 1 and person01.recovered == 1 and random.uniform(0,1) <= self.infection_IR:
                # print('IR: Beep**')
                person01.suceptible = 1

            # IV
            if person01.suceptible == 1 and person00.vaccinated == 1 and random.uniform(0,1) <= self.infection_IV:
                # print('IV: Beep*')
                person00.suceptible = 1
            elif person00.suceptible == 1 and person01.vaccinated == 1 and random.uniform(0,1) <= self.infection_IV:
                # print('IV: Beep**')
                person01.suceptible = 1

            # RR
            if person01.recovered == 1 and person00.recovered == 1 and random.uniform(0,1) <= self.infection_RR:
                # print('RR: Beep*')
                person00.suceptible = 1
                person01.suceptible = 1

            # RV
            if person01.recovered == 1 and person00.vaccinated == 1 and random.uniform(0,1) <= self.infection_RV:
                # print('RV: Beep**')
                person00.suceptible = 1
            elif person00.recovered == 1 and person01.vaccinated == 1 and random.uniform(0,1) <= self.infection_RV:
                # print('RV: Beep*')
                person01.suceptible = 1

            # VV
            if person01.vaccinated == 1 and person00.vaccinated == 1 and random.uniform(0,1) <= self.infection_VV:
                person00.suceptible = 1
                person01.suceptible = 1

            # SI2
            if person00.reinfected == 1 and person01.suceptible == 0 and random.uniform(0,1) <= self.infection_SI2:
                # print('SI: Beep** Beep')
                person01.suceptible = 1
            elif person01.reinfected == 1 and person00.suceptible == 0 and random.uniform(0,1) <= self.infection_SI2:
                # print('SI: Beep* Beep**')
                person00.suceptible = 1
            # II2

            # RI2
            if person00.reinfected == 1 and person01.recovered == 1 and random.uniform(0,1) <= self.infection_RI2:
                # print('!!!')
                person01.suceptible = 1
            elif person01.reinfected == 1 and person00.recovered == 1 and random.uniform(0,1) <= self.infection_RI2:
                # print('!!!')
                person00.suceptible = 1

            # VI2
            if sperson00.reinfected == 1 and person01.vaccinated == 1 and random.uniform(0,1) <= self.infection_VI2:
                # print('?!?')
                person01.suceptible = 1
            elif person01.reinfected == 1 and person00.vaccinated == 1 and random.uniform(0,1) <= self.infection_VI2:
                # print('!?!')
                person00.suceptible = 1

    def infection_clock(self, i):
        if self.people[i].infection_clock >= 30*6 and self.people[i].suceptible == 1 and random.uniform(0,1) <= self.resus:
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
        self.casual_sex()
        self.vaccinate()
        self.infected()
        self.reinfect()
        self.get_states()
        if filename != '':
            write.WriteStates(self, filename)
            write.WriteSex(self, filename)
            if 6 in self.mode:
                write.WriteCondom(self, filename)
