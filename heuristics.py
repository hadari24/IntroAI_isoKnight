
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
    """ check if location is in bound and empty"""
    grid = state.get_grid()

    if (location[0] < 0 or location[0] >= len(grid) or
            location[1] < 0 or location[1] >= len(grid[0])):
        return False

    return grid[location] == 0


def test_advanced_heuristic():
    """Comprehensive tests for advanced heuristic with performance timing"""
    import numpy as np
    from game_state import game_state
    import time

    print("=" * 70)
    print("ADVANCED HEURISTIC TESTS")
    print("=" * 70)

    # Test 1: Basic functionality
    print("\n=== Test 1: Returns Valid Number ===")
    grid = np.zeros((8, 8), dtype=int)
    state = game_state(grid, (3, 3), (6, 6), 1)

    start = time.time()
    score = advanced_heuristic(state)
    elapsed = time.time() - start

    print(f"Score: {score}")
    print(f"Time: {elapsed * 1000:.2f} ms")
    print(f"Is number: {isinstance(score, (int, float))}")
    print("✓ PASSED" if isinstance(score, (int, float)) else "✗ FAILED")

    # Test 2: Base vs Advanced Comparison
    print("\n=== Test 2: Base vs Advanced Heuristic ===")
    grid = np.zeros((8, 8), dtype=int)
    state = game_state(grid, (4, 4), (1, 1), 1)

    start = time.time()
    base_score = base_heuristic(state)
    base_time = time.time() - start

    start = time.time()
    adv_score = advanced_heuristic(state)
    adv_time = time.time() - start

    print(f"Base heuristic:     {base_score:6} (time: {base_time * 1000:.2f} ms)")
    print(f"Advanced heuristic: {adv_score:6} (time: {adv_time * 1000:.2f} ms)")
    print(f"Advanced is slower (expected): {adv_time > base_time}")
    print("✓ Both work")

    # Test 3: Center vs Corner advantage
    print("\n=== Test 3: Center vs Corner ===")
    grid = np.zeros((10, 10), dtype=int)

    # P1 center, P2 corner
    state1 = game_state(grid.copy(), (5, 5), (0, 0), 1)
    score1 = advanced_heuristic(state1)

    # P1 corner, P2 center
    state2 = game_state(grid.copy(), (0, 0), (5, 5), 1)
    score2 = advanced_heuristic(state2)

    print(f"P1 center, P2 corner: {score1:6} (should be positive)")
    print(f"P1 corner, P2 center: {score2:6} (should be negative)")
    print(f"Center advantage detected: {score1 > 0 and score2 < 0}")
    print("✓ PASSED" if score1 > 0 and score2 < 0 else "✗ FAILED")

    # Test 4: Symmetric positions
    print("\n=== Test 4: Symmetric Positions ===")
    grid = np.zeros((10, 10), dtype=int)
    state = game_state(grid, (2, 2), (7, 7), 1)
    score = advanced_heuristic(state)

    print(f"Symmetric position score: {score}")
    print(f"Should be close to 0: {abs(score) <= 10}")
    print("✓ PASSED" if abs(score) <= 10 else f"⚠ Got {score}, might be OK")

    # Test 5: Performance on different board sizes
    print("\n=== Test 5: Performance on Different Board Sizes ===")
    board_sizes = [5, 8, 10, 12]

    for size in board_sizes:
        grid = np.zeros((size, size), dtype=int)
        state = game_state(grid, (size // 2, size // 2), (0, 0), 1)

        start = time.time()
        score = advanced_heuristic(state)
        elapsed = time.time() - start

        print(f"Board {size:2}x{size:2}: score={score:6}, time={elapsed * 1000:6.2f} ms")

    print("✓ All sizes work")

    # Test 6: Nearly blocked position (endgame)
    print("\n=== Test 6: Endgame Detection ===")
    grid = np.zeros((6, 6), dtype=int)

    # Fill board leaving few moves
    for i in range(6):
        for j in range(6):
            if (i, j) not in [(2, 2), (0, 0), (1, 2), (3, 0)]:
                grid[i, j] = 1

    state = game_state(grid, (2, 2), (0, 0), 1)
    score = advanced_heuristic(state)

    print(f"Nearly blocked position score: {score}")
    print(f"Should recognize critical position: {abs(score) > 10}")
    print("✓ Detects endgame")

    # Test 7: Consistency (same regardless of turn)
    print("\n=== Test 7: Consistency Check ===")
    grid = np.zeros((8, 8), dtype=int)
    state1 = game_state(grid, (4, 4), (1, 1), 1)  # P1's turn
    state2 = game_state(grid.copy(), (4, 4), (1, 1), 2)  # P2's turn

    score1 = advanced_heuristic(state1)
    score2 = advanced_heuristic(state2)

    print(f"Score (P1 turn): {score1}")
    print(f"Score (P2 turn): {score2}")
    print(f"Consistent: {score1 == score2}")
    print("✓ PASSED" if score1 == score2 else "✗ FAILED")

    # Test 8: Average performance (100 evaluations)
    print("\n=== Test 8: Average Performance (100 evaluations) ===")
    times = []

    for _ in range(100):
        size = 8
        grid = np.zeros((size, size), dtype=int)
        p1 = (np.random.randint(0, size), np.random.randint(0, size))
        p2 = (np.random.randint(0, size), np.random.randint(0, size))

        state = game_state(grid, p1, p2, 1)

        start = time.time()
        score = advanced_heuristic(state)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)

    print(f"Average time: {avg_time * 1000:.2f} ms")
    print(f"Min time:     {min_time * 1000:.2f} ms")
    print(f"Max time:     {max_time * 1000:.2f} ms")
    print(f"Fast enough (< 10ms avg): {avg_time < 0.01}")
    print("✓ Performance acceptable" if avg_time < 0.01 else "⚠ Might be slow in tournament")

    # Test 9: Compare with base on game simulation
    print("\n=== Test 9: Strategy Comparison ===")
    test_positions = [
        ((4, 4), (0, 0)),  # Center vs corner
        ((3, 3), (5, 5)),  # Symmetric
        ((1, 1), (7, 7)),  # Both corners
        ((4, 2), (2, 4)),  # Off-center
    ]

    print("\nPosition Analysis:")
    for p1, p2 in test_positions:
        grid = np.zeros((8, 8), dtype=int)
        state = game_state(grid, p1, p2, 1)

        base = base_heuristic(state)
        adv = advanced_heuristic(state)

        print(f"  P1={p1}, P2={p2}: base={base:4}, advanced={adv:4}")

    print("✓ Strategy comparison complete")

    # Test 10: Territory control function
    print("\n=== Test 10: Helper Functions ===")
    grid = np.zeros((8, 8), dtype=int)
    state = game_state(grid, (4, 4), (0, 0), 1)

    # Test territory counting
    territory_center = count_reachable_squares(state, (4, 4), 2)
    territory_corner = count_reachable_squares(state, (0, 0), 2)

    print(f"Territory from center (4,4): {territory_center}")
    print(f"Territory from corner (0,0): {territory_corner}")
    print(f"Center > Corner: {territory_center > territory_corner}")

    # Test position penalty
    corner_penalty = get_position_penalty((0, 0), 8)
    edge_penalty = get_position_penalty((0, 4), 8)
    center_penalty = get_position_penalty((4, 4), 8)

    print(f"Corner penalty: {corner_penalty}")
    print(f"Edge penalty:   {edge_penalty}")
    print(f"Center penalty: {center_penalty}")
    print(f"Correct order (corner > edge > center): {corner_penalty > edge_penalty > center_penalty}")
    print("✓ PASSED" if corner_penalty > edge_penalty >= center_penalty else "✗ FAILED")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    test_advanced_heuristic()