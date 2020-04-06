from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def a_star(matrix, start, end, cross=False, show=False):
    grid = Grid(matrix=matrix)
    grid_start = grid.node(start[0], start[1])
    grid_end = grid.node(end[0], end[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    if cross:
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    path, runs = finder.find_path(grid_start, grid_end, grid)

    if show:
        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))
    return path
