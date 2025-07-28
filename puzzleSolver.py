from collections import deque

def solve_queens(matrix):
    positions = [-1] * len(matrix)
    board = [[int(cell[1]) for cell in row] for row in matrix]

    def solve(N, row):
        if row == N:
            return True

        for curr in range(N):
            flag = True

            # Check column conflict
            for prev_index in range(row):
                if curr == positions[prev_index]:
                    flag = False

            # Check adjacency and color constraints
            if row != 0:
                if abs(curr - positions[row - 1]) == 1 or is_color_taken_traversal(row, curr):
                    flag = False

            if flag:
                positions[row] = curr
                if solve(N, row + 1):
                    return True
                positions[row] = -1  # Backtrack

        return False

    def is_color_taken_traversal(row, col):
        target_value = board[row][col]
        rows = len(board)
        cols = len(board[0])

        visited = set()
        queue = deque()
        queue.append((row, col))
        visited.add((row, col))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        while queue:
            r, c = queue.popleft()

            if positions[r] == c:
                return True

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    (nr, nc) not in visited and
                    board[nr][nc] == target_value
                ):
                    queue.append((nr, nc))
                    visited.add((nr, nc))

        return False

    solve(len(board), 0)

    # Apply the solution to the puzzle board
    return [matrix[i][j][0] for i, j in enumerate(positions)]

