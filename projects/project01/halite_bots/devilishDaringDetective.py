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

# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
import random

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Old1")
# Then we print our start message to the logs
logging.info("Starting my My bot!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    all_planets = game_map.all_planets()
    planets_by_size = sorted(all_planets, key=lambda x: x.radius, reverse=True)

    chosen_planets = []
    ships = game_map.get_me().all_ships()

    # For every ship that I control
    for ship in ships:

        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        combined_planets = []
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        planets_by_distance = []
        for distance in sorted(entities_by_distance):
            planets_by_distance.append(next((nearest_entity
                                             for nearest_entity
                                             in entities_by_distance[distance]
                                             if isinstance(nearest_entity,
                                                           hlt.entity.Planet)),
                                            None))
        planets_by_distance = [x for x in planets_by_distance if x is not None]

        # Switch between biggest planets and closest planets
        for planet_number in range(len(all_planets)):
            if not planet_number >= len(planets_by_distance):
                combined_planets.append(planets_by_distance[planet_number])
            if not planet_number >= len(planets_by_size):
                combined_planets.append(planets_by_size[planet_number])

        # Loop through the planets switching between largest and closest
        for planet in combined_planets:

            # If I am in route to this planet or already own it, then skip it
            if planet in chosen_planets or planet.owner == ship.owner:
                continue

            # If we can dock, let's (try to) dock.
            # If two ships try to dock at once, neither will be able to.
            if ship.can_dock(planet):
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(planet))

            else:
                position = ship.closest_point_to(planet)

                navigate_command = ship.navigate(
                    position,
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    max_corrections=18,
                    angular_step=5,
                    ignore_ships=False)

                if navigate_command:
                    chosen_planets.append(planet)
                    command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
