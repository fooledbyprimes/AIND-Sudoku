# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem? 
A: The naked twins problem is local to a game board unit.  We can implement the naked twin problem solution by operating only in such a unit and only with data related to it and the boxes within it.  Therefore, if a naked twin is detected we can eliminate box value possibilities without knowing anything about surrounding units on the board.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem? 
A: We simply encode the two extra diagonals as new units for the puzzle board.  Boxes then gain new peers depending on if they are positioned within the diagonals.  The infrastructure setup prior for row, column, and square units can then augmented with relative ease.  This preexisting infrastructure already implements constraint propagation.  Thus, implementing the diagonal units does not make the computational requirements as unwieldy as we initially thought and the overall computer program can remain resistant to much change.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
