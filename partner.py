import random
import networkx as nx
from matplotlib import pyplot as plt

import person

class Partner:

    def __init__(self, people):
        self.people = people
        self.group_no = None
        self.network = None  # Graph to show partner topology
        self.set_pair()  # By default, all agents have a sex partner.
        self.nwk_graph = nx.Graph(self.network)

    def set_pair(self):
        temp_roster = self.people
        random.shuffle(temp_roster)
        self.network = list(zip(temp_roster[:len(temp_roster)//2],temp_roster[len(temp_roster)//2:]))
        if len(self.people) % 2 == 1:
            self.network.append((self.people[-1],None))

    def show_nwk(self):
        pos = nx.random_layout(self.nwk_graph)
        labels = {}
        for node in self.nwk_graph.nodes:
            if type(node) == person.Person:
                labels[node] = node.id
        nx.draw(self.nwk_graph, pos=pos,with_labels=False)
        nx.draw_networkx_labels(self.nwk_graph,pos=pos,labels=labels,font_size=16)
        plt.show()
