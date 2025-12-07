import math
from email.errors import NonASCIILocalPartDefect


def alphabeta_max(current_game, alpha=-math.inf, beta=math.inf):
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
        beta = min(beta, v)
        if v <= alpha:
            return v, None
    return v, best_move