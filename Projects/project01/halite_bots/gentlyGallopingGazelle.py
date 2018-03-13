#!/usr/bin/env python3
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
from collections import OrderedDict

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Latest")
# Then we print our start message to the logs
logging.info("Starting my Bot!")

while True:
    game_map = game.update_map()
    command_queue = []
    player_id = game_map.get_me().id
    
    all_planets = game_map.all_planets()
    my_planets = [planet for planet in game_map.all_planets() if planet.is_owned() and planet.owner.id == player_id]
    enemy_planets = [planet for planet in game_map.all_planets() if planet.is_owned() and planet.owner.id != player_id]
    enemy_planets_by_radius = list(sorted(enemy_planets, key = lambda t: t.radius))
    planet_threshold = len(my_planets)*1.0/len(all_planets)
    
    team_ships = game_map.get_me().all_ships()
    team_ships_undocked = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == ship.DockingStatus.UNDOCKED]
    team_ships_docked = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == ship.DockingStatus.DOCKED]
    all_enemy_ships = []
    active_player_count = 0
    for p in game_map.all_players():
        if p.id != player_id and len(p.all_ships()) > 0:
            active_player_count += 1
            all_enemy_ships.extend(p.all_ships())
    
    if active_player_count == 0:
        active_player_count = 1
    
    ship_threshold = len(team_ships)*1.0/(len(all_enemy_ships)*1.0/active_player_count)
    
    logging.info("ship_threshold: " + str(ship_threshold))
    logging.info("planet_threshold: " + str(planet_threshold))
    
    squadron_1 = [s for s in team_ships if s.id % 3 == 0 and s.docking_status == s.DockingStatus.UNDOCKED]
    squadron_2 = [s for s in team_ships if s.id % 3 == 1 and s.docking_status == s.DockingStatus.UNDOCKED]
    squadron_3 = [s for s in team_ships if s.id % 3 == 2 and s.docking_status == s.DockingStatus.UNDOCKED]
    
    logging.info("squadron_1: " + str(len(squadron_1)))
    logging.info("squadron_2: " + str(len(squadron_2)))
    logging.info("squadron_3: " + str(len(squadron_3)))
    
    for ship in team_ships:
        if ship in team_ships_docked:
            continue
#        if len(team_ships_docked) > 20 and ship.docking_status == ship.DockingStatus.DOCKED:
#            command_queue.append(ship.undock())
#            continue
            
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key = lambda t: t[0]))
        
#        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and (not entities_by_distance[distance][0].is_owned() or (entities_by_distance[distance][0].is_owned and entities_by_distance[distance][0].owner.id == player_id and len(entities_by_distance[distance][0].all_docked_ships()) < 2))]
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and (not entities_by_distance[distance][0].is_owned() or (entities_by_distance[distance][0].is_owned and entities_by_distance[distance][0].owner.id == player_id and not entities_by_distance[distance][0].is_full()))]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
        closest_docked_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0].DockingStatus.DOCKED and entities_by_distance[distance][0] not in team_ships]
        closest_undocked_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0].DockingStatus.UNDOCKED and entities_by_distance[distance][0] not in team_ships]

            
        if ship in squadron_1 and (planet_threshold >= 0.6 or ship_threshold >= 1.15) and len(enemy_planets) > 0:
            navigate_command = ship.navigate(
                            all_enemy_ships[0],
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            max_corrections=15,
                            angular_step=5,
                            ignore_planets=False)

            if navigate_command:
                command_queue.append(navigate_command)
                continue
        
        if len(closest_empty_planets) > 1:
            closest_planets_by_radius = list(sorted(closest_empty_planets, key = lambda t: t.radius, reverse=True))
            if ship in squadron_1:
                target_planet = closest_empty_planets[0]
            else:
                target_planet = closest_planets_by_radius[0]
                
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            max_corrections=15,
                            angular_step=5,
                            ignore_ships=False)
    
                if navigate_command:
                    command_queue.append(navigate_command)
                        
        else:
            if ship_threshold > 1.7:
                target_ship = closest_enemy_ships[0]
                    
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            max_corrections=15,
                            angular_step=5,
                            ignore_ships=False)
    
                if navigate_command:
                    command_queue.append(navigate_command)
            elif len(closest_docked_enemy_ships) > 0 and (ship in squadron_2 or ship_threshold < .5):
                target_ship = closest_docked_enemy_ships[0]
                    
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            max_corrections=15,
                            angular_step=5,
                            ignore_ships=False)
    
                if navigate_command:
                    command_queue.append(navigate_command)
            elif len(closest_undocked_enemy_ships) > 0 and (ship in squadron_1 or ship in squadron_3):
                target_ship = closest_undocked_enemy_ships[0]
                    
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            max_corrections=15,
                            angular_step=5,
                            ignore_ships=False)
    
                if navigate_command:
                    command_queue.append(navigate_command)
                    
    game.send_command_queue(command_queue)
                
                
                
                
                
                