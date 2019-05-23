import unittest

from optimization.src.City import City
from optimization.src.TSPOptimizerClosestCityStrategy import TSPOptimizerClosestCityStrategy


class TestSolution(unittest.TestCase):
    def setUp(self):
        travel_times = {
            "A": {
                "B": 1,
                "C": 3,
                "D": 3,
                "E": 6,
                "F": 6,
                "G": 6
            },
            "B": {
                "A": 1,
                "C": 1,
                "D": 2,
                "E": 5,
                "F": 6,
                "G": 4
            },
            "C": {
                "A": 3,
                "B": 1,
                "D": 2,
                "E": 4,
                "F": 5,
                "G": 5
            },
            "D": {
                "A": 3,
                "B": 2,
                "C": 2,
                "E": 3,
                "F": 4,
                "G": 4
            },
            "E": {
                "A": 6,
                "B": 5,
                "C": 4,
                "D": 3,
                "F": 4,
                "G": 5
            },
            "F": {
                "A": 6,
                "B": 6,
                "C": 5,
                "D": 4,
                "E": 4,
                "G": 6
            },
            "G": {
                "A": 6,
                "B": 4,
                "C": 5,
                "D": 4,
                "E": 5,
                "F": 6
            },
        }
        self.cities = [City('G', 3, 10, travel_times['G']),
                       City('F', 2, 10, travel_times['F']),
                       City('E', 2, 10, travel_times['E']),
                       City('D', 2, 10, travel_times['D']),
                       City('C', 2, 10, travel_times['C']),
                       City('B', 2, 10, travel_times['B']),
                       ]
        self.origin_city = City('A', 0, 0, travel_times['A'])
        self.optimizer = TSPOptimizerClosestCityStrategy(self.origin_city, self.cities)

    def test_get_closest_city_not_visited(self):
        closest_city = self.optimizer.get_closest_city_not_visited(self.origin_city)
        self.assertEqual(closest_city.name, 'B')

    def test_get_closest_city_not_visited_with_one_visited(self):
        self.optimizer.visited_cities['B'] = True
        closest_city = self.optimizer.get_closest_city_not_visited(self.cities[5])
        self.assertEqual(closest_city.name, 'C')

    def test_optimize(self):
        route = self.optimizer.optimize()
        self.assertEqual(route[0].name, 'B')
        self.assertEqual(route[1].name, 'C')
        self.assertEqual(route[2].name, 'D')
        self.assertEqual(route[3].name, 'E')
        self.assertEqual(route[4].name, 'F')
        self.assertEqual(route[5].name, 'G')


if __name__ == '__main__':
    unittest.main()
