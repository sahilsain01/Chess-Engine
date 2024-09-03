
# CHESS MASTER

Chess Master  is a simple chess engine designed to play chess using a basic implementation of the Alpha-Beta Pruning algorithm and custom piece values. It communicates using the Universal Chess Interface (UCI) protocol.


## Features

- Custom Piece Values: Adjusted values for different chess pieces.

- Alpha-Beta Pruning: Efficient move search with depth-limited evaluation.
- UCI Protocol: Compatible with various chess GUI applications.
- Basic Time Control: Example time control mechanism to manage the engine's thinking time.

## Installation

- Clone Repository:

```bash
  https://github.com/sahilsain01/Chess-Engine.git
  
```
- Requirements :

```bash
  pip install python-Chess

```
- Build File Executable:

```bash
  pyinstaller --onefile chess-engine.py
```
- Integrate with GUI :
   
   The .exe file will be appear in 'dist' folder 
   we have to integrate this .exe file in any GUI 


- Output:

  Run code on vs code , use these command to find best move 
```bash
uci
id name chess_master2
id author Sahil
uciok
isready
readyok
position startpos moves e2e4 e7e5
go
bestmove e2e4
```