import GlobalSettings
import random
import math
from Ship import Ship
from collections import deque

def handle_turn(setting, scoreboard, planets, ships, home_planet, player):
                def cpu_logic():
                    # Auto-spawn CPU ships if enough score
                    while scoreboard.get_scores()[player.player_num - 1] >= 250 and player.ship_count < GlobalSettings.ship_limit:
                        x_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
                        y_offset = random.randint(-home_planet.radius + 15, home_planet.radius - 15)
                        ships.append(Ship(home_planet.x + x_offset, home_planet.y + y_offset,
                                home_planet.id, player=player.player_num))
                        if player.player_num == GlobalSettings.opposing_player:
                            scoreboard.update_opponent(-250)
                        else:
                            scoreboard.update_player(-250)
                        player.ship_count += 1
                        
                #Finds the higest adjacent planet and moves to it
                def best_move_first():
                    best_value = -1
                    adjacent_planets = [planets[i] for i in planets[player.prev_target].connections]
                    candidate_planets = [p for p in adjacent_planets if p.player_num != player.player_num]
                    
                    #If all planets nearby have been conquered, BFS for the next planet nearby
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
                        for candidate_planet in candidate_planets:
                            if candidate_planet.point_value > best_value:
                                player.target_planet = candidate_planet.id
                                best_value = candidate_planet.point_value
                        
                #Finds the lowest adjacent planet and moves to it
                def worst_move_first():
                    worst_value = float('inf')

                    adjacent_planets = [planets[i] for i in planets[player.prev_target].connections]
                    candidate_planets = [p for p in adjacent_planets if p.player_num != player.player_num]

                    #If all planets nearby have been conquered, BFS for the next planet nearby
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
                        for candidate_planet in candidate_planets:
                            if candidate_planet.point_value < worst_value:
                                player.target_planet = candidate_planet.id
                                worst_value = candidate_planet.point_value
        
                    
                #Finds the closest highest value planet and travels to it
                def highest_scoring_first():
                    best_value = -1
                    best_distance = float('inf')
                    current_planet = planets[player.prev_target]

                    non_cpu_planets = [p for p in planets if p.player_num != player.player_num]

                    for candidate_planet in non_cpu_planets:
                        distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
                        if candidate_planet.point_value >= best_value and distance < best_distance:
                            player.target_planet = candidate_planet.id
                            best_value = candidate_planet.point_value
                            best_distance = distance

                #Finds the closest lowest value planet and travles to it
                def lowest_scoring_first():
                    #Among all non-CPU planets, find which is reachable and has the highest point_value
                    worst_value = float('inf')
                    best_distance = float('inf')
                    current_planet = planets[player.prev_target]

                    non_cpu_planets = [p for p in planets if p.player_num != player.player_num]

                    for candidate_planet in non_cpu_planets:
                        distance = math.sqrt((current_planet.x - candidate_planet.x) ** 2 +(current_planet.y - candidate_planet.y) ** 2)
                        if candidate_planet.point_value <= worst_value and distance < best_distance:
                            player.target_planet = candidate_planet.id
                            worst_value = candidate_planet.point_value
                            best_distance = distance
                
                #Traverses the map in a bfs
                def bfs(ship):
                    return
                
                #Moves ship towards its final target planet
                def ship_logic(ship):
                    #Find new target planet
                    if (player.target_planet == None or 
                    (player.target_planet == ship.curr_planet and planets[ship.curr_planet].player_num == player.player_num)):
                        if player.target_planet != None:
                            player.prev_target = player.target_planet
                        player.target_planet = None
                        return
                    #Capture target_planet and do nothing
                    elif player.target_planet == ship.curr_planet and planets[ship.curr_planet].player_num != player.player_num:
                        return
                    else:
                        #Step towards target planet
                        next_step_id = next_step(ship.curr_planet, player.target_planet, planets)
                        ship.set_target(planets[next_step_id])

                #Checks if the logic is a human or cpu player
                if setting != 'player':
                    cpu_logic()
                    
                    
                #Only calculates new target planets if necessary
                if player.target_planet == None:
                    if setting.lower() == 'best move first':
                        best_move_first()  
                    elif setting.lower() == 'worst move first':
                        worst_move_first()   
                    elif setting.lower() == 'highest scoring first':
                        highest_scoring_first()
                    elif setting.lower() == 'lowest scoring first':
                        lowest_scoring_first()
                            
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