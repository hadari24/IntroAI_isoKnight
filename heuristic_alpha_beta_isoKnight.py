import math
h = None


def alphabeta_max_h(current_game, _heuristic, depth=3):
    global h
    h = _heuristic
    return maximin(current_game, depth=depth)


def alphabeta_min_h(current_game, _heuristic, depth=3):
    global h
    h = _heuristic
    return minimax(current_game, depth=depth)


def maximin(current_game, depth):
    global h
    if current_game.is_terminal():
        return current_game.get_score(), None
    if depth == 0:
        return h(current_game), None
    v = -math.inf
    moves = current_game.get_moves()
    for move in moves:
        mx, next_move = minimax(move, depth - 1)
        if v < mx:
            v = mx
            best_move = move
    return v, best_move


def minimax(current_game, depth):
    global h
    if current_game.is_terminal():
        return current_game.get_score(), None
    if depth == 0:
        return h(current_game), None
    v = math.inf
    moves = current_game.get_moves()
    for move in moves:
        mx, next_move = maximin(move, depth - 1)
        if v > mx:
            v = mx
            best_move = move

    return v, best_move


def tests():
    """Test heuristic alpha-beta functions"""
    import numpy as np
    from game_state import game_state
    import heuristics

    print("=" * 60)
    print("HEURISTIC ALPHA-BETA TESTS")
    print("=" * 60)

    # Test 1: Basic functionality with base heuristic
    print("\n=== Test 1: Basic Heuristic Alpha-Beta ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (0, 0), 1)
    score, move = alphabeta_max_h(state, heuristics.base_heuristic, depth=2)
    print(f"Score with depth=2: {score}")
    print(f"Move found: {move is not None}")
    print("✓ PASSED" if isinstance(score, (int, float)) else "✗ FAILED")

    # Test 2: Different depths
    print("\n=== Test 2: Different Depths ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (4, 4), 1)

    score_d1, _ = alphabeta_max_h(state, heuristics.base_heuristic, depth=1)
    score_d2, _ = alphabeta_max_h(state, heuristics.base_heuristic, depth=2)
    score_d3, _ = alphabeta_max_h(state, heuristics.base_heuristic, depth=3)

    print(f"Depth 1 score: {score_d1}")
    print(f"Depth 2 score: {score_d2}")
    print(f"Depth 3 score: {score_d3}")
    print("✓ All depths work")

    # Test 3: Terminal state
    print("\n=== Test 3: Terminal State ===")
    grid = np.ones((3, 3), dtype=int)
    grid[1, 1] = 1
    grid[2, 2] = 2
    state = game_state(grid, (1, 1), (2, 2), 1)

    if state.is_terminal():
        score, move = alphabeta_max_h(state, heuristics.base_heuristic, depth=3)
        print(f"Terminal state score: {score}")
        print(f"Should be -1000 or 1000: {abs(score) == 1000}")
        print("✓ PASSED" if abs(score) == 1000 else "✗ FAILED")
    else:
        print("State not terminal, skipping")

    # Test 4: Depth 0 uses heuristic
    print("\n=== Test 4: Depth 0 Uses Heuristic ===")
    grid = np.zeros((5, 5), dtype=int)
    state = game_state(grid, (2, 2), (0, 0), 1)

    score_d0, _ = alphabeta_max_h(state, heuristics.base_heuristic, depth=0)
    heuristic_direct = heuristics.base_heuristic(state)

    print(f"Score with depth=0: {score_d0}")
    print(f"Direct heuristic: {heuristic_direct}")
    print(f"Should match: {score_d0 == heuristic_direct}")
    print("✓ PASSED" if score_d0 == heuristic_direct else "✗ FAILED")

    # Test 5: Min vs Max
    print("\n=== Test 5: Min vs Max ===")
    grid = np.zeros((5, 5), dtype=int)
    state1 = game_state(grid, (2, 2), (0, 0), 1)  # P1's turn
    state2 = game_state(grid.copy(), (2, 2), (0, 0), 2)  # P2's turn

    max_score, _ = alphabeta_max_h(state1, heuristics.base_heuristic, depth=2)
    min_score, _ = alphabeta_min_h(state2, heuristics.base_heuristic, depth=2)

    print(f"Max score (P1): {max_score}")
    print(f"Min score (P2): {min_score}")
    print("✓ Both functions work")

    # Test 6: Performance check (should be fast with pruning)
    print("\n=== Test 6: Performance Check ===")
    import time
    grid = np.zeros((6, 6), dtype=int)
    state = game_state(grid, (1, 1), (4, 4), 1)

    start = time.time()
    score, move = alphabeta_max_h(state, heuristics.base_heuristic, depth=3)
    elapsed = time.time() - start

    print(f"Time for 6x6 board, depth=3: {elapsed:.3f} seconds")
    print(f"Score: {score}")
    print("✓ Completed" if elapsed < 10 else "⚠ Too slow - are you using alpha-beta pruning?")

    # Test 7: Returns correct format
    print("\n=== Test 7: Return Format ===")
    grid = np.zeros((4, 4), dtype=int)
    state = game_state(grid, (1, 1), (2, 2), 1)
    result = alphabeta_max_h(state, heuristics.base_heuristic, depth=2)

    print(f"Result type: {type(result)}")
    print(f"Is tuple: {isinstance(result, tuple)}")
    print(f"Length 2: {len(result) == 2}")

    score, move = result
    print(f"Score is number: {isinstance(score, (int, float))}")
    print(f"Move is game_state or None: {isinstance(move, game_state) or move is None}")
    print("✓ PASSED" if isinstance(result, tuple) and len(result) == 2 else "✗ FAILED")

    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    tests()