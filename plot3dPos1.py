# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:38:55 2016

@author: xing
"""

from libPsiH.wavetools import loadCubeHiRes,plotPsi,volGenPsi
#from libPsiH import *
   
usePreload=True
if usePreload:
    psi2pNeg1=loadCubeHiRes('H_3d+1.cube.real')+loadCubeHiRes('H_3d+1.cube.imag')*1j
    plotPsi(psi2pNeg1,rep='wireframe',useLighting=False,lineWidth=0.5,zoomIn=1.5,figSize=(320,320))
else:
    psi2pPos1=volGenPsi(3,2,-2)
    plotPsi(psi2pPos1,rep='wireframe')