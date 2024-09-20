def doctor_strange(positions_original, pyramid, expected):
    positions = [0] * 16
    for x in range(len(positions_original)):
        positions[x] = []
        for i in positions_original[x]:
            positions[x].append(i)
    listed = list(pyramid)
    for color in listed:
        for roll in range(1,4):
            new_positions = move_AI(positions[:], color, roll)
            if len(pyramid) == 1:
                rankings = get_rankings_AI(new_positions)
                for color_test in expected.keys():
                    if rankings[0] == color_test:
                        expected[color_test] += 5
                    elif rankings[1] == color_test:
                        expected[color_test] += 1
                    else:
                        expected[color_test] -= 1
                return expected
            return doctor_strange(new_positions[:], pyramid - {color}, expected)


def move_AI(posits, color, roll):
    positions = posits
    ### BEGIN SOLUTION
    for position in range(len(positions)):
        for i in range(len(positions[position])):
            if positions[position][i] == color:
                for k in range(i, len(positions[position])):
                    if (position + roll) < 16:
                        positions[position + roll].append(positions[position][k])
                    else:
                        positions[15].append(positions[position][k])
                        
                positions[position] = positions[position][:i]
                return positions
    ### END SOLUTION
    return positions


def get_rankings_AI(positions):
    camels_found = []
    for position_index in range(len(positions) - 1, -1, -1):
        position = positions[position_index]
        for camel_index in range(len(position) - 1, -1,  -1):
            if len(camels_found) < 2:
                camels_found.append(position[camel_index])
            else:
                return tuple(camels_found)