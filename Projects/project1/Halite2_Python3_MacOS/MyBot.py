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
            if x <= 65:
                attacker_fleet.append(shipid)
            #elif x <= 0:
                #kamakazi_fleet.append(shipid)
            else:
                colonizer_fleet.append(shipid)

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if (isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships) and (entities_by_distance[distance][0].DockingStatus == 1 or entities_by_distance[distance][0].DockingStatus == 2 or entities_by_distance[distance][0].DockingStatus == 3)]

        #DEFAULT, UNCLAIMED TERRITORY
        if shipid in colonizer_fleet and len(closest_empty_planets) > 0:
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
            closest_enemy = [entities_by_distance[distance][0] for distance in entities_by_distance if (isinstance(entities_by_distance[distance][0], hlt.entity.Planet) or isinstance(entities_by_distance[distance][0], hlt.entity.Ship)) and entities_by_distance[distance][0].owner.id != game_map.my_id]

            closest_dockable_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].owner.id == game_map.my_id and entities_by_distance[distance][0].is_full() == False]

            #COLONIZER
            if shipid in colonizer_fleet or len(closest_enemy) == 0:
                if len(closest_dockable_planets) > 0:
                    target_planet = closest_dockable_planets[0]

                if ship.can_dock(target_planet) and target_planet.is_full() == False:
                    command_queue.append(ship.dock(target_planet))
                else:
                    colonizer_fleet = list(filter(lambda a: a != shipid, colonizer_fleet))
                    attacker_fleet.append(shipid)

            #ATTACKER
            elif shipid in attacker_fleet or len(team_ships) > 120:
                if len(closest_enemy) > 0:
                    target = closest_enemy[0]

                    if isinstance(target, hlt.entity.Planet):
                        target = target.all_docked_ships()[0]

                    navigate_command = ship.navigate(
                                    ship.closest_point_to(target),
                                    game_map,
                                    speed=int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
