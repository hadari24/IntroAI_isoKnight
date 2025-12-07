
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


def tests():
    """Test heuristic functions"""
    import numpy as np
    from game_state import game_state

    print("=" * 60)
    print("HEURISTICS TESTS")
    print("=" * 60)

    # Test 1: Basic functionality
    print("\n=== Test 1: Basic Heuristic Returns Number ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (0, 0), 1)
    score = base_heuristic(state)
    print(f"Score: {score}")
    print(f"Is number: {isinstance(score, (int, float))}")
    print("✓ PASSED" if isinstance(score, (int, float)) else "✗ FAILED")

    # Test 2: Player 1 in center (advantage)
    print("\n=== Test 2: Player 1 Advantage ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (0, 0), 1)  # P1 center, P2 corner
    score = base_heuristic(state)
    print(f"Score (P1 center, P2 corner): {score}")
    print(f"Should be positive (P1 has more moves): {score > 0}")
    print("✓ PASSED" if score > 0 else "✗ FAILED")

    # Test 3: Player 2 in center (advantage)
    print("\n=== Test 3: Player 2 Advantage ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (0, 0), (2, 2), 1)  # P1 corner, P2 center
    score = base_heuristic(state)
    print(f"Score (P1 corner, P2 center): {score}")
    print(f"Should be negative (P2 has more moves): {score < 0}")
    print("✓ PASSED" if score < 0 else "✗ FAILED")

    # Test 4: Symmetric positions
    print("\n=== Test 4: Symmetric Positions ===")
    grid = np.zeros((6, 6), dtype=int)
    state = game_state(grid, (1, 1), (4, 4), 1)  # Symmetric corners
    score = base_heuristic(state)
    print(f"Score (symmetric): {score}")
    print(f"Should be close to 0: {abs(score) <= 1}")
    print("✓ PASSED" if abs(score) <= 1 else f"⚠ Got {score}")

    # Test 5: Consistency - same score regardless of whose turn
    print("\n=== Test 5: Consistency Check ===")
    grid = np.zeros((5, 5), dtype=int)
    state1 = game_state(grid, (2, 2), (0, 0), 1)  # P1's turn
    grid2 = np.zeros((5, 5), dtype=int)
    state2 = game_state(grid2, (2, 2), (0, 0), 2)  # P2's turn
    score1 = base_heuristic(state1)
    score2 = base_heuristic(state2)
    print(f"Score when P1's turn: {score1}")
    print(f"Score when P2's turn: {score2}")
    print(f"Should be same: {score1 == score2}")
    print("✓ PASSED" if score1 == score2 else "✗ FAILED - Heuristic should always return p1_moves - p2_moves")

    # Test 6: Current player is restored
    print("\n=== Test 6: State Not Modified ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (0, 0), 1)
    original_player = state.get_curr_player()
    score = base_heuristic(state)
    final_player = state.get_curr_player()
    print(f"Player before heuristic: {original_player}")
    print(f"Player after heuristic: {final_player}")
    print(f"Player restored: {original_player == final_player}")
    print("✓ PASSED" if original_player == final_player else "✗ FAILED - Must restore current player")

    # Test 7: Corner vs Edge vs Center
    print("\n=== Test 7: Position Mobility ===")
    grid = np.zeros((5, 5), dtype=int)

    # Count moves from different positions
    state_corner = game_state(grid.copy(), (0, 0), (4, 4), 1)
    state_corner.set_curr_player(1)
    corner_moves = len(state_corner.potential_moves())

    state_edge = game_state(grid.copy(), (0, 2), (4, 4), 1)
    state_edge.set_curr_player(1)
    edge_moves = len(state_edge.potential_moves())

    state_center = game_state(grid.copy(), (2, 2), (4, 4), 1)
    state_center.set_curr_player(1)
    center_moves = len(state_center.potential_moves())

    print(f"Corner (0,0) moves: {corner_moves}")
    print(f"Edge (0,2) moves: {edge_moves}")
    print(f"Center (2,2) moves: {center_moves}")
    print(f"Center > Edge > Corner: {center_moves > edge_moves > corner_moves}")
    print("✓ PASSED" if center_moves > edge_moves > corner_moves else "✗ FAILED")

    # Test 8: Empty vs Partially filled board
    print("\n=== Test 8: Filled Board ===")
    grid = np.zeros((5, 5), dtype=int)
    # Fill some squares
    grid[1, 0] = 1
    grid[0, 2] = 1
    grid[2, 1] = 1
    state = game_state(grid, (2, 2), (0, 0), 1)
    score = base_heuristic(state)
    print(f"Score on partially filled board: {score}")
    print(f"P1 still has advantage: {score > 0}")
    print("✓ Test completed")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    tests()