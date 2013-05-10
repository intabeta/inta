from math import log, sqrt, cos, sin, pi
from copy import deepcopy

class Graph:
    def __init__(self, points, edges, res): #res should be in the thousands for a decent graph
        self.res = res

        self.points=[]
        self.edges=[]
        self.forces=[]
        self.velocities=[]
        self.bestenergy=10000
        self.bestpoints=[]

        for p in points:
            self.createpoint(p[0],p[1])

        for e in edges:
            self.createedge(e[0],e[1],e[2])

        self.arrangepoints()

        for i in range(res):
            self.update()
            self.updateforces()
            if self.energy() < self.bestenergy:
                self.bestenergy = self.energy()
                self.bestpoints = [ [p[0],p[1]] for p in self.points ]
        self.points = deepcopy(self.bestpoints)
        self.updateforces()

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
            p[0]=150+20*cos(2*pi*i/n)
            p[1]=150+20*sin(2*pi*i/n)

    def energy(self):
        e = 0
##        for f in self.forces:
##            e += f[0]**2 + f[1]**2
        for i in range(len(self.points)):
            p=self.points[i]
            for p1 in self.points[:i]+self.points[i+1:]:
                d=((p[0]-p1[0])**2 + (p[1]-p1[1])**2)**(-0.5)
                e += 200*d
        return e

    def updateforces(self):
        for i in range(len(self.points)):
            f=[0,0]
            p=self.points[i]
            for p1 in self.points[:i]+self.points[i+1:]:
                d=((p[0]-p1[0])**2 + (p[1]-p1[1])**2)**1.5
                f[0]+=10000*(p[0]-p1[0])/d
                f[1]+=10000*(p[1]-p1[1])/d
            self.forces[i]=f

        for e in self.edges:
            p=self.points[e[0]]
            p1=self.points[e[1]]
            f=self.forces[e[0]]
            f1=self.forces[e[1]]
            d=((p[0]-p1[0])**2 + (p[1]-p1[1])**2)**0.5
            s=0.01*e[2]
            f[0]-=s*(p[0]-p1[0])
            f[1]-=s*(p[1]-p1[1])
            f1[0]+=s*(p[0]-p1[0])
            f1[1]+=s*(p[1]-p1[1])
            self.forces[e[0]] = f
            self.forces[e[1]] = f1
            
    
    def update(self):
        for i in range(len(self.points)):
            p=self.points[i]
            v=self.velocities[i]
            f=self.forces[i]
            v[0] += f[0]/100
            v[1] += f[1]/100
            p[0] += v[0]
            p[1] += v[1]
