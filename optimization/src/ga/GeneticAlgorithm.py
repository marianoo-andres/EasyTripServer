import csv
import random
import time

from optimization.src.ga.Population import Population


class Logger:
    def __init__(self, log_name):
        self.log_name = log_name
        file = open(log_name, 'w', newline='')
        csv_writer = csv.writer(file, delimiter=',')
        title = ["Generation", "GenerationsWithoutImprovement", "FitnessBestIndividualGeneration",
                 "FitnessBestIndividualGlobal",
                 "FitnessAverageGeneration", "GenerationsWithoutImprovement"]
        csv_writer.writerow(title)

    def log(self, generation, generations_without_improvement,
            fitness_best_individual_in_generation, fitness_best_individual_global,
            average_fitness_in_generation):
        file = open(self.log_name, 'a', newline='')
        csv_writer = csv.writer(file, delimiter=',')

        csv_writer.writerow(
            [generation, generations_without_improvement, fitness_best_individual_in_generation,
             fitness_best_individual_global,
             average_fitness_in_generation])
        file.close()


class GeneticAlgorithm:
    def __init__(self, origin_city, possible_cities, required_cities, max_trip_time,
                 mutation_probability=0.2, population_size=100, children_size=None,
                 k_tournament=2, max_execution_time=60, percentage_random_individuals=0.5):
        # Params
        self.percentage_random_individuals = percentage_random_individuals
        self.mutation_probability = mutation_probability
        self.population_size = population_size
        if children_size:
            self.children_size = children_size
        else:
            self.children_size = population_size
        self.k_tournament = k_tournament
        self.max_execution_time = max_execution_time  # In seconds
        self.max_generations_without_improvement = 10 ^ 10
        # State
        self.current_generation = 0
        self.start_time = time.time()
        # Creates a population with random individuals
        self.population = Population(self.population_size, origin_city, possible_cities,
                                     required_cities, max_trip_time)
        self.best_individual = None
        self.best_individuals_max_size = 1
        self.best_individuals = []
        self.generations_without_improvement_count = 0

        self.origin_city = origin_city
        self.possible_cities = possible_cities
        self.required_cities = required_cities
        self.max_trip_time = max_trip_time

        # Extra
        self.logger = Logger("ga_log.txt")

    def update_best_individuals(self, individual):
        individual = individual.clone()
        if len(self.best_individuals) < self.best_individuals_max_size:
            self.best_individuals.append(individual)
            return
        self.best_individuals.append(individual)
        self.best_individuals.sort(reverse=True)
        self.best_individuals.pop(len(self.best_individuals) - 1)
        best_individuals = []
        best_fitness = self.best_individuals[0].get_fitness()
        for i in self.best_individuals:
            if i.get_fitness() == best_fitness:
                best_individuals.append(i)
        self.best_individuals = best_individuals

    def iterate(self):
        """Do an iteration of the algorithm. Each iteration represents one generation"""
        self.current_generation += 1

        # Mutate parents
        # self.__mutate_individuals(self.population.individuals)

        # Create children
        children = self.__create_children()

        # Mutate children
        self.__mutate_individuals(children)

        # Merge parents with children
        # self.population.merge_individuals(children)
        # Replace parents with children
        self.population.individuals = children

        # Inject random individuals
        self.population.inject_random_inviduals(self.origin_city, self.possible_cities,
                                                self.required_cities, self.max_trip_time,
                                                self.percentage_random_individuals)

        # Keep only best individuals for the next generation
        # self.population.delete_bad_individuals()

        # Save generation best individual if is the global best
        generation_best_individual = self.population.get_best_individual()
        if self.best_individual is None:
            self.best_individual = generation_best_individual
        elif generation_best_individual.get_fitness() > self.best_individual.get_fitness():
            self.best_individual = generation_best_individual.clone()
            self.generations_without_improvement_count = 0
        elif generation_best_individual.get_fitness() == self.best_individual.get_fitness():
            if generation_best_individual.solution.get_total_travel_time() < self.best_individual.solution.get_total_travel_time():
                # Update generation_best_individual as first objective fitness is same but
                # second objective travel time is better
                self.best_individual = generation_best_individual.clone()
                self.generations_without_improvement_count = 0
            else:
                self.generations_without_improvement_count += 1
        else:
            self.generations_without_improvement_count += 1

        # Update the list of best individuals
        self.update_best_individuals(generation_best_individual)
        self.logger.log(generation=self.current_generation,
                        generations_without_improvement=self.generations_without_improvement_count,
                        fitness_best_individual_in_generation=generation_best_individual.get_fitness(),
                        fitness_best_individual_global=self.best_individual.get_fitness(),
                        average_fitness_in_generation=self.population.average_fitness())

    def __reached_max_execution_time(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time < self.max_execution_time

    def __create_children(self):
        children = []
        for _ in range(self.children_size):
            done = False
            max_try = 5
            i = 0
            while not done:
                i += 1
                if i > max_try:
                    break
                parent1 = self.population.select_parent(k=self.k_tournament)
                parent2 = self.population.select_parent(k=self.k_tournament)
                child = parent1.crossover(parent2)
                if child not in children:
                    done = True
            children.append(child)
        return children

    def __mutate_individuals(self, individuals):
        for individual in individuals:
            if random.random() < self.mutation_probability:
                individual.mutate()
