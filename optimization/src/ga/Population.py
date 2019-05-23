import random

from optimization.src.ga.Individual import Individual


class Population:
    def __init__(self, size, origin_city, possible_cities, required_cities, max_trip_time):
        self.size = size
        # Initialize population
        self.individuals = []
        for i in range(size):
            self.individuals.append(
                self.create_random_individual(origin_city, possible_cities, required_cities,
                                              max_trip_time))

    def delete_bad_individuals(self):
        """Delete the individuals that are not good enough to be present
        in the next generation. Population size needs to remain constant"""
        # Sort individuals from higher to lower fitness
        self.individuals.sort(reverse=True)
        # Keep population size constant deleting bad individuals
        self.individuals = self.individuals[0:self.size]

    def merge_individuals(self, individuals):
        self.individuals += individuals

    def get_best_individual(self):
        self.individuals.sort(reverse=True)
        return self.individuals[0]

    def inject_random_inviduals(self, origin_city, possible_cities, required_cities,
                                max_trip_time, percentage=0.2):
        """
        Replaces percetange worst individuals with random ones
        :param percentage: int representing percentage of population size of
        random individuals to create
        """
        number_to_create = int(self.size * percentage)
        random_individuals = []
        for x in range(number_to_create):
            random_individuals.append(
                self.create_random_individual(origin_city, possible_cities, required_cities,
                                              max_trip_time))
        index_from = self.size - number_to_create
        self.individuals.sort(reverse=True)
        # Replace worst individuals with the random ones
        self.individuals[index_from:] = random_individuals
        # Maintain population size
        self.individuals = self.individuals[0:self.size]

    def total_fitness(self):
        """Returns total fitness of the population"""
        sum = 0
        for individual in self.individuals:
            sum += individual.get_fitness()
        return sum

    def average_fitness(self):
        """Returns average fitness of the population"""
        return self.total_fitness() / len(self.individuals)

    def select_parent(self, k):
        """Select one individual as parent for crossover via k tournament selection"""
        tournament_individuals = []
        for _ in range(k):
            random_individual = self.individuals[random.randint(0, len(self.individuals) - 1)]
            tournament_individuals.append(random_individual)
        tournament_individuals.sort(reverse=True)
        return tournament_individuals[0]

    def create_random_individual(self, origin_city, possible_cities, required_cities,
                                 max_trip_time):
        """Needs to be implemented in child class"""
        return Individual(origin_city, possible_cities, required_cities, max_trip_time)
