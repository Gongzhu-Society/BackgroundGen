#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import numpy,random
from scipy.spatial import Delaunay
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

def gen_tri(HEIGHT=9,WIDTH=16,N_inside=30,N_edge_width=5,N_edge_height=4,margin=0.05):
    if N_edge_width==None:
        N_edge_width=int(N_edge_height/HEIGHT*WIDTH)
    if N_edge_height==None:
        N_edge_height=int(N_edge_width/WIDTH*HEIGHT)

    w_inf=WIDTH*margin
    w_sup=WIDTH*(1-margin)
    h_inf=HEIGHT*margin
    h_sup=HEIGHT*(1-margin)
    pts=[[random.uniform(w_inf,w_sup),random.uniform(h_inf,h_sup)] for i in range(N_inside)]+\
        [[0,random.uniform(h_inf,h_sup)] for i in range(N_edge_height)]+\
        [[WIDTH,random.uniform(h_inf,h_sup)] for i in range(N_edge_height)]+\
        [[random.uniform(w_inf,w_sup),0] for i in range(N_edge_width)]+\
        [[random.uniform(w_inf,w_sup),HEIGHT] for i in range(N_edge_width)]+\
        [[0,0],[0,HEIGHT],[WIDTH,0],[WIDTH,HEIGHT]]
    pts=numpy.array(pts)
    tri=Delaunay(pts)
    return pts,tri

class ColorGen():
    def __init__(self,ts,pts,method="rand",extra_paras=[]):
        self.ts=ts
        self.pts=pts
        self.method=method
        self.extra_paras=extra_paras

    def gen_colors(self):
        if self.method=="rand":
            return self.colors_rand(*self.extra_paras)

    def colors_rand(self):
        #numpy.array([(random.random(),random.random(),random.random()) for t in self.ts])
        #return ['#0f0f0f' for t in self.ts]
        return numpy.array([random.random() for t in self.ts])

if __name__=="__main__":
    pts,tri=gen_tri()
    cg=ColorGen(tri.simplices,pts)
    colors=cg.gen_colors()
    fig=plt.figure(figsize=[16,9],dpi=120) #16*120=1920
    ax=fig.subplots(1)
    #ax.triplot(pts[:,0],pts[:,1],tri.simplices,color='green', marker='o')
    #ax.plot(pts[:,0],pts[:,1],'o')
    plt.tripcolor(pts[:,0],pts[:,1],tri.simplices,facecolors=colors,edgecolors='k')
    plt.gca().set_aspect('equal')
    plt.show()
    fig.savefig("bkg.png")

"""
help(tri)
class Delaunay(_QhullUser)
 |  Delaunay(points, furthest_site=False, incremental=False, qhull_options=None)
 |
 |  Delaunay(points, furthest_site=False, incremental=False, qhull_options=None)
 |
 |  Delaunay tessellation in N dimensions.

 |  Attributes
 |  ----------
 |  points : ndarray of double, shape (npoints, ndim)
 |      Coordinates of input points.
 |  simplices : ndarray of ints, shape (nsimplex, ndim+1)
 |      Indices of the points forming the simplices in the triangulation.
 |      For 2-D, the points are oriented counterclockwise.
 |  neighbors : ndarray of ints, shape (nsimplex, ndim+1)
 |      Indices of neighbor simplices for each simplex.
 |      The kth neighbor is opposite to the kth vertex.
 |      For simplices at the boundary, -1 denotes no neighbor.
"""