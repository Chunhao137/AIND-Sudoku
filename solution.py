assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#dialog constraint
forward_diagonal = [rd+cd for rd in rows for cd in cols if rows.index(rd) == cols.index(cd) ]
back_diagonal = [rd+cd for rd in rows for cd in cols[::-1] if rows.index(rd)== cols[::-1].index(cd)]

unitlist = row_units + column_units + square_units + [forward_diagonal] + [back_diagonal]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    # get only values that are of length 2
    only_boxes_with_values_of_length_2 = [key for key, value in values.items() if len(values[key])==2]
    for box in only_boxes_with_values_of_length_2:
        for unit in units[box]:
            #look for peers in the unit
            for peer in set(unit).intersection(set(peers[box])):
                # If the items in the unit has the same value as the square
                # and the the item is not the same as the box
                # it is a naked twin and we can go ahead and remove the values
                # from it's peers
                if not set(values[peer]).difference(set(values[box])):
                    firstDigit  = values[box][0]
                    secondDigit = values[box][1]
                    # make sure all items in the unit are different
                    # from the box and peer we are comparing to
                    for item in set(unit).difference(set([box,peer])):
                        if firstDigit in values[item]:
                            assign_value(values, item, values[item].replace(firstDigit,''))
                        if secondDigit in values[item]:
                            assign_value(values, item, values[item].replace(secondDigit,''))

    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values=values, box=dplaces[0], value=digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    return search(grid_values(grid))

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[s]) ==1 for s in boxes):
        return values # you solved it
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s])>1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
