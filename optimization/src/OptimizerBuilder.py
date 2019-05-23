import json

from optimization.src.BruteForceStrategy import BruteForceStrategy
from optimization.src.City import City
from optimization.src.GeneticAlgorithmStrategy import GeneticAlgorithmStrategy
from optimization.src.Optimizer import Optimizer
from optimization.src.RandomSearchStrategy import RandomSearchStrategy
from optimization.src.RatioHeuristicStrategy import RatioHeuristicStrategy


class OptimizerBuilder:
    def __get_required_cities(self, required_city_names, possible_trip_cities):
        required_cities = []
        for required_city_name in required_city_names:
            for possible_city in possible_trip_cities:
                if possible_city.name == required_city_name:
                    required_cities.append(possible_city)

        return required_cities

    def __get_possible_trip_cities(self, origin_city_name, stay_times, values, travel_times):
        possible_trip_cities = []
        for city_name in travel_times:
            if city_name == origin_city_name:
                continue
            city = City(city_name, stay_times[city_name], values[city_name],
                        travel_times[city_name])
            possible_trip_cities.append(city)
        return possible_trip_cities

    def __get_origin_city(self, origin_city_name, stay_times, values, travel_times):
        origin_city_name = origin_city_name
        origin_city = City(origin_city_name, stay_times[origin_city_name],
                           values[origin_city_name],
                           travel_times[origin_city_name])
        return origin_city

    def __build_strategy(self, strategy_type, origin_city, possible_trip_cities, required_cities,
                         max_trip_time, max_execution_time):
        if strategy_type == 'random_search':
            strategy = RandomSearchStrategy(origin_city, possible_trip_cities,
                                            required_cities,
                                            max_trip_time,
                                            max_execution_time)
        elif strategy_type == 'brute_force':
            strategy = BruteForceStrategy(origin_city, possible_trip_cities,
                                          required_cities,
                                          max_trip_time,
                                          max_execution_time)
        elif strategy_type == 'ga':
            strategy = GeneticAlgorithmStrategy(origin_city, possible_trip_cities,
                                                required_cities,
                                                max_trip_time,
                                                max_execution_time)
        elif strategy_type == 'ratio':
            strategy = RatioHeuristicStrategy(origin_city, possible_trip_cities,
                                              required_cities,
                                              max_trip_time,
                                              max_execution_time)
        return strategy

    def __load_params(self, config_path, case_path):
        with open(config_path) as file:
            config = json.load(file)
        with open(case_path) as file:
            case = json.load(file)

        max_execution_time = config["max_execution_time"]
        strategy_type = config["strategy"]
        max_trip_time = case["max_trip_time"]
        origin_city_name = case["origin_city"]
        required_city_names = case["required_cities"]
        stay_times = case["stay_times"]
        values = case["values"]
        travel_times = case["travel_times"]

        return max_execution_time, strategy_type, max_trip_time, origin_city_name, required_city_names, stay_times, values, travel_times

    def build_from_api(self, case_path, max_execution_time, strategy_type):
        with open(case_path) as file:
            case = json.load(file)
        max_trip_time = case["max_trip_time"]
        origin_city_name = case["origin_city"]
        required_city_names = case["required_cities"]
        stay_times = case["stay_times"]
        values = case["values"]
        travel_times = case["travel_times"]
        optimizer = self.build(max_execution_time, strategy_type, max_trip_time, origin_city_name,
                               required_city_names, stay_times, values, travel_times)
        return optimizer

    def build(self, max_execution_time, strategy_type, max_trip_time, origin_city_name,
              required_city_names, stay_times, values, travel_times):

        # Get optimizer params
        origin_city = self.__get_origin_city(origin_city_name, stay_times, values, travel_times)
        possible_trip_cities = self.__get_possible_trip_cities(origin_city_name, stay_times, values,
                                                               travel_times)
        required_cities = self.__get_required_cities(required_city_names, possible_trip_cities)

        # Build strategy
        strategy = self.__build_strategy(strategy_type, origin_city, possible_trip_cities,
                                         required_cities, max_trip_time, max_execution_time)
        # Build optimizer
        optimizer = Optimizer(strategy)
        return optimizer

    def build_from_file(self, config_path, case_path):
        max_execution_time, strategy_type, max_trip_time, origin_city_name, required_city_names, stay_times, values, travel_times = self.__load_params(
            config_path, case_path)
        optimizer = self.build(max_execution_time, strategy_type, max_trip_time,
                               origin_city_name, required_city_names, stay_times,
                               values, travel_times)
        return optimizer
