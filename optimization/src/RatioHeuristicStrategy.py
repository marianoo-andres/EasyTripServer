from optimization.src.Solution import Solution
from optimization.src.Strategy import Strategy
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


class RatioHeuristicStrategy(Strategy):
    def __init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                 max_execution_time):
        Strategy.__init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                          max_execution_time)

    def solve(self):
        # Add all required cities
        solution = Solution(self.origin_city, list(self.required_cities), self.required_cities,
                            self.max_trip_time)
        solution.update_fitness()
        if not solution.is_valid():
            raise Exception()

        # Compute ratios
        ratios = []
        for city in self.possible_trip_cities:
            if city in self.required_cities:
                continue
            ratios.append([city, city.value / city.stay_time])
        ratios.sort(reverse=True, key=lambda x: x[1])

        # Add city until knapsack is full
        for r in ratios:
            city = r[0]
            backup = list(solution.cities)
            solution.cities.append(city)
            solution.update_fitness()
            tsp_optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
            solution.cities = tsp_optimizer.optimize()
            if not solution.is_valid_total_trip_time():
                solution.cities = backup
                solution.update_fitness()
                break
        self.improve_solution(solution)
        return solution
