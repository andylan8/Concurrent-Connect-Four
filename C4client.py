import socket

def main():

    host = "localhost"
    port = 3240
    soc = socket.socket()
    soc.connect((host, port))

    for i in range(3):      #Pair 1-3
        message = soc.recv(1024).decode()
        print(message)
        soc.sendall("Break".encode())

    player = soc.recv(1024).decode()        #Pair 4
    soc.sendall("Break".encode())

    opponent = 2
    if player == "1":
        opponent = 1
    game_over = False
    try:
        while not game_over:
            if player == (soc.recv(1024).decode()):  #Pair 5a
                soc.sendall("Break".encode())
                message = soc.recv(1024).decode()        #Pair 6
                move = input(message)
                while not move.isdigit():
                    move = input(message)
                soc.sendall(move.encode())
                is_valid_input = soc.recv(1024).decode() #Pair 7
                while is_valid_input == "False": 
                    soc.sendall("Break".encode())
                    message = soc.recv(1024) .decode()
                    move = input(message)
                    soc.sendall(move.encode())          #pair 8
                    is_valid_input = soc.recv(1024).decode()
                soc.sendall("Break".encode())
                
            else: 
                print("Player ", opponent, " is making a move...")
            #Pair 5b
            try:
                soc.sendall("Break".encode())
            except BrokenPipeError:
                print("Player ", int(message)+1, " Has Won")
            #Pair 9
            board = soc.recv(1024).decode()
            if "Next Turn" in board:
                board = board.replace("Next Turn", "")
            else:
                soc.sendall("Break".encode())
                message = soc.recv(1024).decode()
            print("\n" * 8 + board)
            soc.sendall("Break".encode())       #pair 10
            if message == "0" or message == "1":
                print("Player ", int(message)+1, " Has Won")   
                game_over = True
            elif message == "Draw":
                print("Game Over!!! It's A Draw")
                game_over = True      
                    
    finally:
        soc.close()
    
main()

