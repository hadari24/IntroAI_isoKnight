
def base_heuristic(curr_state):
    #add code here
    # get location for players
    p1_location = curr_state.get_player_locations()[1]
    p2_location = curr_state.get_player_locations()[2]

    # saves the curr player
    curr_player = curr_state.get_curr_player()

    # checks how many moves for player 1 and player 2
    curr_state.set_curr_player(1)
    p1_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(2)
    p2_moves = len(curr_state.potential_moves())

    # setting the current player
    curr_state.set_curr_player(curr_player)

    return p1_moves - p2_moves

def advanced_heuristic(curr_state):
    # the players location
    p1_location = curr_state.get_player_locations()[1]
    p2_location = curr_state.get_player_locations()[2]
    grid = curr_state.get_grid()
    board_size = len(grid)

    # mobility - immediate moves
    # the weight is 10 - important
    curr_state_copy = curr_state

    curr_state_copy.set_curr_player(1)
    p1_moves = len(curr_state_copy.potential_moves())

    curr_state_copy.set_curr_player(2)
    p2_moves = len(curr_state_copy.potential_moves())

    mobility_score = (p1_moves - p2_moves) * 10

    # centrality - distance from center
    # the weight is 3 - important for mid-game
    center = (board_size - 1) / 2.0

    # distance from center
    p1_dist = abs(p1_location[0] - center) + abs(p1_location[1] - center)
    p2_dist = abs(p2_location[0] - center) + abs(p2_location[1] - center)

    # closer to the center is better
    centrality_score = (p2_dist - p1_dist) * 3

    # corner \ edge penalty
    # the weight is 5 - avoid trapped
    p1_corner_penalty = get_position_penalty(p1_location, board_size)
    p2_corner_penalty = get_position_penalty(p2_location, board_size)

    corner_score = (p2_corner_penalty - p1_corner_penalty) * 5

    # territory control - 2 move reach
    # the weight is 2
    p1_territory = count_reachable_squares(curr_state, p1_location, 2)
    p2_territory = count_reachable_squares(curr_state, p2_location, 2)

    territory_score = (p1_territory - p2_territory) * 2

    # aggressive blocking
    # the weight is 15 - important for endgame
    blocking_score = 0

    # if opponent has few moves, were winning
    if p2_moves <= 2:
        blocking_score = 15
    elif p2_moves <= 4:
        blocking_score = 0

    # if we have few moves, were losing
    if p1_moves <= 2:
        blocking_score = -15
    elif p1_moves <= 4:
        blocking_score = -8

    # combine all factors
    total_score = (mobility_score + centrality_score + corner_score + territory_score + blocking_score)

    return total_score

def get_position_penalty(location, board_size):
    """return penalty for being in corner\edge. Higher penalty = worse position"""
    x, y = location

    # corner (worst)
    if (x == 0 or x == board_size-1) and (y == 0 or y == board_size-1):
        return 3

    # edge (bad)
    if x == 0 or x == board_size-1 or y == 0 or y == board_size-1:
        return 1

    # center area (good)
    return 0

def count_reachable_squares(curr_state, location, max_depth):
    """count unique squares reachable within max_depth knight moves. This measures territory control"""
    if max_depth == 0:
        return 0
    visited = set()
    queue = [(location, max_depth)]

    while queue:
        curr_location, remaining_depth = queue.pop(0)

        if curr_location in visited:
            continue
        visited.add(curr_location)

        if remaining_depth > 0:
            # try all moves of the knight
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) == abs(j) or i == 0 or j == 0:
                        continue

                    new_location = (curr_location[0] + i, curr_location[1] + j)

                    # check if legal and not visited
                    if is_location_valid(curr_state, new_location) and new_location not in visited:
                        queue.append((new_location, remaining_depth - 1))

        return len(visited) - 1 # dont count starting position


def is_location_valid(state, location):
    """check if location is in bound and empty"""
    grid = state.get_grid()

    if (location[0] < 0 or location[0] >= len(grid) or
            location[1] < 0 or location[1] >= len(grid[0])):
        return False

    return grid[location] == 0