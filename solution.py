from collections import Counter
import numpy as np

assignments = []

digits = '123456789'
cols = digits
rows = 'ABCDEFGHI'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# here is a good excuse to try some numpy features
diagonal_units = [
    list(np.diagonal(row_units)),
    list(np.diag(np.fliplr(row_units)))]

unitlist = row_units + column_units + square_units + diagonal_units
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

    # Find all instances of naked twins

    # Once a unit with twins is found we'll return a tuple with
    # the unit and the filtered value counts
    # Ex:
    #(['B1', 'B2', ... ], [('27', 2),... ]

    count_if_twin = 2
    filtered_counts = [(unit,
               list(filter(
                   lambda val_count: val_count[1] == count_if_twin,
                   Counter(list(map(lambda u: values[u], unit))).most_common()
               ))
               )
              for unit in unitlist]

    # We need to filter string values that are not len of 2.
    # So, for example, the first tuple below would be omitted but keep second tuple.
    # don't keep: (['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'], [('379', 2)])
    # keep:       (['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'], [('17' , 2)])

    filtered_units = [(u, c[0][0]) for u,c in filtered_counts
                      if c and len(c[0][0]) == count_if_twin]

    # Eliminate the naked twins as possibilities for their peers
    for (unit, twin) in filtered_units:
        for box in unit:
            v = values[box]
            targets = list(set(twin) & set(v))
            if v != twin and len(v) > 2 and targets:
                new_val = list(v)
                for t in targets:
                    new_val.remove(t)
                assign_value(values, box, "".join(new_val))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board = {}
    for i, box in enumerate(boxes):
        if grid[i] == '.':
            board[box] = '123456789'
        else:
            board[box] = grid[i]

    return board

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # this is pretty straightforward but maybe too much nesting
    for k, v in values.items():
        if len(v) == 1:
            for p in peers[k]:
                vals = values[p]
                if v in vals and len(vals) > 1:
                    chars = list(vals)
                    chars.remove(v)
                    assign_value(values, p, "".join(chars))

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    for unit in unitlist:
        targets = [box for box in unit if len(values[box]) > 1]
        if len(targets) > 0:
            digits = "".join([values[box] for box in targets])
            counted = Counter(digits).most_common()
            # counted is sorted so just use the last item
            if counted[-1][1] == 1:
                onechoice = counted[-1][0]
                for box in targets:
                    if onechoice in values[box]:
                        assign_value(values, box, onechoice)
                        return values
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply various strategies
        eliminate(values)
        only_choice(values)
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    unfilled = [(len(values[box]), box)
                for box in boxes
                    if len(values[box]) > 1]
    if len(unfilled) == 0:
        return values
    unfilled.sort()
    box_key = unfilled[0][1]

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for val in values[box_key]:
        vals_copy = values.copy()
        assign_value(vals_copy, box_key, val)
        dfs_next = search(vals_copy)
        if dfs_next:
            return dfs_next


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return reduce_puzzle(grid_values(grid))



if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        # For OSX 10.10.5 had to install XQuartz app from thirdparty
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
