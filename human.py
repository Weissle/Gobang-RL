from rule.GobangBase import *


board = Gobang(15,15)
while board.gameover() == False:
    x =int(input("Please "+board.who_should_place()+" place x: "))
    y =int(input("Please "+board.who_should_place()+" place y: "))
    board.place(x,y)
    board.print_board()
print(board.winner()+" win ")
