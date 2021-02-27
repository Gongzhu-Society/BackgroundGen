#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import numpy,random
from scipy.spatial import Delaunay
from PIL import Image,ImageDraw
import colorsys

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

    def gauss_cut(mu,sigma):
        """
            cut gauss distribution into [0,1]
        """
        r=random.gauss(mu,sigma)
        while r<0 or r>1:
            r=random.gauss(mu,sigma)
        return r

    def colors_rand_rgb(self,rt=(0.8,0.2),gt=(0.1,0.1),bt=(0.1,0.1)):
        """
            random triangular color with rgb format
            rt, gt and bt is (mu,sigma)
        """
        colors=[]
        for t in self.ts:
            r=ColorGen.gauss_cut(*rt)
            g=ColorGen.gauss_cut(*gt)
            b=ColorGen.gauss_cut(*bt)
            colors.append((int(r*255),int(g*255),int(b*255)))
        return colors

    def colors_rand_hsv(self,ht=(0.95,0.05),st=(0.9,0.1),vt=(0.7,0.1)):
        """
            random triangular color with hsv format
            hsv is hue, saturation, value(brightness)
        """
        colors=[]
        for t in self.ts:
            h=ColorGen.gauss_cut(*ht)
            s=ColorGen.gauss_cut(*st)
            v=ColorGen.gauss_cut(*vt)
            rgb=colorsys.hsv_to_rgb(h,s,v)
            colors.append((int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255)))
        return colors

    def colors_rand_pt_rgb(self,rt=(0.5,0.2),gt=(0.1,0.1),bt=(0.1,0.1)):
        """
            random point color and get triangular color as its vertices' average
            I like this mode best
        """
        pt_r=[255*ColorGen.gauss_cut(*rt) for pt in self.pts]
        pt_g=[255*ColorGen.gauss_cut(*gt) for pt in self.pts]
        pt_b=[255*ColorGen.gauss_cut(*bt) for pt in self.pts]
        colors=[]
        for t in self.ts:
            r=int((pt_r[t[0]]+pt_r[t[1]]+pt_r[t[2]])/3)
            g=int((pt_g[t[0]]+pt_g[t[1]]+pt_g[t[2]])/3)
            b=int((pt_b[t[0]]+pt_b[t[1]]+pt_b[t[2]])/3)
            colors.append((r,g,b))
        return colors

if __name__=="__main__":
    pts,tri=gen_tri(N_inside=40)
    cg=ColorGen(tri.simplices,pts)
    #colors=cg.colors_rand_rgb()
    #colors=cg.colors_rand_hsv()
    colors=cg.colors_rand_pt_rgb()

    img=Image.new('RGB',(1920,1080)) #,(255, 255, 255)) # default black
    draw=ImageDraw.Draw(img)
    for i,t in enumerate(tri.simplices):
        draw.polygon([pts[t[0]],pts[t[1]],pts[t[2]]],fill=colors[i])
    img.show()
    img.save('bkg.png')

"""
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

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