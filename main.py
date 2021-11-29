import VirusGame as vg

g = vg.Game(10, 10)
print(g.getString())

turn = 1
move = [-1, -1]
while True:
    move[0], move[1] = map(int, input().split())
    if turn == 1:
        g.makeMove(1, move.copy())
        turn = 2
    else:
        g.makeMove(2, move.copy())
        turn = 1
    print(g.getString())
