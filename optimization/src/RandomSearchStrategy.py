import random

from optimization.src.Solution import Solution
from optimization.src.Strategy import Strategy
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


class RandomSearchStrategy(Strategy):
    def __init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                 max_execution_time):
        Strategy.__init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                          max_execution_time)

    def get_final_solution(self):
        best_solution_fitness = 0
        best_solution_trip_time = 0
        if self.should_print_stats():
            self.print_stats()
        while not self.max_execution_time_reached():
            if self.should_print_stats():
                self.print_stats()

            solution = self.get_valid_solution()
            if solution.fitness > best_solution_fitness:
                best_solution = solution
                self.set_best_solution(best_solution)
                best_solution_fitness = solution.fitness
                best_solution_trip_time = solution.get_total_travel_time()
            elif solution.fitness == best_solution_fitness:
                if solution.get_total_travel_time() < best_solution_trip_time:
                    best_solution = solution
                    self.set_best_solution(best_solution)
                    best_solution_fitness = solution.fitness
                    best_solution_trip_time = solution.get_total_travel_time()
            self.current_iteration += 1
            # self.add_good_solution(solution)
        self.improve_solutions()
        # return self.best_solution, self.good_solutions
        return self.best_solution

    def solve(self):
        solution = self.get_final_solution()
        return solution

    def get_valid_solution(self):
        while True:
            cities = random.sample(self.possible_trip_cities,
                                   random.randint(1, len(self.possible_trip_cities)))
            random.shuffle(cities)
            solution = Solution(self.origin_city, cities, self.required_cities, self.max_trip_time)

            if not solution.is_valid_knapsack_time() or not solution.is_valid_required_city():
                continue

            optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
            solution.cities = optimizer.optimize()

            if solution.is_valid_total_trip_time():
                return solution

    def print_stats(self):
        print("RANDOM SEARCH STRATEGY")
        Strategy.print_stats(self)
