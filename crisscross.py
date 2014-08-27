#!/usr/bin/env python

import random
import math

class Math_wrapper(object):
  def __init__(self):
    def _random():
      return random.random()
    self.random = _random
    def _floor(x):
      return math.floor(x)
    self.floor = _floor
    def _round(x):
      return round(x)
    self.round = _round

class Tile(object):
  def __init__(self, x, y, owner=None, group=None):
    self.x = x
    self.y = y
    self.id = '%s.%s' % (x,y)
    self.owner = owner
    self.tileGroupLetter = group
    self.neighbors = []
  def __repr__(self):
    return self.id
  def __str__(self):
    return self.id

class Mockup_self(object):
  def __init__(self):
    # functions and stuff
    def _debug(string):
      print string
    self.debug=_debug

    # create grid
    width = 7
    height = 7
    self.tileGrid=[]
    tiles = []
    for x in range(width):
      col = []
      for y in range(height):
        t = Tile(x, y)
        tiles.append(t)
        if y > 0:
          n = col[y-1]
          t.neighbors.append(n)
          n.neighbors.append(t)
        if x > 0:
          n = self.tileGrid[x-1][y]
          t.neighbors.append(n)
          n.neighbors.append(t)
        if y > 0 and x > 0:
          n = self.tileGrid[x-1][y-1]
          t.neighbors.append(n)
          n.neighbors.append(t)
        if x > 0 and y < (height - 1):
          n = self.tileGrid[x-1][y+1]
          t.neighbors.append(n)
          n.neighbors.append(t)
        col.append(t)
      self.tileGrid.append(col)

    # assign groups
    groups = []
    self.tileGroups = {}
    for g in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
      self.tileGroups[g] = []
      for i in range(7):
        groups.append(g)
    random.shuffle(groups)
    for t in tiles:
      # select a tilegroup
      group = groups.pop()
      t.tileGroupLetter = group
      self.tileGroups[group].append(t)
    #print self.tileGroups
    
    self.gold = 114
    self.team = 'ogres'
    self._opponent = 'humans'
    self._tiles = tiles
    self.turns = [{
      "number": 0,
      "tileGroup": "A",
      "humanGold": 128,
      "ogreGold": 114,
      "humanBid": {
        "bid": 6,
        "team": "humans",
        "desiredTile": self._tiles[0],
        "invalidBid": False,
        "invalidTile": False },
      "ogreBid": {
        "bid": 14,
        "team": "ogres",
        "desiredTile": self._tiles[0],
        "invalidBid": False,
        "invalidTile": False }}]
  @property
  def myTiles(self):
    return filter(lambda x: x.owner == self.team, self._tiles)
  @property
  def opponentTiles(self):
    return filter(lambda x: x.owner == self._opponent, self._tiles)

if __name__ == '__main__':
  pass
