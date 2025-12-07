
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
    return base_heuristic(curr_state)
