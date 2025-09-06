from threading import Thread
import socket

row = 6
col = 7

def client_thread(conn1, conn2, addr1, addr2):
    board = [[" " for i in range(col)] for i in range(row)]
    str_board = board_to_string(board)
    try:
            conn1.sendall(str_board.encode())                #1 Pair 3
            conn1.recv(1024)
            conn2.sendall(str_board.encode())                #2 pair 3
            conn2.recv(1024)
            conn1.sendall(str(0).encode())                   #1 pair 4
            conn1.recv(1024)
            conn2.sendall(str(1).encode())                   #2 pair 4
            conn2.recv(1024)
            game_loop(conn1, conn2, board)

    except Exception as e:
        print("Error:", e)

    finally:
        print("Player:",addr1, "disconnected")
        print("Player:",addr2, "disconnected")
        conn1.close()
        conn2.close()

def game_loop(conn1, conn2, board):
    game_over = False
    turn = 0
    turns = 0
    while not game_over:
        conn1.sendall((str(turn)).encode())           # 1 pair 5
        conn1.recv(1024)
        conn2.sendall((str(turn)).encode())           # 2 pair 5
        conn2.recv(1024)
        if turn == 0:
            conn1.sendall("Player 1: Make a Move(1-7): ".encode()) # 1 pair 6
            message = conn1.recv(1024).decode()
            if not message.isdigit():
                message = conn1.recv(1024).decode()
            move = int(message)
            move -= 1
            while not is_valid(board, find_next_row(board, move), move):
                conn1.sendall("False".encode())     # 1 pair 7
                conn1.recv(1024)
                conn1.sendall("Move is invalid\nPlease make a valid move(1-7): ".encode())
                move = int(conn1.recv(1024).decode())
                move -= 1
            conn1.sendall("True".encode())
            conn1.recv(1024)

        else:
            conn2.sendall("Player 2: Make a Move(1-7): ".encode())      # 2 pair 6
            message = conn2.recv(1024).decode()
            if not message.isdigit():
                message = conn2.recv(1024).decode()
            move = int(message)
            move -= 1
            while not is_valid(board, find_next_row(board, move), move):
                conn2.sendall("False".encode())     # 2 pair 7
                conn2.recv(1024)
                conn2.sendall("Move is invalid\n Please make a valid move(1-7): ".encode()) #pair 8
                move = int(conn2.recv(1024).decode())
                move -= 1
            conn2.sendall("True".encode())
            conn2.recv(1024)
        piece = turn
        if turn == 0:
            piece = "\u25CF"
        else:
            piece = "\u25CB"

        place_piece(board, find_next_row(board, move), move, piece)
        str_board = board_to_string(board)
        turns += 1
        if has_won(board, piece):
            conn1.sendall(str_board.encode())           #1 pair 9a 
            conn2.sendall(str_board.encode())           #2 pair 9a
            conn1.recv(1024)
            conn2.recv(1024)
            conn1.sendall(str(turn).encode())           #1 pair 10a
            conn2.sendall(str(turn).encode())
            conn1.recv(1024)
            conn2.recv(1024)
            game_over = True
            
        elif turns == 42:
            conn1.sendall(str_board.encode())
            conn2.sendall(str_board.encode())
            conn1.recv(1024)
            conn2.recv(1024)
            conn1.sendall("Draw".encode())
            conn2.sendall("Draw".encode())
            conn1.recv(1024)
            conn2.recv(1024)
            game_over = True
        
        else:
            conn1.sendall((str_board).encode())
            conn2.sendall((str_board).encode())
            conn1.recv(1024)
            conn2.recv(1024)
            conn1.sendall("Next Turn".encode())
            conn2.sendall("Next Turn".encode())
            conn1.recv(1024)
            conn2.recv(1024)
        turn += 1
        turn = turn % 2
    

def place_piece(board, row, col, piece):
    board[row][col] = piece

def find_next_row(board, move):
    r = row-1
    if not (0 <= move < 7):
        return -1
    for i in board[::-1]:
        if i[move] == " ":
            return r
        else:
            r-=1
    return -1

def is_valid(board, r, move): 
    if r < 0:
        return False
    if board[r][move] != " ":
        return False
    return True 

def board_to_string(board):
    str_board = "\n-------------------------\n".join([" | ".join(row) for row in board])
    return str_board

def has_won(board, piece):
    #Horizontal
    for c in range(col-3):
        for r in range(row):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    #Vertical
    for c in range(col):
        for r in range(row-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    #Bottom-Left to top-right diagonal
    for c in range(col-3):
        for r in range(row-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    #Top-left to bottom-right diagonal
    for c in range(col-3):
        for r in range(3, row):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def main():
    port = int(input("Enter port number: "))
    soc = socket.socket()
    soc.bind(('', port))
    soc.listen()
    try:
        while True:
            print("Waiting for Player 1...")
            conn1, addr1 = soc.accept()
            print("Player 1 connected")
            print("Player 1 connection: ", addr1)
            intro_message = "Welcome to Connect Four!!!\n"
            conn1.sendall(intro_message.encode())           # #1 pairs 1-2
            conn1.recv(1024)
            conn1.sendall("You are Player 1 (\u25CF). Waiting for opponent...\n".encode())
            conn1.recv(1024)
            print("Waiting for Player 2...")
            conn2, addr2 = soc.accept()
            print("Player 2 connected")
            print("Player 2 connection: ", addr2)
            conn2.sendall(intro_message.encode())              # #2 Pairs 1-2
            conn2.recv(1024)
            conn2.sendall("You are Player 2 (\u25CB)\n".encode())
            conn2.recv(1024)
            Thread(target = client_thread, args = (conn1, conn2, addr1, addr2,)).start()
            print("\nWaiting For Next Queue...")
    finally:
        soc.close()
main()