# Concurrent Connect Four 

This is a socket-based concurrent Connect Four game implemented in Python.  
The game allows two players to connect to a server and play against each other in real time.

---

## Features
- Multiplayer support (two clients connect to the server).
- Server manages the game state, enforces rules, and handles turn-taking.
- Clients send moves to the server and receive board updates.
- Concurrency is handled with Python’s threading so the server can manage multiple clients at once.
- Detects wins (horizontal, vertical, diagonal) and draws.

---

## Project Structure
- C4client.py : runs the player client, interacts with the server, and prompts player for input.
- C4server.py: runs the game server, manages board state and client communication, checks for wins and inputs.

---

## Requirements
- Python 3.7+
- Standard library only (uses `socket` and `threading`), no extra dependencies

---

## How to Run

### 1. Start the Server
Run the server first so it can accept client connections:
```bash
python server.py
```
### 2. Connect the client to the server
Open two separate terminals and run 
```bash
python client.py
```

### 3. Play
After two clients are connected, a new game will start
