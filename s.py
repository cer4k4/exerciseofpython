def is_safe(board, row, col, n):
    # بررسی ستون
    for i in range(row):
        if board[i][col] == "Q":
            return False

    # بررسی قطر چپ بالا
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == "Q":
            return False
        i -= 1
        j -= 1

    # بررسی قطر راست بالا
    i, j = row, col
    while i >= 0 and j < n:
        if board[i][j] == "Q":
            return False
        i -= 1
        j += 1

    return True

def solve_nqueen(board, row, n):
    if row == n:
        return True  # همه وزیرها گذاشته شدن

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = "Q"
            if solve_nqueen(board, row+1, n):
                return True
            board[row][col] = " "  # بک‌ترک

    return False

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

n = 14
board = [[" " for _ in range(n)] for _ in range(n)]
solve_nqueen(board, 0, n)
print_board(board)
