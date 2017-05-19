# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:39:50 2016

@author: xing
"""

from __future__ import print_function
import numpy as np
from mayavi import mlab
from libPsiH.psi import *
from libPsiH.cube import *

def plotDens(cubdata,isovalue,**kwargs):
    if 'limit_min' in kwargs:
        limit_min=kwargs['limit_min']
    else:
        limit_min=(0,0,0)
    if 'file2save' in kwargs:
        file2save=kwargs['file2save']
    else:
        file2save='rplot.png'
    if 'useCutPlane' in kwargs:
        useCutPlane=kwargs['useCutPlane']
    else:
        useCutPlane=False
    if 'plane_origin' in kwargs:
        plane_origin=kwargs['plane_origin']
    else:
        plane_origin=(0,0,0)
    xmin=limit_min[0]
    ymin=limit_min[1]
    zmin=limit_min[2]
    cubdens=np.real(np.conj(cubdata)*cubdata)    
    min_real = cubdens.min()
    max_real = cubdens.max()
    
    mlab.figure(1, bgcolor=(1.0,1.0,1.0), size=(320,320))
    #mlab.clf()
    
    source_dens = mlab.pipeline.scalar_field(cubdens)
    iso_abs=min_real+isovalue*(max_real-min_real)
    if useCutPlane==True:
        thr = mlab.pipeline.threshold(source_dens, low=iso_abs)
        cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                plane_orientation='z_axes',
                                colormap='Oranges')
        cut_plane.implicit_plane.origin = plane_origin;
        cut_plane.implicit_plane.widget.enabled = False;
        cut_plane.actor.property.lighting = True
                                
    source_dens = mlab.pipeline.extract_grid(source_dens);
    source_dens.set(x_min=xmin,y_min=ymin,z_min=zmin);
    
    #vol = mlab.pipeline.volume(source, vmin=min + 0.65 * (max - min),
    #                                   vmax=min + 0.9 * (max - min))
                                       
    vol1 = mlab.pipeline.iso_surface(source_dens,colormap='Oranges') #No need ot use opacity with wireframes
    #See https://mail.scipy.org/pipermail/scipy-user/2007-March/011466.html
    vol1.contour.set(auto_contours=False,number_of_contours=1)
    vol1.contour.contours = [iso_abs] #braket to make it a list
    vol1.actor.property.representation = 'surface'
    vol1.actor.property.lighting = True
    vol1.actor.property.line_width = 0.5
    vol1.actor.actor.force_opaque=True
    engine=mlab.get_engine();
    currS=engine.current_scene.scene;
    currS.parallel_projection=True
    currS.show_axes=True
    #currS.x_plus_view()
    currS.isometric_view()
    currS.camera.zoom(1.25)
    #currS.camera.azimuth(15)
    #currS.camera.elevation(15)
    currS.save(file2save)
    mlab.show()
    return source_dens


def plotFullDens(cubdata,isovalue,file2save):
    
    cubdens=np.real(np.conj(cubdata)*cubdata)
    mlab.figure(1, bgcolor=(1.0,1.0,1.0), size=(320,320))
    mlab.clf()
    
    source_dens = mlab.pipeline.scalar_field(cubdens)
    #print source_dens
    min_real = cubdens.min()
    max_real = cubdens.max()
    #print (min_real,max_real)
    #vol = mlab.pipeline.volume(source, vmin=min + 0.65 * (max - min),
    #                                   vmax=min + 0.9 * (max - min))
                                       
    vol1 = mlab.pipeline.iso_surface(source_dens,colormap='Oranges') #No need ot use opacity with wireframes
    #See https://mail.scipy.org/pipermail/scipy-user/2007-March/011466.html
    vol1.contour.set(auto_contours=False,number_of_contours=1)
    vol1.contour.contours = [(min_real+isovalue*(max_real-min_real))] #braket to make it a list
    #print vol1.contour.contours
    vol1.actor.property.representation = 'surface'
    vol1.actor.property.lighting = True
    vol1.actor.property.line_width = 0.5
    vol1.actor.actor.force_opaque=True
    engine=mlab.get_engine();
    currS=engine.current_scene.scene;
    currS.parallel_projection=True
    currS.show_axes=True
    #currS.x_plus_view()
    currS.isometric_view()
    currS.camera.zoom(1.25)
    #currS.camera.azimuth(15)
    #currS.camera.elevation(15)
    currS.save(file2save)
    mlab.show()
    return currS