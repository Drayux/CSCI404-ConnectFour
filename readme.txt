===========================
  Liam Dempsey | 10754465
===========================


===========================
  LANGUAGE
===========================
    Python (3.10.0)

===========================
  OPERATING SYSTEM
===========================
    Built on Windows 10 (but should run on any OS that supports Python 3)

===========================
  STRUCTURE
===========================
    Everything is encapsulated into classes, with member functions that direct the flow of the game
    Each game state is saved within a tree structure and each potential move is generated before selection
    Minimax function is Tree.evaluate() (line 559) and modified slightly to support debug information and program optimization
      ^^Consequently, the "second half" of the minimax evaluation is Tree.advance() (line 505)
    Finally, the static evaluation function is a combination of two functions: Board.evaluate() and Board.evaluate_arr() (lines 266 and 201 respectively)
    There are 4 more helper functions which transform the board data into a format that works with these functions: Board.rows, Board.cols, Board.diagRight, and Board.diagLeft

===========================
  COMPILATION
===========================
    As Python is an interpreted language, the program can be run AS-IS with no prior preparation.
    One need call either:
        python3 interactive <input file> <computer-next/human-next> <depth>     (or)
        python3 one-move <input file> <output file> <depth>
    If on a UNIX-based system, else replace `python3` with `python`

    There is also a debug mode included for my own personal testing.
    Do be aware that `python3 debug [depth]` will initialize this mode.

===========================
  NOTES
===========================
    The five testing cases are saved within the states/ directory.
    Each is named TEST-CASE-X.txt where `X` is a number 1 - 5.
