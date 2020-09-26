from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# ==================MY CODE STARTS HERE==================

# dictionary to return the opposite direction
reverse_direction = {"n": "s", "s": "n", "e": "w", "w": "e"}


def dft_recursive(graph, cur_room, prev=None, direction=None, visited=None, path=None):
    # set visited to an empty set, and path to an empty array if first time through
    if visited is None:
        visited = set()
    if path is None:
        path = []
    exits = {}

    # if cur_room has already been visited: end recursion
    if cur_room in visited:
        return

    # if cur_room hasn't been visited, then proceed further
    # find all exits for this room
    for exit_direction in cur_room.get_exits():
        exits[exit_direction] = "?"

    # add the current room, and all of it's exits, to graph
    # also add the current room to the list of visited rooms
    graph[cur_room.id] = exits
    visited.add(cur_room)

    # skip this if NOT coming from a room (aka: on first time through)
    if prev is not None:
        path.append(direction)
        # previous room and current room point/reference each other ('connect' them)
        graph[prev.id][direction] = cur_room.id
        graph[cur_room.id][reverse_direction[direction]] = prev.id

    # find exits in current room that haven't been explored yet (exit == "?")
    for exit_ in cur_room.get_exits():
        if graph[cur_room.id][exit_] == "?":
            # if the current room exits have NOT been explored:
            if cur_room.get_room_in_direction(exit_) not in visited:
                # explore the new, unexplored room for exits and a new path
                _prev = cur_room
                _dir = exit_
                _cur_room = cur_room.get_room_in_direction(exit_)
                dft_recursive(graph, _cur_room, _prev, _dir, visited, path)
                # after new room is explored, and returns the path it took, assign to path list
                path.append(reverse_direction[exit_])

    return path


traversal_path = dft_recursive({}, player.current_room)
# ===========END OF MY CODE=================

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
