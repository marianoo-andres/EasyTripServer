class Optimizer:
    def __init__(self, strategy):
        self.strategy = strategy
        self.best_solution = None
        self.good_solutions = None

    def optimize(self):
        # Get solution
        # best_solution, good_solutions = self.strategy.solve()
        best_solution = self.strategy.solve()

        # Set solution
        self.best_solution = best_solution
        # self.good_solutions = good_solutions
        return self._solution_to_dic(self.best_solution)

    def _solution_to_dic(self, solution):
        solution_dic = {}
        solution_dic["origin_city"] = solution.origin_city.name
        solution_dic["cities"] = [city.name for city in solution.cities]
        solution_dic["cities"].insert(0, solution.origin_city.name)
        solution_dic["cities"].append(solution.origin_city.name)
        solution_dic["required_cities"] = [city.name for city in solution.required_cities]
        solution_dic["max_trip_time"] = solution.max_trip_time
        solution_dic["fitness"] = solution.calculate_fitness()
        solution_dic["total_stay_time"] = solution.get_total_stay_time()
        solution_dic["total_travel_time"] = solution.get_total_travel_time()
        solution_dic["total_trip_time"] = solution.get_total_trip_time()
        solution_dic["valid"] = solution.is_valid()
        return solution_dic
