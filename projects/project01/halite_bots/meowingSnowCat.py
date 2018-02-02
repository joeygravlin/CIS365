import hlt
import logging

game = hlt.Game("Settler")

def go_towards_planet(ship, planet, map):
    # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
    # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
    # We run this navigate command each turn until we arrive to get the latest move.
    # Here we move at half our maximum speed to better control the ships
    # In order to execute faster we also choose to ignore ship collision calculations during navigation.
    # This will mean that you have a higher probability of crashing into ships, but it also means you will
    # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
    # wish to turn that option off.
    return ship.navigate(
        ship.closest_point_to(planet),
        map,
        speed=int(hlt.constants.MAX_SPEED),
        ignore_ships=True)

def me(game_map):
    return game_map.get_me()


def get_nearest_planets(ship, map):

    planets = []
    nearby_entities = map.nearby_entities_by_distance(ship)
    logging.info(nearby_entities)
    closest = 1000.0
    for key in nearby_entities:
        #logging.info(val)
        #nearby_entities = map.nearby_entities_by_distance(ship)
        #logging.info(key)

        if isinstance(nearby_entities[key][0], hlt.entity.Planet):
            logging.info("NEARBY PLANET FOUND: " + str(key))
            planets.append(nearby_entities[key][0])
            if key < closest:
                closest_planet = nearby_entities[key][0]
                closest = key
                logging.info("closest set: " + str(closest))
            #planets.append(nearby_entities[key][0])
    return planets

def get_sorted_distances(thing, map):

    planets = []
    nearby_entities = map.nearby_entities_by_distance(thing)
    keys = []
    for key in sorted(nearby_entities.keys()):
        #keys.append(key)
        #logging.info(key)
        entity = nearby_entities[key][0]
        #logging.info(entity)
        if isinstance(entity, hlt.entity.Planet):
            planets.append(nearby_entities[key][0])

    return planets



def get_nearest_planet(thing, map):

    planets = []
    nearby_entities = map.nearby_entities_by_distance(ship)
    logging.info(nearby_entities)
    closest = 1000.0
    for key in nearby_entities:
        # logging.info(val)
        # nearby_entities = map.nearby_entities_by_distance(ship)
        # logging.info(key)

        if isinstance(nearby_entities[key][0], hlt.entity.Planet):
            logging.info("NEARBY PLANET FOUND: " + str(key))
            planets.append(nearby_entities[key][0])
            if key < closest:
                closest_planet = nearby_entities[key][0]
                closest = key
                logging.info("closest set: " + str(closest))
                # planets.append(nearby_entities[key][0])
    return nearby_entities[key][0]


def determine_attack_viability(ship, planet, map):

    first_enemy = planet.all_docked_ships()[0]
    navigate_command = ship.navigate(
        ship.closest_point_to(first_enemy),
        map,
        speed=int(hlt.constants.MAX_SPEED),
        ignore_ships=True
    )

    return navigate_command



while True:

    game_map = game.update_map()
    command_queue = []
    player = me(game_map)
    ships = player.all_ships()

    for ship in ships:

        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        planets = get_sorted_distances(ship, game_map)

        for planet in planets:
        #planet = get_nearest_planet(ship, game_map)
            logging.info(planet)
            if planet.is_owned():
                if planet.owner != player:
                    command = determine_attack_viability(ship, planet, game_map)
                    if command:
                        command_queue.append(command)
                        logging.info("attack")
                        break
                else: continue

            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
                logging.info("dock")
                break
            else:
                command = go_towards_planet(ship, planet, game_map)
                if(command):
                    command_queue.append(command)
                    logging.info("colonize")
                    break


    game.send_command_queue(command_queue)