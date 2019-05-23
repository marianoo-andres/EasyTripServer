from itertools import combinations

from optimization.src.Solution import Solution
from optimization.src.Strategy import Strategy
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


class BruteForceStrategy(Strategy):
    def __init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                 max_execution_time):
        Strategy.__init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                          max_execution_time)

    def solve(self):
        best_solution_fitness = 0
        best_solution_trip_time = 0
        if self.should_print_stats():
            self.print_stats()
        for x in range(1, len(self.possible_trip_cities) + 1):
            for cities in combinations(self.possible_trip_cities, x):
                self.current_iteration += 1
                if self.should_print_stats():
                    self.print_stats()

                solution = Solution(self.origin_city, cities, self.required_cities,
                                    self.max_trip_time)
                if not solution.is_valid_knapsack_time() or not solution.is_valid_required_city():
                    continue

                # Apply construction heuristic
                optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
                solution.cities = optimizer.optimize()

                if not solution.is_valid_total_trip_time():
                    continue

                if solution.fitness > best_solution_fitness:
                    # Update best_solution as first objective fitness is better
                    best_solution = solution
                    self.set_best_solution(best_solution)
                    best_solution_fitness = solution.fitness
                    best_solution_trip_time = solution.get_total_travel_time()
                elif solution.fitness == best_solution_fitness:
                    if solution.get_total_travel_time() < best_solution_trip_time:
                        # Update best_solution as first objective fitness is same but
                        # second objective travel time is better
                        best_solution = solution
                        self.set_best_solution(best_solution)
                        best_solution_fitness = solution.fitness
                        best_solution_trip_time = solution.get_total_travel_time()
                # self.add_good_solution(solution)
        self.improve_solutions()
        # return self.best_solution, self.good_solutions
        return self.best_solution

    def print_stats(self):
        print("BRUTE FORCE STRATEGY")
        Strategy.print_stats(self)
