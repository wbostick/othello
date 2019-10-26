#!/usr/bin/python

import sys
import json
import socket

def get_valid_moves():
  valid_moves = []

  rows = len(board)
  cols = len(board[0])
  for i in range(rows):
    for j in range(cols):
      m = move_t(i, j, player, board)
      if m.is_valid():
        valid_moves.append(m)

  for mov in valid_moves:
    print(mov)

  return valid_moves

def get_move(player, board):
  valid_moves = get_valid_moves()

  # TODO determine valid moves
  # TODO determine best move
  return valid_moves[0]


class move_t:
  pos = None
  player = -1
  board = [[]]

  def __init__(self, _x, _y, _player, _board):
    self.pos = position(_x, _y)
    self.player = _player
    self.board = _board

  def is_valid(self):
    if not self.on_board():
      # print("NOT ON BOARD")
      return False
    elif self.occupied():
      # print("OCCUPIED")
      return False
    elif self.flips() is 0:
      # print("FILPS NOTHING")
      return False
    else:
      return True

  def on_board(self, pos = None):
    if pos is None:
      pos = self.pos

    if pos.x < 0 or pos.x >= len(board):
      return False
    if pos.y < 0 or pos.y >= len(board[0]):
      return False
    
    return True

  def occupied(self, pos = None):
    if pos is None:
      pos = self.pos
    return board[pos.x][pos.y]

  def flips(self):
    total_move_will_flip = 0
    for i in range(-1, 2):
      for j in range(-1, 2):
        
        if i is 0 and j is 0:
          continue

        else:
          flips_in_dir = 0
          new_xy = self.pos
          while True:
            new_xy += position(i,j)
            
            if not self.on_board(new_xy) or self.occupied(new_xy) is 0:
              flips_in_dir = 0
              break
            elif self.occupied(new_xy) is player:
              break

            else:
              flips_in_dir += 1

          total_move_will_flip += flips_in_dir


    return total_move_will_flip

  def __str__(self):
    validity = self.is_valid()
    vstring = "valid" if validity else "not valid"

    return "[%d, %d] is %s" % (self.pos.x, self.pos.y, vstring)
  


class position:
  x = -1
  y = -1

  def __init__(self, _x, _y):
    self.x = _x
    self.y = _y

  def __add__(self, other):
    new_pos = position(self.x + other.x, self.y + other.y)
    return new_pos


def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
