import numpy as np
import random
import matplotlib.pyplot as plt
import time
import elytra_physics
np.set_printoptions(precision=2, suppress=True, linewidth=200, edgeitems=10)

generationLimit = 1000
populationSize = 100
maxTick = 1000
X_MIN = -90
X_MAX = 90
PITCH_MIN = 1
crossOverProbability = .90
positionY = 75
mutationProbability = 0.1

def fitness(gene):
    return elytra_physics.update_physics(positionY, gene, maxTick)


def fitnessFunc(population):
    scores = []
    for i in population:
        scores.append(fitness(i))
    return np.array(scores)

def tournament_selection(population, scores, numOfSelection = 10):
    idx = np.random.randint(0, population.shape[0], size=numOfSelection)

    tournament_scores = scores[idx]

    winner_i = idx[np.argmax(tournament_scores)]
    
    return population[winner_i].copy()

population = 2*np.random.rand(populationSize,maxTick)-1

start = time.perf_counter()
for i in range(generationLimit):
    current_scores = fitnessFunc(population)
    
    next_population = np.empty((populationSize, maxTick))
    for j in range(0, populationSize, 2):

        p1 = tournament_selection(population, current_scores)
        p2 = tournament_selection(population, current_scores)
        if (np.random.rand() < crossOverProbability):
            c1, c2 = elytra_physics.crossover(p1, p2)
        else:
            c1, c2 = p1, p2
        next_population[j] = elytra_physics.mutate(c1, mutationProbability)
        
        next_population[j+1] = elytra_physics.mutate(c1, mutationProbability)
    
    population = next_population
    #current_scores = fitnessFunc(population)
    #print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")

end = time.perf_counter() 
print (end-start)


current_scores = fitnessFunc(population)
print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")

list1 = [0]
cumm = 0
with open("out.txt", "w") as a:
    for i in range(0,population[np.argmax(current_scores)].size):
        curr = float(population[np.argmax(current_scores)][i])
        cumm += float(population[np.argmax(current_scores)][i])
        list1.append(cumm)
        a.write(str(curr) + "\n")
         
print(elytra_physics.check_physics(maxTick, positionY))

list2 = [0]
for i in range(population[np.argmax(current_scores)].size):
    list2.append(round(float(population[np.argmax(current_scores)][i]),2))

xpoints = range(0,maxTick)
plt.plot(list1)
plt.show()