#!/usr/bin/env python

#import json
import crisscross as cc

#self = cc.Mockup_self()
#tileGroupLetter = 'B'
Math = cc.Math_wrapper()

def makeBid(self, tileGroupLetter):
  alltiles = []
  for row in self.tileGrid:
    for cell in row:
      alltiles.append(cell)
  
  def calc_weight(tile, team):
    #self.debug('called weight on', tile)
    if tile.owner is None:
      return 100
    if tile.owner == team:
        return 1
    return 7000
  
  def numerical_sort(a,b):
    return a - b
  
  def numerical_sort_tuple(a,b):
    return a[0] - b[0]
  
  def value(tiles, team, starttiles, endtiles):
    visited = {}
    fringe = []
    parents = {}
    costs = {}
    bestcost = 9999999
    objectives = []
  
    for t in tiles:
      # initialize set
      visited[t.id] = False
      # start from bottom row
  
    for t in starttiles:
      parents[t.id] = []
      #self.debug('calling weight')
      cost = calc_weight(t, team)
      #self.debug('called weight')
      element = (cost, t)
      fringe.append(element)
    #self.debug('visited', visited)
  
    #self.debug('got here')
    while len(fringe) > 0:
      # simulate a priority queue
      #self.debug('fringe', fringe)
      fringe.sort(numerical_sort_tuple)
      #self.debug('sorted fringe', fringe)
      fringe.reverse()
      (curcost, current) = fringe.pop()
      #self.debug('popped', curcost, current)
      visited[current.id] = True
      costs[current.id] = curcost
      #self.debug('visited', current.id)
      # check if we have arrived
      if current in endtiles:
        if curcost == bestcost:
          objectives.append(current)
          #self.debug('adding objective', current)
          continue
        if curcost < bestcost:
          #self.debug('best objective', current)
          bestcost = curcost
          objectives = [current]
          continue
        #self.debug('reached', current, 'with cost', curcost, 'ending')
        break
      for n in current.neighbors:
        # skip opponent's tiles
        #if n.owner and n.owner != self.team: continue
        # only move upwards
        #if n.y < current.y: continue
        #self.debug('inspecting', n.id)
        cost = calc_weight(n, team)
        if visited[n.id]:
          #self.debug('already visited', n.id)
          # even if already visited there might be an alternate path
          if costs[n.id] == curcost + cost:
            parents[n.id].append(current)
          continue
        # look for this cell in the fringe
        in_fringe = False
        for i in range(len(fringe)):
          fcost, fcell = fringe[i]
          if fcell.id == n.id:
            in_fringe = True
            if ((curcost + cost) < fcost):
              #self.debug('found in fringe', n)
              # found a better path!
              fcost = (curcost + cost)
              fringe[i] = (fcost, fcell)
              parents[n.id] = [current]
            if ((curcost + cost) == fcost):
              parents[n.id].append(current)
            break
        if not in_fringe:
          fringe.append((curcost + cost, n))
          parents[n.id] = [current]
    #self.debug('visited', filter(lambda x: x[1], visited))
    #self.debug('costs', costs)
    #self.debug('parents', parents)
    #self.debug('objectives', objectives)
    
    #print parents
    p = objectives[0] 
    path = [p]
    while len(parents[p.id]) > 0:
      #print p, parents[p.id]
      p = parents[p.id][0]
      if p.owner == None:
        path.append(p)
    needed = len(path)
  
    visited = {}
    wanted = {}
    fringe = []
    for o in objectives:
      fringe.append(o)
    while len(fringe) > 0:
      curr = fringe.pop()
      if visited.get(curr.id):
        continue
      visited[curr.id] = curr
      if curr.owner is None:
        wanted[curr.id] = curr
      for p in parents[curr.id]:
        fringe.append(p)
  
    #self.debug('wanted', wanted.values())
    return (wanted.values(), needed)
  
  def bids(player):
    result = []
    keys = {'humans': 'humanBid', 'ogres': 'ogreBid'}
    key = keys[player]
    for turn in self.turns:
      #self.debug(turn)
      if turn[key]['invalidBid'] or turn[key]['invalidTile']: continue
      bid = turn[key]['bid']
      result.append(bid)
    return result

  def rank_tiles(tile):
    if tile.owner != None:
      return 0
    score = 0
    tilegroups = {}
    tilegroups[tile.tileGroupLetter] = True
    #opptiles = 0
    for n in tile.neighbors:
      tilegroups[n.tileGroupLetter] = True
      if n.owner != None:
        if n.owner != self.team:
          # close to opponent is ok for disruption, but let's ignore that for now
          score += 0
        if n.owner == self.team:
          score += 10 # connected tiles cannot be disconnected
    score += (len(tilegroups) - 1)
    # favour center
    score += (3 - (Math.abs(3-tile.x)))
    score += (3 - (Math.abs(3-tile.y)))
    return score

  def better_strategy():
    start_o = []
    end_o = []
    for i in range(7):
      start_o.append(self.tileGrid[i][0])
      end_o.append(self.tileGrid[i][6])
    start_h = self.tileGrid[0]
    end_h = self.tileGrid[6]
    #self.debug('start_o', start_o)
    #self.debug('end_o', end_o)
    #self.debug('start_h', start_h)
    #self.debug('end_h', end_h)
  
    (wanted_o, needed_o) = value(alltiles, 'ogres', start_o, end_o)
    (wanted_h, needed_h) = value(alltiles, 'humans', start_h, end_h)

    if self.team == 'ogres':
      needed = needed_o
      wanted = wanted_o
      needed_opp = needed_h
      wanted_opp = wanted_h
    if self.team == 'humans':
      needed = needed_h
      wanted = wanted_h
      needed_opp = needed_o
      wanted_opp = wanted_o

    wanted_both = []
    for t in wanted_o:
      if t in wanted_h:
        wanted_both.append(t)
    #self.debug('wanted human tiles: ', wanted_h)
    #self.debug('wanted ogre tiles: ', wanted_o)
    #self.debug('both teams want: ', wanted_both)

    ranked_tiles = []
    for t in wanted:
      if t.tileGroupLetter != tileGroupLetter:
        continue
      score = rank_tiles(t)
      if t in wanted_both:
        score = score * 100
      ranked_tiles.append((score, t))

    ranked_tiles.sort(numerical_sort_tuple)
    #ranked_tiles.reverse()
    self.debug(ranked_tiles)
    bidtile = None
    if len(ranked_tiles) > 0:
      (score, bidtile) = ranked_tiles.pop()

    if bidtile is None:
      # we have nothing to bid for :(
      # let's see if we can avoid wasting a turn
      if len(wanted_opp) > 0 and needed_opp <= 4 and self.gold > (needed * 2)+2:
        # let's make a bid for one of his tiles with a bid of 2
        # just to screw with him if he's trying to steal
        stealtile = None
        for t in wanted_opp:
          if t.tileGroupLetter == tileGroupLetter:
            stealtile = t
            break
        if stealtile is not None:
          return {'gold': 2, 'desiredTile': stealtile}
      # nothing to do :(
      return None

    self.debug('needed', needed)
    myBid = Math.floor(self.gold/Math.max(1,needed))
    #self.debug(self.gold, myBid)
    extra = Math.round(Math.random() * (self.gold % Math.max(1,needed)))
    #self.debug(extra)
    myBid += extra
    if len(self.turns) < 4:
      myBid = 10 + Math.round(Math.random() * 4)
    opp_gold = 128 - sum(bids('humans'))
    self.debug(opp_gold)

    # if opponent has nothing to bid for, make a low bid
    opponent_will_bid = False
    for t in wanted_opp:
      if t.tileGroupLetter == tileGroupLetter:
        opponent_will_bid = True
        break
    if not opponent_will_bid:
      # steal a tile
      myBid = 1

    if needed == 1:
      myBid = self.gold # bust the bank
    # never bid more gold than opponent has
    myBid = int(Math.min(myBid, opp_gold + 1))
    if myBid < 0:
      self.debug('bid below 0!', myBid)
      myBid = 1
    return {'gold': myBid, 'desiredTile': bidtile}
  
  #self.debug('round, turn', self.round, len(self.turns))
  #self.debug('round', self.round, 'turn', len(self.turns))
  #self.debug('ogre bids', bids('ogres'))
  #self.debug('human bids', bids('humans'))
  result = better_strategy()
  return result

def main():
  self = cc.Mockup_self()
  print self
  print self.printtiles()
  tileGroupLetter='A'
  print makeBid(self, tileGroupLetter)

  self.tileGrid[0][4].owner = 'humans'
  self.tileGrid[2][4].owner = 'humans'
  self.tileGrid[3][4].owner = 'humans'
  self.tileGrid[4][4].owner = 'humans'

  self.tileGrid[1][0].owner = 'ogres'
  self.tileGrid[1][1].owner = 'ogres'
  self.tileGrid[1][2].owner = 'ogres'
  self.tileGrid[1][3].owner = 'ogres'
  self.tileGrid[1][5].owner = 'ogres'
  self.tileGrid[1][4].tileGroupLetter = 'A'

  print self
  print self.printtiles()
  print makeBid(self, tileGroupLetter)

  self.team='humans'
  print makeBid(self, tileGroupLetter)

  self.tileGrid[1][4].owner = 'ogres'
  self.tileGrid[2][3].owner = 'ogres'
  self.tileGrid[1][3].owner = 'humans'
  self.tileGrid[0][6].tileGroupLetter='B'
  self.tileGrid[1][6].tileGroupLetter='B'
  self.tileGrid[2][6].tileGroupLetter='B'
  self.tileGrid[6][6].tileGroupLetter='A'
  print self
  print self.printtiles()
  print makeBid(self, tileGroupLetter)


if __name__ == '__main__':
  main()
