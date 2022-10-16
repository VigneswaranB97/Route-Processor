from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from src.traveling_salesman import GeneticAlgo

geolocator = Nominatim(user_agent="Pareto")

cities = """
Chennai
Bangalore
Hyderabad
Telangana
Jaipur
Delhi
"""


def get_lat_long(city):
    location = geolocator.geocode(city)
    return location.latitude, location.longitude


def get_distance(point_1, point_2):
    return geodesic(point_1, point_2).kilometers


cities = [c for c in cities.split('\n') if c != '']

edges = []
dist_dict = {c: {} for c in cities}
for idx_1 in range(0, len(cities) - 1):
    for idx_2 in range(idx_1 + 1, len(cities)):
        city_a = cities[idx_1]
        city_b = cities[idx_2]
        dist = get_distance(get_lat_long(city_a), get_lat_long(city_b))
        print(f"Dist from {city_a} to {city_b} is {dist}")
        dist_dict[city_a][city_b] = dist
        dist_dict[city_b][city_a] = dist

g = GeneticAlgo(hash_map=dist_dict, start='Chennai', mutation_prob=0.25, crossover_prob=0.25,
                population_size=30, steps=45, iterations=2000)
order = g.converge()
print(order)
