import GlobalSettings
import random
import math
from Ship import Ship
from collections import deque

def handle_cpu_turn(setting, scoreboard, planets, ships, home_planet, player_num):
                #Finds the higest adjacent planet and moves to it
                def best_move_first(ship):
                    best_value = -1
                    best_next_step_id = None

                    adjacent_planets = [planets[i] for i in planets[ship.curr_planet].connections]
                    candidate_planets = [p for p in adjacent_planets if p.player_num != player_num]
                    
                    #If all planets nearby have been conquered, BFS for the next planet nearby
                    if not candidate_planets:
                        planet_deque = deque(adjacent_planets)
                        while planet_deque:
                            planet = planet_deque.pop()
                            if planet.player_num != player_num:
                                best_next_step_id = bfs_next_step(ship.curr_planet, planet.id, planets)
                                break
                            else:
                                adjacent_planets = [planets[i] for i in planet.connections]
                                for adjacent_planet in adjacent_planets:
                                    planet_deque.appendleft(adjacent_planet)
                    else:
                        for candidate_planet in candidate_planets:
                            if candidate_planet.point_value > best_value:
                                best_next_step_id = candidate_planet.id
                                best_value = candidate_planet.point_value
                    #If we found a reachable planet, move one hop toward it
                    if best_next_step_id is not None:
                    # next_step_id is the planet ID of the next immediate planet in the BFS path
                        ship.set_target(planets[best_next_step_id])
                        
                #Finds the lowest adjacent planet and moves to it
                def worst_move_first(ship):
                    worst_value = float('inf')
                    worst_next_step_id = None

                    adjacent_planets = [planets[i] for i in planets[ship.curr_planet].connections]
                    candidate_planets = [p for p in adjacent_planets if p.player_num != player_num]

                    #If all planets nearby have been conquered, BFS for the next planet nearby
                    if not candidate_planets:
                        planet_deque = deque(adjacent_planets)
                        while planet_deque:
                            planet = planet_deque.pop()
                            if planet.player_num != player_num:
                                worst_next_step_id = bfs_next_step(ship.curr_planet, planet.id, planets)
                                break
                            else:
                                adjacent_planets = [planets[i] for i in planet.connections]
                                for adjacent_planet in adjacent_planets:
                                    planet_deque.appendleft(adjacent_planet)
                    else:
                        for candidate_planet in candidate_planets:
                            if candidate_planet.point_value < worst_value:
                                worst_next_step_id = candidate_planet.id
                                worst_value = candidate_planet.point_value
                        #If we found a reachable planet, move one hop toward it
                    if worst_next_step_id is not None:
                    # next_step_id is the planet ID of the next immediate planet in the BFS path
                        ship.set_target(planets[worst_next_step_id])
                    
                #Finds the closest highest value planet and travels to it
                def highest_scoring_first(ship):
                    best_planet = None
                    best_value = -1
                    best_next_step_id = None
                    best_distance = float('inf')

                    non_cpu_planets = [p for p in planets if p.player_num != player_num]

                    for candidate_planet in non_cpu_planets:
                        distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
                        if candidate_planet.point_value >= best_value and distance < best_distance:
                            next_step_id = bfs_next_step(current_planet.id, candidate_planet.id, planets)
                            if next_step_id is not None:
                                # BFS found a path => see if it's "better"
                                best_planet = candidate_planet
                                best_value = candidate_planet.point_value
                                best_next_step_id = next_step_id
                                best_distance = distance
                    #If we found a reachable planet, move one hop toward it
                    if best_planet is not None and best_next_step_id is not None:
                    # next_step_id is the planet ID of the next immediate planet in the BFS path
                        ship.set_target(planets[best_next_step_id])

                #Finds the closest lowest value planet and travles to it
                def lowest_scoring_first(ship):
                    #Among all non-CPU planets, find which is reachable and has the highest point_value
                    worst_planet = None
                    worst_value = float('inf')
                    worst_next_step_id = None
                    best_distance = float('inf')

                    non_cpu_planets = [p for p in planets if p.player_num != player_num]

                    for candidate_planet in non_cpu_planets:
                        distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
                        if candidate_planet.point_value <= worst_value and distance < best_distance:
                            next_step_id = bfs_next_step(current_planet.id, candidate_planet.id, planets)
                            if next_step_id is not None:
                                # BFS found a path => see if it's "better"
                                worst_value = candidate_planet.point_value
                                worst_planet = candidate_planet
                                worst_next_step_id = next_step_id
                                best_distance = distance
                    #If we found a reachable planet, move one hop toward it
                    if worst_planet is not None and worst_next_step_id is not None:
                        # next_step_id is the planet ID of the next immediate planet in the BFS path
                        ship.set_target(planets[worst_next_step_id])
                            
                # Auto-spawn CPU ships if enough score
                while scoreboard.get_scores()[player_num - 1] >= 250:
                    x_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
                    y_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
                    ships.append(Ship(home_planet.x + x_offset, home_planet.y + y_offset,
                            home_planet.id, player=player_num))
                    if player_num == GlobalSettings.opposing_player:
                        scoreboard.update_opponent(-250)
                    else:
                        scoreboard.update_player(-250)
                #For each CPU ship, pick the best planet to capture and move one step along BFS
                for ship in ships:
                    if ship.player != player_num:
                        continue  # only manage CPU ships

                    current_planet = planets[ship.curr_planet]

                    #If physically on a planet that isn't owned yet, skip movement (still capturing).
                    distance = math.hypot(ship.x - current_planet.x, ship.y - current_planet.y)
                    if distance < current_planet.radius and current_planet.player_num != player_num:
                        continue
                    if setting.lower() == 'best move first':
                        best_move_first(ship)  
                    if setting.lower() == 'worst move first':
                        worst_move_first(ship)   
                    if setting.lower() == 'highest scoring first':
                        highest_scoring_first(ship)
                    elif setting.lower() == 'lowest scoring first':
                        lowest_scoring_first(ship)
                        
def bfs_next_step(start_planet_id, goal_planet_id, planets):
    """
    Returns the planet ID of the *next step* on the shortest path from start_planet_id 
    to goal_planet_id, traversing any hyperlane (ignoring ownership).
    If no path is found or if start == goal, returns None.
    """
    if start_planet_id == goal_planet_id:
        return None

    parent = {p.id: -1 for p in planets}
    visited = set([start_planet_id])
    queue = [start_planet_id]

    while queue:
        curr = queue.pop(0)
        if curr == goal_planet_id:
            break

        # Explore all neighbors in the hyperlane graph
        for neighbor_id in planets[curr].connections:
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                parent[neighbor_id] = curr
                queue.append(neighbor_id)
    else:
        # BFS never reached goal_planet_id
        return None

    # Reconstruct path by going backwards from goal to start
    path = []
    node = goal_planet_id
    while node != -1:
        path.append(node)
        node = parent[node]
    path.reverse() # path is now from start to goal

    # If there's at least one step to take, path will have length >= 2
    if len(path) > 1:
        return path[1]  # the immediate next planet to move toward
    return None