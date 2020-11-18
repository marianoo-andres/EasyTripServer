import itertools
import os
import googlemaps


class GoogleMapsFacade:
    def __init__(self):
        self.googlemapsClient = googlemaps.Client(key=os.environ.get("API_KEY"))

    def get_travel_times(self, cities):
        """
        :param cities: name of the cities
        :return: travel times matrix in hours
        """
        distances = {}
        durations = {}
        for city in cities:
            distances[city] = {}
            durations[city] = {}

        city_pairs = [pair for pair in itertools.combinations(cities, 2)]

        distance_matrix_params = {
            "mode": "driving",
            "units": "metric",
            "region": "AR"
        }
        for i, pair in enumerate(city_pairs):
            print("Requesting pair {} of {}...".format(i + 1, len(city_pairs)))
            city_origin = pair[0]
            city_destination = pair[1]
            distance_matrix_params["origins"] = city_origin
            distance_matrix_params["destinations"] = city_destination
            distance_matrix_result = self.googlemapsClient.distance_matrix(**distance_matrix_params)
            distance_in_km = distance_matrix_result["rows"][0]["elements"][0]["distance"][
                                 "value"] / 1000
            time_in_hours = distance_matrix_result["rows"][0]["elements"][0]["duration"][
                                "value"] / 60 / 60
            distances[city_origin][city_destination] = distance_in_km
            distances[city_destination][city_origin] = distance_in_km
            durations[city_origin][city_destination] = time_in_hours
            durations[city_destination][city_origin] = time_in_hours

        # Only care about durations (travel times)
        return durations
