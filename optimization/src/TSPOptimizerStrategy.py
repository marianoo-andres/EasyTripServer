class TSPOptimizerStrategy:
    def __init__(self, origin_city, cities):
        self.origin_city = origin_city
        self.cities = cities

    def optimize(self):
        raise NotImplementedError()
