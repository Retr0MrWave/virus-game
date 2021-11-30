import VirusGame as vg

print("Welcome to Virus:The Game")
print("Please enter width and height of your desired field")
w, h = map(int, input().split())
g = vg.Game(w, h)
print(g.getString())

turn = 1
move = [-1, -1]
while True:
    if turn == 1:
        print("First player, your turn")
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(1, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(1)):
            print("Player 2 won")
            break
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(1, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(1)):
            print("Player 2 won")
            break
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(1, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(2)):
            print("Player 1 won")
            break
        turn = 2
    else:
        print("Second player, your turn")
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(2, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(2)):
            print("Player 1 won")
            break
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(2, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(2)):
            print("Player 1 won")
            break
        move[0], move[1] = map(int, input().split())
        while not(g.makeMove(2, move.copy())):
            print("Invalid move. Please try again")
            move[0], move[1] = map(int, input().split())
        print(g.getString())
        if (g.checkGameEnd(1)):
            print("Player 2 won")
            break
        turn = 1
input("Thanks for playing. Press Enter to exit")
