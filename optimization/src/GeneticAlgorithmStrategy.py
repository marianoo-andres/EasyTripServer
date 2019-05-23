import time

from optimization.src.Strategy import Strategy
from optimization.src.ga.GeneticAlgorithm import GeneticAlgorithm


class GeneticAlgorithmStrategy(Strategy):
    def __init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                 max_execution_time):
        Strategy.__init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                          max_execution_time)

        self.genetic_algorithm = GeneticAlgorithm(origin_city, possible_trip_cities,
                                                  required_cities,
                                                  max_trip_time, population_size=100,
                                                  mutation_probability=0,
                                                  percentage_random_individuals=0.25)
        self.best_solutions = []

    def solve(self):
        if self.should_print_stats():
            self.print_stats()
        while not self.max_execution_time_reached():
            self.current_iteration = self.genetic_algorithm.current_generation
            self.genetic_algorithm.iterate()

            if self.should_print_stats():
                self.print_stats()

        self.best_solutions = [self.genetic_algorithm.best_individual.solution]
        self.improve_solutions()
        return self.best_solutions[0]

    def improve_solutions(self):
        for best_solution in self.best_solutions:
            self.improve_solution(best_solution)

    def print_stats(self):
        print(
            "Time: {}/{}".format(time.time() - self.start_execution_time, self.max_execution_time))
        print("Generation: {}".format(self.current_iteration))
        print("Generations without improvement: {}".format(
            self.genetic_algorithm.generations_without_improvement_count))
        if self.genetic_algorithm.best_individual:
            print("Best solution (global)")
            self.genetic_algorithm.best_individual.solution.print()
        print("\n\n")
