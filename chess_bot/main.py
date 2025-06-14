import pygame
import json
import os
import time
from ai import make_ai_move

WIDTH, HEIGHT = 600, 680
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
GRAY = (119, 136, 153)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

images = {}
score = {"w": 0, "b": 0}
win_tracker_path = "win_tracker.json"

if not os.path.exists(win_tracker_path) or os.stat(win_tracker_path).st_size == 0:
    with open(win_tracker_path, "w") as f:
        json.dump({"player": 0, "ai": 0}, f)

with open(win_tracker_path, "r") as f:
    win_tracker = json.load(f)

board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["wp"] * 8,
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for p in pieces:
        images[p] = pygame.transform.scale(pygame.image.load(f"assets/{p}.png"), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(win):
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if (r + c) % 2 == 0 else GRAY
            pygame.draw.rect(win, color, (c*SQUARE_SIZE, r*SQUARE_SIZE+80, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece != "":
                win.blit(images[piece], (c*SQUARE_SIZE, r*SQUARE_SIZE+80))

def draw_moves(win, moves):
    for r, c in moves:
        pygame.draw.circle(win, GREEN, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2 + 80), 10)

def draw_ui(win, timer_white, timer_black):
    font = pygame.font.SysFont("arial", 22)
    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, 80))
    text = font.render(f"White: {score['w']} | Black: {score['b']}", True, BLACK)
    win.blit(text, (10, 10))
    win.blit(font.render(f"Timer W: {int(timer_white)}s", True, BLACK), (10, 40))
    win.blit(font.render(f"Timer B: {int(timer_black)}s", True, BLACK), (150, 40))
    win.blit(font.render(f"Wins - You: {win_tracker['player']} | AI: {win_tracker['ai']}", True, BLACK), (300, 10))
    pygame.draw.rect(win, RED, (480, 40, 100, 30))
    win.blit(font.render("Restart", True, WHITE), (490, 42))

def move_piece(start, end):
    sr, sc = start
    er, ec = end
    captured = board[er][ec]
    if captured != "":
        score[board[sr][sc][0]] += 1
    board[er][ec] = board[sr][sc]
    board[sr][sc] = ""

def is_game_over():
    kings = {"wK": False, "bK": False}
    for row in board:
        for cell in row:
            if cell in kings:
                kings[cell] = True
    if not kings["wK"]:
        win_tracker["ai"] += 1
        return "AI Wins"
    elif not kings["bK"]:
        win_tracker["player"] += 1
        return "You Win"
    return None

def get_possible_moves(pos):
    r, c = pos
    piece = board[r][c]
    moves = []
    if not piece.startswith("w"):
        return moves

    directions = {
        "wp": [(-1, 0), (-2, 0), (-1, -1), (-1, 1)],
        "wN": [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
        "wR": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        "wB": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        "wQ": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        "wK": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    }

    if piece == "wp":
        if r - 1 >= 0 and board[r - 1][c] == "":
            moves.append((r - 1, c))
            if r == 6 and board[r - 2][c] == "":
                moves.append((r - 2, c))
        if r - 1 >= 0 and c - 1 >= 0 and board[r - 1][c - 1].startswith("b"):
            moves.append((r - 1, c - 1))
        if r - 1 >= 0 and c + 1 < 8 and board[r - 1][c + 1].startswith("b"):
            moves.append((r - 1, c + 1))
    elif piece in directions:
        for dr, dc in directions[piece]:
            for i in range(1, 8 if piece in ["wR", "wB", "wQ"] else 2):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = board[nr][nc]
                    if target == "":
                        moves.append((nr, nc))
                    elif target.startswith("b"):
                        moves.append((nr, nc))
                        break
                    else:
                        break
    return moves

def reset_game():
    global board, score, player_turn, selected, legal_moves, timer_white, timer_black, start_time
    board[:] = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["wp"] * 8,
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    score = {"w": 0, "b": 0}
    player_turn = "w"
    selected = None
    legal_moves = []
    timer_white = 300
    timer_black = 300
    start_time = time.time()

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess Bot")
load_images()
TIMER_FONT = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()

selected = None
legal_moves = []
player_turn = "w"
timer_white = 300
timer_black = 300
start_time = time.time()
game_over_text = None

running = True
while running:
    clock.tick(60)
    current_time = time.time()
    elapsed = current_time - start_time
    if player_turn == "w":
        timer_white -= elapsed
    else:
        timer_black -= elapsed
    start_time = current_time

    if timer_white <= 0:
        game_over_text = "AI Wins (Time)"
        win_tracker["ai"] += 1
    elif timer_black <= 0:
        game_over_text = "You Win (Time)"
        win_tracker["player"] += 1

    win.fill(WHITE)
    draw_ui(win, max(0, timer_white), max(0, timer_black))
    draw_board(win)
    draw_moves(win, legal_moves)
    draw_pieces(win)
    pygame.display.flip()

    if not game_over_text:
        result = is_game_over()
        if result:
            game_over_text = result
            with open(win_tracker_path, "w") as f:
                json.dump(win_tracker, f)

    if game_over_text:
        font = pygame.font.SysFont("arial", 30)
        text = font.render(game_over_text + " | Click Restart", True, RED)
        win.blit(text, (50, HEIGHT // 2))
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open(win_tracker_path, "w") as f:
                json.dump(win_tracker, f)
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 480 <= mx <= 580 and 40 <= my <= 70:
                reset_game()
                game_over_text = None
                continue
            if player_turn == "w" and not game_over_text:
                row, col = (my - 80) // SQUARE_SIZE, mx // SQUARE_SIZE
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected and (row, col) in legal_moves:
                        move_piece(selected, (row, col))
                        selected = None
                        legal_moves = []
                        player_turn = "b"
                    elif board[row][col].startswith("w"):
                        selected = (row, col)
                        legal_moves = get_possible_moves((row, col))
                    else:
                        selected = None
                        legal_moves = []

    if player_turn == "b" and not game_over_text:
        pygame.time.wait(500)
        ai_move = make_ai_move(board)
        if ai_move:
            move_piece(ai_move[0], ai_move[1])
        player_turn = "w"

pygame.quit()
