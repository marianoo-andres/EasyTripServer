import json
import os
import uuid

from optimization.GoogleMapsFacade import GoogleMapsFacade
from optimization.src.OptimizerBuilder import OptimizerBuilder


def create_case(username, data):
    # Get travel times
    cities = data["stay_times"].keys()
    travel_times = GoogleMapsFacade().get_travel_times(cities)

    # Add travel times to the json dic
    data["travel_times"] = travel_times

    # Create case
    if "name" in data:
        file_name = data["name"] + ".json"
    else:
        name = str(uuid.uuid4())
        file_name = name + ".json"
        data["name"] = name
    file_path = os.path.join('db', username.upper(), file_name)
    with open(file_path, "w") as file:
        json.dump(data, file, sort_keys=True, indent=4)


def update_case(username, data):
    if data["name"] + ".json" not in os.listdir(os.path.join('db', username.upper())):
        create_case(username, data)
        return

    case_path = os.path.join('db', username.upper(), data["name"] + ".json")
    with open(case_path) as file:
        case = json.load(file)
    case["required_cities"] = data["required_cities"]
    case["origin_city"] = data["origin_city"]
    case["max_trip_time"] = data["max_trip_time"]

    # Delete cities that were deleted
    cities = data["values"].keys()
    for city in list(case["travel_times"].keys()):
        if city not in cities:
            case["travel_times"].pop(city)
        else:
            for city2 in list(case["travel_times"][city].keys()):
                if city2 not in cities:
                    case["travel_times"][city].pop(city2)
    for city in list(case["values"].keys()):
        if city not in cities:
            case["values"].pop(city)
    for city in list(case["stay_times"].keys()):
        if city not in cities:
            case["stay_times"].pop(city)
    for city in list(case["lat_longs"].keys()):
        if city not in cities:
            case["lat_longs"].pop(city)

    with open(case_path, "w") as file:
        json.dump(case, file, sort_keys=True, indent=4)


def delete_case(username, casename):
    file_name = casename + ".json"
    file_path = os.path.join('db', username.upper(), file_name)
    try:
        os.remove(file_path)
    except:
        pass
    return {}


def create_user(data):
    username = data["username"].upper()
    for file_name in os.listdir('db'):
        if username == file_name:
            return False

    path = os.path.join('db', username)
    os.mkdir(path)
    return True


def get_cases(username):
    cases = []
    dir_path = os.path.join('db', username.upper())
    for file_name in os.listdir(dir_path):
        with open(os.path.join(dir_path, file_name)) as f:
            data = json.load(f)
        case = {}
        cities = []
        for city in data["values"].keys():
            cities.append({"name": city, "stay_time": data["stay_times"][city],
                           "value": data["values"][city],
                           "latitude": data["lat_longs"][city]["latitude"],
                           "longitude": data["lat_longs"][city]["longitude"]})
        case["cities"] = cities
        case["name"] = data["name"]
        case["max_trip_time"] = data["max_trip_time"]
        case["required_cities"] = data["required_cities"]
        case["origin_city"] = data["origin_city"]
        cases.append(case)
    return cases


def optimize(username, case_name, max_execution_time, strategy):
    case_path = os.path.join('db', username.upper(), case_name + ".json")
    optimizer_builder = OptimizerBuilder()
    optimizer = optimizer_builder.build_from_api(case_path, max_execution_time, strategy)
    if not optimizer:
        return {"error": "Not possible to construct valid solution with required cities"}
    result = optimizer.optimize()
    with open(case_path) as f:
        case = json.load(f)
    cities = []
    for city_name in result["cities"]:
        cities.append({
            "name": city_name,
            "latitude": case["lat_longs"][city_name]["latitude"],
            "longitude": case["lat_longs"][city_name]["longitude"],
            "stay_time": case["stay_times"][city_name],
            "value": case["values"][city_name]
        })
    result["cities"] = cities
    return result
