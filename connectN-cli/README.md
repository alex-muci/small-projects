Generalization of the classical [Connect 4 game](https://en.wikipedia.org/wiki/Connect_Four) using only standard Python 3.6 libraries (no numpy allowed, which will make winning checks faster).

#### *Use*
============

Run the following command in the CLI

    $ python connectz.py [inputfilename]

where:
[inputfilename] is an ASCII textfile with the following features:

- the first line contains three integers, respectively, the (i) no of columns and (ii) rows of the board/ frame and the (iii) minimum number of adjacent pieces/counters required to win a game.
- each subsequent line is a single integer representing a move in the game (column where piece drops), starting with player one and alternating.

#### *Result*
============

Running the above command returns an integer between 0 and 9 (included) with the following meaning:

| integer       | reason            |  description  |
| ------------- | -------------     | ------------- |
| 0             | Draw              | This happens when every possible space in the frame was filled with a counter, but neither player achieved a line of the required length |
| 1             | Win for player 1  | The first player achieved a line of the required length  |
| 2             | Win for player 2  | The second player achieved a line of the required length |
| 3             | Incomplete        | The file conforms to the format and contains only legal moves, but the game is neither won nor drawn by either player and there are remaining available moves in the frame. Note that a file with only a dimensions line constitutes an incomplete game|
| 4             | Illegal continue  | All moves are valid in all other respects but the game has already been won on a previous turn so continued play is considered an illegal move |
| 5             | Illegal row       | The file conforms to the format and all moves are for legal columns but the move is for a column that is already full due to previous moves |
| 6             | Illegal column    | The file conforms to the format but contains a move for a column that is out side the dimensions of the board. i.e. the column selected is greater than X |
| 7             | Illegal game      | The file conforms to the format but the dimensions describe a game that can never be won |
| 8             | Invalid file      | The file is opened but does not conform the format |
| 9             | File error        | The file can not be found, opened or read for some reason |


#### *Examples*
============
Tests or examples of input files can be found in [examples](http://github.com/alex-muci/small-projects/blob/master/connectN-cli/examples).

NB: the last number in a file name is the expected result. E.g. running

    $ python connectz.py examples/test2.txt in the CLI

should return 2.
