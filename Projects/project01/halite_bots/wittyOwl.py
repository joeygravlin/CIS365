"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Then let's import the logging module so we can print out information
import logging

import math

# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("TestBot")
# Then we print our start message to the logs
logging.info("Starting my Test bot!")

direction_switcher = 'right'
type_switcher = 'collector'
BUFFER = 3

ship_details = {}
chosen_planets = []
combined_planets = []


def almost_equal(num1, num2, offset=0):
    return (
        num1 == num2 or int(num1 * 10 ** offset) == int(num2 * 10 ** offset)
    )


def set_up_planets(map_of_game, ship_list):
    global combined_planets

    logging.info('Generating planets list')

    all_planets = map_of_game.all_planets()

    planets_by_size = sorted(all_planets,
                             key=lambda x: x.radius, reverse=True)

    # sort planets by biggest and nearest every other
    # at the beginning of the game
    entities_by_distance = map_of_game.nearby_entities_by_distance(
        ship_list[0])
    planets_by_distance = []
    for distance in sorted(entities_by_distance):
        planets_by_distance.append(next((nearest_entity
                                         for nearest_entity
                                         in
                                         entities_by_distance[distance]
                                         if isinstance(nearest_entity,
                                                       hlt.entity.Planet)
                                         ),
                                        None))
    planets_by_distance = [x for x in planets_by_distance if
                           x is not None]

    # Switch between biggest planets and closest planets
    for planet_number in range(2 * len(all_planets)):
        if not planet_number >= len(planets_by_distance):
            combined_planets.append(planets_by_distance[planet_number])
        if not planet_number >= len(planets_by_size):
            combined_planets.append(planets_by_size[planet_number])


def get_new_planet():
    global chosen_planets, combined_planets

    new_planet = combined_planets.pop()
    chosen_planets.append(new_planet.id)

    return new_planet


while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent
    # to the Halite engine at the end of the turn
    command_queue = []

    ships = game_map.get_me().all_ships()

    # For every ship that I control
    for ship in ships:

        # If this is a newly spawned ship, set it up in my data structure
        if ship.id not in ship_details:
            if not combined_planets:
                set_up_planets(game_map, ships)

            ship_details[ship.id] = {'type': type_switcher,
                                     'angle': 0,
                                     'destination': None}

            ship_details[ship.id]['destination'] = get_new_planet()
            logging.info("Ship " + str(ship.id) + " has planet " +
                        str(ship_details[ship.id]['destination'].id))

            if len(ship_details) > 3:
                if type_switcher == 'collector':
                    type_switcher = 'guard'
                elif type_switcher == 'guard':
                    type_switcher = 'collector'

        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        docking = False
        planet = ship_details[ship.id]['destination']

        # If a guard is next to a planet
        if ship.can_dock(planet) \
                and ship_details[ship.id]['type'] == 'guard':

            # If no one owns the planet change into a collector and dock
            if not planet.owner:
                logging.info('Planet Owner ' + str(planet.owner))
                logging.info(
                    'Guard ' + str(ship.id) + ' becoming collector')
                ship_details[ship.id]['type'] = 'collector'
                command_queue.append(ship.dock(planet))
                docking = True
                logging.info('Collector ' + str(ship.id) + ' docking')

        # If we are close to a planet
        # and am a collector let's (try to) dock.
        if ship.can_dock(planet) \
                and ship_details[ship.id]['type'] == 'collector' \
                and not docking:

            # If another person owns the planet change into a guard
            if planet.owner and planet.owner != ship.owner:
                logging.info(
                    'Collector ' + str(ship.id) + ' becoming guard')
                ship_details[ship.id]['type'] = 'guard'

            # If I'm a collector, then collect
            if ship_details[ship.id]['type'] == 'collector':
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(planet))
                if planet.id in chosen_planets:
                    chosen_planets.remove(planet.id)
                docking = True
                logging.info('Collector ' + str(ship.id) + ' Docking')

        # If I didn't find that I could dock navigate to/around a planet
        if not docking:
            position = ship.closest_point_to(planet)

            # Guards should circle the planet
            if ship_details[ship.id]['type'] == 'guard':
                logging.info('Guard ' + str(ship.id) + ' circling')

                angle = ship_details[ship.id]['angle'] + (math.pi / 8)
                ship_details[ship.id]['angle'] = angle
                position.x = (planet.radius + 3) * math.cos(
                    angle) + planet.x
                position.y = (planet.radius + 3) * math.sin(
                    angle) + planet.y

            logging.info('Ship ' + str(ship.id)
                         + ' Navigating to old planet')
            navigate_command = ship.navigate(
                position,
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                max_corrections=18,
                angular_step=5,
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
