import math
from email.errors import NonASCIILocalPartDefect

import numpy as np
from game_state import game_state
import alpha_beta_isoKnight
import minimax_isoKnight

def alphabeta_max(current_game, alpha=-math.inf, beta=math.inf):
    #add code here for alpha-beta
    if current_game.is_terminal():
        return current_game.get_score(), None

    v = -math.inf
    best_move = None
    moves = current_game.get_moves()

    for move in moves:
        maxVal, idc = alphabeta_min(move, alpha, beta)
        if v < maxVal:
            v = maxVal
            best_move = move
        alpha = max(alpha, v)
        if v >= beta:
            return v, None
    return v, best_move

def alphabeta_min(current_game, alpha=-math.inf, beta=math.inf):
    #add code here for alpha-beta
    if current_game.is_terminal():
        return current_game.get_score(), None
    v = math.inf
    best_move = None
    moves = current_game.get_moves()

    for move in moves:
        maxVal, idc = alphabeta_max(move, alpha, beta)
        if v > maxVal:
            v = maxVal
            best_move = move
        beta = min(beta, v)
        if v <= alpha:
            return v, None
    return v, best_move

def maximin(current_game, alpha=-math.inf, beta=math.inf):
    if current_game.is_terminal():
        return current_game.get_score(), None
    v = -math.inf
    # best_move = None
    moves = current_game.get_moves()
    for move in moves:
        mx, next_move = minimax(move)
        if v < mx:
            v = mx
            best_move = move
        #add code here for alpha-beta algorithm
        alpha = max(alpha, v)
        if v >= beta:
            return v, None
    return v, best_move


def minimax(current_game, alpha=-math.inf, beta=math.inf):
    if current_game.is_terminal():
        return current_game.get_score(), None
    v = math.inf
    # best_move = None
    moves = current_game.get_moves()
    for move in moves:
        mx, next_move = maximin(move)
        if v > mx:
            v = mx
            best_move = move
        #add code here for alpha-beta algorithm
        beta = min(beta, v)
        if v <= alpha:
            return v, None
    return v, best_move

def tests():
    print("Test 1: Basic Alpha-Beta Test")
    grid = np.zeros((3, 3), dtype=int)
    state = game_state(grid, (0, 1), (2, 1), 1)
    score, move = alpha_beta_isoKnight.alphabeta_max(state)
    print(f"Score: {score}, Move found: {move is not None}")

    # Test 2: Compare with minimax (should give same result)
    print("\nTest 2: Alpha-Beta vs Minimax")
    grid = np.zeros((3, 3), dtype=int)
    state = game_state(grid, (0, 1), (2, 1), 1)
    ab_score, _ = alpha_beta_isoKnight.alphabeta_max(state)
    mm_score, _ = minimax_isoKnight.maximin(state)
    print(f"Alpha-Beta: {ab_score}, Minimax: {mm_score}")
    print(f"Match: {ab_score == mm_score}")

    # Test 3: Test terminal state
    print("\nTest 3: Terminal State")
    grid = np.zeros((3, 3), dtype=int)
    grid[0, 1] = 1
    grid[2, 1] = 2
    # Fill positions to create terminal state
    for i in range(3):
        for j in range(3):
            if (i, j) != (0, 1) and (i, j) != (2, 1):
                grid[i, j] = 1
    state = game_state(grid, (0, 1), (2, 1), 1)
    if state.is_terminal():
        score, move = alpha_beta_isoKnight.alphabeta_max(state)
        print(f"Terminal score: {score}")


if __name__ == "__main__":
    tests()