#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import numpy,random
from scipy.spatial import Delaunay
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from PIL import Image,ImageDraw

def gen_tri(HEIGHT=1080,WIDTH=1920,N_inside=30,N_edge_width=5,N_edge_height=4,margin=0.05):
    w_inf=int(WIDTH*margin)
    w_sup=int(WIDTH*(1-margin))
    h_inf=int(HEIGHT*margin)
    h_sup=int(HEIGHT*(1-margin))
    pts=[(random.randint(w_inf,w_sup),random.randint(h_inf,h_sup)) for i in range(N_inside)]
    pts+=[(0,random.randint(h_inf,h_sup)) for i in range(N_edge_height)]
    pts+=[(WIDTH,random.randint(h_inf,h_sup)) for i in range(N_edge_height)]
    pts+=[(random.randint(w_inf,w_sup),0) for i in range(N_edge_width)]
    pts+=[(random.randint(w_inf,w_sup),HEIGHT) for i in range(N_edge_width)]
    pts+=[(0,0),(0,HEIGHT),(WIDTH,0),(WIDTH,HEIGHT)]
    tri=Delaunay(numpy.array(pts))
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
        #return numpy.array([random.random() for t in self.ts])
        return [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for t in self.ts]


if __name__=="__main__":
    pts,tri=gen_tri(N_inside=30)
    cg=ColorGen(tri.simplices,pts)
    colors=cg.gen_colors()

    img=Image.new('RGB',(1920,1080)) #,(255, 255, 255)) # default black
    draw=ImageDraw.Draw(img)
    for i,t in enumerate(tri.simplices):
        draw.polygon([pts[t[0]],pts[t[1]],pts[t[2]]],fill=colors[i])
    img.show()
    img.save('bkg.png')
    img.save('bkg.jpg')

"""
    fig=plt.figure(figsize=[16,9],dpi=30) #16*120=1920
    ax=fig.subplots(1)
    #ax.triplot(pts[:,0],pts[:,1],tri.simplices,color='green', marker='o')
    #ax.plot(pts[:,0],pts[:,1],'o')
    plt.tripcolor(pts[:,0],pts[:,1],tri.simplices,facecolors=colors,edgecolors='k')
    plt.gca().set_aspect('equal')
    plt.show()
    fig.savefig("bkg.png")
"""

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