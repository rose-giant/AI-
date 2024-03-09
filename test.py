import random


def applyMutation(genes):
    mutationProbability = random.random()
    print("mutation prob is ", mutationProbability)
    for i in range(len(genes)):
        for j in range(len(genes[i]) - 1):  # Adjusted loop range
            if random.random() < mutationProbability:
                temp = genes[i][j]
                genes[i][j] = genes[i][j+1]
                genes[i][j+1] = temp

    print(genes)
    return genes

genes = [[1,2,3,4,5,6,7],[8,9,10],[11,12],[13,14]]
applyMutation(genes=genes)
