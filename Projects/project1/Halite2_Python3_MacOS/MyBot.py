import logging
import hlt
from collections import OrderedDict
from random import randint

game = hlt.Game("wheezlebot-v2")
logging.info("Starting")
attacker_fleet = []
colonizer_fleet = []
kamakazi_fleet = []

while True:
    game_map = game.update_map()
    command_queue = []
    team_ships = game_map.get_me().all_ships()

    for ship in team_ships:
        shipid = ship.id

        #ship not in fleet
        x = randint(1,100)
        if shipid not in attacker_fleet and shipid not in colonizer_fleet and shipid not in kamakazi_fleet:
            if x <= 60:
                attacker_fleet.append(shipid)
            elif x <= 80:
                kamakazi_fleet.append(shipid)
            else:
                colonizer_fleet.append(shipid)

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if (isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships)]

        #DEFAULT, UNCLAIMED TERRITORY
        if len(closest_empty_planets) > 0:
            target_planet = closest_empty_planets[0]
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
        else:
            closest_enemy_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].owner.id != game_map.my_id]

            closest_dockable_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].owner.id == game_map.my_id and entities_by_distance[distance][0].is_full() == False]

            #COLONIZER
            if shipid in colonizer_fleet:
                if len(closest_dockable_planets) > 0:
                    target_planet = closest_dockable_planets[0]
                    if ship.can_dock(target_planet):
                        command_queue.append(ship.dock(target_planet))
                    else:
                        navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed=int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)

                        if navigate_command:
                            command_queue.append(navigate_command)

            #ATTACKER
            if shipid in attacker_fleet or len(closest_dockable_planets) == 0:
                if len(closest_enemy_ships) > 0:
                    target_ship = closest_enemy_ships[0]
                    navigate_command = ship.navigate(
                                    ship.closest_point_to(target_ship),
                                    game_map,
                                    speed=int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

            #KAMAKAZI
            elif shipid in kamakazi_fleet:
                if len(closest_enemy_planets) > 0:
                    target_planet = closest_enemy_planets[0]
                    navigate_command = ship.navigate(
                                    target_planet,
                                    game_map,
                                    speed=int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)


    game.send_command_queue(command_queue)
    # TURN END
# GAME END
