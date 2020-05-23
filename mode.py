from person import Person
import random
import networkx as nx

class Mode:
    def __init__(self, people):
        # Flag to alert setting has been loaded.
        self.flag = ' '   # If loaded then has value 'X'.
        # Population objects
        self.people = people

    def raise_flag(self):
        '''
        If loaded then has value 'X'.
        '''
        self.flag = 'X'

    def drop_flag(self):
        '''
        If settings unloaded then delete the settings and mute the flagged icon.
        '''
        self.flag = ' '

'''
01: Living in city/ suburb/ rural
'''
class Mode01(Mode):
    '''
    Attributes
    ----------

    '''

    def __init__(self, people, partner_nwk):
        super().__init__(people)
        # Initially set partner living in the same region.
        self.partner_nwk = partner_nwk
        # Frequency of interaction. (City, Suburb, Rural)
        self.interaction = [[0.6, 0.39, 0.01], [0.39, 0.51, 0.1], [0.01, 0.1, 0.89]]

    def assign_regions(self):
        weight = [4,5,1]
        for pair in self.partner_nwk.network:
            pair[0] = random.choices(list(range(3)), weights = weight, k=1)[0]
            pair[1] = random.choices(list(range(3)), weights = weight, k=1)[0]

    def __call__(self):
        self.assign_regions()
        self.raise_flag()

'''
02: Visit GP Sex clinic
'''
class Mode02(Mode):
    def __init__(self, people):
        super().__init__(people)
        self.f = 0
        # Proportion of agents seeing a GP or sex clinic
        self.gp = 0
        self.sc = 0

    def set_proportion(self):
        gp_temp = float(input('Proportion of people seeing a GP (Decimal): '))
        sc_temp = float(input('Proportion of people seeing a sex clinic (Decimal): '))
        print()
        if gp_temp + sc_temp > 1:
            print('Check your input values.')
        elif gp_temp == '' or sc_temp == '':
            print('No changes has been made.')
        else:
            # Main code cont.
            self.gp = gp_temp
            self.sc = sc_temp

    def __call__(self):
        if self.gp != 0 and self.sc != 0:
            self.raise_flag()
        else:
            self.drop_flag()

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()


'''
04: Casual sex
'''
class Mode04(Mode):
    def __init__(self, people, partner_nwk):
        super().__init__(people)
        self.partner_nwk = partner_nwk

    def casual_sex(self, person):
        '''Casual sex. Used in Epidemic class
        '''
        if type(person) != Person:
            print('Error: person is not the correct type. Please check code.')
            return

        for other_person in self.people:
            seed = random.randint(1000)/1000
            if seed < self.partner_nwk.network.degree(other_person):
                # print record
                return (person,other_person)

    def __call__(self):
        self.raise_flag()

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()


'''
05: Edit partner network
'''
class Mode05(Mode):
    def __init__(self, people, g):
        super().__init__(people)
        self.g = g   # Import from Partner object. Graph of social network
        self.data = None # User requests to change social network topology


    def view_network(self):
        '''
        Import graph from main.py and view them.
        '''
        try:
            self.g.show_nwk()
        except NameError:
            print('Topology will be generated after the first run.')
            pass

    def read_data(self):
        self.data = self.data.split()
        for i in range(len(self.data)):
            self.data[i] = self.data[i].split('-')
            print(self.data[i][0],self.data[i][1])
        tmp_container = []
        for i in range(len(self.data)):
            print(self.data[i])
            for j in range(len(self.people)):
                if self.people[j].id == int(self.data[i][0]) or self.people[j].id == int(self.data[i][1]):
                    tmp_container.append(self.people[j])
                    print(tmp_container)
                if len(tmp_container) == 2:
                    self.g.network.append(tuple(tmp_container))
                    self.g.nwk_graph.add_edges_from([tuple(tmp_container)])
                    tmp_container = []
                    print('Added')
                    break
        self.data = None

    def __call__(self):
        cmd = None
        while cmd != 'y':
            print('Please review the partner topology network.')
            self.view_network()

            print('Input the agents you wished to connect... ')
            print('Agents are linked by "-" and pairs separated by space.')
            self.data = input('> ')
            self.read_data()
            if self.data != '':
                self.raise_flag()

            cmd = input('Do you want to leave?')
            if cmd == 'y':
                return

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

'''
06: Risk compensation (%)
'''
class Mode06(Mode):
    '''
    Attributes
    ----------
    condom_rate: iterable of floats
        Frequency of condoms. Highest, median and lowest.
    '''

    def __init__(self, people, partner_nwk):
        super().__init__(people)
        self.partner_nwk = partner_nwk
        # Hard coded frequency of replacing condoms.
        self.condom_rate = [0.85, 0.5, 0.03]
        # Each agent has their own risk compensation (i.e. replacement of condoms)


    def set_condom_rate(self):
        for i in range(3):
            try:
                self.condom_rate[0] = float(input('High condom use rate:'))
                self.condom_rate[1] = float(input('Median condom use rate:'))
                self.condom_rate[2] = float(input('Low condom use rate:'))
            except ValueError:
                print('Wrong data type. Please check your data')
                continue

    def set_population(self,input = None):
        '''
        Set whom uses condom and their habits.

        parameter
        ---------
        input: iterable, optional
            Define population and their condom use.

        Notes
        -----
        0 represents infrequent use of condom, 1 means user group lies in the median and 2 has the highest frequency.

        '''
        for person in self.people:
            person.condom_group = random.randint(0,2)

    def infect_condom_use(self, beta, sex_rate):
        '''
        Sexual intercourse when condom involved. Overide the normal `Epidemic.infect()` function.

        Parameters
        ----------
        sex_rate: float
            From epidemic class. Represents population frequency of making sexual intercourse.
        '''


        for pair in self.partner_nwk.network:
            sex_seed = random.randint(0,1000)/1000
            if sex_seed > sex_rate:
                # Not making sex
                continue
            condom_seed = random.randint(0,1000)/1000
            seed = random.randint(0,1000)/1000
            condom_rate = max(self.condom_rate[pair[0].condom_group], self.condom_rate[pair[1].condom_group])
            if condom_seed > condom_rate and seed < beta:
                if pair[0].suceptible == 0 and pair[0].vaccinated == 0 and (pair[1].suceptible == 1 or pair[1].reinfected == 1 or pair[1].recovered == 1):
                    pair[0].suceptible = 1
                if pair[1].suceptible == 0 and pair[1].vaccinated == 0 and (pair[0].suceptible == 1 or pair[0].reinfected == 1 or pair[0].recovered == 1):
                    pair[1].suceptible = 1
                # Both party could be infected, so not `elif`.

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

    def __call__(self):
        try:
            self.set_population()
            # self.set_condom_rate()
        except ValueError:
            pass
        self.raise_flag()

'''
21: Partner negotiates for sex
'''
class Mode21(Mode):
    def __init__(self, people, partner_nwk):
        super().__init__(people)
        self.partner_nwk = partner_nwk
        self.r = 0.5
        self.rI = 0.8

        # Trust factor of population
        self.m = 1
        self.mu = 2

    def mate(self, pair):

        if len(pair) > 1:
            i = random.randint(0,len(pair)-1)  # Who is making the request
            self.mu = 2
        else:
            return None
        for j in range(len(pair)):
            if i == j:
                continue # Skip the person is deciding
            # [Distrust, Abuse, Honour trust]
            self.m = 1
            Ej = [1,1,1]
            Mj = [-self.rI,self.infection*self.rI,(1-self.infection)*self.r]
            Kj = [self.m * (1 - self.infection) * self.r, self.m * self.infection * self.rI, self.m * (1-self.infection) * self.r]
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

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

'''
31: Include on demand PrEP.
'''
class Mode31(Mode):
    def __init__(self, people):
        super().__init__(people)

        # Proportion of agents that takes on demand PrEP
        self.p = 0

    def raise_flag(self):
        return super().raise_flag()

    def drop_flag(self):
        return super().drop_flag()

    def init_on_demand_PrEP(self, person_id):
        '''
        Allow the specific agent start on demand PrEP.

        Parameter:
        self - Mode31 object.
        person_id - id of the person instance.
        '''
        self.people[person_id].on_demand = 1
        self.people[person_id].vaccinated = 0

    def mate(self, person_id, start=None):
        '''
        If the agent made sex in the time step, a mark is made to the agent to decide if the agent is suceptible if forgot to take on-demand PrEP with in 48 hours.

        Values of mated_marker:
        None - Does not have sex before/ Last sex more than 2 days ago.
        1 - Had sex 1 day ago.
        2 - Had sex 2 days ago.

        Values of Person.on_demand:
        0 - Not on on-demand PrEP
        1 - Taking on-demand PrEP
        '''
        marker = self.people[person_id].mated_marker  # Make code neater
        if start != None and marker == None:
            marker = 0
            self.people[person_id].on_demand = 1
        elif marker == 0:
            marker += 1  # become 1
        elif marker == 1:
            marker += 1  # become 2
        elif marker == 2:
            marker = None
        # At the end reassign the values back to the attributes
        self.people[person_id].mated_marker = marker

    def forget_medication(self,person_id):
        '''
        Allow the specific agent start on demand PrEP.

        Parameter:
        self - Instance of mode 31.
        person_id - id of the person instance.
        '''
        self.people[person_id].on_demand = 0
        self.people[person_id].vaccinated = 0

    def __call__(self):
        is_on = 0
        for i in range(len(self.people)):
            if self.people[i].on_demand != None:
                self.mate(self.people[i].id-1)  # Increase the marker
                is_on = 1
        if is_on == 0:
            # If everyone is not taking on-demand PrEP, drop the flag
            self.drop_flag()
        else:
            self.raise_flag()
