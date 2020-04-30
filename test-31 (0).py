from person import Person
from mode import Mode31

N = 2
T = 10

# Generate population
population = [Person() for i in range(N)]
print(population)

# Generate mode 31
mode31 = Mode31(population)

for t in range(T):
    print('=== t = {} ==='.format(t))
    mode31()
    if t == 0 or t == 5:
        mode31.mate(1,'Yes')
    for i in range(N):
        print(population[i].mated_marker)
    print()
