import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():#用于存储游戏的信息
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    每个句子由一组单元格（cells）和一个计数值（count）组成。计数值表示在这些单元格中有多少个是地雷。
    """

    def __init__(self, cells, count):
        self.cells = set(cells) #cell集合代表推理中未确定状态的单元格
        self.count = count  #count是为了技术和self.count中有mine的cell

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):  #返回 self.cells 中已知为地雷的所有单元格的集合
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells) and len(self.cells)>0:
            return self.cells.copy()
        else :
            return set() 


    def known_safes(self): #返回 self.cells 中已知安全的所有单元格的集合
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):  #更新句子中的地雷
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return 1
        return 0

    def mark_safe(self, cell): #更新句子中的安全
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return 1
        return 0


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
                                    #标记已经操作过的单元格
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []                                 #AI知道为真的所有sentence列表

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:                  #sentence为不同的实例化的变量，存储的是每走过一个单元格，所对应的是其对应的cell和周围的count
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        self.safes.add(cell)新的信息到 AI 的知识库：a
        
        cell 是当前揭开的单元格，count 是该单元格周围地雷的数量。
        """
        self.safes.add(cell)
        for sentence in self.knowledge: #在循环中，Sentence变量杯一次赋值为self.knowledge中的每一个sentence对象
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):#
        """
        add_knowledge应该接受一个单元格（表示为元组 （i， j））及
        其相应的计数，并使用 AI 可以推断的任何新信息更新 self.mines、
        self.safes、self.moves_made 和 self.knowledge，因为已知
        该单元格是一个安全的单元格，附近有 count 地雷。

        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        在得到一个安全cell的相关信息之后做出适当的推理和知识更新。
        将该单元格标记为已经操作的
        将该单元格标记为安全的

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines       
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base    ？？？？
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  #mark the cell as a move that has been made
        self.safes.add(cell)  # mark the cell as safe
        #self.mark_mine(self, cell)
        self.mark_safe(cell)
        # add new sentence
        # find neighbors
        i, j = cell
        neighbors = set()
        for a in range(max(0, i-1), min(i+2, self.height)):
            for b in range(max(0, j-1), min(j+2, self.width)):
                if (a, b) != (i, j):
                    neighbors.add((a, b))

        if count ==0:
            self.safes.update(neighbors)
        for sentence in self.knowledge: #在循环中，Sentence变量杯一次赋值为self.knowledge中的每一个sentence对象
            sentence.mark_safe(neighbors)
        print(self.knowledge)

        if count !=0:
            neighbors.difference_update(self.safes)
        for sentence in self.knowledge: #在出来数字之后，更新一下可能是mine的地方
            self.mines.update(sentence.known_mines())       
            self.safes.update(sentence.known_safes())

        self.knowledge.append(Sentence(neighbors, count))
        print(self.knowledge)


        
        # add neighbors and value to sentence


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        返回一个安全的单元格
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move

        return None
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
        返回一个随机移动，如果AI不知道往哪里移动
        移动的cell不是能使已经taken的，也不能是一致地雷的
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # 创建一个包含所有可用单元格的列表
        all_possible_moves = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        # 如果有可用的移动，随机选择一个返回
        if len(all_possible_moves) > 0:
            return random.choice(all_possible_moves)
        raise NotImplementedError
