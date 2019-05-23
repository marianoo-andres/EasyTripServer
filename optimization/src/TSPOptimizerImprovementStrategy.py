from itertools import permutations

from optimization.src.Solution import Solution
from optimization.src.TSPOptimizerStrategy import TSPOptimizerStrategy


class TSPOptimizerImprovementStrategy(TSPOptimizerStrategy):
    def __init__(self, origin_city, cities, window_size):
        TSPOptimizerStrategy.__init__(self, origin_city, cities)
        self.window_size = window_size
        self.visited_cities = {}
        for city in self.cities:
            self.visited_cities[city.name] = False

    # def optimize(self):
    #     """Optimize a cities route and returns it"""
    #     previous_travel_time = self.get_travel_time(self.cities)
    #     best_travel_time = previous_travel_time
    #     while True:
    #         for i in range(0, len(self.cities) - 1):
    #             self.swap(i, i + 1, self.cities)
    #             travel_time = self.get_travel_time(self.cities)
    #             if travel_time < best_travel_time:
    #                 best_travel_time = travel_time
    #             else:
    #                 # Go back
    #                 self.swap(i, i + 1, self.cities)
    #         if not best_travel_time < previous_travel_time:
    #             # Cannot improve anymore
    #             break
    #         else:
    #             previous_travel_time = best_travel_time
    #     return self.cities

    def optimize(self):
        """Optimize a cities route and returns it"""
        previous_travel_time = self.get_travel_time(self.cities)
        best_travel_time = previous_travel_time
        window_size = self.window_size
        if self.window_size > len(self.cities):
            window_size = len(self.cities)
        while True:
            for i in range(0, len(self.cities) - window_size + 1):

                window_start_index = i
                window_end_index = i + window_size - 1
                sub_cities = self.cities[window_start_index:window_end_index + 1]
                for permutation in permutations(sub_cities, window_size):
                    backup = self.cities[window_start_index:window_end_index + 1]
                    self.cities[window_start_index:window_end_index + 1] = list(permutation)
                    travel_time = self.get_travel_time(self.cities)
                    if travel_time < best_travel_time:
                        best_travel_time = travel_time
                    else:
                        # Go back
                        self.cities[window_start_index:window_end_index + 1] = backup
            if not best_travel_time < previous_travel_time:
                # Cannot improve anymore
                break
            else:
                previous_travel_time = best_travel_time
        return self.cities

    def swap(self, i, j, cities):
        temp = cities[i]
        cities[i] = cities[j]
        cities[j] = temp

    def get_travel_time(self, cities):
        solution = Solution(self.origin_city, cities, required_cities=[], max_trip_time=0)
        return solution.get_total_travel_time()
