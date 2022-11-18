from board import Direction, Rotation, Shape, Action
from itertools import repeat
import random
class Player:
    def height(self, clone):
        col_height = [0, 0, 0, 0, 0, 0, 0, 0, 0,0]
        for x in range(clone.width):
            for y in range(clone.height):
                if (x, y) in clone.cells:
                    col_height[x] = clone.height - y
                    break
        return col_height

    def completed_lines(self, clone, oldscore):
        diff = clone.score - oldscore
        if 100 < diff < 130:
            return 1
        elif 400 < diff < 450:
            return 2
        elif 800 < diff < 850:
            return 3
        elif 1600 < diff < 1650:
            return 4
        else:
            return 0

    def check_holes(self, clone):
        holes = 0
        for y in range(10, clone.height):
            for x in range(clone.width):
                if (x, y) not in clone.cells and (x, (y - 1)) in clone.cells:
                    holes += 1
        return holes

    def bumpiness(self, heights):
        bumpy = 0
        for i in range(len(heights) - 1):
            bumpy += abs(heights[i] - heights[i + 1])
        return bumpy
    def choose_action(self, board):
        bestscore = float('-inf')
        bestmoves = []
        shaperot4 = [Shape.L, Shape.T, Shape.J]
        shaperot2 = [Shape.I, Shape.S, Shape.Z]
        try:
            x = 1
            if board.falling.shape in shaperot4:
                x = 5
            elif board.falling.shape in shaperot2:
                x = 3
            for rot in range(x):
                for pos in range(-5, 5):
                    tempMoves = []
                    clone = board.clone()
                    [clone.rotate(Rotation.Clockwise) for i in range(rot-1)]
                    tempMoves.extend(repeat(Rotation.Clockwise, rot-1))
                    if pos > 0:
                        [clone.move(Direction.Right) for i in range(abs(pos))]
                        tempMoves.extend(repeat(Direction.Right, pos))
                    if pos < 0:
                        [clone.move(Direction.Left) for i in range(abs(pos))]
                        tempMoves.extend(repeat(Direction.Left, abs(pos)))
                    clone.move(Direction.Drop)
                    tempMoves.append(Direction.Drop)
                    heights = self.height(clone)
                    scoreAgg = sum(heights) * -0.5
                    scoreLines = self.completed_lines(clone, board.score) * 0.7
                    scoreHoles = self.check_holes(clone) * -0.6
                    scoreBump = self.bumpiness(heights) * -0.2
                    score = scoreAgg + scoreLines + scoreHoles + scoreBump
                    if score > bestscore:
                        bestscore = score
                        bestmoves = tempMoves

        except:
            pass

        if random.random() > 0.5 and self.check_holes(clone) > self.check_holes(board) and board.discards_remaining > 0:
            if board.discards_remaining > 0:
                return Action.Discard
        return bestmoves

SelectedPlayer = Player