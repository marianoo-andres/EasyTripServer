import unittest

from optimization.src.City import City
from optimization.src.Solution import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        travel_times = {
            "Buenos Aires": {
                "Cordoba": 1 * 24,
                "Rosario": 2 * 24,
                "Ushuaia": 3 * 24
            },
            "Cordoba": {
                "Buenos Aires": 1 * 24,
                "Rosario": 1 * 24,
                "Ushuaia": 3 * 24
            },
            "Rosario": {
                "Buenos Aires": 2 * 24,
                "Cordoba": 1 * 24,
                "Ushuaia": 3 * 24
            },
            "Ushuaia": {
                "Buenos Aires": 3 * 24,
                "Cordoba": 3 * 24,
                "Rosario": 3 * 24
            },
        }
        self.possible_cities = []
        self.origin_city = City('Buenos Aires', 0, 0, travel_times['Buenos Aires'])
        self.possible_cities = {
            "Cordoba": City('Cordoba', 2, 10, travel_times['Cordoba']),
            "Rosario": City('Rosario', 1, 10, travel_times['Rosario']),
            "Ushuaia": City('Ushuaia', 3, 10, travel_times['Ushuaia'])
        }

    def test_solution_valid_without_required_cities(self):
        required_cities = []
        max_trip_time = 14
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                 self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 6
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 1 + 1 + 3 + 3
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertTrue(solution.is_valid())

    def test_solution_valid_with_required_cities(self):
        required_cities = [self.possible_cities["Cordoba"]]
        max_trip_time = 14
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                 self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 6
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 1 + 1 + 3 + 3
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertTrue(solution.is_valid())

    def test_solution_valid_with_all_required_cities(self):
        required_cities = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                           self.possible_cities["Ushuaia"]]
        max_trip_time = 14
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                 self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 6
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 1 + 1 + 3 + 3
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertTrue(solution.is_valid())

    def test_solution_invalid_travel_time(self):
        required_cities = []
        max_trip_time = 13
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                 self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 6
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 1 + 1 + 3 + 3
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertFalse(solution.is_valid_total_trip_time())

        self.assertFalse(solution.is_valid())

    def test_solution_invalid_knapsack_time(self):
        required_cities = []
        max_trip_time = 5
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"],
                 self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 6
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 1 + 1 + 3 + 3
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertFalse(solution.is_valid_knapsack_time())

        self.assertFalse(solution.is_valid_total_trip_time())

        self.assertFalse(solution.is_valid())

    def test_solution_invalid_required_city_not_present(self):
        required_cities = [self.possible_cities["Rosario"]]
        max_trip_time = 999999
        route = [self.possible_cities["Cordoba"], self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        self.assertFalse(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertFalse(solution.is_valid())

    def test_solution_invalid_with_two_required_city_both_not_present(self):
        required_cities = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        max_trip_time = 999999
        route = [self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        self.assertFalse(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertFalse(solution.is_valid())

    def test_solution_invalid_with_two_required_city_one_not_present(self):
        required_cities = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        max_trip_time = 999999
        route = [self.possible_cities["Cordoba"], self.possible_cities["Ushuaia"]]
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        self.assertFalse(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertFalse(solution.is_valid())

    def test_solution_valid_with_just_origin_city(self):
        required_cities = []
        max_trip_time = 999999
        route = []
        solution = Solution(origin_city=self.origin_city, cities=route,
                            required_cities=required_cities,
                            max_trip_time=max_trip_time)

        expected_total_stay_time = 0
        self.assertEqual(expected_total_stay_time, solution.get_total_stay_time())

        expected_total_travel_time = 0
        self.assertEqual(expected_total_travel_time, solution.get_total_travel_time())

        expected_total_trip_time = expected_total_stay_time + expected_total_travel_time
        self.assertEqual(expected_total_trip_time, solution.get_total_trip_time())

        self.assertTrue(solution.is_valid_required_city())

        self.assertTrue(solution.is_valid_knapsack_time())

        self.assertTrue(solution.is_valid_total_trip_time())

        self.assertTrue(solution.is_valid())

    def test_solution_similarity(self):
        route = [self.possible_cities["Cordoba"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Rosario"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        solution3 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        route = [self.possible_cities["Ushuaia"], self.possible_cities["Rosario"]]
        solution4 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        expected_similarity = 1
        self.assertEqual(solution1.get_similarity(solution1), expected_similarity)

        expected_similarity = 1
        self.assertEqual(solution2.get_similarity(solution2), expected_similarity)

        expected_similarity = 2
        self.assertEqual(solution3.get_similarity(solution3), expected_similarity)

        expected_similarity = 2
        self.assertEqual(solution4.get_similarity(solution4), expected_similarity)

        expected_similarity = 0
        self.assertEqual(solution1.get_similarity(solution2), expected_similarity)
        self.assertEqual(solution2.get_similarity(solution1), expected_similarity)

        expected_similarity = 1
        self.assertEqual(solution1.get_similarity(solution3), expected_similarity)
        self.assertEqual(solution3.get_similarity(solution1), expected_similarity)

        expected_similarity = 0
        self.assertEqual(solution1.get_similarity(solution4), expected_similarity)
        self.assertEqual(solution4.get_similarity(solution1), expected_similarity)

        expected_similarity = 1
        self.assertEqual(solution2.get_similarity(solution3), expected_similarity)
        self.assertEqual(solution3.get_similarity(solution2), expected_similarity)

        expected_similarity = 1
        self.assertEqual(solution2.get_similarity(solution4), expected_similarity)
        self.assertEqual(solution4.get_similarity(solution2), expected_similarity)

        expected_similarity = 1
        self.assertEqual(solution3.get_similarity(solution4), expected_similarity)
        self.assertEqual(solution4.get_similarity(solution3), expected_similarity)

    def test_solution_equal(self):
        route = [self.possible_cities["Cordoba"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Cordoba"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        self.assertEqual(solution1, solution2)

    def test_solution_equal2(self):
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        self.assertEqual(solution1, solution2)

    def test_solution_notequal1(self):
        route = [self.possible_cities["Cordoba"], self.possible_cities["Ushuaia"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        self.assertNotEqual(solution1, solution2)

    def test_solution_notequal2(self):
        route = [self.possible_cities["Cordoba"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Cordoba"], self.possible_cities["Rosario"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        self.assertNotEqual(solution1, solution2)

    def test_solution_notequal3(self):
        route = [self.possible_cities["Cordoba"]]
        solution1 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)
        route = [self.possible_cities["Rosario"]]
        solution2 = Solution(origin_city=self.origin_city, cities=route, required_cities=[],
                             max_trip_time=0)

        self.assertNotEqual(solution1, solution2)


if __name__ == '__main__':
    unittest.main()
