########################################
# An Evolutionary Algorithm Framework  #
# By Austin Dickerson                  #
# 10/9/2023                            #
########################################


# imports evoman and controller frameworks
from evoman.environment import Environment
from demo_controller import player_controller
import os, random, time, csv, itertools
import numpy as np
import pandas as pd

# Game Parameters
evoman = True
set = [1,4,6]
generalist = True
multiple_mode = True

# NN Parameters
n_hidden_neurons = 10
num_vars = n_hidden_neurons * (21) + (n_hidden_neurons + 1) * 5

# Experiment Parameters
pop_size = 100
generations = 20
early_stop = False

# Mutation Parameters
mutation_intensity = 1
mutagenic_temperature = 0.2
mutation_reset = False

# Reproduction Parameters
discrete = False
individual_cross = False
crossover_line = False
curve_parents = True

# Elitism Parameters
elitism = 1
half = False

# Optimization Parameters
prioritize_life = False
prioritize_time = False
objective_switchpoint = False

# Doomsday parameter
reseed_cycle = False


##### Reproduction Strategy ##### 
# reproduce_generational is default if all below are false)
reproduce_steady = False
comma_strategy = False
evolutionary_programming = False

# Non-traditional reproductive algorithms
particle_swarm_optimization = False
pso_weights = [0.5, 0.5, 0.3] 

differential_evolution = False
scaling_factor = 0.8

# Speciation Paremeters
speciate = False
threshold = 0.65
speciation_frequency = 10


# Reproducability
random.seed(579)
np.random.seed(135)
runs = 1
save = True

# Experiment state variables
pop = []
midpoint = False

# Name of the experiment
filename = 'GENERALIST_TEST'

experiment_name = 'controller_generalist'

if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# Name of the folder where statistics will be saved
stat_directory = 'Experiments_Evoman/EA_Statistics'

if not os.path.exists(f'{stat_directory}_{filename}'):
    os.makedirs(f'{stat_directory}_{filename}')


##### Population manipulating methods #####

# Create the randomized population
def initialize_population(pop_size, num_vars):
    pop = []

    for _ in range(pop_size):
        member = np.zeros(num_vars)

        for j in range(num_vars):
            member[j] = random.uniform(-1,1)

        pop.append(member)   

    return pop

# Initializes the population with additional parameters for sigma
def initialize_population_EP(pop_size, num_vars):
    pop = []
    perturbation_vectors = []

    for _ in range(pop_size):
        member = np.zeros(num_vars)
        perturbation = np.ones(num_vars)

        for j in range(num_vars):
            member[j] = random.uniform(-1,1)

        pop.append(member)   
        perturbation_vectors.append(perturbation)

    return pop, perturbation_vectors

# Run simulation for entire pop
def test_population(pop):
    scores = []
    lives = []
    gametimes = []

    for unit in pop:

        if evoman:
            fit, p_life, e_life, gametime = env.play(pcont=unit)
        else:
            # Space for alternate environments/games
            fit, p_life, e_life, gametime = 0, 0, 0, 0

        scores.append(fit)
        lives.append(p_life)
        gametimes.append(gametime)

    # Base best parameters on the right metric
    if prioritize_life == True:
        maximum = max(lives)
        ind = lives.index(maximum)
    elif prioritize_time == True:
        maximum = max(gametimes)    
        ind = gametimes.index(maximum)
    else:
        maximum = max(scores)
        ind = scores.index(maximum)

    return scores, maximum, ind, lives, gametimes


##### Statistics #####

# Normalize with lowest ~~0
def normalize(scores):
    scores = np.array(scores,float)
    lo = min(scores)
    hi = max(scores)
    scores -= lo
    scores /= (hi-lo)

    return scores

# Normalize on full range
def evo_normalize(scores):
    scores = np.array(scores)

    # Accommodate the greater range of fit scores during multi_mode (min varies by st. dev.)
    if multiple_mode:
        scores += 20
        scores /= 120
    else:
        scores += 10
        scores /= 110

    return scores

# Return as normalized probabilities
def relative_prob(fit_scores):
    probabilities = np.array(fit_scores)/np.array(fit_scores).sum()
    probabilities = np.nan_to_num(probabilities)
    probabilities = np.clip(probabilities, 0, 1)
    probabilities = probabilities / np.sum(probabilities)

    return probabilities

# List population in ascending order of fit score
def sort(pop, fit_scores):
    sorted_pairs = sorted(zip(pop, fit_scores), key=lambda x: x[1])
    pop, fit_scores = zip(*sorted_pairs)

    return pop, fit_scores


##### Selection #####

# Find 2 parents to reproduce
def select_parents(pop, low=None, high=None, probabilities=None):

    # Select based on proportion to fitness scores
    if curve_parents == True:
        selected = np.random.choice(len(pop), 2, p=probabilities, replace=False)
        p1 = pop[selected[0]]
        p2 = pop[selected[1]]

    else:
        first = random.randint(low,high-1)
        second = random.randint(low,high-1)

        while first == second:
            second = random.randint(low,high-1)

        p1 = pop[first]
        p2 = pop[second]

    return p1, p2


##### Recombination #####

# Returns one or two children from two parents
def reproduction(p1, p2, two_child=True):
    if discrete:
        child = combine_genes_discrete(p1, p2)
        if two_child:
            child2 = combine_genes_discrete(p1, p2)

    elif individual_cross:
        child = combine_genes_individual_cross(p1, p2)
        if two_child:
            child2 = combine_genes_individual_cross(p1, p2)

    else:
        child = combine_genes_cross(p1, p2)
        if two_child:
            child2 = combine_genes_cross(p1, p2)

    if two_child:
        return child, child2
    else:
        return child

# Take one allele from each parent with uniform probability
def combine_genes_discrete(p1, p2):
    child = p1

    for i in range(len(p1)):

        if random.random() > 0.5:
            child[i] = p2[i]

    return child

# Merge all alleles at a random split ratio
def combine_genes_cross(p1, p2):
    temp = np.random.random()

    if crossover_line == True:
        ind = int(len(p1) * temp)
        child = np.concatenate((p1[:ind], p2[ind:]))
    else:
        zygote1 = temp * p1
        zygote2 = (1 - temp) * p2
        child = zygote1 + zygote2

    return child

# Merge each allele individually
def combine_genes_individual_cross(p1, p2):
    temp = np.random.rand(num_vars)
    zygote1 = temp * p1
    zygote2 = (1 - temp) * p2
    child = zygote1 + zygote2

    return child


##### Mutation #####

# Alter some alleles in a new child
def mutate_offspring(child):
    for i in range(len(child)):

        if random.random() < mutagenic_temperature:

            # Either reset the allele or alter the existing
            if mutation_reset == True:
                child[i] = np.random.uniform(-1,1)
            else:
                child[i] += np.random.normal(0, mutation_intensity)

                if child[i] < -1:
                    child[i] = -1
                if child[i] > 1:
                    child[i] = 1

    return child

# Mutate based on Evolutionary Programming
def mutate_offspring_EP(child, perturbation_vector):

    # Update sigma parameters
    for i in range(num_vars):

        perturbation_vector[i] *= (0.2*np.random.normal(0, perturbation_vector[i])) + 1

        # Bound sigma at 0.1
        if perturbation_vector[i] < 0.1:
            perturbation_vector[i] = 0.1

        # Mutate NN parameters
        child[i] += np.random.normal(0, perturbation_vector[i])

    return child, perturbation_vector


##### Reproduction and Survival #####

# Reproduce with all parents replaced by offspring
def reproduce_generational(pop, probabilities, old_fit):
    pop = list(pop)
    new_pop = []
    new_fit = []

    # Select and replace all the parents with their offspring and update fit scores
    for _ in range(pop_size):
        p1, p2 = select_parents(pop, int(pop_size/2), len(pop), probabilities)

        child, child2 = reproduction(p1, p2)

        new_pop.append(mutate_offspring(child))
        new_pop.append(mutate_offspring(child2))

        if evoman:
            fit, p_life, e_life, gametime = env.play(pcont=child)
            fit2, p_life2, e_life2, gametime2 = env.play(pcont=child2)
            
            # Add the metric being optimized
            if prioritize_life:
                new_fit.append(p_life)
                new_fit.append(p_life2)
            elif prioritize_time:
                new_fit.append(gametime)
                new_fit.append(gametime2)
            else:
                new_fit.append(fit)
                new_fit.append(fit2)

    # Assign the fitness score list to the right performance metric
    if prioritize_life:
        probabilities = relative_prob(new_fit)
    elif prioritize_time:
        new_fit = normalize(new_fit)
        probabilities = relative_prob(new_fit)
    else:
        new_fit_norm = normalize(new_fit)
        probabilities = relative_prob(new_fit_norm)

    new_pop = np.array(new_pop)
    new_fit = np.array(new_fit)
    
    # Copy the top performers or let them be replaced
    if type(elitism) == int and (midpoint == True or half == False):
        selected = np.random.choice(pop_size*2, pop_size-elitism, p=probabilities, replace=False)
        new_pop = new_pop[selected]
        new_fit = new_fit[selected]
        new_pop = np.concatenate((new_pop, pop[-elitism:]))
        new_fit = np.concatenate((new_fit, old_fit[-elitism:]))
    else:
        selected = np.random.choice(pop_size*2, pop_size, p=probabilities, replace=False)
        new_pop = new_pop[selected]
        new_fit = new_fit[selected]

    return new_pop, new_fit

# Replace only a small part of the population with each generation
def reproduce_steady_pop(pop, probabilities, old_fit):
    pop = list(pop)
    new_pop = []
    new_fit = []
    next_gen = int(pop_size/10)

    for _ in range(next_gen):
        p1, p2 = select_parents(pop, int(pop_size/2), len(pop), probabilities)

        child, child2 = reproduction(p1, p2)
        
        new_pop.append(mutate_offspring(child))
        new_pop.append(mutate_offspring(child2))

        if evoman:
            fit, p_life, e_life, gametime = env.play(pcont=child)
            fit2, p_life2, e_life2, gametime2 = env.play(pcont=child2)

            # Add the metric being optimized
            if prioritize_life:
                new_fit.append(p_life)
                new_fit.append(p_life2)
            elif prioritize_time:
                new_fit.append(gametime)
                new_fit.append(gametime2)
            else:
                new_fit.append(fit)
                new_fit.append(fit2)

        if not prioritize_life:
            new_fit_norm = evo_normalize(new_fit)
            probabilities = relative_prob(new_fit_norm)

    selected = np.random.choice(next_gen*2, next_gen, p=probabilities,
                                replace=False)
    
    new_pop = np.array(new_pop)
    new_fit = np.array(new_fit)
    new_pop = new_pop[selected]
    new_fit = new_fit[selected]
    new_pop = np.concatenate((new_pop, pop[-(pop_size-next_gen):]))
    new_fit = np.concatenate((new_fit, old_fit[-(pop_size-next_gen):]))

    return new_pop, new_fit

# Create a large new generation and keep the top performers only
def reproduce_comma_strategy(pop, probabilities, old_fit):
    pop = list(pop)
    new_pop = []
    new_fit = []
    next_gen = pop_size * 3

    # Populate the new generation
    for _ in range(next_gen):
        p1, p2 = select_parents(pop, int(pop_size / 2), len(pop), probabilities)

        child = reproduction(p1, p2, two_child=False)
        new_pop.append(mutate_offspring(child))

        if evoman:
            fit, p_life, e_life, gametime = env.play(pcont=new_pop[-1])

            # Add the metric being optimized
            if prioritize_life:
                new_fit.append(p_life)
            elif prioritize_time:
                new_fit.append(gametime)
            else:
                new_fit.append(fit)

    new_pop, new_fit = sort(new_pop, new_fit)
    new_pop = np.array(new_pop)
    new_fit = np.array(new_fit)

    # Handle elitism parameters is any
    if type(elitism) == int and (midpoint or not half):
        new_pop = new_pop[-(pop_size - elitism):]
        new_fit = new_fit[-(pop_size - elitism):]
        new_pop = np.concatenate((new_pop, [pop[-elitism]]))
        new_fit = np.concatenate((new_fit, [old_fit[-elitism]]))
    else:
        new_pop = new_pop[-pop_size:]
        new_fit = new_fit[-pop_size:]

    return new_pop, new_fit

# Reproduce in the EP setup where individual parents are mutated
def reproduce_EP(pop, perturbation_vectors):
    pop = np.array(pop)
    perturbation_vectors = np.array(perturbation_vectors)
    new_pop = []

    for i in range(pop_size):
        new_pop.append(mutate_offspring_EP(pop[i], perturbation_vectors[i]))

    new_pop = np.array(new_pop)
    pop = np.vstack((pop,new_pop))

    scores, maxi, ind, lives, gametimes = test_population(pop)

    if prioritize_life:
        scores = normalize(lives)
    elif prioritize_time:
        scores = normalize(gametimes)
    else:
        scores = evo_normalize(scores)
        
    probabilities = relative_prob(scores)

    # Survival based probabilistically on relative fitness
    selected = np.random.choice(pop_size*2, pop_size, p=probabilities, replace=False)
    pop = pop[selected]
    scores = scores[selected]

    return pop, perturbation_vectors, scores

# Reproduce with the DE strategy
def reproduce_differential_evolution(pop):
    pop = np.array(pop)
    mutation_vectors = np.zeros((pop_size, num_vars))
    advantage = 0
    fit_scores = []

    for i in range(pop_size):

        # Assign perturbation vector
        choices = [item for j, item in enumerate(pop) if j != i]
        Ai, Bi, Ci = random.sample(choices, 3)

        mutation_vectors[i] = Ai + scaling_factor * (Bi - Ci)

        # Create child Ui
        for j in range(num_vars):
            if random.random() > 0.5:
                mutation_vectors[i,j] = pop[i][j]

        # Tournament between progenitor and offspring for survival
        if evoman:
            fit, p_life, e_life, gametime = env.play(pcont=pop[i])
            fit2, p_life2, e_life2, gametime2 = env.play(pcont=mutation_vectors[i])

            if prioritize_life:
                if p_life2 > p_life:
                    pop[i] = mutation_vectors[i]
                    fit_scores.append(p_life2)
                    advantage += 1
                else:
                    fit_scores.append(p_life)

            elif prioritize_time:
                if gametime2 > gametime:
                    pop[i] = mutation_vectors[i]
                    fit_scores.append(gametime2)
                    advantage += 1
                else:
                    fit_scores.append(gametime)

            else:
                if fit2 > fit:
                    pop[i] = mutation_vectors[i]
                    fit_scores.append(p_life2)
                    advantage += 1
                else:
                    fit_scores.append(p_life)

    # Tracks effectiveness of mutations
    print(f'{(advantage/pop_size)*100} percent of mutations conferred advantage')

    return pop, fit_scores

# Modify the velocity and positioan of particles in a PSO algorithm
def vector_shift_PSO(pop, velocity_vectors, previous_bests, previous_scores, global_best, best_score):
    pop = np.array(pop)
    velocity_vectors = np.array(velocity_vectors)

    for i in range(pop_size):
        prev_velocity = velocity_vectors[i]

        # Calculate new particle 
        velocity_vectors[i] = (pso_weights[0] * velocity_vectors[i]) + (pso_weights[1] * random.random() * 
                            (previous_bests[i] - pop[i])) + (pso_weights[2] * random.random() * (global_best - pop[i]))
        
        # Update and test new position
        pop[i] = pop[i] + prev_velocity

        for j in range(num_vars):
            if pop[i][j] > 1:
                pop [i][j] = 1
            if pop[i][j] < -1:
                pop[i][j] = -1

        if evoman:
            score, p_life, e_life, gametime = env.play(pcont=pop[i])
            
            if prioritize_life:
                score = p_life
            elif prioritize_time:
                score = gametime
            
        if score > best_score:
            global_best = pop[i]
            best_score = score
        if score > previous_scores[i]:
            previous_bests[i] = pop[i]
            previous_scores[i] = score

    print(f'Average velocity per variable is {np.average(np.abs(velocity_vectors))}')

    return  pop, velocity_vectors, previous_bests, previous_scores, global_best, best_score 

# Reproduce within subgroups of individuals only
def reproduce_by_species(pop, generation, species=None):

    # Speciate based on frequency
    if curve_parents and generation == 0:
        species_count, _, species = speciate_population(threshold, pop)
    elif curve_parents and (generation%speciation_frequency) == 0:
        species_count, _, species = speciate_population(threshold, pop)
    else:
        species_count, _, species = speciate_population(threshold, pop[-pop_size:])
    
    species_max = []
    species_avg = []
    new_pop = []
    norm_avg = []
    count_each_species = []
    probability_sets = []

    # Test each species
    for i in range(species_count):
        scores, maximum, _ = test_population(species[f'species_{i+1}_list'])
        probability_sets.append(relative_prob(scores))
        scores2 = evo_normalize(scores)
        norm_avg.append(np.average(scores2))
        species_max.append(maximum)
        species_avg.append(np.average(scores))

    for k in range(species_count):
        count_each_species.append(len(species[f'species_{k+1}_list']))

    print(f'Species Counts: {count_each_species}')
    print(f'Species Maximums: {np.round(species_max,2)}')
    print(f'Species Averages: {np.round(species_avg,2)}')

    # Allocate next generation spaces among species
    probabilities = relative_prob(norm_avg)
    ratios = pop_size * probabilities
    ratios = [round(num) for num in ratios]
    approved = np.ones(species_count)
    reallocation = 0

    # Sift out species with too few to reproduce
    for i in range(species_count):

        if count_each_species[i] < 4:
                reallocation += ratios[i]
                approved[i] = 0

    # Renormalize allocations
    probabilities = probabilities * approved
    probabilities = probabilities / probabilities.sum()
    ratios1 = ratios * approved
    ratios2 = reallocation * probabilities + ratios1
    ratios3 = [round(num) for num in ratios2]

    old_pop_ratios = np.array(count_each_species) * approved
    old_pop_ratios = (old_pop_ratios / old_pop_ratios.sum()) * pop_size
    old_pop_ratios = [round(num) for num in old_pop_ratios]
    ratios = (np.array(ratios3) + np.array(old_pop_ratios)) / 2
    ratios = [round(num) for num in ratios]

    print(f'Old allocation: {old_pop_ratios}')
    print(f'After smoothing, species are now allocated: {ratios}')
    print(f'Totaling: {sum(ratios)}')

    species2 = {}

    for i in range(species_count):

        # Initialize the new generation for each species
        species2[f'species_{i+1}_list'] = []
        
        if count_each_species[i] >= 4:

            for _ in range(ratios[i]):

                # Selection, reproduction, and mutation
                if curve_parents:
                    p1, p2 = select_parents(species[f'species_{i+1}_list'], probability_sets[i])
                    child = reproduction(p1, p2, two_child=False)
                else:
                    p1, p2 = random.sample(species[f'species_{i+1}_list'], 2)
                    child, child2 = reproduction(p1, p2)
                
                child = mutate_offspring(child)
                if not curve_parents:
                    child2 = mutate_offspring(child2)

                species2[f'species_{i+1}_list'].append(child)
                new_pop.append(child)
                if not curve_parents:
                    species2[f'species_{i+1}_list'].append(child2)  
                    new_pop.append(child2)

    return new_pop, species2


##### Speciation #####

# Change the speciation threshold to keep in desired range
def dynamic_speciation(species_count):
    if species_count >= 10:
        globals() ['threshold'] += 0.025
    if species_count < 5:
        globals() ['threshold'] -= 0.025

# Separate a generation into species based on threshold
def speciate_population(threshold, pop):
    pop = np.flip(pop)
    representatives = [random.choice(pop)]
    species_count = 1
    species = {}
    species[f'species_{species_count}_list'] = []

    for individual in pop:
        found = False
        count = 0

        while found == False:

            # Check for individuals whose normalized average difference in parameters is below the threshold
            difference = np.average(np.abs(individual-representatives[count])/2)

            if difference < threshold:
                species[f'species_{count+1}_list'].append(individual)
                found = True

            count += 1

            # Add a new species if the current individual cannot be classified
            if count == species_count:
                species_count += 1
                representatives.append(individual)
                species[f'species_{species_count}_list'] = [individual]
                found = True

    # Modify the threshold for species difference to cultivate diversity
    if dynamic_speciation:
        dynamic_speciation(species_count)

    print(f'Thereshold: {np.round((threshold), 3)}')

    return species_count, representatives, species


##### Doomsday #####

# Kill off a quarter of the population and replace them with highly mutated copies of the top 5 individuals
def reseed_event(pop, fit_scores):
    print("RESEED")
    indices = sorted(range(len(fit_scores)), key=lambda x: fit_scores[x], reverse=True)[:5]
    indices2 = sorted(range(len(fit_scores)), key=lambda x: fit_scores[x], reverse=True)[int(-len(pop) / 4):]
    
    for count, unit in enumerate(pop):

        if count in indices2:
            parent = random.randint(0,4)
            geno_fidelity = random.random()

            for i in range(len(unit)):

                # Copy an allele or create a new random one
                if random.random() > geno_fidelity:
                    unit[i] = random.uniform(-1,1)
                else:
                    unit[i] = pop[indices[parent]][i]

    return pop


##### Evolutionary Algorithm for Neural Network Parameters #####

# Set up an envolutionary learning process based on the style of EA and the number of generations
def training_run(mutagenic_temperature, mutation_intensity, mutation_reset, discrete, crossover_line, 
                 individual_cross, reproduce_steady, comma_strategy, reseed_cycle, elitism, half, curve_parents, 
                 speciate, threshold, speciation_frequency, prioritize_life, prioritize_time, objective_switchpoint, 
                 generalist, evolutionary_programming, differential_evolution, scaling_factor, 
                 particle_swarm_optimization, pop):
    
    globals() ['particle_swarm_optimization'] = particle_swarm_optimization
    globals() ['evolutionary_programming'] = evolutionary_programming
    globals() ['differential_evolution'] = differential_evolution
    globals() ['mutagenic_temperature'] = mutagenic_temperature
    globals() ['objecive_switchpoint'] = objective_switchpoint
    globals() ['speciation_frequency'] = speciation_frequency
    globals() ['mutation_intensity'] = mutation_intensity
    globals() ['reproduce_steady'] = reproduce_steady
    globals() ['individual_cross'] = individual_cross
    globals() ['prioritize_life'] = prioritize_life
    globals() ['prioritize_time'] = prioritize_time
    globals() ['scaling_factor'] = scaling_factor
    globals() ['crossover_line'] = crossover_line
    globals() ['mutation_reset'] = mutation_reset
    globals() ['comma_strategy'] = comma_strategy
    globals() ['curve_parents'] = curve_parents
    globals() ['reseed_cycle'] = reseed_cycle
    globals() ['generalist'] = generalist
    globals() ['threshold'] = threshold
    globals() ['discrete'] = discrete
    globals() ['speciate'] = speciate
    globals() ['elitism'] = elitism
    globals() ['half'] = half
    
    mean_stat = [0]
    st_devs = [0]
    upper_avg_stat = [0]
    performance = [0]
    upper_avg = [0]  
    best = 0

    # Initialize the population in a manner fitting the EA approach
    if len(pop) == 0 and not evolutionary_programming and not particle_swarm_optimization:
        pop = initialize_population(pop_size, num_vars)
    elif evolutionary_programming:
        pop, perturbation_vectors = initialize_population_EP(pop_size, num_vars)
    elif particle_swarm_optimization:
        if len(pop) == 0:
            pop = initialize_population(pop_size, num_vars)
        velocity_vectors = initialize_population(pop_size, num_vars)
        previous_bests = np.zeros((pop_size, num_vars))
        previous_scores = np.zeros(pop_size)
        global_best = np.zeros((1, num_vars))
        best_score = 0

    # Loop through the selection and reproduction processes
    for g in range(generations):

        if evoman:

            if objective_switchpoint != False and objective_switchpoint == g:
                print('switch')
                globals() ['prioritize_life'] = False
                globals() ['prioritize_time'] = False

            if g == 0:
                # Run simulation of the game with each individual 
                fit_scores, maxi, ind, lives, gametimes = test_population(pop)
                
                if prioritize_life:
                    fit_scores = lives
                elif prioritize_time:
                    fit_scores = gametimes

            maxi = max(fit_scores)
            ind = list(fit_scores).index(maxi)

        # Keep track of the best set of parameters so far
        if np.round(maxi, decimals=2) > max(performance) or (type(objective_switchpoint) == int and np.round(maxi, decimals=2) > max(performance[objective_switchpoint:])):
            best = pop[ind]

        # Sort the population by their scores
        pop, fit_scores = sort(pop, fit_scores)

        # Store statistics about this generation
        performance.append(np.round(maxi, decimals=2))
        
        upper_avg = np.mean(fit_scores[-int(pop_size / 10):])
        st_dev = np.std(fit_scores)

        upper_avg_stat.append(np.round(upper_avg, decimals=2))
        mean_stat.append(np.round(np.mean(fit_scores), decimals=2))
        st_devs.append(st_dev)

        if g == int(generations / 2):
            globals() ['midpoint'] = True

        if reseed_cycle and g % 20 == 9:
            pop = reseed_event(pop, fit_scores)

        # Set up probabilities based on relative fitness
        if prioritize_life:
            fit_scores_norm = fit_scores
        elif prioritize_time:
            fit_scores_norm = normalize(np.array(fit_scores))
        else:
            fit_scores_norm = evo_normalize(fit_scores)

        probabilities = relative_prob(fit_scores_norm)
        
        # Run the chosen type of reproduction
        if reproduce_steady: 
            pop, fit_scores = reproduce_steady_pop(pop, probabilities, fit_scores)
        elif comma_strategy: 
            pop, fit_scores = reproduce_comma_strategy(pop, probabilities, fit_scores)
        elif evolutionary_programming: 
            pop, perturbation_vectors, fit_scores = reproduce_EP(pop, perturbation_vectors)
        elif differential_evolution: 
            pop, fit_scores = reproduce_differential_evolution(pop)
        elif particle_swarm_optimization: 
            pop, velocity_vectors, previous_bests, fit_scores, global_best, best_score = vector_shift_PSO(pop, velocity_vectors, previous_bests, 
                                                                                                                previous_scores, global_best, best_score)
        elif speciate and g != 0: 
            pop, species = reproduce_by_species(pop, g, species)
        elif speciate: 
            pop, species = reproduce_by_species(pop, g)
        else: 
            pop, fit_scores = reproduce_generational(pop, probabilities, fit_scores)

        if g%5 == 0:
            print(f"Generation {g+1} top 10% avg: {np.round(upper_avg, decimals=2)}")

        # Stop the experiment if performance has crossed threshold
        if upper_avg >= 97 and not prioritize_time:
            globals() ['early_stop'] = True
            print(performance)
            print(max(performance))
            return best, mean_stat, performance, upper_avg_stat, st_devs, pop

    print(performance)
    print(max(performance))
    
    return best, mean_stat, performance, upper_avg_stat, st_devs, pop


##### Evoman EA Training #####

# Train a specilist or generalist agent through the EA framework against the selected bosses all experiment parameters 
# are specified as parameters
def evoman_train_set(string="V0", mutagenic_temperature=0.2, mutation_intensity=1, 
              mutation_reset=False, discrete=False, crossover_line=False, individual_cross=False, 
              reproduce_steady=False, comma_strategy=False, reseed_cycle=False, elitism=False, 
              half=False, curve_parents=False,speciate=False, threshold=False, speciation_frequency=False, 
              prioritize_life=False, prioritize_time=False, objective_switchpoint=False,
              generalist=False, evolutionary_programming=False, differential_evolution=False, 
              scaling_factor=False, particle_swarm_optimization=False, pop=[], enemy_set=[1,2,3,4,5,6,7,8], 
              runs=1, save=True):

    times = {enemy: [] for enemy in enemy_set}
    globals() ['last_boss'] = enemy_set[-1]

    if multiple_mode:
        enemies = [0]
    else:
        enemies = enemy_set
    
    # Iterate through each boss
    for j in enemies:

        # Iterate through each experiment run
        for run in range(0, runs):

            # Set up environment and complete one training run
            if multiple_mode:
                env.enemies = enemy_set
                env.multiplemode = "yes"
            
            start_time = time.perf_counter_ns()

            best, mean_stat, performance, upper_avg_stat, st_dev, pop = training_run(mutagenic_temperature, mutation_intensity, 
                                                                                     mutation_reset, discrete, crossover_line, individual_cross, 
                                                                                     reproduce_steady, comma_strategy, reseed_cycle, elitism, half, 
                                                                                     curve_parents, speciate, threshold, speciation_frequency, 
                                                                                     prioritize_life, prioritize_time, objective_switchpoint, 
                                                                                     generalist, evolutionary_programming, differential_evolution,
                                                                                     scaling_factor, particle_swarm_optimization, pop)
            # Test the winning parameters
            print(f'Test score is {env.play(pcont=best)}')
            runtime = time.perf_counter_ns() - start_time
            times[enemy_set[1]].append(runtime)
            
            # Save all the important stats in the specified folder
            if save:
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Means.csv", mean_stat, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Peaks.csv", performance, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Upper_Avg.csv", upper_avg_stat, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_St_Dev.csv", st_dev, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Params.csv", best, delimiter=",")

    # Save runtimes for computational comparison
    if save:
        with open(f"{stat_directory}_{string}/{string}_Runtimes.csv", 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['enemy', 'run', 'time'])

            for enemy in times:

                for run in range(0, len(times[enemy])):
                    writer.writerow([enemy, run, times[enemy][run]])

# Test a set of NN parameters from the stored csv file
def evoman_test_params(string, attempts=1, set=[1,2,3,4,5,6,7,8], experiment_count=1, save=False, generalist=False):

    set_of_performances = []
    set_of_life = []
    # Set up the environment params and game statistics
    for j in set:

        # switch off for testing
        if multiple_mode:
            env.multiplemode = "no"

        env.enemies = [j]
        performance = []
        avg_enemy_life = []
        avg_life = []
        avg_time = []

        # Test parameters from each separate experiment
        for run in range(experiment_count):

            scores = []
            life_left = []
            gametimes = []
            enemy_life = []
            win_count = 0

            # Get the right parameters
            if generalist:
                if multiple_mode:
                    best_params = pd.read_csv(f"{stat_directory}_{string}/{string}_{0}_{run}_Params.csv", delimiter=",", header=None)
                else:
                    best_params = pd.read_csv(f"{stat_directory}_{string}/{string}_{last_boss}_{run}_Params.csv", delimiter=",", header=None)
            else:    
                best_params = pd.read_csv(f"{stat_directory}_{string}/{string}_{j}_{run}_Params.csv", delimiter=",", header=None)
            
            # Sheds sigma values in cases with variation coded into the genetics
            params = best_params.iloc[:num_vars,0]

            # Complete the number of runs for the boss and stores the statitics
            for _ in range(attempts):   
                
                fit, p_life, e_life, gametime = env.play(pcont=np.array(params))
                
                if e_life == 0:
                    win_count += 1

                print(f'Boss {j}, run {np.round(run,2)}, fitness score {np.round(fit,2)}, player life {np.round(p_life,2)}, enemy life {np.round(e_life,2)}, runtime {gametime}')
                scores.append(fit)
                life_left.append(p_life)
                gametimes.append(gametime)
                enemy_life.append(e_life)

            performance.append(np.mean(np.array(scores)))
            avg_enemy_life.append(np.mean(np.array(enemy_life)))
            avg_life.append(np.mean(np.array(life_left)))
            avg_time.append(np.mean(np.array(gametimes)))

            # Save stats from individual experiments
            if save:
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Fit_Scores.csv", scores, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Enemy_Life.csv", enemy_life, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Player_Life.csv", life_left, delimiter=",")
                np.savetxt(f"{stat_directory}_{string}/{string}_{j}_{run}_Gametime.csv", gametimes, delimiter=",")

        # Save stats from averages of experiments
        if save:
            np.savetxt(f"{stat_directory}_{string}/{string}_{j}_avg_Fit_Scores.csv", performance, delimiter=",")
            np.savetxt(f"{stat_directory}_{string}/{string}_{j}_avg_Enemy_Life.csv", avg_enemy_life, delimiter=",")
            np.savetxt(f"{stat_directory}_{string}/{string}_{j}_avg_Player_Life.csv", avg_life, delimiter=",")
            np.savetxt(f"{stat_directory}_{string}/{string}_{j}_avg_Gametime.csv", avg_time, delimiter=",")

        set_of_performances.append(np.round(np.mean(performance),2))
        set_of_life.append(np.round(np.mean(avg_life),2))

    return set_of_performances, set_of_life

# Run the grid search algorithm
if __name__ == '__main__':
    
    performances = []
    avg_lives = []
    combinations = [list(comb) for comb in itertools.combinations(range(1,9), 4)]

    # Initialize the game environment
    env = Environment(experiment_name=experiment_name,
                            playermode="ai",
                            enemies=[1],
                            player_controller=player_controller(n_hidden_neurons),
                            speed="fastest",
                            enemymode="static",
                            level=2,
                            visuals=False)
    

    # Test all combinations of 4
    for group in combinations:
        print(f'Combination: {group}')
        filename = f'GENERALIST_GRID_{group}'

        if not os.path.exists(f'{stat_directory}_{filename}'):
            os.makedirs(f'{stat_directory}_{filename}')

        # Train New GAs
        evoman_train_set(filename, mutagenic_temperature, mutation_intensity, mutation_reset, discrete, crossover_line, 
                            individual_cross, reproduce_steady, comma_strategy, reseed_cycle, elitism, half, curve_parents,
                            speciate, threshold, speciation_frequency, prioritize_life, prioritize_time, objective_switchpoint, 
                            generalist, evolutionary_programming, differential_evolution, scaling_factor, particle_swarm_optimization, 
                            pop, group, runs, save)

        # Test the best parameters
        performance, avg_life = evoman_test_params(filename, 1, set=[1,2,3,4,5,6,7,8], experiment_count=1, generalist=generalist, save=True)

        performances.append(performance)
        avg_lives.append(avg_life)

    for i in range(len(performances)):
        print(f'Combination {combinations[i]}')
        print(f'Fit Scores: {performances[i]}')
        print(f'Fit Scores avg: {np.mean(performances[i])}')
        print(f'Player Life: {avg_lives[i]}')
        print(f'Player Life avg: {np.mean(avg_lives[i])}')
    
    if save:
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Fit_Scores_4.csv", performances, delimiter=",")
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Player_Life_4.csv", avg_lives, delimiter=",")
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Combo_Key_4.csv", combinations, delimiter=",")

    performances2 = []
    avg_lives2 = []
    combinations2 = [list(comb) for comb in itertools.combinations(range(1,9), 3)]

    # Test all combinations of 3
    for group in combinations:
        print(f'Combination: {group}')
        filename = f'GENERALIST_GRID_{group}'

        # Train New GAs
        evoman_train_set(filename, mutagenic_temperature, mutation_intensity, mutation_reset, discrete, crossover_line, 
                            individual_cross, reproduce_steady, comma_strategy, reseed_cycle, elitism, half, curve_parents,
                            speciate, threshold, speciation_frequency, prioritize_life, prioritize_time, objective_switchpoint, 
                            generalist, evolutionary_programming, differential_evolution, scaling_factor, particle_swarm_optimization, 
                            pop, group, runs, save)

        # Test the best parameters
        performance, avg_life = evoman_test_params(filename, 1, set=[1,2,3,4,5,6,7,8], experiment_count=1, generalist=generalist, save=True)

        performances.append(performance)
        avg_lives.append(avg_life)

    for i in range(len(performances)):
        print(f'Combination {combinations[i]}')
        print(f'Fit Scores: {performances[i]}')
        print(f'Fit Scores avg: {np.mean(performances[i])}')
        print(f'Player Life: {avg_lives[i]}')
        print(f'Player Life avg: {np.mean(avg_lives[i])}')
    
    if save:
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Fit_Scores_3.csv", performances, delimiter=",")
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Player_Life_3.csv", avg_lives, delimiter=",")
        np.savetxt(f"{stat_directory}_{filename}/GridSearch_Combo_Key_3.csv", combinations, delimiter=",")

