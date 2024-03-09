import random
import pandas as pd

def initializePopulation(dfSize):
    population = []
    for i in range (0, dfSize):
        population.append(0)

    return population

def generateRandomWeight(minWeight, maxWeight):
    return random.uniform(minWeight, maxWeight)

def addWeights(gene):
    weightSum = 0
    for i in range(0, len(gene)):
        weightSum = weightSum + gene[i]
    
    return weightSum

def generateSnackWeights(pickedIndices, maxWeight, df):
    gene = initializePopulation(df.shape[0])
    weightSum = 0

    for i in range(0, len(pickedIndices)):
        if i == len(pickedIndices) -1:
            if df['Available Weight'][pickedIndices[i]] <= (maxWeight - weightSum):
                gene[pickedIndices[i]] = df['Available Weight'][pickedIndices[i]]
            
            else:
                gene[pickedIndices[i]] = maxWeight - weightSum
           # print("for last ", gene[pickedIndices[i]], " was selected", df['Available Weight'][pickedIndices[i]]," was available")

        else:
            w = generateRandomWeight(0, df['Available Weight'][pickedIndices[i]])
            gene[pickedIndices[i]] = w

            while(weightSum + w > maxWeight):
                w = generateRandomWeight(0, df['Available Weight'][pickedIndices[i]])

                if w + weightSum <= maxWeight:
                    gene[pickedIndices[i]] = w
                    break
                        
            weightSum += w

    #print(gene)
    return gene

def isWeightValid(snackIndex, pickedWeight, df):
    if (df['Available Weight'][snackIndex + 1] < pickedWeight * df['value_per_weight'][snackIndex + 1]):
        return False

    return True

def fitnessCalculator(gene, df, minVal):
    df['value_per_weight'] = df['Value'] / df['Available Weight']
    fitnesss = 0
    for i in range(0, len(gene)):
        if gene[i] != 0:
            fitnesss += df['value_per_weight'][i] * gene[i]

    if fitnesss < minVal:
        return 0
    return fitnesss

def generateSubset(genes):
    subsetSize = random.randint(2, len(genes))
    pickedIndices = []
    while len(pickedIndices) < subsetSize:
        r = random.randint(0, len(genes) - 1)
        if r not in pickedIndices:
            pickedIndices.append(r)

    #print("sub is ", pickedIndices, " len is ", subsetSize)
    return pickedIndices

def sortSubsetsByFitness(genes, minVal):
    maxFit = 0
    maxIndex = 0
    pickedGene = []
    df = pd.read_csv('snacks.csv')

    #while maxFit == 0:
    pickedIndices = generateSubset(genes)

    for i in range (0, len(pickedIndices)):
        fitness = fitnessCalculator(genes[pickedIndices[i]], df, minVal)
        #print("it is", len(pickedIndices))
        if fitness > maxFit:
            maxFit = fitness
            maxIndex = pickedIndices[i]
            pickedGene = genes[maxIndex]

    print("fitness is ", maxFit)
    # print("picked gene is ", gene)
    return pickedGene

def tournamentSelection(genes, minVal):
    parents = []
    while True:
        mom = sortSubsetsByFitness(genes, minVal)
        dad = sortSubsetsByFitness(genes, minVal)
        if mom == dad:
            continue
        else:
            break

    # print("mom is ", mom)
    # print("dad is ", dad)
    parents.append(mom)
    parents.append(dad)
    return parents

def crossover(mom, dad, crossPoint):
    if crossPoint < 0 or crossPoint >= min(len(mom), len(dad)):
        raise ValueError("Cross point is out of range")

    crossed_chromosome = mom[:crossPoint] + dad[crossPoint:]
    return crossed_chromosome


df = pd.read_csv('snacks.csv')
#print(df)

allPopulationNumber = df.shape[0]
minVal = input()
maxWeight= input()
minNumber= input()
maxNumber= input()

minVal = int(minVal)
maxWeight = int(maxWeight)
minNumber = int(minNumber)
maxNumber = int(maxNumber)

chromosome = 0
gene = []
genes = []
fitnessSofar = 0
algorithmRound = 0
maxRound = 5
pickedIndices = []
selectedParants = []

lowerBoundWeight = 0
upperBoundWeight = maxWeight

for n in range(minNumber, maxNumber+1):
    algorithmRound = 0
    pickedWeight = []

    gene = initializePopulation(df.shape[0])
    while algorithmRound < maxRound:
        for i in range(0, n):

            randIndex = random.randint(0, df.shape[0]-1)
            while pickedIndices.count(randIndex) == 1:
                randIndex = random.randint(0, df.shape[0]-1)
            pickedIndices.append(randIndex)

        gene = generateSnackWeights(pickedIndices, maxWeight, df)
        #print("the whole weight is ", addWeights(gene))

        newFitness = fitnessCalculator(gene, df, minVal)
        if newFitness == 0:
            continue

        genes.append(gene)
        if newFitness > fitnessSofar:
            fitnessSofar = newFitness

        #print("so far fitness is", fitnessSofar)

        pickedIndices.clear()
        gene = initializePopulation(df.shape[0])
        algorithmRound = algorithmRound + 1

#print(genes)
#select
parents = random.randint(round(len(genes) / 4), round(len(genes) / 2))
for i in range(0, parents):
    selectedParants.append(tournamentSelection(genes, minVal))

print(selectedParants)

#crossover
genes2 = []
for i in range(0, len(selectedParants)):
    newGene = crossover(selectedParants[i][0], selectedParants[i][1], random.randint(1, df.shape[0]))
    genes2.append(newGene)

#print(genes2)
#mutation
#continuou with the new population