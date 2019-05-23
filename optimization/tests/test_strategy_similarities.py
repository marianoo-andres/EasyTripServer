import unittest

from optimization.src.City import City
from optimization.src.Solution import Solution
from optimization.src.Strategy import Strategy


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.origin_city = City('1', 0, 0, None)
        self.possible_cities = {
            "2": City('2', 2, 10, None),
            "3": City('3', 1, 10, None),
            "4": City('4', 3, 10, None),
            "5": City('5', 3, 10, None),
            "6": City('6', 3, 10, None),
            "7": City('7', 3, 10, None),
            "8": City('8', 3, 10, None),
        }
        self.strategy = Strategy(self.origin_city, self.possible_cities, [], 0, 0)

    def test_add_good_solution(self):
        self.strategy.max_good_solution_length = 5
        self.strategy.good_solution_fitness_threshold = 0.8

        route = [self.possible_cities["2"], self.possible_cities["8"]]
        best_solution = Solution(self.origin_city, route, [], 0)
        best_solution.fitness = 100
        self.strategy.best_solution = best_solution

        good_solutions = []
        route = [self.possible_cities["2"]]
        s1 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s1)

        route = [self.possible_cities["2"], self.possible_cities["4"], self.possible_cities["8"]]
        s2 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s2)

        route = [self.possible_cities["2"], self.possible_cities["5"]]
        s3 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s3)

        route = [self.possible_cities["6"], self.possible_cities["7"]]
        s4 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s4)

        route = [self.possible_cities["6"], self.possible_cities["5"]]
        s5 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s5)

        for s in good_solutions:
            s.fitness = 100

        self.strategy.good_solutions = good_solutions

        route = [self.possible_cities["3"]]
        s6 = Solution(self.origin_city, route, [], 0)
        s6.fitness = 100

        self.strategy.add_good_solution(s6)
        self.assertEqual(self.strategy.good_solutions[0], s6)
        self.assertEqual(self.strategy.good_solutions[1], s4)
        self.assertEqual(self.strategy.good_solutions[2], s5)
        self.assertEqual(self.strategy.good_solutions[3], s1)
        self.assertEqual(self.strategy.good_solutions[4], s2)

    def test_add_good_solution_with_good_solutions_list_not_full(self):
        self.strategy.max_good_solution_length = 5

        route = [self.possible_cities["2"], self.possible_cities["8"]]
        best_solution = Solution(self.origin_city, route, [], 0)
        best_solution.fitness = 100
        self.strategy.best_solution = best_solution

        good_solutions = []
        route = [self.possible_cities["2"]]
        s1 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s1)

        route = [self.possible_cities["2"], self.possible_cities["4"], self.possible_cities["8"]]
        s2 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s2)

        route = [self.possible_cities["2"], self.possible_cities["5"]]
        s3 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s3)

        route = [self.possible_cities["6"], self.possible_cities["7"]]
        s4 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s4)

        route = [self.possible_cities["6"], self.possible_cities["5"]]
        s5 = Solution(self.origin_city, route, [], 0)
        good_solutions.append(s5)

        for s in good_solutions:
            s.fitness = 100

        self.strategy.add_good_solution(s1)
        self.assertEqual(self.strategy.good_solutions[0], s1)

        self.strategy.add_good_solution(s2)
        self.assertEqual(self.strategy.good_solutions[1], s2)

        self.strategy.add_good_solution(s3)
        self.assertEqual(self.strategy.good_solutions[2], s3)

        self.strategy.add_good_solution(s4)
        self.assertEqual(self.strategy.good_solutions[3], s4)

        self.strategy.add_good_solution(s5)
        self.assertEqual(self.strategy.good_solutions[4], s5)

    def test_add_good_solution_with_fitness_not_good_enough(self):
        self.strategy.max_good_solution_length = 5
        self.strategy.good_solution_fitness_threshold = 0.8

        route = [self.possible_cities["2"], self.possible_cities["8"]]
        best_solution = Solution(self.origin_city, route, [], 0)
        best_solution.fitness = 100
        self.strategy.best_solution = best_solution

        route = [self.possible_cities["2"]]
        s1 = Solution(self.origin_city, route, [], 0)
        s1.fitness = 79

        route = [self.possible_cities["2"], self.possible_cities["4"], self.possible_cities["8"]]
        s2 = Solution(self.origin_city, route, [], 0)
        s2.fitness = 70

        route = [self.possible_cities["2"], self.possible_cities["5"]]
        s3 = Solution(self.origin_city, route, [], 0)
        s3.fitness = 60

        route = [self.possible_cities["6"], self.possible_cities["7"]]
        s4 = Solution(self.origin_city, route, [], 0)
        s4.fitness = 50

        route = [self.possible_cities["6"], self.possible_cities["5"]]
        s5 = Solution(self.origin_city, route, [], 0)
        s5.fitness = 0

        self.strategy.add_good_solution(s1)
        self.assertEqual(len(self.strategy.good_solutions), 0)

        self.strategy.add_good_solution(s2)
        self.assertEqual(len(self.strategy.good_solutions), 0)

        self.strategy.add_good_solution(s3)
        self.assertEqual(len(self.strategy.good_solutions), 0)

        self.strategy.add_good_solution(s4)
        self.assertEqual(len(self.strategy.good_solutions), 0)

        self.strategy.add_good_solution(s5)
        self.assertEqual(len(self.strategy.good_solutions), 0)


if __name__ == '__main__':
    unittest.main()
