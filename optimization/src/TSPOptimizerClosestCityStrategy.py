from optimization.src.TSPOptimizerStrategy import TSPOptimizerStrategy


class TSPOptimizerClosestCityStrategy(TSPOptimizerStrategy):
    def __init__(self, origin_city, cities):
        TSPOptimizerStrategy.__init__(self, origin_city, cities)
        self.visited_cities = {}
        for city in self.cities:
            self.visited_cities[city.name] = False

    def optimize(self):
        """Optimize a cities route and returns it"""
        if len(self.cities) == 0:
            return []
        route = []
        previous_city = self.origin_city
        for x in range(len(self.cities)):
            city = self.get_closest_city_not_visited(previous_city)
            self.visited_cities[city.name] = True
            route.append(city)
            previous_city = city
        return route

    def get_closest_city_not_visited(self, city):
        closest_city = None
        closest_city_trip_time = 9999999
        for other_city in self.cities:
            if self.is_city_visited(other_city):
                continue
            else:
                trip_time = city.get_trip_time(other_city)
                if trip_time < closest_city_trip_time:
                    closest_city = other_city
                    closest_city_trip_time = trip_time
        return closest_city

    def is_city_visited(self, city):
        return self.visited_cities[city.name]
