#!/usr/bin/env python

import crisscross as cc

#self = cc.Mockup_self()
#tileGroupLetter = 'B'
Math = cc.Math_wrapper()


def makeBid(self, tileGroupLetter):
  alltiles = []
  histiles = []
  mytiles = []
  for row in self.tileGrid:
    for cell in row:
      alltiles.append(cell)
      if cell.owner == self.team: mytiles.append(cell)
      if cell.owner and cell.owner != self.team: histiles.append(cell)
  
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
  
  def tiley(tile):
    return tile.y
  
  def tilex(tile):
    return tile.x
  
  def opp_bid_avg():
    spent = 0
    turns = 0
    for turn in self.turns:
      hb = turn.get('humanBid')
      if not hb:
        continue
      bid = hb.get('bid')
      if not bid:
        continue
      spent += bid
      turns += 1
    return spent/Math.max(1,turns)

  def rank_tiles(tile):
    if tile.owner != None:
      return 0
    score = 0
    tilegroups = {}
    tilegroups[tile.tileGroupLetter] = True
    #opptiles = 0
    for n in tile.neighbors:
      tilegroups[n.tileGroupLetter] = True
      if n.owner != None and n.owner != self.team:
        score += 1
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
    self.debug('start_o', start_o)
    self.debug('end_o', end_o)
    self.debug('start_h', start_h)
    self.debug('end_h', end_h)
  
    (wanted_o, needed_o) = value(alltiles, 'ogres', start_o, end_o)
    (wanted_h, needed_h) = value(alltiles, 'humans', start_h, end_h)
    self.debug('wanted human tiles: ', wanted_h)
    self.debug('wanted ogre tiles: ', wanted_o)
    
    ranked_tiles = []
    for t in wanted_o:
      score = rank_tiles(t)
      if t in wanted_h:
        # if opponent also wants it then double value
        score = score * 2
      ranked_tiles.append((score, t))
    ranked_tiles.sort(numerical_sort_tuple)
    ranked_tiles.reverse()
    self.debug(ranked_tiles)

    bidtile = None
    for (score, t) in ranked_tiles:
      if t.tileGroupLetter == tileGroupLetter:
        bidtile = t
        break
    if bidtile is None: return None
    #tilesleft = 7 - len(self.myTiles)
    tilesleft = needed_o
    self.debug('needed', needed_o)
    myBid = Math.floor(self.gold/Math.max(1,tilesleft))
    #self.debug(self.gold, myBid)
    extra = Math.round(Math.random() * (self.gold % Math.max(1,tilesleft)))
    #self.debug(extra)
    myBid += extra
    return {'gold': myBid, 'desiredTile': bidtile}
  
  #self.debug('round, turn', self.round, len(self.turns))
  result = better_strategy()
  return result

def main():
  self = cc.Mockup_self()
  self.tileGrid[0][4].owner = 'humans'
  self.tileGrid[2][4].owner = 'humans'
  self.tileGrid[3][4].owner = 'humans'
  self.tileGrid[4][4].owner = 'humans'

  self.tileGrid[1][0].owner = 'ogres'
  self.tileGrid[1][1].owner = 'ogres'
  self.tileGrid[1][2].owner = 'ogres'
  self.tileGrid[1][3].owner = 'ogres'
  self.tileGrid[1][5].owner = 'ogres'

  print self
  print self.printtiles()

  tileGroupLetter = self.tileGrid[1][4].tileGroupLetter
  print makeBid(self, tileGroupLetter)
  
  self.tileGrid[0][4].owner = None
  self.tileGrid[2][4].owner = None
  self.tileGrid[3][4].owner = None
  self.tileGrid[4][4].owner = None

  self.tileGrid[1][0].owner = None
  self.tileGrid[1][1].owner = None
  self.tileGrid[1][2].owner = None
  self.tileGrid[1][3].owner = None
  self.tileGrid[1][5].owner = None
  print makeBid(self, tileGroupLetter)

if __name__ == '__main__':
  main()
