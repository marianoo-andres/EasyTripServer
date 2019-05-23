import time

from optimization.src.TSPOptimizerImprovementStrategy import TSPOptimizerImprovementStrategy


class Strategy:
    def __init__(self, origin_city, possible_trip_cities, required_cities, max_trip_time,
                 max_execution_time):
        self.origin_city = origin_city
        self.possible_trip_cities = possible_trip_cities
        self.required_cities = required_cities
        self.max_trip_time = max_trip_time
        # Receives minutes stores in seconds
        self.max_execution_time = max_execution_time * 60

        self.current_iteration = 0
        self.start_execution_time = time.time()

        self.time_between_print_stats = 10  # seconds
        self.start_time_between_print_stats = time.time()
        # The best solution calculated so far
        self.best_solution = None
        # All the good solutions
        self.good_solutions = []
        # Max number of good solutions to take into account
        self.max_good_solution_length = 1
        # A good solution cannot have a threshold * best_solution fitness lower
        # than the best_solution
        self.good_solution_fitness_threshold = 0.9

        # Size of the window (value k in k-improvement)
        self.improve_solution_window_size = 5

        # Debug
        self.log_activated = False

    def max_execution_time_reached(self):
        current_execution_time = time.time() - self.start_execution_time
        if current_execution_time > self.max_execution_time:
            print("current_execution_time: " + str(current_execution_time))
            print("self.max_execution_time: " + str(self.max_execution_time))
        return current_execution_time > self.max_execution_time

    def improve_solution(self, solution):
        window_size = self.improve_solution_window_size
        optimizer = TSPOptimizerImprovementStrategy(self.origin_city, solution.cities, window_size)
        solution.cities = optimizer.optimize()

    def improve_solutions(self):
        self.improve_solution(self.best_solution)
        # if self.good_solutions is not None:
        #    for good_solution in self.good_solutions:
        #        self.improve_solution(good_solution)

    def get_current_iteration(self):
        return self.current_iteration

    def set_best_solution(self, solution):
        self.best_solution = solution

    def clean_good_solutions(self):
        # Update good solutions to keep only the ones that have the necessary fitness
        temp = []
        for s in self.good_solutions:
            if s.fitness >= self.good_solution_fitness_threshold * self.best_solution.fitness:
                temp.append(s)
        self.good_solutions = temp

    def add_good_solution(self, solution):
        self.clean_good_solutions()

        # Don't add the best solution
        if solution == self.best_solution:
            return

        # Don't add a solution that already exists
        if solution in self.good_solutions:
            return

        # Don't add the solution if the fitness isn't good enough
        if solution.fitness < self.good_solution_fitness_threshold * self.best_solution.fitness:
            return

        # Add the solution if we don't have a full good solutions list
        if len(self.good_solutions) < self.max_good_solution_length:
            self.good_solutions.append(solution)
            return

        # We have a good fitness and the good solution list is full. We update the good
        # solutions by adding the new solution, recomputing the similarities and then
        # removing the worst solution of the list. Note: the solution removed could
        # be the new solution added.
        self.update_good_solutions(solution)

    def update_good_solutions(self, new_solution):
        """
        A good solution needs to be different than the best solution and the rest of the
        good solutions. We compare the candidate with the best solution and all the other
        good ones and compute the sum of the similarities to each of the other solutions.
        So, a good candidate would be one that has low total similarity

        Recomputes the similiraties and removes the worst solution of the good solutions
        """
        # Gives more weight so that solutions are more different to the best solution
        best_solution_similarity_weigth = 1
        similarity_dic = {}
        self.good_solutions.append(new_solution)

        # Compute total similarity
        for i, solution in enumerate(self.good_solutions):
            similarity_dic[
                i] = best_solution_similarity_weigth * self.best_solution.get_similarity(
                solution)
            for solution2 in self.good_solutions:
                if solution == solution2:
                    continue
                similarity_dic[i] += solution.get_similarity(solution2)

        # Compute total similarity
        for i in similarity_dic:
            similarity_dic[i] = similarity_dic[i] / (len(self.good_solutions) + 1)

        # Order solutions by lowest total similarity aka more different to others
        good_solutions = list(similarity_dic.items())
        good_solutions.sort(key=lambda x: x[1])
        # Remove the worst solution
        good_solutions.pop(len(good_solutions) - 1)
        # Store new best solutions
        temp = self.good_solutions
        self.good_solutions = []
        for s in good_solutions:
            self.good_solutions.append(temp[s[0]])

    def should_print_stats(self):
        if not self.log_activated:
            return False
        current_time_between_print_stats = time.time() - self.start_time_between_print_stats
        if current_time_between_print_stats > self.time_between_print_stats:
            self.start_time_between_print_stats = time.time()
            return True
        return False

    def print_stats(self):
        print("Iteracion: {}".format(self.current_iteration))
        print("Time: {}/{}".format((time.time() - self.start_execution_time),
                                   self.max_execution_time))
        if self.best_solution:
            print("BEST SOLUTION")
            self.best_solution.print()
        # for i, s in enumerate(self.good_solutions):
        #   print("GOOD SOLUTION", i)
        #    s.print()
        print("\n")

    def solve(self):
        raise NotImplementedError()
