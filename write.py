import csv
import networkx as nx
import datetime

def WriteStates(obs, filename):
    '''
        Write everyone's infected state into a .csv file.
    '''
    filename = str(filename)+'.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([obs.S, obs.I, obs.V, obs.R])

def WriteOpinion(obs, filename):
    '''
        Write everyone's opinion and infected state into a .csv file.
    '''
    filename = str(filename)+'.csv'
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for i in range(len(obs.people)):
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].opinion])

    # for i in range(len(obs)):
        # print('{} - o: {}, s: {}'.format(obs[i].id, obs[i].opinion, obs[i].suceptible))

def WriteOpinionPersonality(obs, filename):
    '''
        Write everyone's opinion into a .csv file. Their personality are flagged as well.

        Coulmns
        - Group number of the agent
        - Agent name
        - Agent's personality
            - 0 means normal
            - 1 means inflexible
            - 2 means balancer
        - Agent's opinion at time step
    '''
    filename_template = filename
    for i in range(len(obs.people)):
        filename = str(filename_template)+' '+str(i)+'.csv'
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow([obs.people[i].group_no, obs.people[i].id, obs.people[i].personality, obs.people[i].opinion])
        filename = ''

def WriteNetwork(graph_obj, filename):
    export_graph = graph_obj
    mapping = {}
    for node in graph_obj.nodes:
        mapping[node] = node.id
    export_graph = nx.relabel_nodes(export_graph, mapping)
    nx.write_graphml(export_graph, filename+'.graphml')

def WriteSex(obs, filename):
    filename = str(filename)+'-sex.csv'
    # Generate all agents's move in a row.
    sex_data = []
    for i in range(len(obs.people)):
        # print('{}: {}'.format(obs.people[i].id, obs.people[i].sex_history))
        sex_data.append(obs.people[i].sex_history[-1])

    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(sex_data)
    condom_data = []

def WriteCondom(obs, filename):
    '''
    Save condom simulation data.

    Parameters
    ----------
    obs: Epidemic
        Accepts Epidemic object
    filename: str
        File name for export
    '''
    filename = str(filename)+'-condom.csv'
    # Generate all agents's move in a row.
    condom_data = []
    for i in range(len(obs.people)):
        # print('{}: {}'.format(obs.people[i].id, obs.people[i].condom_history))
        condom_data.append(obs.people[i].condom_history[-1])

    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(condom_data)
    condom_data = []

def WriteCondomData(obs):
    '''
    Save basic condom data.

    Parameters
    ----------
    obs: Simulation
        Accepts Simulation object
    filename: str
        File name for export
    '''
    text = []

    text.append('=============================\n\n')
    text.append('Condom usage\n\n')
    text.append('=============================\n\n')
    text.append('# Basic data\n\n')
    text.append('Number of people (N): {}\n\n'.format(len(obs.N)))
    text.append('Frequency compartments: {}\n\n'.format(len(obs.modes[6].condom_rate)))
    text.append('# Compartments\n\n')
    text.append('All agents are separated in {} condom usage groups. They are differentiated by their usage frequency.\n\n'.format(len(obs.modes[6].condom_rate)))
    text.append('Category: high, median, low\n\n')
    text.append('Proportion of groups (respect with order):\n\n')
    text.append('{}, {}, {}\n\n'.format(obs.modes[6].condom_proportion[0], obs.modes[6].condom_proportion[1], obs.modes[6].condom_proportion[2]))
    text.append('# Risk compensation\n\n')
    text.append('Risk compensation is represented by the frequency of condom usage at each sexual intercourse. This probabilitic value determines if the person wears condom during sexual intercourse.\n\n')
    text.append('Category: high, median, low\n\n')
    text.append('Frequency of groups (respect with order):\n\n')
    text.append('{}, {}, {}\n\n'.format(obs.modes[6].condom_rate[0], obs.modes[6].condom_rate[1], obs.modes[6].condom_rate[2]))
    text.append('# Extract data\n\n')
    text.append('When extracting inputs parameters from this document, please the following:\n\n')
    text.append('* Row 9: N\n')
    text.append('* Row 21: Proportions\n')
    text.append('* Row 31: Frequency\n')

    with open(obs.filename + '-basic.txt', 'w') as f:
        f.writelines(text)
