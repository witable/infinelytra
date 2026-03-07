import numpy as np
import random
import matplotlib
import time
np.set_printoptions(precision=2, suppress=True, linewidth=200, edgeitems=10)
class Vec3:
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, d, e, f):
        return Vec3(self.x * d, self.y * e, self.z * f)

    def horizontalDistance(self):
        return np.sqrt(self.x * self.x + self.z * self.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    def add(self, d, e, f):
        return Vec3(self.x + d, self.y + e, self.z + f)
    
    def length(self):
        return np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
def calculateViewVector(x, y):

    h = x * np.pi / 180
    i = -y * np.pi / 180
    j = np.cos(i)
    k = np.sin(i)
    l = np.cos(h)
    m = np.sin(h)
    return Vec3(k * l, -m, j * l)


def getLookAngle():
    return calculateViewVector(0, 2)

def updateFallFlyingMovement(vec3, x, y):
    vec32 = calculateViewVector(x, y)
    f = x * np.pi / 180
    d = vec32.horizontalDistance()
    e = vec3.horizontalDistance()
    g = 0.08
    h = np.square(np.cos(f))
    vec3 = vec3.add(0, g*(-1 + h * 0.75), 0)

    if (vec3.y < 0 and d > 0):
        i = vec3.y * -.1 * h
        vec3 = vec3.add(vec32.x * i / d, i, vec32.z * i / d)
        
    if (f < 0 and d > 0):
        i = e * -np.sin(f) * 0.04
        vec3 = vec3.add((-vec32.x * i / d), i * 3.2, -vec32.z * i / d)

    if (d > 0):
        vec3 = vec3.add((vec32.x / d * e - vec3.x) * 0.1, 0, (vec32.z / d * e - vec3.z) * 0.1)

    return vec3.multiply(0.99, 0.98, 0.99)

def move(position, movement):
    return position.add(movement.x, movement.y, movement.z)

max = 0
bestAngle = 0

vector = Vec3(0, 0, 0)

"""for pitch in range(91):
    vec3 = Vec3(0, 0, 0)
    for x in range(10000):
        vec3 = updateFallFlyingMovement(vec3, pitch, 0)
    if (max < vec3.length()):
        max = vec3.length()
        bestAngle = pitch"""



"""print(bestAngle)"""


max = 0
bestAngle = 0
vector = Vec3(0, 0, 0)

"""for pitch in range(91):
    vec3 = Vec3(0, 0, 0)
    for x in range(10000):
        vec3 = updateFallFlyingMovement(vec3, pitch, 0)
    if (max < vec3.horizontalDistance()):
        max = vec3.horizontalDistance()
        bestAngle = pitch"""

"""print(bestAngle)"""

precision = 5

def maximumMove(moveDown, moveSame, moveUp):
    
    if (moveDown.x > moveSame.x):
        max1 = moveDown
    else:
        max1 = moveSame

    if (moveSame.x > moveUp.x):
        max2 = moveSame
    else:
        max2 = moveUp

    if (max1.x > max2.x):
        max3 = max1
    else:
        max3 = max2
    return max3

def recurseBestMove(tick, pitch, position, movement):
    if (tick == maxTick):
        return position
    moveDown = movement
    moveSame = movement
    moveUp = movement
    if (pitch > -90):
        moveDown = move(position, recurseBestMove(tick+1, pitch-precision, position+movement, updateFallFlyingMovement(movement, pitch, 0)))
    
    if (pitch < 90):
        moveUp = move(position, recurseBestMove(tick+1, pitch+precision, position+movement, updateFallFlyingMovement(movement, pitch, 0)))

    moveSame = move(position, recurseBestMove(tick+1, pitch, position+movement, updateFallFlyingMovement(movement, pitch, 0)))
    
    return maximumMove(moveDown, moveSame, moveUp)




def recurseBestMove(tick, pitch, position, movement):
    if (tick == maxTick):
        return position
    moveDown = movement
    moveSame = movement
    moveUp = movement
    if (pitch > -90):
        moveDown = move(position, recurseBestMove(tick+1, pitch-precision, position+movement, updateFallFlyingMovement(movement, pitch, 0)))
    
    if (pitch < 90):
        moveUp = move(position, recurseBestMove(tick+1, pitch+precision, position+movement, updateFallFlyingMovement(movement, pitch, 0)))

    moveSame = move(position, recurseBestMove(tick+1, pitch, position+movement, updateFallFlyingMovement(movement, pitch, 0)))
    
    return maximumMove(moveDown, moveSame, moveUp)



generationLimit = 100
populationSize = 20
maxTick = 100
X_MIN = -90
X_MAX = 90
PITCH_MIN = 1
crossOverProbability = .8
mutationProbability = 0.1

def crossover(a,b):
    #if (a.shape < 2):
        #return a,b
    p = random.randint(1, len(a))
    return np.concatenate((a[0:p],b[p:]), axis = 0),np.concatenate((b[0:p],a[p:]), axis = 0)

def mutate(gene, mutation_rate):
    for i in range(1,gene.size):
        if np.random.rand() < mutation_rate:
            gene[i] = gene[i] + np.random.uniform(-1, 1)
            if (gene[i] > PITCH_MIN):
                gene[i] = PITCH_MIN
            if (gene[i] < -PITCH_MIN):
                gene[i] = -PITCH_MIN

    return gene

def fitness(gene):
    position = Vec3(0, 50, 0)
    movement = Vec3(0, 0, 0)
    currentPitch = 0
    for x in (range(maxTick)):
        currentPitch = currentPitch+gene[x]
        if (currentPitch > X_MAX):
            currentPitch = X_MAX
        if (currentPitch < X_MIN):
            currentPitch = X_MIN
        movement = updateFallFlyingMovement(movement, currentPitch, 0)    
        position = position + movement
    if (position.y < 0):
        return 0
    return position.horizontalDistance()


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
    #current_scores = fitnessFunc(population)
    #print(f"Gen {i}: Best Distance = {np.max(current_scores):.2f}")
    #print(population[np.argmax(current_scores)])
end = time.perf_counter() 
print (end-start)



