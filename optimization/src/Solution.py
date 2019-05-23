class Solution:
    def __init__(self, origin_city, cities, required_cities, max_trip_time):

        # Contains the list of cities to be visited (the origin_city is not present here)
        # The trip is given by the order of the cities in this list
        self.cities = cities

        # The origin of the trip
        self.origin_city = origin_city

        # Required cities to visit
        self.required_cities = required_cities

        # Max available time in days to complete the trip
        self.max_trip_time = max_trip_time

        # How good the solution is
        self.fitness = self.calculate_fitness()

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if len(self.cities) != len(other.cities):
            return False
        for city in self.cities:
            if city not in other.cities:
                return False
        return True

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        if len(self.cities) != len(other.cities):
            return True
        for city in self.cities:
            if city not in other.cities:
                return True
        return False

    def print(self):
        print("------RECORRIDO------")
        print(self.origin_city.name)
        for city in self.cities:
            print(city.name)
        print(self.origin_city.name)
        print("---------------------")
        print()
        print("VALOR TOTAL: {}".format(self.fitness))
        print("TIEMPO ESTADIA TOTAL: {}".format(self.get_total_stay_time()))
        print("TIEMPO VIAJE TOTAL: {}".format(self.get_total_travel_time()))
        print("TIEMPO TOTAL: {}".format(self.get_total_trip_time()))
        print("SOLUCION VALIDA: {}".format(self.is_valid()))

    def get_total_stay_time(self):
        """"Returns the total time used to stay in the cities"""
        if len(self.cities) == 0:
            return 0

        total_stay_time = 0
        for city in self.cities:
            total_stay_time += city.stay_time
        return total_stay_time

    def get_total_travel_time(self):
        """"Returns the total time used to travel between cities"""
        if len(self.cities) == 0:
            return 0

        total_travel_time = 0
        first_visited_city = self.cities[0]
        last_visited_city = self.cities[len(self.cities) - 1]

        # Travel from origin to first city
        total_travel_time += self.origin_city.get_trip_time(first_visited_city)

        # Do the trip
        for i in range(0, len(self.cities) - 1):
            city_from = self.cities[i]
            city_to = self.cities[i + 1]
            total_travel_time += city_from.get_trip_time(city_to)

        # Travel from last city to origin
        total_travel_time += last_visited_city.get_trip_time(self.origin_city)

        return total_travel_time / 24  # convert to days

    def get_total_trip_time(self):
        """Returns the total time needed to complete the trip"""
        return self.get_total_stay_time() + self.get_total_travel_time()

    def is_valid_knapsack_time(self):
        return self.get_total_stay_time() <= self.max_trip_time

    def is_valid_required_city(self):
        for required_city in self.required_cities:
            if required_city not in self.cities:
                return False
        return True

    def is_valid_total_trip_time(self):
        return self.get_total_trip_time() <= self.max_trip_time

    def is_valid(self):
        """Returns true if is a valid solution for the problem"""
        if not self.is_valid_required_city():
            return False
        if not self.is_valid_knapsack_time():
            return False
        if not self.is_valid_total_trip_time():
            return False
        return True

    def calculate_fitness(self):
        fitness = 0
        if len(self.cities) == 0:
            return fitness
        for city in self.cities:
            fitness += city.value
        return fitness

    def update_fitness(self):
        self.fitness = self.calculate_fitness()

    def get_similarity(self, other_solution):
        similarity = 0
        for city in self.cities:
            if city in other_solution.cities:
                similarity += 1
        return similarity

    def get_distance(self, other_solution):
        distance = 0
        for city in self.cities:
            if city not in other_solution.cities:
                distance += 1
        for city in other_solution.cities:
            if city not in self.cities:
                distance += 1
        return distance

    def clone(self):
        return Solution(self.origin_city, list(self.cities), self.required_cities,
                        self.max_trip_time)
