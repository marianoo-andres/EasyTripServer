class City:
    def __init__(self, name, stay_time, value, trip_times):
        # Name of the city
        self.name = name

        # Time in days needed to stay in the city
        self.stay_time = stay_time

        # Quantifiable desire of visiting it
        self.value = value

        # Dic of trip times in days between self and other cities
        # self.trip_times = self.convert_trip_times(trip_times)
        # Dic of trip times in days between self and other cities
        self.trip_times = trip_times

    def __str__(self):
        return self.name

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.name == other.name

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.name != other.name

    def get_trip_time(self, another_city):
        """Get trip time from self to anotherCity"""
        return self.trip_times[another_city.name]


"""
    def convert_trip_times(self, trip_times):
        trip_times_in_days = {}
        for city_name in trip_times:
            trip_times_in_days[city_name] = trip_times[city_name] / 24
        return trip_times_in_days
"""
