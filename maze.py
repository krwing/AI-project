from queue import PriorityQueue

def load_maze(file_path):
    maze = []
    with open(file_path, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip().split()]
            maze.append(row)
    return maze


# Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def path_search(maze, start, end):
    # Initialize list
    list = PriorityQueue()
    list.put((0, start))
    path = {}
    # Cost from start to a node
    start_cost = {start: 0}
    # Estimated cost from start to end through a node
    f_score = {start: heuristic(start, end)}

    while not list.empty():
        pos = list.get()[1]

        if pos == end:
            return True  # Find possible path


        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Explore neighbors
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])

            # Ensure within bounds and passable
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[0]][neighbor[1]] == 0:
                temp = start_cost[pos] + 1

                if neighbor not in start_cost or temp < start_cost[neighbor]:
                    path[neighbor] = pos
                    start_cost[neighbor] = temp
                    f_score[neighbor] = temp + heuristic(neighbor, end)
                    list.put((f_score[neighbor], neighbor))

    return False  # Can't find path



#Load the maze from file
file_path="C:/Graduate/AI/project1/maze.txt"
maze = load_maze(file_path)

start_point = (1, 1)
end_point = (1, 8)

if path_search(maze, start_point, end_point):
    print("YES")
else:
    print("No")