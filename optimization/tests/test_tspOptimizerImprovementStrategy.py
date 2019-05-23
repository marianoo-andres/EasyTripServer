import unittest

from optimization.src.City import City
from optimization.src.TSPOptimizerImprovementStrategy import TSPOptimizerImprovementStrategy


class TestSolution(unittest.TestCase):
    def setUp(self):
        travel_times = {
            "A": {
                "B": 1,
                "C": 2,
                "D": 3,
            },
            "B": {
                "A": 1,
                "C": 2,
                "D": 3,
            },
            "C": {
                "A": 2,
                "B": 2,
                "D": 5,
            },
            "D": {
                "A": 3,
                "B": 3,
                "C": 5,
            }
        }
        self.cities = [City('B', 3, 10, travel_times['B']),
                       City('C', 2, 10, travel_times['C']),
                       City('D', 2, 10, travel_times['D'])
                       ]
        self.origin_city = City('A', 0, 0, travel_times['A'])
        self.optimizer = TSPOptimizerImprovementStrategy(self.origin_city, self.cities, 2)

    def test_optimize(self):
        route = self.optimizer.optimize()
        self.assertEqual(route[0].name, 'C')
        self.assertEqual(route[1].name, 'B')
        self.assertEqual(route[2].name, 'D')

    def test_optimize2(self):
        travel_times = {
            "Buenos Aires": {
                "Parana, Entre Rios": 5.397777777777778,
                "Formosa, Formosa": 12.465833333333334,
                "Catamarca, Catamarca Province": 11.876944444444444,
            },
            "Parana, Entre Rios": {
                "Buenos Aires": 5.397777777777778,
                "Formosa, Formosa": 9.135833333333332,
                "Catamarca, Catamarca Province": 9.137222222222222,
            },
            "Formosa, Formosa": {
                "Buenos Aires": 12.465833333333334,
                "Parana, Entre Rios": 9.135833333333332,
                "Catamarca, Catamarca Province": 12.189722222222223,
            },
            "Catamarca, Catamarca Province": {
                "Buenos Aires": 11.876944444444444,
                "Parana, Entre Rios": 9.137222222222222,
                "Formosa, Formosa": 12.189722222222223,
            }
        }
        self.cities = [City('Parana, Entre Rios', 2, 10, travel_times['Parana, Entre Rios']),
                       City('Formosa, Formosa', 2, 10, travel_times['Formosa, Formosa']),
                       City('Catamarca, Catamarca Province', 3, 10,
                            travel_times['Catamarca, Catamarca Province'])
                       ]
        self.origin_city = City('Buenos Aires', 0, 0, travel_times['Buenos Aires'])
        self.optimizer = TSPOptimizerImprovementStrategy(self.origin_city, self.cities, 2)
        route = self.optimizer.optimize()
        self.assertEqual(route[0].name, 'Parana, Entre Rios')
        self.assertEqual(route[1].name, 'Formosa, Formosa')
        self.assertEqual(route[2].name, 'Catamarca, Catamarca Province')


if __name__ == '__main__':
    unittest.main()
