import csv

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
