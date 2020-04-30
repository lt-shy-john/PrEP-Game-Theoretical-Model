from person import Person
from epidemic import Epidemic
from mode import Mode31

N = 5
T = 10

# Generate population
population = [Person() for i in range(N)]
# print(population)

# Start epidemic
epidemic = Epidemic(0.1, 0.2, 0.9, 0.01, population)
epidemic.start_epidemic()

# Generate mode 31
mode31 = Mode31(population)

for t in range(T):
    print('=== t = {} ==='.format(t))
    mode31()
    if t == 1 or t == 5:
        mode31.mate(1,'Yes')
        print('<3')
    for i in range(N):
        mode31.mate(i)
        epidemic.next('')
        print('id: {}, mated: {}, S = {}'.format(population[i].id, population[i].mated_marker, population[i].suceptible))
    print()
