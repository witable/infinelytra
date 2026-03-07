import numpy as np
import random
import matplotlib.pyplot as plt
import time
import elytra_physics
np.set_printoptions(precision=2, suppress=True, linewidth=200, edgeitems=10)

generationLimit = 100
populationSize = 100
maxTick = 500
X_MIN = -90
X_MAX = 90
PITCH_MIN = 1
crossOverProbability = .90
mutationProbability = 0.001

def fitness(gene):
    positiony = 50
    return elytra_physics.update_physics(positiony, gene, maxTick)


def fitnessFunc(population):
    scores = []
    for i in population:
        scores.append(fitness(i))
    return np.array(scores)

def fitnessFuncInx(population, idx):
    return [fitness(population[i]) for i in idx]
    #return np.array(scores)


def tournament_selection(population, numOfSelection = 10):
    #scores = np.array(fitnessFunc(population))
    def selectRandom():
        idx = np.random.randint(0, population.shape[0], size=numOfSelection)
        tournament_scores = fitnessFuncInx(population,idx)
        winner_i = idx[np.argmax(tournament_scores)]
        return population[winner_i].copy()
    
    return selectRandom(), selectRandom()

population = 2*np.random.rand(populationSize,maxTick)-1

start = time.perf_counter()
for i in range(generationLimit):
    offspring = []
    for j in range(0, populationSize, 2):
        parents = tournament_selection(population)
        if (np.random.rand() < crossOverProbability):
            c1, c2 = elytra_physics.crossover(parents[0], parents[1])
        else:
            c1, c2 = parents[0], parents[1]
        offspring.append(elytra_physics.mutate(c1, mutationProbability))
        offspring.append(elytra_physics.mutate(c2, mutationProbability))
    
    population = np.reshape(np.array(offspring), (populationSize,maxTick))
    #current_scores = fitnessFunc(population)
    #print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")

end = time.perf_counter() 
print (end-start)


current_scores = fitnessFunc(population)
print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")

list = [0]
curr = 0

for i in range(0,population[np.argmax(current_scores)].size):
    curr += float(population[np.argmax(current_scores)][i])
    list.append(round(curr,2))
    with open("out.txt", "a") as a:
        a.write(str(round(curr,2)) + "\n")
         

list2 = [0]
for i in range(population[np.argmax(current_scores)].size):
    list2.append(round(float(population[np.argmax(current_scores)][i]),2))

xpoints = range(0,maxTick)
plt.plot(list)
plt.show()