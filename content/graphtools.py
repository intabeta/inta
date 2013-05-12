from math import log, sqrt, cos, sin, pi
from copy import deepcopy

class Graph:
    def __init__(self, points, edges, res): #points is a number of points; res should be in the thousands for a decent graph
        self.res = res

        self.points=[]
        self.edges=[]
        self.forces=[]
        self.velocities=[]
        self.bestenergy=10000
        self.bestpoints=[]

        for p in range(points):
            self.createpoint(0,0)

        for e in edges:
            self.createedge(e[0],e[1],e[2])

        self.arrangepoints()

        for i in range(res):
            self.update()

        minx = min([ p[0] for p in self.points ])
        maxx = max([ p[0] for p in self.points ])
        miny = min([ p[1] for p in self.points ])
        maxy = max([ p[1] for p in self.points ])
        minx -= 0.1*abs(minx)
        maxx += 0.1*abs(maxx)
        miny -= 0.1*abs(miny)
        maxy += 0.1*abs(maxy)
        xrange = maxx - minx
        yrange = maxy - miny
        r = max([xrange,yrange])
        self.points = [ [(p[0]-minx)*300/r,(p[1]-miny)*300/r] for p in self.points ]

    def createpoint(self,x,y):
        self.points.append([x,y])
        self.forces.append([0,0])
        self.velocities.append([0,0])
        
    def createedge(self,v1,v2,s): #s is the strength
        self.edges.append([v1,v2,s])

    def arrangepoints(self):
        n = len(self.points)
        for i in range(n):
            p=self.points[i]
            p[0]=150+100*cos(2*pi*i/n)
            p[1]=150+100*sin(2*pi*i/n)

    def update(self):
        for i in range(len(self.points)):
            p = self.points[i]
            v = self.velocities[i]
            f = self.forces[i]
            v[0] += f[0]/100
            v[1] += f[1]/100
            p[0] += v[0]
            p[1] += v[1]
            f[0] = -v[0]*0.3 #resets forces and adds damping force
            f[1] = -v[1]*0.3
            for p1 in self.points[:i]+self.points[i+1:]:
                d=((p[0]-p1[0])**2 + (p[1]-p1[1])**2)**1.5
                f[0]+=30000*(p[0]-p1[0])/d
                f[1]+=30000*(p[1]-p1[1])/d
            self.forces[i] = f
            
        for e in self.edges:
            p=self.points[e[0]]
            p1=self.points[e[1]]
            f=self.forces[e[0]]
            f1=self.forces[e[1]]
            dx=p[0]-p1[0]
            dy=p[1]-p1[1]
            d=(dx**2 + dy**2)**0.5
            s=0.001*(1-10/(e[2]*d))
            f[0]-=s*dx
            f[1]-=s*dy
            f1[0]+=s*dx
            f1[1]+=s*dy
            self.forces[e[0]] = f
            self.forces[e[1]] = f1
