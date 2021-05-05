import hlt
import logging
from collections import OrderedDict

game = hlt.Game("Foguetinho")
logging.info("Start ")

turnCount = 0

maxSpeed = hlt.constants.MAX_SPEED


while True:
    game_map = game.update_map()

    logging.info(turnCount)

    numShips = int(len(game_map.get_me().all_ships())*.4)
    team_ships  = game_map.get_me().all_ships()[0:numShips]

    command_queue = []
    myPlanetsNotFull = []
    fullPlanets = []

    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue


        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        nearEmptyPlanets = [entities_by_distance[distance][0]
            for distance in entities_by_distance
                if isinstance(entities_by_distance[distance][0], hlt.entity.Planet)
                and not entities_by_distance[distance][0].is_owned()
                and entities_by_distance[distance][0]]
        team_ships1 = game_map.get_me().all_ships()



        nearEnemyShips = [entities_by_distance[distance][0]
            for distance in entities_by_distance
                if isinstance(entities_by_distance[distance][0], hlt.entity.Ship)
                and  entities_by_distance[distance][0] not in team_ships1]


        if len(nearEmptyPlanets) > 0:

            target_planet = nearEmptyPlanets[0]

            if ship in team_ships:
                target_ship = nearEnemyShips[0]
                navigateCommand = ship.navigate(ship.closest_point_to(target_ship),game_map,speed=int(maxSpeed),ignore_ships=False)
                if navigateCommand:
                    command_queue.append(navigateCommand)
            elif ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigateCommand = ship.navigate(ship.closest_point_to(target_planet),game_map,speed=int(maxSpeed),ignore_ships=False)

                if navigateCommand:
                    command_queue.append(navigateCommand)


        elif len(nearEnemyShips) > 0:
            target_ship = nearEnemyShips[0]
            navigateCommand = ship.navigate(ship.closest_point_to(target_ship),game_map,speed=int(maxSpeed),ignore_ships=False)
            if navigateCommand:
                command_queue.append(navigateCommand)


    game.send_command_queue(command_queue)


    # TURN END
# GAME END
