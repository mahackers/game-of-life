import io
import argparse
import os
import time

class Grid(object):

    def __init__(self, grid):
        self.grid = grid

    def next_grid(self):
        new_grid = []
        for r in range(len(self.grid)):
            line = []
            for c in range(len(self.grid[0])):
                line.append(self.cell_survives(r, c))
            new_grid.append(line)
        return Grid(new_grid)


    def cell_survives(self, r, c):
        adj_cells = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                radj = (r + i) % len(self.grid)
                cadj = (c + j) % len(self.grid[0])
                if not (i == 0 and j == 0) and self.grid[radj][cadj]:
                    adj_cells += 1

        if adj_cells <= 1:
            return False
        elif adj_cells == 2:
            return self.grid[r][c]
        elif adj_cells == 3:
            return True
        elif adj_cells > 3:
            return False

    @classmethod
    def from_repr(cls, string):
        stream = io.StringIO(string)
        return Grid.from_stream(stream)

    @classmethod
    def from_stream(cls, stream):
        rows = int(stream.readline())
        cols = int(stream.readline())
        grid = []
        for line in stream.read().splitlines():
            row = []
            for char in line:
                if char == '-':
                    row.append(False)
                else:
                    row.append(True)
            grid.append(row)
        grid.remove([])

        return Grid(grid)

    def __repr__(self):
        str_output = ''
        str_output += str(len(self.grid)) + '\n'
        str_output += str(len(self.grid[0])) + '\n'
        return str_output

    def __str__(self):
        str_output = ''
        for row in self.grid:
            for alive in row:
                if alive:
                    str_output += 'X'
                else:
                    str_output += '-'

            str_output += '\n'
        return str_output


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


parser = argparse.ArgumentParser(description='Runs a conway\'s game of life simulation')
parser.add_argument('file', type=str,
                    help='the file to read the setup from')
parser.add_argument('-n', dest='num', type=int,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

f = open(args.file, "r", encoding="utf-8" )

grid = Grid.from_stream(f)


clearScreen()
for i in range(0, args.num):
    print(str(grid))
    time.sleep(.4)
    clearScreen()
    grid = grid.next_grid()


