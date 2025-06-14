import copy

piece_value = {
    "p": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 1000
}

def make_ai_move(board, depth=3):
    best_score = float("-inf")
    best_move = None

    for r in range(8):
        for c in range(8):
            if board[r][c].startswith("b"):
                moves = get_possible_moves(board, r, c)
                for move in moves:
                    new_board = copy.deepcopy(board)
                    apply_move(new_board, (r, c), move)
                    score = minimax(new_board, depth - 1, False, float("-inf"), float("inf"))
                    if score > best_score:
                        best_score = score
                        best_move = ((r, c), move)
    return best_move

def minimax(board, depth, maximizing, alpha, beta):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board)

    if maximizing:
        max_eval = float("-inf")
        for r in range(8):
            for c in range(8):
                if board[r][c].startswith("b"):
                    for move in get_possible_moves(board, r, c):
                        new_board = copy.deepcopy(board)
                        apply_move(new_board, (r, c), move)
                        eval = minimax(new_board, depth - 1, False, alpha, beta)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
        return max_eval
    else:
        min_eval = float("inf")
        for r in range(8):
            for c in range(8):
                if board[r][c].startswith("w"):
                    for move in get_possible_moves_for_white(board, (r, c)):
                        new_board = copy.deepcopy(board)
                        apply_move(new_board, (r, c), move)
                        eval = minimax(new_board, depth - 1, True, alpha, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return min_eval

def evaluate_board(board):
    score = 0
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece:
                value = piece_value.get(piece[1], 0)
                if piece[0] == "b":
                    score += value
                    if piece[1] == "K":
                        score += king_safety_bonus(board, "b", (r, c))
                else:
                    score -= value
                    if piece[1] == "K":
                        score -= king_safety_bonus(board, "w", (r, c))
    return score

def king_safety_bonus(board, color, pos):
    r, c = pos
    bonus = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc].startswith(color):
                bonus += 1
    return bonus * 50

def apply_move(board, start, end):
    sr, sc = start
    er, ec = end
    board[er][ec] = board[sr][sc]
    board[sr][sc] = ""

def get_possible_moves(board, r, c):
    piece = board[r][c]
    moves = []
    directions = get_directions(piece)
    if piece == "bp":
        if r + 1 < 8 and board[r + 1][c] == "":
            moves.append((r + 1, c))
            if r == 1 and board[r + 2][c] == "":
                moves.append((r + 2, c))
        for dc in [-1, 1]:
            nr, nc = r + 1, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc].startswith("w"):
                moves.append((nr, nc))
    elif piece == "bN":
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board[nr][nc] == "" or board[nr][nc].startswith("w"):
                    moves.append((nr, nc))
    elif piece in ["bR", "bB", "bQ"]:
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if board[nr][nc] == "":
                        moves.append((nr, nc))
                    elif board[nr][nc].startswith("w"):
                        moves.append((nr, nc))
                        break
                    else:
                        break
    elif piece == "bK":
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board[nr][nc] == "" or board[nr][nc].startswith("w"):
                    moves.append((nr, nc))
    return moves

def get_possible_moves_for_white(board, pos):
    from main import get_possible_moves
    return get_possible_moves(pos)

def is_terminal(board):
    kings = [cell for row in board for cell in row if "K" in cell]
    return len(kings) < 2

def get_directions(piece):
    if piece == "bN":
        return [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    elif piece == "bR":
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif piece == "bB":
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    elif piece == "bQ":
        return get_directions("bR") + get_directions("bB")
    elif piece == "bK":
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    return []
