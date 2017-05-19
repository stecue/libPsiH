# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:38:55 2016

@author: xing
"""

from libPsiH.pplot import *
from mayavi import mlab
import numpy as np

usePreLoad=False
if usePreLoad==True:   
    psi2pNeg1=loadCube('H_2p-1.cube.real')+loadCube('H_2p-1.cube.imag')*1j
    psi2pZero=loadCube('H_2p+0.cube.real')+loadCube('H_2p+0.cube.imag')*1j
    psi2pPos1=loadCube('H_2p+1.cube.real')+loadCube('H_2p+1.cube.imag')*1j
else:
    psi2pNeg1=np.array([0,0]);
    psi2pZero=np.array([0,0]);
    psi2pPos1=np.array([0,0]);

psi2p_x=np.sqrt(1/2.0)*(-1.0*psi2pNeg1+psi2pPos1)
psi2p_y=np.sqrt(1/2.0)*(psi2pNeg1+psi2pPos1)*(-1j)
psi2p_z=psi2pZero
def plotMixedReal(c1,c2,c3):
    sumPsi=c1*psi2p_x+c2*psi2p_y+c3*psi2p_z
    redCof=np.sqrt(np.abs(c1)**2+np.abs(c2)**2+np.abs(c3)**2)
    sumPsi=sumPsi/redCof
    plotPsi(sumPsi,'test1.png')
    coNeg1=-1*c1*np.sqrt(1/2.0)-1j*c2*np.sqrt(1/2.0)
    coPos1=c1*np.sqrt(1/2.0)-1j*c2*np.sqrt(1/2.0)
    coZero=c3
    print('coNeg1: {:.3f}\ncoZero: {:.3f}\ncoPos1: {:.3f}'.format(coNeg1,coZero,coPos1))
    return coNeg1,coPos1,coZero

def plotMixedEigen(c1,c2,c3):
    sumPsi=c1*psi2pNeg1+c2*psi2pZero+c3*psi2pPos1
    redCof=np.sqrt(np.abs(c1)**2+np.abs(c2)**2+np.abs(c3)**2)
    sumPsi=sumPsi/redCof
    plotPsi(sumPsi,'test1.png')
    coNeg1=c1/redCof
    coPos1=c2/redCof
    coZero=c3/redCof
    print('coNeg1: {:.3f}\ncoZero: {:.3f}\ncoPos1: {:.3f}'.format(coNeg1,coZero,coPos1))
    return coNeg1,coPos1,coZero

def plotMixedDens(c1,c2,c3):
    sumPsi=c1*psi2pNeg1+c2*psi2pZero+c3*psi2pPos1
    redCof=np.sqrt(np.abs(c1)**2+np.abs(c2)**2+np.abs(c3)**2)
    sumPsi=sumPsi/redCof
    plotDens(sumPsi,0.2,'test1.png')
    coNeg1=c1/redCof
    coPos1=c2/redCof
    coZero=c3/redCof
    print('coNeg1: {:.3f}\ncoZero: {:.3f}\ncoPos1: {:.3f}'.format(coNeg1,coZero,coPos1))
    return coNeg1,coPos1,coZero
#plotPsi(volGenPsi(3,2,1))
#plotDens(psi2pNeg1)
#print(plotPsi(psi2pZero*1j))
#print(plotPsi(psi2pZero))
#plotPsi((-1.0*psi2pNeg1+psi2pPos1+0.0*psi2pZero)*np.sqrt(1/1.5))
#plotPsi(psi2pZero)
    
#print(plotMixed(1.0,1.0,-1.0))
#plotMixed(1,1.414,1)
#imag_y
#plotMixed(-1.0-1j,1.414,1-1j)

#print(plotMixedEigen(1,1,1))
#plotMixedDens(1,1,1)
#plotDens(loadCube('H_2p+1.cube.dens'),0.2,'test.png')
print(np.arange(2,10,3)*0.1)

testPsi=False
if testPsi:
    plotFullDens(volGenPsi(4,0,0),0.2,'test_full.png')
    plotPsi(volGenPsi(4,0,0),'wireframe',False,'test_full.png')

useFull=2
if useFull==0:
    volData=volGenPsi(1,0,0);
    plotPsi(volData,'wireframe',False,'test_psi.png')
    plotFullDens(volData,0.04,'test_full.png')
elif useFull==1:
    plotDens(volGenPsi(3,0,0),0.04,0,0,25,'test_cut.png',True,(25.5,25.5,25.5))
elif useFull==2:
    volex=1.2
    nvol=31 #Note that volex*nvol is the diameter! volex*nvol/2 is the radius!
    if nvol%2==0:
        pOrigin=nvol/2.0+1
    else:
        pOrigin=nvol/2.0+0.55
    useHiRes=True
    if useHiRes==True:
        useSaved=True
        if useSaved:
            volData=loadCubeHiRes('H_2p+1.cube.real')+loadCubeHiRes('H_2p+1.cube.imag')*1j
            #plotPsi(volData,np.array([0.25,0.5,0.9]),(nvol/2,1000,1000),(1000,nvol/2,1000),'surface',True,'test_psi.png',False,'x_axes','y_axes',(pOrigin,pOrigin,pOrigin))
            plotPsi(volData,np.array([0.25,0.5,0.9]),rep='wireframe',useLighting=False)
        else:
            plotPsi(volGenPsiHiRes(3,2,0,volex,nvol),np.array([0.2,0.6,0.9]),True,(nvol/2,1000,1000),(1000,nvol/2,1000),'surface',True,'test_psi.png',False,'x_axes','y_axes',(pOrigin,pOrigin,pOrigin))
    else:
        plotPsi(volGenPsi(3,0,0),np.array([0.05,0.3,0.8]),(25,100,100),(100,25,100),'surface',True,'test_psi.png',True,'x_axes','y_axes',(26.1,26.1,26.1))
            
#plotDens(volGenPsi(3,2,2),0.2,'H3p2_rho.png')

#volS=volGenPsi(3,0,0)
#plotPsi(volS,'surface',True,'test2.png')
