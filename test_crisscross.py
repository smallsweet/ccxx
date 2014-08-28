#!/usr/bin/env python

import crisscross as cc

def test_tile_in_list():
  a = []
  for i in range(4):
    t = cc.Tile(0, i)
    a.append(t)
  
  t = a[0]
  assert t in a

def test_crisscross_mockup():
  self = cc.Mockup_self()
  t00 =  self.tileGrid[0][0]
  t01 =  self.tileGrid[0][1]
  t10 =  self.tileGrid[1][0]
  t11 =  self.tileGrid[1][1]
  t12 =  self.tileGrid[1][2]
  assert t00.id == '0.0'
  assert len(t00.neighbors) == 3
  assert t01 in t00.neighbors
  assert t10 in t00.neighbors
  assert t11 in t00.neighbors
  assert t12 not in t00.neighbors
  #self.debug(t12.neighbors)
  #self.debug(self.tileGroups)
  for (letter, group) in self.tileGroups.items():
    assert len(group) == 7
    for t in group:
      assert t.tileGroupLetter == letter
  t00.owner = self.team
  t01.owner = self.team
  t12.owner = self._opponent
  assert t00 in self.myTiles
  assert t12 in self.opponentTiles
  assert len(self.turns) == 1
  assert self.turns[0]['tileGroup'] == 'A'
  #
  assert self._tiles[0].id == self.tileGrid[0][0].id
  assert self._tiles[6].id == self.tileGrid[0][6].id
  assert self._tiles[7].id == self.tileGrid[1][0].id
  assert self._tiles[7*4+5].id == self.tileGrid[4][5].id

def test_functions():
  self = cc.Mockup_self()
  self.tileGrid[0][4].owner = 'humans'
  self.tileGrid[2][4].owner = 'humans'
  self.tileGrid[3][4].owner = 'humans'
  self.tileGrid[4][4].owner = 'humans'
  print self
  print self.printtiles()


def test_math():
  Math = cc.Math_wrapper()
  assert Math.random() < 1
  assert Math.random() > 0
  assert Math.floor(0.6) == 0
  assert Math.round(0.6) == 1
  assert Math.max(0,6) == 6
  assert Math.max(0,6,5) == 6

if __name__=='__main__':
  test_tile_in_list()
  test_crisscross_mockup()
  test_functions()
