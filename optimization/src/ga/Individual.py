import random

from optimization.src.Solution import Solution
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


class Individual:
    def __init__(self, origin_city, possible_cities, required_cities, max_trip_time, solution=None):
        self.possible_cities = possible_cities
        self.origin_city = origin_city
        self.required_cities = required_cities
        self.max_trip_time = max_trip_time

        if solution is None:
            self.solution = self.create_random_solution()
        else:
            self.solution = solution

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.solution == other.solution

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.solution != other.solution

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()

    def get_fitness(self):
        """Return the fitness of the individual"""
        return self.solution.fitness

    def __get_child(self, other):
        child_solution_cities = []
        # Add required cities
        child_solution_cities += self.required_cities
        # Add cities present in both parents
        for city_parent_1 in self.solution.cities:
            if city_parent_1 in other.solution.cities:
                if city_parent_1 not in child_solution_cities:
                    child_solution_cities.append(city_parent_1)

        # Get random sample of cities from parent 1 and add them to child if not already present
        parent_solution_cities = []
        if len(self.solution.cities) > 0:
            parent_solution_cities = random.sample(self.solution.cities,
                                                   random.randint(1, len(self.solution.cities)))
            random.shuffle(parent_solution_cities)
        for parent_solution_city in parent_solution_cities:
            if parent_solution_city in child_solution_cities:
                continue
            child_solution_cities.append(parent_solution_city)

        # Get random sample of cities from parent 2 and add them to child if not already present
        parent_solution_cities = []
        if len(other.solution.cities) > 0:
            parent_solution_cities = random.sample(other.solution.cities,
                                                   random.randint(1, len(other.solution.cities)))
            random.shuffle(parent_solution_cities)
        for parent_solution_city in parent_solution_cities:
            if parent_solution_city in child_solution_cities:
                continue
            child_solution_cities.append(parent_solution_city)

        # Get child solution
        child_solution = Solution(self.origin_city, child_solution_cities, self.required_cities,
                                  self.max_trip_time)

        # Optimize tsp
        optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, child_solution.cities)
        child_solution.cities = optimizer.optimize()

        # Delete random cities until solution is valid
        while not child_solution.is_valid_total_trip_time():
            self.solution_delete_city(child_solution)
            # Optimize the tsp part of the solution
            optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, child_solution.cities)
            child_solution.cities = optimizer.optimize()
        child_solution.update_fitness()
        child_individual = Individual(self.origin_city, self.possible_cities, self.required_cities,
                                      self.max_trip_time, child_solution)
        return child_individual

    def crossover(self, other):
        """Mate with other individual. Return a new child individual"""
        children_to_compete = 5
        children = []
        for x in range(children_to_compete):
            children.append(self.__get_child(other))
        children.sort(reverse=True)
        return children[0]

    def mutate(self):
        """Mutate the individual doing some transformation.
        Adds a city or deletes a city."""
        mutate_add_city_prob = 0.5
        city_added = False
        if random.random() < mutate_add_city_prob:
            city_added = self.mutate_add_city()
        if not city_added:
            self.mutate_delete_city()
        # Mutation done
        self.solution.update_fitness()

    def solution_delete_city(self, solution):
        if len(solution.cities) == 0:
            return
        # Get a copy and shuffle
        solution_cities = list(solution.cities)
        random.shuffle(solution_cities)
        backup = list(solution.cities)
        for solution_city in solution_cities:
            # Delete city
            solution.cities.pop(solution.cities.index(solution_city))
            if not solution.is_valid_required_city():
                # Not required city valid. Roll back and try another one
                solution.cities = list(backup)
                solution.update_fitness()
                continue

            # Delete done
            return

    def mutate_delete_city(self):
        self.solution_delete_city(self.solution)
        # Optimize the tsp. As we are just deleting a city we know the resulting solution
        # it's tsp valid
        optimizer = TSPOptimizerClosestCityStrategy(self.solution.origin_city,
                                                    self.solution.cities)
        self.solution.cities = optimizer.optimize()

    def mutate_add_city(self):
        # Get a copy and shuffle
        possible_cities = list(self.possible_cities)
        random.shuffle(possible_cities)
        backup = list(self.solution.cities)
        for possible_city in possible_cities:
            if possible_city in self.solution.cities:
                # City already in solution. Try another one
                continue
            # City not in solution. See if adding it gives a valid solution
            self.solution.cities.append(possible_city)
            if not self.solution.is_valid_knapsack_time():
                # Not knapsack valid. Roll back and try another one
                self.solution.cities = list(backup)
                self.solution.update_fitness()
                continue
            # Optimize the tsp and see if it's valid
            optimizer = TSPOptimizerClosestCityStrategy(self.solution.origin_city,
                                                        self.solution.cities)
            self.solution.cities = optimizer.optimize()
            if not self.solution.is_valid_total_trip_time():
                # Not tsp valid. Roll back and try another one
                self.solution.cities = list(backup)
                self.solution.update_fitness()
                continue

            # Mutation done.
            return True
        return False

    def create_random_solution(self):
        while True:
            cities = []
            cities += self.required_cities
            sample_size = random.randint(1, len(self.possible_cities))
            random_sample_cities = random.sample(self.possible_cities, sample_size)
            for random_city in random_sample_cities:
                if random_city not in cities:
                    cities.append(random_city)
            random.shuffle(cities)
            solution = Solution(self.origin_city, cities, self.required_cities, self.max_trip_time)

            if not solution.is_valid_knapsack_time() or not solution.is_valid_required_city():
                continue

            optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, solution.cities)
            solution.cities = optimizer.optimize()

            if solution.is_valid_total_trip_time():
                return solution

    def print(self):
        self.solution.print()

    def clone(self):
        return Individual(self.origin_city, self.possible_cities, self.required_cities,
                          self.max_trip_time, self.solution.clone())
