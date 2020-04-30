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
01: Living in city/ suburb
'''
class Mode01(Mode):
    def __init__(self, people):
        super().__init__(people)
        self.f = 0
        # Proportion of agents seeing a GP or sex clinic
        self.gp = 0
        self.sc = 0

    def __call__(self):
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
        if self.gp != 0 and self.sc != 0:
            self.raise_flag()
        else:
            self.drop_flag()

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

            cmd = input('Do you want to leave?')
            if cmd == 'y':
                return

'''
06: Risk compensation (%)
'''
class Mode06(Mode):
    def __init__(self):
        super().__init__()
        self.condom_rate = 0.03  # Hard coded frequency of use condoms.

    def set_condom_rate(input):
        self.condom_rate = input

    def set_population(input):
        '''
        Set whom uses condom and their habits.
        '''
        pass

    def set_high_condom_use(self):
        '''
        Set the person uses condom frequently.
        '''
        pass

    def set_median_condom_use(self):
        '''
        Set the person uses condom frequently, around the median.
        '''
        pass

    def set_low_condom_use(self):
        '''
        Set the person uses condom infrequently.
        '''
        pass

    def infect_condom_use(self):
        '''
        By pass the act of sex when condom involved
        '''
        # new_beta_0 = self.beta - level * self.condom_rate
        # new_beta_1 = self.beta - level * self.condom_rate 
        # Max of beta if different compartment
        pass




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
