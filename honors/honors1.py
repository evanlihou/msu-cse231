"""
Honors Project 1

Run single simulation
Run a user-input number of simulations and report statistics
See functions below for an explaination of what each does
"""

import random
import numpy
import copy


def generate_passengers():
    '''
    Generate passenger data for one simulation run.
    List items are a tuple: (arrival_time, source_floor, destination_floor)
    Return: List, elevator speed (sec/floor), loading/unloading rate (sec/pass)
    Implicitly uses the simulation's seed for random.randint.
    '''
    FLOORS = 20       # number of floors: 20
    PASSENGERS = 1000  # number of passengers: 1000
    ELEVATOR_SPEEDS = [0.5, 1, 1.5, 2]  # poss. speeds of elevator (sec/floor)
    LOADING_RATE = [0.2, 0.3, 0.4]  # possible speeds to load and unload

    t = 0
    L = []
    random.shuffle(ELEVATOR_SPEEDS)
    random.shuffle(LOADING_RATE)
    for i in range(PASSENGERS):
        t += numpy.random.poisson()
        L.append((t, random.randint(0, FLOORS), random.randint(0, FLOORS)))
    return L, ELEVATOR_SPEEDS[0], LOADING_RATE[0]


def new_passengers(t, passenger_list):
    '''
    Gets all passengers waiting that we don't know about yet.
    t (float): current time in sec
    passenger_list (list): a list of passengers not known about yet
    Returns: new passengers (list), passenger_list w/o new passengers (list)
    '''
    new = []
    for passenger in passenger_list:
        if passenger[0] <= t:
            new.append(passenger)
    for passenger in new:
        passenger_list.remove(passenger)
    return new, passenger_list


def closest_floor(current_floor, on_elevator):
    '''
    Gets the closest destination floor of all people on_elevator
    current_floor (int): current floor of elevator
    on_elevator (list): all passengers on the elevator
    Returns: closest_floor (int)
    '''
    x = 1
    x = 2  # We want to check dest floors
    closest_distance = 999
    closest_floor = 0
    # We want to pick randomly if more than one floor is closest, this'll do it
    random.shuffle(on_elevator)
    # Find the closest now recursively
    for passenger in on_elevator:
        distance = abs(current_floor-passenger[x])
        if distance < closest_distance:
            closest_distance = distance
            closest_floor = passenger[x]
    return closest_floor


def most_waiting(queue):
    '''
    Gets the floor where the most people are waiting to be picked up
    queue (list): all passengers currently in the queue to be picked up
    Returns: list with format [floor, num_waiting]
    '''
    waiting_floors = []
    # We want to pick randomly if more than one floor is closest, this'll do it
    random.shuffle(queue)
    for passenger in queue:
        waiting_floors.append(passenger[1])
    waiting_count = [[x, waiting_floors.count(x)] for x in set(waiting_floors)]
    return max(waiting_count)


def out_string(arrival_time, current_floor, loading_rate,
               loaded, unloaded, onboard, file):
    """
    Takes in data and prints a normalized string with information of movement
    arrival_time (float): time arrived on floor in sec
    current_floor (int): current floor
    loading_rate (float): amount of time to load or unload 1 passenger (sec)
    loaded (int): num of passengers loaded
    unloaded (int): num of passengers unloaded
    onboard (int): num of passengers onboard
    file (file object): optional. file to print lines to.
        If no file, lines will be printed to stdout
    Returns: Nothing.
    """
    out_str = "Arrived on floor {} at {:.2f} sec. Load/unload time: {:.2f};" \
              "pass loaded: {}, pass unloaded: {}, pass onboard: {}".format(
                  current_floor, arrival_time, loading_rate*(loaded+unloaded),
                  loaded, unloaded, onboard)
    if file:
        print(out_str, file=file)


def random_elevator(passenger_list, elevator_speed, loading_rate,
                    capacity, output=None):
    '''
    Runs the random elevator based on the algoritm laid out in the specs.
    passenger_list (list of tuples): list of passengers
    elevator_speed (float): time to travel one floor
    loading_rate (float): time to load or unload one passenger
    capacity (int): number of people who can be on the elevator at once
    output (file): file to write output to. Will print nothing if not specified
    '''
    t = 0.0
    current_floor = 0
    # queue[i] = (arrival_time, source_floor, dest_floor)
    queue = []
    # on_elevator[i] = (arrival_time, source_floor, dest_floor)
    on_elevator = []
    # A list of all wait times for the passengers, to be used in statistics
    wait_times = []
    if output:
        print("==== Starting Random Run ====", file=output)
    while True:
        new, passenger_list = new_passengers(t, passenger_list)
        for passenger in new:
            queue.append(passenger)
        while len(on_elevator) > 0:
            # There's someone on the elevator, deal with them before the queue
            # But first, check for new passengers in the queue often
            new, passenger_list = new_passengers(t, passenger_list)
            for passenger in new:
                queue.append(passenger)

            # Travel to dest floor of someone on elevator
            rp = random.randint(0, len(on_elevator)-1)  # Random passenger
            t += abs(on_elevator[rp][2]-current_floor)*elevator_speed
            current_floor = on_elevator[rp][2]

            # Unload
            unloaded_num = 0
            for travelling_passenger in on_elevator:
                if travelling_passenger[2] == current_floor:
                    t += loading_rate
                    unloaded_num += 1
                    on_elevator.remove(travelling_passenger)
                    wait_times.append(t-travelling_passenger[0])

            # Load any waiting passengers
            loaded_num = 0
            t_before_load = t
            for waiting_passenger in queue:
                if (waiting_passenger[1] == current_floor and
                        len(on_elevator) < capacity):
                    t += loading_rate
                    loaded_num += 1
                    on_elevator.append(waiting_passenger)
                    queue.remove(waiting_passenger)
            out_string(t_before_load, current_floor, loading_rate, loaded_num,
                       0, len(on_elevator), output)

        if len(queue) == 0:
            # There's nobody waiting! Just wait a bit.
            t += 1

        else:
            # Someone's in the queue
            rp = random.randint(0, len(queue)-1)  # Random passenger
            # Travel to source floor of someone in queue
            t += abs(queue[rp][1]-current_floor)*elevator_speed
            current_floor = queue[rp][1]
            # Load the passengers waiting on this floor
            num_loaded = 0
            t_before_load = t
            for passenger in queue:
                if (passenger[1] == current_floor and
                        len(on_elevator) < capacity):
                    t += loading_rate
                    num_loaded += 1
                    on_elevator.append(passenger)
                    queue.remove(passenger)
            out_string(
                       t_before_load, current_floor, loading_rate, num_loaded,
                       0, len(on_elevator), output)

        if (len(passenger_list) == 0 and len(queue) == 0 and
                len(on_elevator) == 0):
            # Everybody's gone to the rapture. We're done
            break
    final_str = "Finished in {:.2f} sec. Min/max/avg wait time: " \
                "{:.2f}/{:.2f}/{:.2f}\n".format(t, min(wait_times),
                                                max(wait_times),
                                                numpy.mean(wait_times))
    if output:
        print(final_str, file=output)

    return t, wait_times


def strategy_elevator(passenger_list, elevator_speed, loading_rate,
                      capacity, output=None):
    '''
    Runs the strategy elevator based on the algoritm laid out in the specs.
    passenger_list (list of tuples): list of passengers
    elevator_speed (float): time to travel one floor
    loading_rate (float): time to load or unload one passenger
    capacity (int): number of people who can be on the elevator at once
    output (file): file to write output to. Will print nothing if not specified
    '''
    t = 0.0
    current_floor = 0
    # queue[i] = (arrival_time, source_floor, dest_floor)
    queue = []
    # on_elevator[i] = (arrival_time, source_floor, dest_floor)
    on_elevator = []
    # A list of all wait times for the passengers, to be used in statistics
    wait_times = []
    if output:
        print("==== Starting Strategic Run ====", file=output)
    while True:
        new, passenger_list = new_passengers(t, passenger_list)
        for passenger in new:
            queue.append(passenger)
        while len(on_elevator) > 0:
            # There's someone on the elevator, deal with them before the queue
            # But first, check for new passengers in the queue often
            new, passenger_list = new_passengers(t, passenger_list)
            for passenger in new:
                queue.append(passenger)

            # Travel to closest dest floor
            floor = closest_floor(current_floor, on_elevator)
            t += abs(floor-current_floor)*elevator_speed
            current_floor = floor

            # Unload
            num_unloaded = 0
            for travelling_passenger in on_elevator:
                if travelling_passenger[2] == current_floor:
                    t += loading_rate
                    num_unloaded += 1
                    on_elevator.remove(travelling_passenger)
                    wait_times.append(t-travelling_passenger[0])

            # Load any waiting passengers
            t_before_load = t
            num_loaded = 0
            for waiting_passenger in queue:
                if (waiting_passenger[1] == current_floor and
                        len(on_elevator) < capacity):
                    t += loading_rate
                    num_loaded += 1
                    on_elevator.append(waiting_passenger)
                    queue.remove(waiting_passenger)

            out_string(
                       t_before_load, current_floor, loading_rate, num_loaded,
                       num_unloaded, len(on_elevator), output)

        if len(queue) == 0:
            # There's nobody waiting! Just wait a bit.
            t += 1

        else:
            # Someone's in the queue
            floor = most_waiting(queue)[0]  # [0] is floor, [1] is count
            # Travel to source floor of someone in queue
            t += abs(floor-current_floor)*elevator_speed
            current_floor = floor
            # Load the passengers waiting on this floor
            t_before_load = t
            num_loaded = 0
            for passenger in queue:
                if (passenger[1] == current_floor and
                        len(on_elevator) < capacity):
                    t += loading_rate
                    num_loaded += 1
                    on_elevator.append(passenger)
                    queue.remove(passenger)
            out_string(
                       t_before_load, current_floor, loading_rate, num_loaded,
                       0, len(on_elevator), output)

        if (len(passenger_list) == 0 and len(queue) == 0 and
                len(on_elevator) == 0):
            # Everybody's gone to the rapture. We're done
            break

    final_str = "Finished in {:.2f} sec. " \
                "Min/max/avg wait time: {:.2f}/{:.2f}/{:.2f}\n".format(
                   t, min(wait_times), max(wait_times), numpy.mean(wait_times))
    if output:
        print(final_str, file=output)

    return t, wait_times


def single_run():
    '''
    Runs one instance of both a random and strategic elevator by calling
    their respective functions.
    '''
    sr_file = open('single_run.txt', 'w')

    passenger_list, elevator_speed, loading_rate = generate_passengers()
    random_passengers = copy.copy(passenger_list)
    strategy_passengers = copy.copy(passenger_list)

    random_elevator(random_passengers, elevator_speed,
                    loading_rate, capacity, sr_file)
    strategy_elevator(strategy_passengers, elevator_speed, loading_rate,
                      capacity, sr_file)
    print("Successfully ran single simulations. "
          "See single_run.txt for results.")
    sr_file.close()


def multi_run():
    '''
    Sets up multiple runs of both random and strategic elevators, and gets
    statistics on the results.
    '''
    runs = input("Enter number of runs: ")
    if runs == "0":
        return None
    r_results = [[], []]  # Random elevator results [[times], [waits]]
    s_results = [[], []]  # Strategy elevator results [[times], [waits]]
    mr_file = open('multi_run.txt', 'w')
    while not runs.isdigit():
        runs = input("Integers only. Enter runs: ")
    else:
        runs = int(runs)

    for simulation_count in range(1, runs+1):
        random.seed(simulation_count)
        passenger_list, elevator_speed, loading_rate = generate_passengers()
        random_passengers = copy.copy(passenger_list)
        strategy_passengers = copy.copy(passenger_list)
        r_run_time, r_run_wait = random_elevator(random_passengers,
                                                 elevator_speed, loading_rate,
                                                 capacity)
        r_results[0].append(r_run_time)
        for wait in r_run_wait:
            r_results[1].append(wait)
        s_run_time, s_run_wait = strategy_elevator(strategy_passengers,
                                                   elevator_speed,
                                                   loading_rate, capacity)
        s_results[0].append(s_run_time)
        for wait in s_run_wait:
            s_results[1].append(wait)

    # Print results to file
    print("=== Random ===", file=mr_file)
    print("Average time to complete {:.2f}"
          .format(numpy.mean(r_results[0])), file=mr_file)
    print("Min time to complete {:.2f}"
          .format(min(r_results[0])), file=mr_file)
    print("Max time to complete {:.2f}"
          .format(max(r_results[0])), file=mr_file)
    print("Average wait time {:.2f}"
          .format(numpy.mean(r_results[1])), file=mr_file)
    print("Min wait time {:.2f}"
          .format(min(r_results[1])), file=mr_file)
    print("Max wait time {:.2f}"
          .format(max(r_results[1])), file=mr_file)

    print("=== Strategy ===", file=mr_file)
    print("Average time to complete {:.2f}"
          .format(numpy.mean(s_results[0])), file=mr_file)
    print("Min time to complete {:.2f}"
          .format(min(s_results[0])), file=mr_file)
    print("Max time to complete {:.2f}"
          .format(max(s_results[0])), file=mr_file)
    print("Average wait time {:.2f}"
          .format(numpy.mean(s_results[1])), file=mr_file)
    print("Min wait time {:.2f}"
          .format(min(s_results[1])), file=mr_file)
    print("Max wait time {:.2f}"
          .format(max(s_results[1])), file=mr_file)

    print("Successfully ran multi simulations. See multi_run.txt for results.")

    mr_file.close()


# Main part of the program that runs everything else
# the numpy random seed is set once at the beginning of the program
seed = input("Enter seed: ")
while not seed.isdigit():
    seed = input("Integers only. Enter seed: ")
else:
    seed = int(seed)
capacity = input("Enter capacity: ")
while not capacity.isdigit():
    capacity = input("Integers only. Enter capcity: ")
else:
    capacity = int(capacity)

numpy.random.seed(seed)

single_run()
multi_run()
