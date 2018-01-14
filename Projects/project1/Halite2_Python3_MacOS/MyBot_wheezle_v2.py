import hlt
import logging
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
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        closest_enemy_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned() and entities_by_distance[distance][0].owner != game_map.my_id]

        #ATTACKER
        if shipid in attacker_fleet or (len(closest_empty_planets) == 0 and shipid in colonizer_fleet):
            if (len(closest_enemy_ships) > 0 and len(closest_enemy_ships) * 2 < len(team_ships)) or len(closest_empty_planets) == 0:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        #COLONIZER
        elif shipid in colonizer_fleet:
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

        #KAMAKAZI
        elif shipid in kamakazi_fleet:
            target_ship = closest_enemy_planets[0]
            navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

        #ship not in fleet
        else:
            if len(team_ships) < 2 * len(closest_enemy_ships) and len(closest_empty_planets) > 0:
                attacker_fleet = []
                kamakazi_fleet = []
                colonizer_fleet.append(shipid)
            else:
                if len(colonizer_fleet) <= 2 * len(attacker_fleet) and len(colonizer_fleet) <= 2 * len(kamakazi_fleet):
                    colonizer_fleet.append(shipid)
                else:
                    x = randint(1,10)
                    if x > 5:
                        attacker_fleet.append(shipid)
                    if x <= 5:
                        kamakazi_fleet.append(shipid)

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
