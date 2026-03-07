import numpy as np
import random
import matplotlib
import time
import elytra_physics
np.set_printoptions(precision=2, suppress=True, linewidth=200, edgeitems=10)

generationLimit = 100
populationSize = 100
maxTick = 100
X_MIN = -90
X_MAX = 90
PITCH_MIN = 1
crossOverProbability = .8
mutationProbability = 0.5

def calculateViewVector(x, y):
    h = x * np.pi / 180
    i = -y * np.pi / 180
    j = np.cos(i)
    k = np.sin(i)
    l = np.cos(h)
    m = np.sin(h)
    return (k * l, -m, j * l)

def updateFallFlyingMovement(vx, vy, vz, x, y):
    v2x, v2y, v2z = (calculateViewVector(x,y))
    f = x * np.pi / 180
    d = np.sqrt(v2x**2 + v2z**2)
    e = np.sqrt(vx**2 + vz**2)
    g = 0.08
    h = np.square(np.cos(f))
    vy += g * (-1 + h * 0.75)

    if (vy < 0 and d > 0):
        i = vy * -0.1 * h
        vx += v2x * i / d
        vy += i
        vz += v2z * i / d
        
    if (f < 0 and d > 0):
        i = e * -np.sin(f) * 0.04
        vx += -v2x * i / d
        vy += i * 3.2
        vz += -v2z * i / d

    if (d > 0):
        vx += (v2x / d * e - vx) * 0.1
        vz += (v2z / d * e - vz) * 0.1
        
    return vx * 0.99, vy * 0.98, vz * 0.99

def crossover(a,b):
    #if (a.shape < 2):
        #return a,b
    p = random.randint(1, len(a))
    return np.concatenate((a[0:p],b[p:]), axis = 0),np.concatenate((b[0:p],a[p:]), axis = 0)

def mutate(gene, mutation_rate):
    for i in range(1,gene.size):
        if np.random.rand() < mutation_rate:
            gene[i] = round(gene[i] + np.random.uniform(-1, 1),2)
            if (gene[i] > PITCH_MIN):
                gene[i] = PITCH_MIN
            if (gene[i] < -PITCH_MIN):
                gene[i] = -PITCH_MIN

    return gene

def horizontalFitness(gene):
    positionx = 0
    positiony = 30
    positionz = 0
    movementx = 0
    movementy = 0
    movementz = 0
    currentPitch = 0
    for x in (range(maxTick)):
        currentPitch = currentPitch+gene[x]
        if (currentPitch > X_MAX):
            currentPitch = X_MAX
        if (currentPitch < X_MIN):
            currentPitch = X_MIN
        movementx, movementy, movementz = elytra_physics.update_physics(movementx, movementy, movementz, currentPitch, 0) 
        #print(movementx, movementy, movementz)   
        positionx += movementx
        positiony += movementy
        positionz += movementz
    #if (positiony < 0):
     #   return 0
    return np.sqrt(positionx**2 + positionz**2)

def fitness(gene):
    positionx = 0
    positiony = 30
    positionz = 0
    movementx = 0
    movementy = 0
    movementz = 0
    currentPitch = 0
    for x in (range(maxTick)):
        currentPitch = currentPitch+gene[x]
        if (currentPitch > X_MAX):
            currentPitch = X_MAX
        if (currentPitch < X_MIN):
            currentPitch = X_MIN
        movementx, movementy, movementz = elytra_physics.update_physics(movementx, movementy, movementz, currentPitch, 0) 
        #print(movementx, movementy, movementz)   
        positionx += movementx
        positiony += movementy
        positionz += movementz
    if (positiony < 0):
        return 0
    return np.sqrt(positionx**2 + positionz**2)


def fitnessFunc(population):
    scores = []
    for i in population:
        scores.append(fitness(i))
    return np.array(scores)

def fitnessFuncInx(population, idx):
    return [fitness(population[i]) for i in idx]
    #return np.array(scores)


def tournament_selection(population, numOfSelection = 5):
    #scores = np.array(fitnessFunc(population))
    def selectRandom():
        idx = np.random.randint(0, population.shape[0], size=numOfSelection)
        tournament_scores = fitnessFuncInx(population,idx)
        winner_i = idx[np.argmax(tournament_scores)]
        return population[winner_i].copy()
    
    return selectRandom(), selectRandom()



population = np.zeros((populationSize,maxTick))
start = time.perf_counter()
for i in range(generationLimit):
    
    offspring = []
    for j in range(0, populationSize, 2):
        parents = tournament_selection(population)
        if (np.random.rand() < crossOverProbability):
            c1, c2 = crossover(parents[0], parents[1])
        else:
            c1, c2 = parents[0], parents[1]
        offspring.append(mutate(c1, mutationProbability))
        offspring.append(mutate(c2, mutationProbability))
    
    population = np.reshape(np.array(offspring), (populationSize,maxTick))
    current_scores = fitnessFunc(population)
    #print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")
    #print(population[np.argmax(current_scores)])

current_scores = fitnessFunc(population)
print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")
#print(population[np.argmax(current_scores)])

end = time.perf_counter() 
print (end-start)



