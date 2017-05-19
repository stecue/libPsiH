# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:11:54 2016

@author: xing
"""
from __future__ import print_function
import numpy as np
from libPsiH.psi import *

def loadCube(cubefile):
    data = np.fromstring(' '.join(open(cubefile).readlines()[7:]),sep=' ')
    data=data.reshape(50,50,50)
    return data

def loadCubeHiRes(cubefile):
    data = np.fromstring(' '.join(open(cubefile).readlines()[7:]),sep=' ')
    print('Loaded: '+'{:d}'.format(len(data)))
    nvolex=int(round(len(data)**(1./3)))
    data=data.reshape(nvolex,nvolex,nvolex)
    return data

def cubgen(cub2w,data,startX,startY,startZ,NX,NY,NZ,volX,volY,volZ):
    fcub=open(cub2w, 'w')
    fcub.write("DENSITY: cube filed generated by wavfunc_H\n");
    fcub.write("\n");
    fcub.write(" {:>4d} {:11.6f} {:11.6f} {:11.6f}\n".format(1,startX,startY,startZ))
    fcub.write(" {:>4d} {:11.6f} {:11.6f} {:11.6f}\n".format(NX,volX,0,0))
    fcub.write(" {:>4d} {:11.6f} {:11.6f} {:11.6f}\n".format(NY,0,volY,0))
    fcub.write(" {:>4d} {:11.6f} {:11.6f} {:11.6f}\n".format(NY,0,0,volZ))
    fcub.write(" {:>4d} {:11.6f} {:11.6f} {:11.6f} {:11.6f}\n".format(1,0,0,0,0))
    for ix in range(0,NX):
        for iy in range(0,NY):
            for iz in range(0,NZ):
                #fcub.write(" {:12.5E}".format(data[ix*NX+iy*NY+iz]));
                fcub.write(" {:12.5E}".format(data[ix][iy][iz]));
                if iz%6 == 5:
                    fcub.write('\n');
            fcub.write('\n');

#formated as h2o-elf.cube
def volGenPsi(n,l,m):
    if l==0:
        OAM='s'
    elif l==1:
        OAM='p'
    elif l==2:
        OAM='d'
    elif l==3:
        OAM='f'
    else:
        return 0        
    wavfunc_cub="H_"+'{:1d}'.format(n)+OAM+'{:+2d}'.format(m)+'.cube'
    if n<3.0:
        volex=0.25 #volex in Angstrom. 0.25 for l<2
    else:
        volex=0.45
    NX=50 #Positive means Ang
    NY=50
    NZ=50
    startX=-1.0*volex*NX/2+0.5*volex
    startY=-1.0*volex*NY/2+0.5*volex
    startZ=-1.0*volex*NZ/2+0.5*volex
    cubdata=np.zeros(NX*NY*NZ)+np.zeros(NX*NY*NZ)*1j
    cubdata=cubdata.reshape(NX,NY,NZ);
    Ang2Bohr=1.889725989
    for ix in range(NX):
        for iy in range(NY):
            for iz in range(NZ):
                #calculate iz points at the same time
                currX=startX*Ang2Bohr+ix*volex*Ang2Bohr
                currY=startY*Ang2Bohr+iy*volex*Ang2Bohr
                currZ=startZ*Ang2Bohr+np.arange(NZ)*volex*Ang2Bohr
                #currZ=startZ*Ang2Bohr+iz*volex*Ang2Bohr
                #cubdata[ix*NX+iy*NY:ix*NX+iy*NY+NZ]=psiH(currX,currY,currZ,2,0,0)
                if 2*l+1-m==0:
                    for mz in range(1,l+1):
                        cubdata[ix][iy][0:NZ]=psiH(currX,currY,currZ,n,l,mz)
                        cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]+psiH(currX,currY,currZ,n,l,-mz)
                    cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]+psiH(currX,currY,currZ,n,l,0)
                    cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]*np.sqrt(1.0/m)
                elif m<=l:
                    cubdata[ix][iy][0:NZ]=psiH(currX,currY,currZ,n,l,m)
                else:
                    return 0
    #Get the electron density:
    cubdata_dens=np.real(np.conj(cubdata)*cubdata);
    #cubdata=cubdata/cubdata.max();
    cubgen(wavfunc_cub+".dens",cubdata_dens,startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    cubgen(wavfunc_cub+".real",np.real(cubdata),startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    cubgen(wavfunc_cub+".imag",np.imag(cubdata),startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    return cubdata

def volGenPsiHiRes(n,l,m,volex,nvolex):
    #volex is in Angstrom!
    if l==0:
        OAM='s'
    elif l==1:
        OAM='p'
    elif l==2:
        OAM='d'
    elif l==3:
        OAM='f'
    else:
        return 0        
    wavfunc_cub="H_"+'{:1d}'.format(n)+OAM+'{:+2d}'.format(m)+'.cube'
    NX=nvolex #Positive means Ang
    NY=nvolex
    NZ=nvolex
    startX=-1.0*volex*NX/2+0.5*volex #Make sure a[NX][NY][NZ]=0 or 0.5volex
    startY=-1.0*volex*NY/2+0.5*volex
    startZ=-1.0*volex*NZ/2+0.5*volex
    cubdata=np.zeros(NX*NY*NZ)+np.zeros(NX*NY*NZ)*1j
    Ang2Bohr=1.889725989
    useLoop=False
    if useLoop:        
        cubdata=cubdata.reshape(NX,NY,NZ)
        for ix in range(NX):
            for iy in range(NY):
                for iz in range(NZ):
                    #calculate iz points at the same time
                    currX=startX*Ang2Bohr+ix*volex*Ang2Bohr
                    currY=startY*Ang2Bohr+iy*volex*Ang2Bohr
                    currZ=startZ*Ang2Bohr+np.arange(NZ)*volex*Ang2Bohr
                    #currZ=startZ*Ang2Bohr+iz*volex*Ang2Bohr
                    #cubdata[ix*NX+iy*NY:ix*NX+iy*NY+NZ]=psiH(currX,currY,currZ,2,0,0)
                    if 2*l+1-m==0:
                        for mz in range(1,l+1):
                            cubdata[ix][iy][0:NZ]=psiH(currX,currY,currZ,n,l,mz)
                            cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]+psiH(currX,currY,currZ,n,l,-mz)
                        cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]+psiH(currX,currY,currZ,n,l,0)
                        cubdata[ix][iy][0:NZ]=cubdata[ix][iy][0:NZ]*np.sqrt(1.0/m)
                    elif m<=l:
                        cubdata[ix][iy][0:NZ]=psiH(currX,currY,currZ,n,l,m)
                    else:
                        return 0
            print('...{:.1f}%'.format((ix+1)*1.0/NX*100),end='')
        print('...Done!')
    else:
        print('Using np.meshgrid()')
        coord_x=np.arange(startX,startX+NX*volex-0.1*volex,volex)
        coord_y=np.arange(startY,startX+NX*volex-0.1*volex,volex)
        coord_z=np.arange(startZ,startX+NX*volex-0.1*volex,volex)
        cubdata_x,cubdata_y,cubdata_z=np.meshgrid(coord_x,coord_y,coord_z,sparse=False,indexing='ij')
        print(cubdata_x[NX/2][NY/2][NZ/2],cubdata_y[NX/2][NY/2][NZ/2],cubdata_z[NX/2][NY/2][NZ/2])
        print(cubdata_x.shape)
        cubdata_x=cubdata_x.reshape(NX*NY*NZ)*Ang2Bohr
        cubdata_y=cubdata_y.reshape(NX*NY*NZ)*Ang2Bohr
        cubdata_z=cubdata_z.reshape(NX*NY*NZ)*Ang2Bohr
        print('Calculating Wavefunctions...')
        cubdata=psiH(cubdata_x,cubdata_y,cubdata_z,n,l,m)
        cubdata=cubdata.reshape(NX,NY,NZ)
    #Get the electron density:
    cubdata_dens=np.real(np.conj(cubdata)*cubdata);
    #cubdata=cubdata/cubdata.max();
    if nvolex%2==1:
        centroid=(nvolex-1)/2;
        cubdata[centroid][centroid][centroid]=0;
        cubdata[centroid][centroid][centroid]=(cubdata[centroid][centroid][centroid-1]+cubdata[centroid][centroid][centroid+1])/2;
    cubgen(wavfunc_cub+".dens",cubdata_dens,startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    cubgen(wavfunc_cub+".real",np.real(cubdata),startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    cubgen(wavfunc_cub+".imag",np.imag(cubdata),startX,startY,startZ,NX,NY,NZ,volex,volex,volex)
    return cubdata
