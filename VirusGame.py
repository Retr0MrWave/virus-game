class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.p1 = [[0, 0]]
        self.p2 = [[height-1, width-1]]
        self.p1c = []
        self.p2c = []
    
    def goodp1c(self):
        r = []
        look_through = self.p1.copy()
        for cell in look_through:
            if [cell[0] - 1, cell[1]] in self.p1c and not([cell[0] - 1, cell[1]] in r):
                r.append([cell[0] - 1, cell[1]].copy())
                look_through.append([cell[0] - 1, cell[1]].copy())
            if [cell[0] + 1, cell[1]] in self.p1c and not([cell[0] + 1, cell[1]] in r):
                r.append([cell[0] + 1, cell[1]].copy())
                look_through.append([cell[0] + 1, cell[1]].copy())
            if [cell[0], cell[1] - 1] in self.p1c and not([cell[0], cell[1] - 1] in r):
                r.append([cell[0], cell[1] - 1].copy())
                look_through.append([cell[0], cell[1] - 1].copy())
            if [cell[0], cell[1] + 1] in self.p1c and not([cell[0], cell[1] + 1] in r):
                r.append([cell[0], cell[1] + 1].copy())
                look_through.append([cell[0], cell[1] + 1].copy())
        return r.copy()
        
    def goodp2c(self):
        r = []
        look_through = self.p2.copy()
        for cell in look_through:
            if [cell[0] - 1, cell[1]] in self.p2c and not([cell[0] - 1, cell[1]] in r):
                r.append([cell[0] - 1, cell[1]].copy())
                look_through.append([cell[0] - 1, cell[1]].copy())
            if [cell[0] + 1, cell[1]] in self.p2c and not([cell[0] + 1, cell[1]] in r):
                r.append([cell[0] + 1, cell[1]].copy())
                look_through.append([cell[0] + 1, cell[1]].copy())
            if [cell[0], cell[1] - 1] in self.p2c and not([cell[0], cell[1] - 1] in r):
                r.append([cell[0], cell[1] - 1].copy())
                look_through.append([cell[0], cell[1] - 1].copy())
            if [cell[0], cell[1] + 1] in self.p2c and not([cell[0], cell[1] + 1] in r):
                r.append([cell[0], cell[1] + 1].copy())
                look_through.append([cell[0], cell[1] + 1].copy())
        return r.copy()

    def validateMove(self, player, move):
        if move[0] < 0 or move[1] < 0 or move[0] >= self.width or move[1] >= self.height:
            return False
        if player == 1:
            p1gc = self.goodp1c()
            if move in self.p1 or move in self.p1c or move in self.p2c:
                return False
            gc1 = self.p1.copy() + p1gc.copy()
            if [move[0]-1, move[1]] in gc1 or [move[0]+1, move[1]] in gc1 or [move[0], move[1]-1] in gc1 or [move[0], move[1]+1] in gc1:
                return True
            else:
                return False
        else:
            p2gc = self.goodp2c()
            if move in self.p2 or move in self.p2c or move in self.p1c:
                return False
            gc2 = self.p2.copy() + p2gc.copy()
            if [move[0]-1, move[1]] in gc2 or [move[0]+1, move[1]] in gc2 or [move[0], move[1]-1] in gc2 or [move[0], move[1]+1] in gc2:
                return True
            else:
                return False
        return False
    
    def makeMove(self, player, move):
        if not(self.validateMove(player, move.copy())):
            return False
        if player == 1:
            if move in self.p2:
                self.p1c.append(move.copy())
                self.p2.remove(move.copy())
            else:
                self.p1.append(move.copy())
        elif player == 2:
            if move in self.p1:
                self.p2c.append(move.copy())
                self.p1.remove(move.copy())
            else:
                self.p2.append(move.copy())
        return True

    def checkGameEnd(self, player):
        for i in range(self.width):
            for j in range(self.height):
                if self.validateMove(player, [i, j].copy()):
                    return False
        return True

    def getString(self):
        sarr = []
        t = []
        for i in range(self.width):
            t.append('.')
        for i in range(self.height):
            sarr.append(t.copy())
        for cell in self.p1:
            sarr[cell[0]][cell[1]] = 'X'
        for cell in self.p2:
            sarr[cell[0]][cell[1]] = 'O'
        for cell in self.p1c:
            sarr[cell[0]][cell[1]] = 'C'
        for cell in self.p2c:
            sarr[cell[0]][cell[1]] = 'P'
        s = ""
        for i in sarr:
            for j in i:
                s += j
            s += '\n'
        return s
