import GlobalSettings
import random
import math
from Ship import Ship
from collections import deque

def handle_turn(setting, scoreboard, planets, ships, home_planet, player):
    def cpu_purchase_logic():
        '''Helper function which buys ships for the CPU player.'''
        
        # If a CPU player has more than the ship price it will buy ships until it reaches the ship limit or runs out of points.
        while scoreboard.get_scores()[player.player_num - 1] >= GlobalSettings.ship_price and player.ship_count < GlobalSettings.ship_limit:
            x_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
            y_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
            ships.append(Ship(home_planet.x + x_offset, home_planet.y + y_offset,
                home_planet.id, player=player.player_num))
            if player.player_num == GlobalSettings.opposing_player:
                scoreboard.update_opponent(-GlobalSettings.ship_price)
            else:
                scoreboard.update_player(-GlobalSettings.ship_price)
            player.ship_count += 1
                        
    def best_move_first():
        '''Helper function which finds the best adjacent planetfor the CPU player.'''
                    
        best_value = -1
        adjacent_planets = [planets[i] for i in planets[player.prev_target].connections]
        
        # Candiate planets are those which are not owned by the CPU player and adjacent.
        candidate_planets = [p for p in adjacent_planets if p.player_num != player.player_num]
                    
        # If all planets nearby have been conquered, BFS for the next planet nearby.
        if not candidate_planets:
            planet_deque = deque(adjacent_planets)
            while planet_deque:
                planet = planet_deque.pop()
                if planet.player_num != player.player_num:
                    player.target_planet = planet.id
                    break
                else:
                    adjacent_planets = [planets[i] for i in planet.connections]
                    for adjacent_planet in adjacent_planets:
                        planet_deque.appendleft(adjacent_planet)
        # If there are candidate planets, find the one with the highest point value.
        else:
            for candidate_planet in candidate_planets:
                if candidate_planet.point_value > best_value:
                    player.target_planet = candidate_planet.id
                    best_value = candidate_planet.point_value
                        
                
    def worst_move_first():
        '''
        Helper function which finds the worst adjacent planet for the CPU player.
        '''
                    
        worst_value = float('inf')
        adjacent_planets = [planets[i] for i in planets[player.prev_target].connections]
        
        # Candiate planets are those which are not owned by the CPU player and adjacent.
        candidate_planets = [p for p in adjacent_planets if p.player_num != player.player_num]

        # If all planets nearby have been conquered, BFS for the next planet nearby.
        if not candidate_planets:
            planet_deque = deque(adjacent_planets)
            while planet_deque:
                planet = planet_deque.pop()
                if planet.player_num != player.player_num:
                    player.target_planet = planet.id
                    break
                else:
                    adjacent_planets = [planets[i] for i in planet.connections]
                    for adjacent_planet in adjacent_planets:
                        planet_deque.appendleft(adjacent_planet)
        else:
        # If there are candidate planets, find the one with the lowest point value.
            for candidate_planet in candidate_planets:
                if candidate_planet.point_value < worst_value:
                    player.target_planet = candidate_planet.id
                    worst_value = candidate_planet.point_value
        
                    
                
    def highest_scoring_first():
        '''
        Helper function which finds and moves to the overall highest scoring planet for the CPU player.
        '''
        
        best_value = -1
        best_distance = float('inf')
        current_planet = planets[player.prev_target]

        non_cpu_planets = [p for p in planets if p.player_num != player.player_num]

        # Finds the best planet to move to, which is not owned by the CPU player, and the shortest distance away.
        for candidate_planet in non_cpu_planets:
            distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
            if candidate_planet.point_value >= best_value and distance < best_distance:
                player.target_planet = candidate_planet.id
                best_value = candidate_planet.point_value
                best_distance = distance

    def lowest_scoring_first():
        '''
        Helper function which finds and moves to the overall lowest scoring planet for the CPU player.
        '''
        
        worst_value = float('inf')
        best_distance = float('inf')
        current_planet = planets[player.prev_target]

        non_cpu_planets = [p for p in planets if p.player_num != player.player_num]

        # Finds the worst planet to move to, which is not owned by the CPU player, and the shortest distance away.
        for candidate_planet in non_cpu_planets:
            distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
            if candidate_planet.point_value <= worst_value and distance < best_distance:
                player.target_planet = candidate_planet.id
                worst_value = candidate_planet.point_value
                best_distance = distance
                
    def bfs():
        '''
        Helper function which allows the ships to travel with bfs.
        '''
        
        # Uses bfs to find the next planet to move to (visited is if it is taken over yet).
        for connection in planets[player.prev_target].connections:
            # Checks if the planet is not owned by the CPU player and not already in queue.
            if planets[connection].player_num != player.player_num and connection not in player.bfs:
                player.bfs.appendleft(connection)
        # Goes to the next planet in the queue (which is the least recent planet added to the queue).
        player.target_planet = player.bfs.pop()
                    
    def dfs():
        '''
        Helper function which allows the ships to travel with dfs.
        '''
        
        # Uses dfs to find the next planet to move to (visited is if it is taken over yet).
        for connection in planets[player.prev_target].connections:
            # Checks if the planet is not owned by the CPU player and not already in queue.
            if planets[connection].player_num != player.player_num and connection not in player.dfs:
                player.dfs.append(connection)
        # Goes to the next planet in the queue (which is the most recent planet added to the queue).
        player.target_planet = player.dfs.pop()
                
    def ship_logic(ship):
        '''
        Helper function which moves the ship towards the target planet.
        '''
        
        # If the ship is at the target planet, it will land and stop moving.
        if (player.target_planet == None or 
            (player.target_planet == ship.curr_planet and planets[ship.curr_planet].player_num == player.player_num)):
            if player.target_planet != None:
                player.prev_target = player.target_planet
            player.target_planet = None
            return
        # If the ship is at the target planet, but it is not owned by the CPU player, it will stop moving.
        elif player.target_planet == ship.curr_planet and planets[ship.curr_planet].player_num != player.player_num:
            return
        else:
            # If the ship has an enemy ship on the current planet, it will stop moving.
            for enemy_ship in ships:
                if enemy_ship.player != player.player_num and enemy_ship.curr_planet == ship.curr_planet:
                    return
            # Step towards target planet using the next step helper function.
            next_step_id = next_step(ship.curr_planet, player.target_planet, planets)
            ship.set_target(planets[next_step_id])

    # Checks if the logic is a human or cpu player for purchasing ships.
    if setting != 'player':
        cpu_purchase_logic()
                    
                    
    # Only calculates new target planets if necessary and follows the respective strategy using the helper functions.
    if player.target_planet == None:
        if setting.lower() == 'best move first':
            best_move_first()  
        elif setting.lower() == 'worst move first':
            worst_move_first()   
        elif setting.lower() == 'highest scoring first':
            highest_scoring_first()
        elif setting.lower() == 'lowest scoring first':
            lowest_scoring_first()
        elif setting.lower() == 'bfs':
            bfs()
        elif setting.lower() == 'dfs':
            dfs()
    
    # Manages all of the player's ships.       
    for ship in ships:
        if ship.player != player.player_num:
            continue  # only manage current ships
        ship_logic(ship)
                        
def next_step(start_planet_id, goal_planet_id, planets):
    """
    Returns the planet ID of the *next step* on the shortest path from start_planet_id 
    to goal_planet_id, traversing any hyperlane (ignoring ownership).
    If no path is found or if start == goal, returns None.
    """
    
    # If already at the goal, return None.
    if start_planet_id == goal_planet_id:
        return None

    # BFS to find the shortest path from start_planet_id to goal_planet_id
    parent = {p.id: -1 for p in planets}
    visited = set([start_planet_id])
    queue = [start_planet_id]

    while queue:
        curr = queue.pop(0)
        if curr == goal_planet_id:
            break

        # Explore all neighbors in the hyperlane graph.
        for neighbor_id in planets[curr].connections:
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                parent[neighbor_id] = curr
                queue.append(neighbor_id)
    else:
        # BFS never reached goal_planet_id.
        return None

    # Reconstruct path by going backwards from goal to start.
    path = []
    node = goal_planet_id
    while node != -1:
        path.append(node)
        node = parent[node]
    path.reverse() # path is now from start to goal.

    # If there's at least one step to take, path will have length >= 2.
    if len(path) > 1:
        return path[1]  # then immediate next planet to move toward.
    return None