import hlt, logging
from collections import OrderedDict

"""
This code was built off of the starter bot given by the Halite website
"""

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("AlperionII")
# Then we print our start message to the logs
logging.info("Initiating the AlperionII start processes.")

ship_targets = {}

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    team_ships = game_map.get_me().all_ships()
    # For every ship that I control
    for i in range(len(team_ships)):
        ship = team_ships[i]
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # check if the ship has a target already
        if ship in ship_targets.keys():
            target = ship_targets[ship]
            # check if target is a planet and player can dock
            if isinstance(target, hlt.entity.Planet) and ship.can_dock(target):
                # add the dock command to the command queue
                command_queue.append(ship.dock(target))
                # remove the planet from planned planets provided it was in there to begin with
                del ship_targets[ship]
            else:
                # navigate toward target, taking ship collisions into effect
                navigate_command = ship.navigate(
                    ship.closest_point_to(target),
                    game_map,
                    speed = int(hlt.constants.MAX_SPEED),
                    ignore_ships = False)
                # add the move to the command queue and add the planet in question to planned planets if the move is possible
                if navigate_command:
                    command_queue.append(navigate_command)

        # get the a list of entities closest to the ship
        # code received from sentdex's tutorial on Youtube
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        target = None
        # see if there is an empty planet not already being traveled to
        for planet in closest_empty_planets:
            # check if another ship is targeting the planet OR
            # if there is room for the ship to dock and it is qualified to dock
            if planet not in ship_targets.values() or (list(ship_targets.values()).count(planet) < planet.num_docking_spots and i % 2 == 0):
                # make this planet the target, and store this target
                target = planet
                ship_targets[ship] = target
                break
                
        if target != None:
            if ship.can_dock(target):
                # add the dock command to the command queue
                command_queue.append(ship.dock(target))
                # remove the planet from planned planets provided it was in there to begin with
                del ship_targets[ship]
            else:
                # navigate toward target, taking ship collisions into effect
                navigate_command = ship.navigate(
                    ship.closest_point_to(target),
                    game_map,
                    speed = int(hlt.constants.MAX_SPEED),
                    ignore_ships = False)
                # add the move to the command queue and add the planet in question to planned planets if the move is possible
                if navigate_command:
                    command_queue.append(navigate_command)
        elif len(closest_enemy_ships) > 0: # no empty planets, attack enemy ships instead
            target_ship = closest_enemy_ships[0]
            # navigate to closest enemy ship, taking ship collisions into effect
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed = int(hlt.constants.MAX_SPEED),
                ignore_ships = False)
            # add the move to the command queue and add the planet in question to planned planets if the move is possible
            if navigate_command:
                command_queue.append(navigate_command)

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
