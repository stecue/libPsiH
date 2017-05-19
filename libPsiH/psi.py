# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:14:55 2016

@author: xing
"""
from __future__ import print_function
import numpy as np
import scipy.misc as sm
import scipy.special as ssp

#I'll follow the "physics convention",e.g., phi is [0,2pi]:
def spharm(l,m,theta,phi):
    #Note that the convention is different in ssp.sph_harm
    return (-1)**m*ssp.sph_harm(m,l,phi,theta)
    #The following is for references only
    if l==0:
        return 1.0/2.0*np.sqrt(1.0/np.pi);
    elif l==1:
        if m==-1:
            return 1.0/2.0*np.sqrt(3.0/2.0/np.pi)*np.exp(-1j*phi)*np.sin(theta)
        elif m==0:
            return 1.0/2.0*np.sqrt(3.0/np.pi)*np.cos(theta)
        elif m==1:
            return -1.0/2.0*np.sqrt(3.0/2.0/np.pi)*np.exp(1j*phi)*np.sin(theta)
        else:
            return 0
    else:
        return 0

def genLag(n,l,x):
    #See https://en.wikipedia.org/wiki/Laguerre_polynomials#Generalized_Laguerre_polynomials
    alpha=2.0*l+1.0
    n=n-l-1
    return ssp.eval_genlaguerre(n,alpha,x)
    #The following is for references only
    x=x*1.0
    print(n,alpha)
    if n==0:
        return 1;
    elif n==1:
        return -x+alpha+1.0
    elif n==2:
        return x**2/2.0-(alpha+2)*x+(alpha+2)*(alpha+1)/2
    elif n==3:
        return -x**3/6.0+(alpha+3)*x**2/2.0-(alpha+2)*(alpha+3)*x/2.0+(alpha+1)*(alpha+2)*(alpha+3)/6.0
    else:
        return 0

def car2sphere(x,y,z):
    x=x*1.0
    y=y*1.0
    z=z*1.0
    r=np.sqrt(x**2+y**2+z**2);
    theta=np.arccos(z/r)
    phi=np.arctan2(y,x)
    #Make phi in [0,2pi], not necessary though,especially if vectorized.
    #if (phi<0):
    #    phi=phi+2*np.pi
    return r,theta,phi

def sphere2car(r,theta,phi):
    r=r*1.0
    theta=theta*1.0
    phi=phi*1.0
    x=r*np.sin(theta)*np.cos(phi)
    y=r*np.sin(theta)*np.sin(phi)
    z=r*np.cos(theta)
    return x,y,z

def psiH(x,y,z,n,l,m):
    n=n*1.0
    l=l*1.0
    m=m*1.0
    (r,theta,phi)=car2sphere(x,y,z)
    rho=2.0*r/n #set a_0 to 1
    preFactor=np.sqrt((2/n)**3*sm.factorial(n-l-1)/2/n/sm.factorial(n+1))
    # See https://en.wikipedia.org/wiki/Hydrogen_atom#Wavefunction
    return preFactor*(rho**l)*genLag(n,l,rho)*np.exp(-0.5*rho)*spharm(l,m,theta,phi)
