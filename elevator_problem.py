import itertools
from random import choices

global floor_dist
floor_dist = [100, 120, 60, 120, 80, 20]
possible_floors = [1, 2, 3, 4, 5, 6]

total_eta = 0
def inefficient_sim():
    global total_eta
    weights = [floor_dist[0]/500, floor_dist[1]/500, floor_dist[2]/500, floor_dist[3]/500, floor_dist[4]/500, floor_dist[5]/500]
    if sum(weights) == 0: 
        return total_eta
    elev_set = []
    for i in range(10): 
        elev_set.append(choices(possible_floors, weights))
    flat_elev_set = [x[0] for x in elev_set]
    for i in range(0, 6):
        floor_count = flat_elev_set.count(i + 1)
        floor_dist[i] = max(0, floor_dist[i] - floor_count)
    individiual_floors = len(set(flat_elev_set))
    highest_floor = max(flat_elev_set)
    eta = (15 + 2*5*highest_floor + 10*individiual_floors)*1
    total_eta += eta
counter = 0
for i in range(100):
    floor_dist = [100, 120, 60, 120, 80, 20]   
    total_eta = 0                                
    while any(floor_dist):
        inefficient_sim()
    counter += total_eta / 4
print(counter / 100)

# print(total_eta, iterations, total_eta_per_elevator)

def numb_elevators_serving(distribution, floor): 
    dist = ''.join(distribution)
    floors_served=str(dist).replace('-', "").replace(",","").replace(" ", "")
    floor = str(floor)
    return floors_served.count(floor)

def test_pairing(set): 
    highest_time = 0
    sum_of_time = 0
    for elevators in set:
        if len(elevators) == 1: 
            ppl_taking_elevator = floor_dist[int(elevators[0])-1]/numb_elevators_serving(set, elevators[0]) 
        else: 
            f = str(elevators.replace('-', "").replace(",","").replace(" ", ""))
            ppl_taking_elevator = floor_dist[int(f[0])-1]/numb_elevators_serving(set, f[0]) + floor_dist[int(f[1])-1]/numb_elevators_serving(set, f[1])
        floors_going_to = elevators.split('-')
        trips = ppl_taking_elevator/10 
        stops = len(floors_going_to)
        highest_floor = max(int(floor) for floor in floors_going_to)
        time_to_arrive = (15 + 2*5*highest_floor + 10*stops)*trips
        # print(time_to_arrive)
        sum_of_time += time_to_arrive
        if time_to_arrive > highest_time: 
            highest_time = time_to_arrive
    avg_time = sum_of_time/4
    return highest_time, avg_time

pair = ['1-2', '1-3', '5-6', '4']
# print(test_pairing(pair)[0])
# print(test_pairing(pair)[1])

def test_all_pairs():
    lowest_time = 10000
    lowest_avg_pair_time = 10000
    lowest_pair = None
    single_slots = [str(i) for i in range(1,7)]
    pair_slots = [f"{i}-{j}" for i, j in itertools.combinations(range(1, 7), r=2)]
    possible_slots = pair_slots+single_slots
    combos = itertools.combinations_with_replacement(possible_slots, r=4)
    final_combos = []
    for combo in combos: 
        if all(any(str(num) in slot for slot in combo) for num in range(1, 7)):
            final_combos.append(combo)
    for elev_tuple in final_combos: 
            time = test_pairing(list(elev_tuple))[0]
            avg_time = test_pairing(list(elev_tuple))[1]
            if time < lowest_time:
                lowest_time = time
                lowest_pair = list(elev_tuple)
            if avg_time < lowest_avg_pair_time: 
                lowest_avg_pair_time = avg_time
    
    return lowest_pair, lowest_time, lowest_avg_pair_time

# print(test_all_pairs())
