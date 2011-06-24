#!/usr/bin/python
# ecole polytechnique - c.durr - 2009

# Kuhn-Munkres, The hungarian algorithm.  Complexity O(n^3)
# Computes a max weight perfect matching in a bipartite graph
# for min weight matching, simply negate the weights.

import random
import time

""" Global variables:
       n = number of vertices on each side
       U,V vertex sets
       lu,lv are the labels of U and V resp.
       the matching is encoded as 
       - a mapping Mu from U to V, 
       - and Mv from V to U.
    
    The algorithm repeatedly builds an alternating tree, rooted in a
    free vertex u0. S is the set of vertices in U covered by the tree.
    For every vertex v, T[v] is the parent in the tree and Mv[v] the
    child.

    The algorithm maintains minSlack, s.t. for every vertex v not in
    T, minSlack[v]=(val,u1), where val is the minimum slack
    lu[u]+lv[v]-w[u][v] over u in S, and u1 is the vertex that
    realizes this minimum.

    Complexity is O(n^3), because there are n iterations in
    maxWeightMatching, and each call to augment costs O(n^2). This is
    because augment() makes at most n iterations itself, and each
    updating of minSlack costs O(n).
    """

def improveLabels(val):
    """ change the labels, and maintain minSlack. 
    """
    for u in S:
        lu[u] -= val
    for v in xrange(n):
        if v in T:
            lv[v] += val
        else:
            minSlack[v][0] -= val

def improveMatching(v):
    """ apply the alternating path from v to the root in the tree. 
    """
    u = T[v]
    if u in Mu:
        improveMatching(Mu[u])
    Mu[u] = v
    Mv[v] = u

def slack(u,v): return lu[u]+lv[v]-w[u][v]

def augment():
    """ augment the matching, possibly improving the lablels on the way.
    """
    while True:
        # select edge (u,v) with u in S, v not in T and min slack
        ((val, u), v) = min([(minSlack[v], v) for v in xrange(n) if v not in T])
        assert u in S
        if val>0:        
            improveLabels(val)
        # now we are sure that (u,v) is saturated
        #assert slack(u,v)==0
        T[v] = u                            # add (u,v) to the tree
        if v in Mv:
            u1 = Mv[v]                      # matched edge, 
            #assert not u1 in S
            S[u1] = True                    # ... add endpoint to tree 
            for v in xrange(n):                     # maintain minSlack
                if not v in T and minSlack[v][0] > slack(u1,v):
                    minSlack[v] = [slack(u1,v), u1]
        else:
            improveMatching(v)              # v is a free vertex
            return

def maxWeightMatching(weights):
    """ given w, the weight matrix of a complete bipartite graph,
        returns the mappings Mu : U->V ,Mv : V->U encoding the matching
        as well as the value of it.
    """
    global S,T,Mu,Mv,lu,lv, minSlack, w, n
    w  = weights
    n  = len(w)
    lu = [max([w[u][v] for v in xrange(n)]) for u in xrange(n)]  # start with trivial labels
    lv = [ 0                                for _ in xrange(n)]
    Mu = {}                                       # start with empty matching
    Mv = {}
    while len(Mu)<n:
        free = [u for u in xrange(n) if u not in Mu]      # choose free vertex u0
        u0 = free[0]
        S = {u0: True}                            # grow tree from u0 on
        T = {}
        minSlack = [[slack(u0,v), u0] for v in xrange(n)]
        augment()
    #                                    val. of matching is total edge weight
    return (Mu, Mv, sum(lu)+sum(lv))

#print maxWeightMatching([[20,2,3,40],[2,20,40,8],[3,40,20,12],[40,8,12,20]])
  
#  a small example 
#h = 3
#w = 3
#ll = [[random.randint(1, 10) for _ in xrange(w)] for _ in xrange(h)]
#ll = [[i+j for i in xrange(w)] for j in xrange(h)]
#print ll

#s = time.clock()

#print maxWeightMatching(ll)

#t = time.clock() - s
#print '>> %f'%t

# read from standard input a line with n
# then n*n lines with u,v,w[u][v]

#n = int(raw_input())
#w = [[0 for v in range(n)] for u in range(n)]
#for _ in range(n*n):
#    u,v,w[u][v] = map(int, raw_input().split())

#print maxWeightMatching(w)
