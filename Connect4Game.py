class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

    def __repr__(self):
        """This method returns a string representation for an object of type Board."""
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'
        s += (2*self.width + 1) * '-'   # Bottom of the board
        
        # Add code here to put the numbers underneath
        s += '\n' + ' ' #new row
        for col in range(0, self.width):
            s += str(col % 10) + ' '
        return s       # The board is complete; return it

    def addMove(self, col, ox):
        """drops a checker with ox (either 'X' or 'O') into column col"""
        for row in range(0,self.height):
            if self.data[-1-row][col] == ' ':
                self.data[-1-row][col] = ox
                break
    
    def clear(self):
        """clears the board"""
        for row in range(0,self.height):
            for col in range(0, self.width):
                self.data[row][col] = ' '
    
    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'

    def allowsMove(self,c):
        """returns True if the calling object allows a move into column c.
        Returns False if it is not a legal move or if the column c is full."""

        if 0 <= c < self.width:
            if self.data[0][c] == ' ':
                return True
        return False
    
    def isFull(self):
        """returns True if Board is completely full of checkers"""
        for i in range(0,self.width):
            if self.allowsMove(i):
                return False
        return True

    def delMove(self,c):
        """removes the top checker from column c"""
        for i in range(0,self.height):
            if self.data[i][c] != ' ':
                self.data[i][c] = ' '
                break
    
    def winsFor(self,ox):
        """returns True if there are 4 checkers of type ox in a row on the board"""

        for row in range(0,self.height):
            for col in range(0,self.width):
                if inarow_Neast(ox,row,col,self.data,4) or inarow_Nsouth(ox,row,col,self.data,4) or \
                    inarow_Nnortheast(ox,row,col,self.data,4) or inarow_Nsoutheast(ox,row,col,self.data,4):
                    return True
        return False
    
    def hostGame(self):
        """hosts a game of Connect-4 alternating between turns 'X' and 'O'
        """
        print("\nWelcome to Connect Four!")
        b = Board(7,6)
        turn = 'O'

        while True:
            print()
            print(b)
            print()

            if turn == 'O':
                turn = 'X'
                place = -1    # Note! This -1 is _intentionally_ not valid!
                while b.allowsMove(place) == False:  # _while_ not valid
                    place = int(input(turn + "'s choice: "))  # ask for a column
                b.addMove(place, turn)
                if b.winsFor(turn):
                    print('X wins. Congratulations! :)')
                    break
            else: 
                turn = 'O'
                place = -1    # Note! This -1 is _intentionally_ not valid!
                while b.allowsMove(place) == False:  # _while_ not valid
                    place = self.aiMove(turn)
                if b.allowsMove(place):
                    b.addMove(place, turn)
                if b.winsFor(turn):
                    print('O wins. Congratulations! :)')
                    break


    def colsToWin(self,ox):
        """returns the list of columns where player ox can move in the next turn to win & finish the game
        """
        W = self.width
        rows = []

        for c in range(W):
            if self.allowsMove(c):
                self.addMove(c,ox)
                if self.winsFor(ox):
                    rows += [c]
                self.delMove(c)
        return rows
    
    def aiMove(self,ox):
        """accepts argument ox, the player X or O, and returns an integer representing
        the legal column in which to make a move
        """
        if len(self.colsToWin(ox)) > 0:
            return self.colsToWin(ox)[0]
        if ox == 'X':
            other = 'O'
        else:
            other = 'X'
        if len(self.colsToWin(other)) > 0:
            return self.colsToWin(other)[0]
        for i in [3,2,4,1,5,0,6]:
            if self.allowsMove(i):
                return i

        





#Helper Functions
def inarow_Neast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
    within the 2d list-of-lists A (array),
    returns True if there are N ch's in a row
    heading east and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start > H - 1:
        return False            # Out-of-bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False            # O.o.b. column
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start][c_start+i] != ch: # A mismatch!
            return False
    return True                 # All offsets succeeded, so we return True

def inarow_Nsouth(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading south and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start] != ch: # A mismatch!
            return False
    return True                 # All offsets succeeded, so we return True

def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading northeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start - (N-1) < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start-i][c_start+i] != ch: # A mismatch!
            return False
    return True                 # All offsets succeeded, so we return True

def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading southeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False            # Out-of-bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False            # O.o.b. column
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start+i] != ch: # A mismatch!
            return False
    return True                 # All offsets succeeded, so we return True















b = Board(7,6)

