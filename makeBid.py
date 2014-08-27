#!/usr/bin/env python

import crisscross as cc

self = cc.Mockup_self()
Math = cc.Math_wrapper()
tileGroupLetter = 'B'

alltiles = []
histiles = []
mytiles = []
for row in self.tileGrid:
  for cell in row:
    alltiles.append(cell)
    if cell.owner == self.team: mytiles.append(cell)
    if cell.owner and cell.owner != self.team: histiles.append(cell)

def calc_weight(tile):
  #self.debug('called weight on', tile)
  if tile.owner is None:
    return 10
  if tile.owner == self.team:
      return 0
  return 700

def numerical_sort(a,b):
  return a - b

def numerical_sort_tuple(a,b):
  return a[0] - b[0]

def value_ogre(tiles):
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
    if t.y == 0:
      parents[t.id] = []
      #self.debug('calling weight')
      cost = calc_weight(t)
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
    if current.y == 6:
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
      if n.y < current.y: continue
      #self.debug('inspecting', n.id)
      cost = calc_weight(n)
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
  return wanted.values()

def tiley(tile):
  return tile.y

def tilex(tile):
  return tile.x

def sillystrategy(self):
  tileIWant = None
  bidtiles = self.tileGroups[tileGroupLetter]  # tiles available this turn
  yowned = map(tiley, mytiles)
  xowned = map(tilex, mytiles)
  yowned.sort(numerical_sort)
  xowned.sort(numerical_sort)
  for tile in bidtiles:
    if tile.owner: continue  # can't buy a tile that's been bought
    if tile.y in yowned: continue
    if tile.x not in [4, 5]: continue
    tileIWant = tile
    break
    
  # If none of the tiles you want are available, skip this round
  if not tileIWant: return None
  
  # 2. Choose your bid price. You only pay and win the tile if your bid wins.
  tilesleft = 7 - len(self.myTiles)
  myBid = Math.floor(self.gold/Math.max(1,tilesleft))
  extra = Math.round(Math.random() * (self.gold % tilesleft))
  mybid += extra
  return {'gold': myBid, 'desiredTile': tileIWant}


#self.debug('turn', len(self.turns))
#if self.round == 0 and len(self.turns) == 6:
  #self.debug('alltiles', alltiles)
  #(costs, parents) = value_ogre(alltiles)
  #self.debug('costs', costs)
  #self.debug('parents', parents)
#wanted = value_ogre(alltiles)
#self.debug('wanted tiles: ',wanted)

#result = sillystrategy(self)

def better_strategy():
  wanted = value_ogre(alltiles)
  #self.debug('wanted tiles: ', wanted)
  bidtiles = self.tileGroups[tileGroupLetter]  # tiles available this turn
  #self.debug(bidtiles)
  bidtile = None
  candidates = []
  for tile in bidtiles:
    if tile in wanted:
      candidates.append(tile)
  if len(candidates) > 0:
    index = Math.floor(Math.random() * len(candidates))
    bidtile = candidates[int(index)]
  if not bidtile: return None
  tilesleft = 7 - len(self.myTiles)
  myBid = Math.floor(self.gold/Math.max(1,tilesleft))
  #self.debug(self.gold, myBid)
  extra = Math.round(Math.random() * (self.gold % tilesleft))
  #self.debug(extra)
  myBid += extra
  return {'gold': myBid, 'desiredTile': bidtile}

#self.debug('round, turn', self.round, len(self.turns))
result = better_strategy()
#print result
return result

