# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:38:55 2016

@author: xing
"""

from libPsiH.wavetools import *
#from libPsiH import *

usePreload=False
if usePreload:
    psi2pZero=loadCubeHiRes('H_2p+0.cube.real')+loadCubeHiRes('H_2p+0.cube.imag')*1j
    plotPsi(psi2pZero,rep='wireframe',useLighting=False,lineWidth=0.5,zoomIn=1.25,figSize=(320,320))
else:
    psi2pPos1=volGenPsi(2,1,0)
    plotPsi(psi2pPos1,rep='wireframe')
