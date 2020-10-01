from collections import defaultdict


class Solution():
    """
        A class used to represent a solution for the problem.

        ...

        Attributes
        ----------
        no_fuel_stations : int
            total number of fuel stations available
        no_cities : int
            total number of cities
        roads : int
            total number of roads available with cities
        fuel_tank : int
            fuel tank capacity of the vehicle
        fuel_needed : dict
            fuel needed between cities
        gas_stations : dict
            cities of the petrol pump are the keys and values are the respective prices of the fuel
        origin : int
            origin city where vehicle start
        dest : int
            destination city where vehicle heading to

        Methods
        -------
        find_all_paths(origin, dest, path=[])
            returns all paths available from origin to destination
        find_min_cost()
            returns minimum cost with which vehicle can travel from origin to destination
        """

    def __init__(self, data_dict):
        self.no_fuel_stations = data_dict['no_fuel_stations']
        self.no_cities = data_dict['no_cities']
        self.roads = data_dict['roads']
        self.fuel_tank = data_dict['fuel_tank']
        self.fuel_needed = data_dict['fuel_needed']
        self.gas_stations = data_dict['gas_stations']
        self.origin = data_dict['origin']
        self.dest = data_dict['dest']

    def find_all_paths(self, origin, dest, path=[]):
        """Finds all paths that are available from origin to destination

            Parameters
            ----------
            origin : int
                Origin city of the vehicle
            dest : int
                destination city of the vehicle
            path : list
                path of the vehicle from origin to destination
            Returns
            -------
            list
                a list of all paths that are available from origin to destination
        """
        path = path + [origin]
        if origin == dest: return [path]
        if origin not in self.graph.keys(): return []
        paths = []
        for node in self.graph[origin]:
            if node not in path:
                new_paths = self.find_all_paths(node, dest, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def find_min_cost(self):
        """Finds the minimum cost with which vehicle can reach from origin to destination

            Returns
            -------
            int
                minimum cost with which vehicle can reach from origin to destination
        """
        self.graph = defaultdict(list)
        for i, j in self.fuel_needed:
            if i not in self.graph:
                self.graph[i] = [j]
            else:
                self.graph[i].append(j)
        paths = self.find_all_paths(self.origin, self.dest)
        costs = []
        for path in paths:
            total_required_fuel = 0
            cost = 0
            add_flag = True
            cur_capacity = 0
            # Calculating the total required fuel for the journey
            for i in range(len(path) - 1):
                total_required_fuel += self.fuel_needed[(path[i], path[i + 1])]
            fuel_needed_remaining_path = total_required_fuel
            for i in range(len(path) - 1):
                min_fuel = self.fuel_needed[(path[i], path[i + 1])]
                if path[i + 1] in self.gas_stations and self.gas_stations[path[i + 1]] > self.gas_stations[path[i]]:
                    # if price is cheaper than next petrol pump on the path, then fill as much as possible
                    if fuel_needed_remaining_path > self.fuel_tank:
                        buy_amount = self.fuel_tank
                    else:
                        buy_amount = fuel_needed_remaining_path
                else:
                    # fill only the required fuel to travel to the next city
                    if min_fuel > fuel_needed_remaining_path:
                        buy_amount = fuel_needed_remaining_path
                    else:
                        buy_amount = min_fuel - cur_capacity
                try:
                    # add amount bought to the total cost
                    cost += buy_amount * self.gas_stations[path[i]]
                    cur_capacity += buy_amount
                    # travel to the next city and subtract the current capacity
                    cur_capacity -= min_fuel
                except:
                    # not possible to travel to the next city because insufficient fuel.
                    add_flag = False
                fuel_needed_remaining_path = fuel_needed_remaining_path - buy_amount
                if fuel_needed_remaining_path == 0: break
            if add_flag: costs.append(cost)
        try:
            min_cost = min(costs)
        except ValueError:
            # no available route to travel
            min_cost = None
        return min_cost


if __name__ == "__main__":
    input_dict = {'no_fuel_stations': 3,
                  'no_cities': 5,
                  'roads': 5,
                  'fuel_tank': 1000,
                  'fuel_needed': {(1, 2): 900, (2, 3): 900, (3, 5): 200},
                  'gas_stations': {1: 5, 2: 10, 3: 7},
                  'origin': 1,
                  'dest': 5}
    sol_obj = Solution(input_dict)
    min_cost = sol_obj.find_min_cost()
    if min_cost:
        print(f"Minimum Cost is {min_cost}.")
    else:
        print("Not possible to travel from origin to destination")
