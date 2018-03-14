#!/usr/bin/env python3
# coding: utf-8

# Class handling adventurers behaviour
class Adventurer(object):

    # Handle direction changes for Gauche (G) and Droite (D)
    DIRECTION_CHANGE = {
        'G': {
            'N': 'O',
            'S': 'E',
            'E': 'N',
            'O': 'S'
        },
        'D': {
            'N': 'E',
            'S': 'O',
            'E': 'S',
            'O': 'N'
        },
    }

    def __init__(self, adventurer):
        self.name = adventurer['name']
        self.position = adventurer['position']
        self.direction = adventurer['direction']
        self.actions = list(adventurer['actions'])

    @property
    def get_position(self):
        return self.position

    def update_position(self, position):
        self.position = position

    def handle_direction(self, position, direction):
        new_position = [position[0], position[1]]

        if direction == 'S':
            new_position[1] = position[1] + 1
        elif direction == 'E':
            new_position[0] = position[0] + 1
        elif direction == 'N':
            new_position[1] = position[1] - 1
        elif direction == 'O':
            new_position[0] = position[0] - 1

        return new_position

    def get_turn_action(self, turn):
        return self.actions[turn]

    def get_next_position(self, action):
        if action in ['G', 'D']:
            self.direction = self.DIRECTION_CHANGE[action][self.direction]
            return self.position
        else:
            return self.handle_direction(self.position, self.direction)

# Class handling treasures behaviour
class Treasure(object):

    def __init__(self, position, count):
        self.position = position
        self.count = count

    def loot_treasure(self, position):
        self.count -= 1
        if self.count == 0:
            return ''
        else:
            return 'T'

# Class handling treasure map behaviour
class TreasureMap(object):

    def __init__(self, dimensions, mountains, treasures, adventurers):

        self.treasure_map = None
        self.Treasures = []
        self.Adventurers = []

        self.adventurer_positions = {}
        self.leaderboard = {}
        self.turn_count = 0

        # Get treasure map dimensions
        columns = dimensions[0]
        rows = dimensions[1]

        # Create 2d treasure map
        new_treasure_map = [['' for x in range(columns)] for y in range(rows)]

        # Place mountains on treasure map
        for mountain in mountains:
            new_treasure_map[mountain[1]][mountain[0]] = 'M'

        # Place treasures on treasure map
        for treasure in treasures:
            new_treasure_map[treasure[1]][treasure[0]] = 'T'

            position = [treasure[0], treasure[1]]
            new_Treasure = Treasure(position, treasure[2])
            self.Treasures.append(new_Treasure)

        # Store adventurers position on treasure map
        for adventurer in adventurers:
            new_Adventurer = Adventurer(adventurer)

            self.Adventurers.append(new_Adventurer)
            self.adventurer_positions[new_Adventurer.name] = new_Adventurer.position
            self.leaderboard[new_Adventurer.name] = 0

            if len(new_Adventurer.actions) > self.turn_count:
                self.turn_count = len(new_Adventurer.actions)

        self.treasure_map = new_treasure_map

    @property
    def get_treasure_map(self):
        treasure_map = []
        for row in self.treasure_map:
            new_row = []
            for item in row:
                new_row.append(item)
            treasure_map.append(new_row)
        return treasure_map

        return self.treasure_map

    def get_treasure(self, position):
        for Treasure in self.Treasures:
            if Treasure.position == position:
                return Treasure

    @property
    def get_treasures(self):
        return self.Treasures

    def get_adventurer(self, name):
        return self.Adventurers[name]

    @property
    def get_adventurers(self):
        return self.Adventurers

    @property
    def get_adventurer_positions(self):
        return self.adventurer_positions

    def update_adventurer_position(self, name, position):
        self.adventurer_positions[name] = position

    def get_content(self, position):
        try:
            return self.treasure_map[position[1]][position[0]]
        except IndexError:
            return 'M'

    def update_content(self, position, content):
        self.treasure_map[position[1]][position[0]] = content

    @property
    def get_leaderboard(self):
        leaderboard = {}
        for k, v in self.leaderboard.items():
            leaderboard[k] = v
        return leaderboard

    def update_leaderboard(self, name):
        self.leaderboard[name] += 1

    @property
    def get_turn_count(self):
        return self.turn_count

# Class handling the steps of the algorithm
class RunTreasureMap(object):

    def __init__(self, dimensions, mountains, treasures, adventurers):
        self.turns = {}

        Treasure_map = TreasureMap(dimensions, mountains, treasures, adventurers)

        init_treasure_map = Treasure_map.get_treasure_map
        init_leaderboard = Treasure_map.get_leaderboard
        turn_count = Treasure_map.get_turn_count
        turn = 0

        self.turns[0] = {
            'treasures': treasures,
            'adventurers': adventurers,
            'treasure_map': init_treasure_map,
            'leaderboard': init_leaderboard,
            'turn_count': turn_count
        }

        while turn < turn_count:
            turn_treasures = []
            turn_adventurers = []
            Adventurers = Treasure_map.get_adventurers

            # For each turn, move adventurers one after the others
            for Adventurer in Adventurers:
                position = Adventurer.position
                action = Adventurer.get_turn_action(turn)
                next_position = Adventurer.get_next_position(action)

                next_position_content = Treasure_map.get_content(next_position)
                adventurer_positions = Treasure_map.get_adventurer_positions

                # Move adventurer if path is clear
                if next_position not in list(adventurer_positions.values()) and next_position_content != 'M':

                    # Handle adventurer movement
                    if position != next_position:
                        Adventurer.update_position(next_position)
                        Treasure_map.update_adventurer_position(Adventurer.name, next_position)

                        # Handle treasure picking
                        if next_position_content == 'T':
                            Treasure = Treasure_map.get_treasure(next_position)
                            new_content = Treasure.loot_treasure(next_position)

                            Treasure_map.update_content(next_position, new_content)
                            Treasure_map.update_leaderboard(Adventurer.name)

                else:
                    continue

            # Get treasures information
            for Treasure in Treasure_map.get_treasures:
                turn_treasures.append({
                    'position': Treasure.position,
                    'count': Treasure.count
                })

            # Get adventurers information
            for Adventurer in Treasure_map.get_adventurers:
                turn_adventurers.append({
                    'name': Adventurer.name,
                    'position': Adventurer.position,
                    'direction': Adventurer.direction
                })

            # Get treasure map state
            new_treasure_map = Treasure_map.get_treasure_map

            # Get leaderboard state
            new_leaderboard = Treasure_map.get_leaderboard

            self.turns[turn + 1] = {
                'treasures': turn_treasures,
                'adventurers': turn_adventurers,
                'treasure_map': new_treasure_map,
                'leaderboard': new_leaderboard,
                'turn_count': turn_count
            }

            turn += 1

    @property
    def get_init_state(self):
        return self.turns[0]

    @property
    def get_final_state(self):
        return self.turns[len(self.turns) - 1]

    def get_turn(self, turn):
        return self.turns[int(turn)]
