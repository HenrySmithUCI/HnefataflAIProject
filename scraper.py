from bs4 import BeautifulSoup
from urllib import request, parse
import re

def getPage(url, params):
    data = parse.urlencode(params).encode()
    req = request.Request(url, data=data)
    resp = request.urlopen(req)
    html = resp.read()
    return BeautifulSoup(html, 'html.parser')

moveTranslate = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6,
                 '1' : 0, '2' : 1, '3' : 2, '4' : 3, '5' : 4, '6' : 5, '7' : 6}

class MoveException(Exception):
    pass

class Move:
    def __init__(self, player, moveMatch):
        self.player = player
        self.startCol = moveMatch.group(2)
        self.startRow = moveMatch.group(3)
        self.endCol = moveMatch.group(4)
        self.endRow = moveMatch.group(5)
        self.capture = bool(moveMatch.group(7))
        self.capCol = []
        self.capRow = []
        for i in [7, 9, 11]:
            if moveMatch.group(i):
                self.capCol.append(moveMatch.group(i - 1))
                self.capRow.append(moveMatch.group(i))
            else:
                break

    def start(self):
        return moveTranslate[self.startCol], moveTranslate[self.startRow]

    def end(self):
        return moveTranslate[self.endCol], moveTranslate[self.endRow]

    def cap(self):
        if self.capture:
            return [(moveTranslate[self.capCol[i]], moveTranslate[self.capRow[i]]) for i in range(len(self.capCol))]
        return [(None, None)]

    def __str__(self):
        result = self.player + ': ' + self.startCol + self.startRow + '-' + self.endCol + self.endRow
        if(self.capture):
            result += 'x' + self.capCol + self.capRow
        return result

class BoardState:
    def __init__(self, copy = None):
        self.black = []
        self.white = []
        self.king = []
        if(copy):
            self.black = [[j for j in i] for i in copy.black]
            self.white = [[j for j in i] for i in copy.white]
            self.king = [[j for j in i] for i in copy.king]
        else:
            self.black = [[0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 0, 0, 0, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0]]
            self.white = [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 1, 1, 1, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]]
            self.king =  [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]]

    def applyMove(self, move):
        sj, si = move.start()
        ej, ei = move.end()
        cap = move.cap()
        active = self.black if move.player == 'black' else self.white
        passive = self.white if move.player == 'black' else self.black
        if active[si][sj] == 0 or active[ei][ej] == 1 or passive[ei][ej] == 1:
            print("Invalid move", move, "applied to board", self, sep = '\n')
            raise MoveException
        if move.capture:
            for cj, ci in cap:
                if passive[ci][cj] == 0:
                    print("Invalid move", move, "applied to board", self, sep = '\n')
                    raise MoveException
        kingMove = move.player == 'white' and self.king[si][sj] == 1
        active[si][sj] = 0
        active[ei][ej] = 1
        if kingMove:
            self.king[si][sj] = 0
            self.king[ei][ej] = 1
        if move.capture:
            passive[ci][cj] = 0
        return self

    def __str__(self):
        result = '  A B C D E F G\n'
        for i in range(7):
            result += str(i + 1) + ' '
            for j in range(7):
                if self.king[i][j]:
                    char = 'K '
                elif self.white[i][j]:
                    char = 'W '
                elif self.black[i][j]:
                    char = 'B '
                else:
                    char = '. '
                result += char
            result += '\n'
        return result

    def serialize(self):
        return " ".join([str(j) for l in [self. black, self.white, self.king] for i in l for j in i])
            

def analyzeGame(gamePage):
    lastState = BoardState()
    boardStates = [lastState.serialize()]
    moveNums = [0]
    num = 0
    for tr in gamePage.find_all('tr'):
        row = tr.find_all('td', recursive=False)
        if len(row) >= 2:
            numText = row[0].find(string = True);
            if not numText:
                continue    #no row number, this is not a move line
            numMatch = re.match(re.compile('(\d+)\.'), str(numText))
            if not numMatch:
                continue    #not a row number, this is not a move line
            num += 1
            if num != int(numMatch.group(1)):
                print("Input mismatch, wrong row number:", numMatch.group(1))
                raise MoveException
            pattern = re.compile("(resigned|timeout)|([a-g])([1-7])-([a-g])([1-7])(?:x([a-g])([1-7]))?(?:x([a-g])([1-7]))?(?:x([a-g])([1-7]))?")
            for i in range(1, 3):
                if len(row) <= i:
                    break   #reached last move, no move for white
                moveText = row[i].find(string = True)
                moveMatch = re.match(pattern, str(moveText))
                if not moveMatch:
                    print("Input mismatch, unrecognizable move:", moveText)
                    raise MoveException
                if moveMatch.group(1):
                    break   #a player resigned
                newState = BoardState(lastState)
                lastState = newState.applyMove(Move('black' if i == 1 else 'white', moveMatch))
                boardStates.append(newState.serialize())
                moveNums.append(num)
    winPattern = re.compile("(?:(Black|White) won\.|(Draw)\.)")
    winMatch = re.match(winPattern, str(gamePage.find(string = winPattern)).strip())
    if not winMatch:
        print("No win state found.")
        raise MoveException
    winValue = 0
    if winMatch.group(1):
        winValue = (1 if winMatch.group(1) == "Black" else -1)
    boardValues = [str(winValue / (num - sNum + 1)) for sNum in moveNums]
    return "\n".join([item for pair in zip(boardStates, boardValues) for item in pair])
                

def main(numGames):
    url = 'http://aagenielsen.dk/visallespil.php'
    values = {'mere' : '1', 'alias1' : '', 'alias2' : '', 'spiltype' : '51'}
    gameList = getPage(url, values)
    data = []
    count = 0
    for table in gameList.body.find_all('table'):
        tds = table.find_all('td')
        if len(tds) == 3 and len(tds[2].find_all(string = re.compile("ongoing"))) == 0:
            url = 'http://aagenielsen.dk/visspil.php'
            values = {}
            count += 1
            for inp in tds[1].form.find_all('input'):
                values[inp['name']] = inp['value']
            try:
                data.append(analyzeGame(getPage(url, values)))
            except MoveException:
                print("Exception on #:", count)
            if numGames > 0 and count >= numGames:
                break
    outFile = open("data.txt", 'w')
    outFile.write('\n'.join(data))

main(0)