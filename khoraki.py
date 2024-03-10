import random
import pandas as pd

AVAILABLE_WEIGHT_COLUMN = 'Available Weight'
VALUE_COLUMN = 'Value'
SNACK_COLUMN = 'Snack'
FILE_NAME = 'snacks.csv'

def initializePopulation(dfSize):
    population = []
    for i in range (0, dfSize):
        population.append(0)

    return population

def generateRandomWeight(minWeight, maxWeight):
    return random.uniform(minWeight, maxWeight)

def generateSnackWeights(pickedIndices, df):
    gene = initializePopulation(df.shape[0])
    for i in range(0, len(pickedIndices)):
        w = generateRandomWeight(0, df[AVAILABLE_WEIGHT_COLUMN][pickedIndices[i]])
        gene[pickedIndices[i]] = w

    return gene

def addWeights(gene):
    weightSUm = 0
    for i in range(0, len(gene)): 
        weightSUm += gene[i]
    return weightSUm

def fitnessCalculator(gene, df, minVal, maxWeight, minNumber, maxNumber) -> tuple[int, int]:
    df['value_per_weight'] = df[VALUE_COLUMN] / df[AVAILABLE_WEIGHT_COLUMN]
    value = 0
    types = 0
    fitness = 0
    weightSUm = 0
    for i in range(0, len(gene)):
        if gene[i] > df[AVAILABLE_WEIGHT_COLUMN][i]:
            return 0, 0

    for i in range(0, len(gene)):
        if gene[i] != 0:
            weightSUm += gene[i]
            types += 1
            value += df['value_per_weight'][i] * gene[i]

    if value < minVal:
        fitness =  0
    elif weightSUm > maxWeight:
        fitness =  0
    elif types < minNumber or types > maxNumber:
        fitness =  0
    else:
        fitness = value

    return fitness, weightSUm

def sortGenes(genes, df, minVal, maxWeight, minNumber, maxNumber):
    geneFitnessPair = [(gene, fitnessCalculator(gene, df, minVal, maxWeight, minNumber, maxNumber)) for gene in genes]
    sortedPairs = sorted(geneFitnessPair, key=lambda x: x[1], reverse=True)
    sortedGenes = [gene[0] for gene in sortedPairs]
    return sortedGenes

def generateCrossoverProbabilities(genesLength):
    crossProbs = []
    for i in range (0, genesLength):
        randomProb = random.random()
        crossProbs.append(randomProb)

    return crossProbs

def extractEliteChromosomes(genes):
    mid = len(genes) // 2 + len(genes) // 4 + len(genes) // 8
    larger_half = genes[:mid]
    pickedIndices = []

    eliteNum = random.randint(0, mid)
    for i in range (0, eliteNum):
        pickedIndices.append(random.randint(0, len(larger_half) - 1))

    #not an English newbbie, just a bunny
    newjeans = []
    for i in range(0, len(pickedIndices)):
        newjeans.append(larger_half[pickedIndices[i]])

    return newjeans

def applyCrossOver(genes):
    crossOverProbability = random.random()
    crossoverProbs = generateCrossoverProbabilities(len(genes))
    crossPicked = []

    for i in range(0, len(genes)):
        if crossoverProbs[i] < crossOverProbability:
            crossPicked.append(i)

    for i in range(0, len(crossPicked) - 1):
        ch1 = genes[crossPicked[i]]
        ch2 = genes[crossPicked[len(crossPicked) - 1 - i]]
        ch1, ch2 = performCrossOver(ch1, ch2)
        genes[crossPicked[i]] = ch1
        genes[crossPicked[i+1]] = ch2

    return genes

def performCrossOver(mom, dad):
    crossoverPoints = sorted(random.sample(range(0, len(mom)), 2))
    child1 = mom[:crossoverPoints[0]] + dad[crossoverPoints[0]:crossoverPoints[1]] + mom[crossoverPoints[1]:]
    child2 = dad[:crossoverPoints[0]] + mom[crossoverPoints[0]:crossoverPoints[1]] + dad[crossoverPoints[1]:]

    return child1, child2

def applyMutation(genes):
    mutationRound = random.randint(1, 10)
    for j in range(0, mutationRound):
        mutationProbability = random.random()
        for i in range(len(genes)):
            for j in range(len(genes[i]) - 1): 
                if random.random() < mutationProbability:
                    temp = genes[i][j]
                    genes[i][j] = genes[i][j+1]
                    genes[i][j+1] = temp

    return genes

def generateChromosome(minNumber, maxNumber, df):
    gene = []
    pickedIndices = []
    for n in range(minNumber, maxNumber+1):
            for i in range(0, n):
                randIndex = random.randint(0, df.shape[0]-1)
                while pickedIndices.count(randIndex) == 1:
                    randIndex = random.randint(0, df.shape[0]-1)
                pickedIndices.append(randIndex)

            gene = generateSnackWeights(pickedIndices, df)
            pickedIndices.clear()

    return gene

def generatePrimaryPopulation(minNumber, maxNumber, df, minVal, maxWeight):
    generationRound = random.randint(100, 500)
    for i in range (0, generationRound):
        gene = generateChromosome(minNumber, maxNumber, df)
        genes.append(gene)
        
    return genes


df = pd.read_csv(FILE_NAME)
minVal = input()
maxWeight= input()
minNumber= input()
maxNumber= input()

minVal = int(minVal)
maxWeight = int(maxWeight)
minNumber = int(minNumber)
maxNumber = int(maxNumber)

gene = []
genes = []
algorithmRound = 0
maxRound = 25
elite = []
answers = []
restartNum = random.randint(10,100)
print("restart: ", restartNum)
restartCount = 0
while True:
    while restartCount < restartNum:
        genes = generatePrimaryPopulation(minNumber, maxNumber, df, minVal, maxWeight)
        while algorithmRound < maxRound:
            sortedGenes = sortGenes(genes, df, minVal, maxWeight, minNumber, maxNumber)
            elite = extractEliteChromosomes(sortedGenes)
            genes = applyCrossOver(elite)
            genes = applyMutation(genes)
            if (len(genes) == 0):
                break
            sortedGenes = sortGenes(genes, df, minVal, maxWeight, minNumber, maxNumber)
            answers.append(sortedGenes[0])
            algorithmRound += 1

            i = 0
            while i < len(answers):
                a, _ = fitnessCalculator(answers[i], df, minVal, maxWeight, minNumber, maxNumber)
                if a == 0:
                    answers.pop(i)
                else:
                    i += 1

        print("restart count: ", restartCount)
        restartCount += 1
        algorithmRound = 0

    if (len(answers) == 0):
        print("continue")
        restartCount -= 1
        continue
    else:
        break

sortedAnswers = sortGenes(answers, df, minVal, maxWeight, minNumber, maxNumber)
print(fitnessCalculator(sortedAnswers[0], df, minVal, maxWeight, minNumber, maxNumber))
print("\n", answers[0])
for i in range(0, df.shape[0]):
    print("snack name is: ", df[SNACK_COLUMN][i]," and available: " ,df[AVAILABLE_WEIGHT_COLUMN][i], " gene is: ", answers[0][i])
