import csv
import random

from optimization.src.RatioHeuristicStrategy import RatioHeuristicStrategy
from optimization.src.Solution import Solution
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


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


class Ga:
    def __init__(self, origin_city, possible_cities, required_cities, max_trip_time,
                 mutation_times=2, population_size=100,
                 k_tournament=2, percentage_random_individuals=0.5):

        # Ga Metaheuristic params
        self.mutation_times = mutation_times
        self.population_size = population_size
        self.k_tournament = k_tournament
        self.percentage_random_individuals = percentage_random_individuals

        # Problem params
        self.origin_city = origin_city
        self.possible_cities = possible_cities
        self.required_cities = required_cities
        self.max_trip_time = max_trip_time

        # To optimize repair operation
        self.not_required_possible_cities = [city for city in self.possible_cities if
                                             city not in self.required_cities]
        # Sort cities by value/weight ratio from lower to higher
        self.not_required_possible_cities_asc = sorted(self.not_required_possible_cities,
                                                       key=lambda city: city.value / city.stay_time)
        # Sort cities by value/weight ratio from higher to lower
        self.not_required_possible_cities_desc = sorted(self.not_required_possible_cities,
                                                        key=lambda
                                                            city: city.value / city.stay_time,
                                                        reverse=True)
        # State
        self.individuals = []
        self.init_population()
        self.best_individual = None
        self.generations_without_improvement_count = 0
        self.current_generation = 0

        # Extra
        self.logger = Logger("ga_log.txt")

    def create_random_individual(self):
        cities = []
        cities += self.required_cities
        random.shuffle(self.not_required_possible_cities)
        for random_city in self.not_required_possible_cities:
            if random_city not in cities:
                backup = list(cities)
                cities.append(random_city)
                solution = Solution(self.origin_city, cities, self.required_cities,
                                    self.max_trip_time)
                if not solution.is_valid_knapsack_time():
                    cities = backup
                    continue

                optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, cities)
                cities = optimizer.optimize()
                solution.cities = cities
                if not solution.is_valid_total_trip_time():
                    cities = backup
                    continue

        solution = Solution(self.origin_city, cities, self.required_cities, self.max_trip_time)
        optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, cities)
        solution.cities = optimizer.optimize()
        return solution

    def init_population(self):
        strategy = RatioHeuristicStrategy(self.origin_city, self.possible_cities,
                                          self.required_cities, self.max_trip_time, 9999)
        solution = strategy.solve()
        self.individuals.append(solution)
        for x in range(self.population_size - 1):
            self.individuals.append(self.create_random_individual())

    def iterate(self):
        self.current_generation += 1
        child_exist_in_population = True
        while child_exist_in_population:
            # Select parents for crossover
            parent1 = self.select_parent()
            parent2 = self.select_parent()

            # Do the crossover and get a child
            child = self.crossover(parent1, parent2)

            # Mutate the child
            self.mutate(child)

            # Apply repair to make the child a feasible solution
            self.repair(child)

            # Recompute the fitness so that it reflects the
            # correct fitness after all transformations
            child.update_fitness()

            # We want a new child solution not present in the population of individuals
            if child not in self.individuals:
                child_exist_in_population = False

        # Add child to population and remove the worst individual
        self.individuals.append(child)
        self.individuals.sort(key=lambda s: s.fitness, reverse=True)
        self.individuals.pop()

        # Inject randomness
        self.inject_random_inviduals()

        # Update best individual
        best_in_gen = self.individuals[0]
        if self.best_individual is None:
            self.best_individual = best_in_gen
            self.generations_without_improvement_count = 0
        elif best_in_gen == self.best_individual:
            self.generations_without_improvement_count += 1
        else:
            self.best_individual = best_in_gen
            self.generations_without_improvement_count = 0

        self.logger.log(generation=self.current_generation,
                        generations_without_improvement=self.generations_without_improvement_count,
                        fitness_best_individual_in_generation=best_in_gen.fitness,
                        fitness_best_individual_global=self.best_individual.fitness,
                        average_fitness_in_generation=self.compute_average_fitness())

    def select_parent(self):
        """Select one individual as parent for crossover via k tournament selection"""
        tournament_individuals = []
        for _ in range(self.k_tournament):
            random_individual = self.individuals[random.randint(0, len(self.individuals) - 1)]
            tournament_individuals.append(random_individual)
        tournament_individuals.sort(key=lambda s: s.fitness, reverse=True)
        return tournament_individuals[0]

    def crossover(self, parent1, parent2):
        child_solution_cities = []
        # Add required cities
        child_solution_cities += self.required_cities
        # Add cities present in both parents
        for city_parent_1 in parent1.cities:
            if city_parent_1 in parent2.cities:
                if city_parent_1 not in child_solution_cities:
                    child_solution_cities.append(city_parent_1)

        # Get random sample of cities from parent 1 and add them to child if not already present
        parent_solution_cities = []
        if len(parent1.cities) > 0:
            parent_solution_cities = random.sample(parent1.cities,
                                                   random.randint(1, len(parent1.cities)))
            random.shuffle(parent_solution_cities)
        for parent_solution_city in parent_solution_cities:
            if parent_solution_city in child_solution_cities:
                continue
            child_solution_cities.append(parent_solution_city)

        # Get random sample of cities from parent 2 and add them to child if not already present
        parent_solution_cities = []
        if len(parent2.cities) > 0:
            parent_solution_cities = random.sample(parent2.cities,
                                                   random.randint(1, len(parent2.cities)))
            random.shuffle(parent_solution_cities)
        for parent_solution_city in parent_solution_cities:
            if parent_solution_city in child_solution_cities:
                continue
            child_solution_cities.append(parent_solution_city)

        # Get child solution
        child_solution = Solution(self.origin_city, child_solution_cities, self.required_cities,
                                  self.max_trip_time)
        return child_solution

    def mutate(self, solution):
        for x in range(self.mutation_times):
            # Select a random city of the possible ones that is not required
            not_required_cities = [city for city in self.possible_cities if
                                   city not in self.required_cities]
            random.shuffle(not_required_cities)
            random_city = not_required_cities[0]

            if random_city not in solution.cities:
                # Add the city if not present
                solution.cities.append(random_city)
            else:
                # Delete the city if already present in solution
                solution.cities.pop(solution.cities.index(random_city))

    def repair(self, solution):

        # If already valid return
        if solution.is_valid_total_trip_time():
            return

        # Delete process
        for city_to_delete in self.not_required_possible_cities_asc:
            if city_to_delete not in solution.cities:
                continue
            for i, solution_city in enumerate(solution.cities):
                if solution_city == city_to_delete:
                    break
            solution.cities.pop(i)

            if not solution.is_valid_knapsack_time():
                continue

            optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
            solution.cities = optimizer.optimize()

            if not solution.is_valid_total_trip_time():
                continue

            break

        # Add process
        for city_to_add in self.not_required_possible_cities_desc:
            if city_to_add in solution.cities:
                continue
            backup = list(solution.cities)
            solution.cities.append(city_to_add)
            if not solution.is_valid_knapsack_time():
                solution.cities = backup
                continue
            optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
            solution.cities = optimizer.optimize()
            if not solution.is_valid_total_trip_time():
                solution.cities = backup
                continue

    def compute_average_fitness(self):
        total_fitness = 0
        for individual in self.individuals:
            total_fitness += individual.fitness
        return total_fitness / len(self.individuals)

    def inject_random_inviduals(self):
        """
        Replaces percetange worst individuals with random ones
        """
        number_to_create = int(self.population_size * self.percentage_random_individuals)
        random_individuals = []
        for x in range(number_to_create):
            random_individuals.append(self.create_random_individual())
        index_from = self.population_size - number_to_create
        # Replace worst individuals with the random ones
        self.individuals[index_from:] = random_individuals
        # Maintain population size
        self.individuals = self.individuals[0:self.population_size]
