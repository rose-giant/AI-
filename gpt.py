import random
import pandas as pd

# Define parameters
population_size = 100
mutation_rate = 0.1
crossover_rate = 0.8
max_weight = 100  # Set your maximum weight here
max_generations = 1000

# Function to initialize a chromosome
def initialize_chromosome(num_snacks):
    return [random.choice([0, 1]) for _ in range(num_snacks)]

# Function to calculate fitness of a chromosome
def calculate_fitness(chromosome, snacks):
    total_value = sum(chromosome[i] * snacks['Value'].iloc[i] for i in range(len(chromosome)))
    total_weight = sum(chromosome[i] * snacks['value_per_weight'].iloc[i] for i in range(len(chromosome)))
    return total_value if total_weight <= max_weight else 0

# Function to perform crossover between two chromosomes
def crossover(chromosome1, chromosome2):
    crossover_point = random.randint(1, len(chromosome1) - 1)
    return chromosome1[:crossover_point] + chromosome2[crossover_point:], \
           chromosome2[:crossover_point] + chromosome1[crossover_point:]

# Function to perform mutation on a chromosome
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]  # Flip 0 to 1 or 1 to 0
    return chromosome

# Read snacks data
snacks = pd.read_csv('snacks.csv')
snacks['value_per_weight'] = snacks['Value'] / snacks['Available Weight']

# Main genetic algorithm loop
generation = 0
population = [initialize_chromosome(len(snacks)) for _ in range(population_size)]

while generation < max_generations:
    # Calculate fitness for each chromosome
    fitness_scores = [calculate_fitness(chromosome, snacks) for chromosome in population]
    
    # Select parents for crossover
    selected_indices = random.choices(range(len(population)), weights=fitness_scores, k=2)
    parent1 = population[selected_indices[0]]
    parent2 = population[selected_indices[1]]
    
    # Perform crossover
    if random.random() < crossover_rate:
        child1, child2 = crossover(parent1, parent2)
    else:
        child1, child2 = parent1, parent2
    
    # Mutate offspring
    child1 = mutate(child1)
    child2 = mutate(child2)
    
    # Replace parents with offspring
    population[selected_indices[0]] = child1
    population[selected_indices[1]] = child2
    
    generation += 1

# Find the best solution in the final population
best_index = max(range(len(population)), key=lambda i: calculate_fitness(population[i], snacks))
best_solution = population[best_index]
best_fitness = calculate_fitness(best_solution, snacks)

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
