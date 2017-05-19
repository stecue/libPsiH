# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:44:37 2016

@author: xing
"""
from __future__ import print_function
import numpy as np
from mayavi import mlab
from mayavi.filters.transform_data import TransformData
from libPsiH.psi import *
from libPsiH.cube import *

def rotMat3D(axis, angle, tol=1e-12):
    """Return the flattened rotation matrix for 3D rotation by angle `angle` degrees about an
    arbitrary axis `axis`.
    """
    t = np.radians(angle)
    x, y, z = axis
    R = (np.cos(t))*np.eye(3) +\
    (1-np.cos(t))*np.matrix(((x**2,x*y,x*z),(x*y,y**2,y*z),(z*x,z*y,z**2))) + \
    np.sin(t)*np.matrix(((0,-z,y),(z,0,-x),(-y,x,0)))
    R[np.abs(R)<tol]=0.0
    Rt = np.eye(4)
    Rt[0:3,0:3] = R # in homogeneous coordinates
    Rtl = list(Rt.flatten())
    return Rtl

def plotPsi(cubdata,relContours=np.array([0.2,0.5,0.8]),**kwargs):
    if 'useOpaque' in kwargs:
        useOpaque=kwargs['useOpaque']
    else:
        useOpaque=True
    if 'limitA' in kwargs:
        limitA=kwargs['limitA']
    else:
        limitA=(1000,1000,1000)
    if 'limitB' in kwargs:
        limitB=kwargs['limitB']
    else:
        limitB=(1000,1000,1000)
    if 'rep' in kwargs:
        rep=kwargs['rep']
    else:
        rep='surface'
    if 'useLighting' in kwargs:
        useLighting=kwargs['useLighting']
    else:
        useLighting=True
    if 'lineWidth' in kwargs:
        lineWidth=kwargs['lineWidth']
    else:
        lineWidth=2.0
    if 'figSize' in kwargs:
        figSize=kwargs['figSize']
    else:
        figSize=(500,500)
    if 'zoomIn' in kwargs:
        zoomIn=kwargs['zoomIn']
    else:
        zoomIn=1.5
    if 'file2save' in kwargs:
        file2save=kwargs['file2save']
    else:
        file2save='pplot.png'
    if 'useCutPlane' in kwargs:
        useCutPlane=kwargs['useCutPlane']
    else:
        useCutPlane=False
    if 'planeA' in kwargs:
        planeA=kwargs['planeA']
    else:
        planeA='x_axes'
    if 'planeB' in kwargs:
        planeB=kwargs['planeB']
    else:
        planeB='y_axes'
    if 'planeOrigin' in kwargs:
        planeOrigin=kwargs['planeOrigin']
    else:
        planeOrigin=(0,0,0)
    if 'useRotation' in kwargs:
        useRotation=kwargs['useRotation']
    else:
        useRotation=False
    if 'rotAxis' in kwargs:
        rotAxis=kwargs['rotAxis']
    else:
        rotAxis=(0,0,1)
    if 'rotAngle' in kwargs:
        rotAngle=kwargs['rotAngle']
    else:
        rotAngle=0;
    #Disable useRotation
    if useRotation:
        print('NOT IMPLEMENTED YET: ImageData/StructuredPoints/RectilinearGrid not supported now.')
        #See http://docs.enthought.com/mayavi/mayavi/data.html for data types.
        useRotation=False

    cubreal=np.real(cubdata)
    cubimag=np.imag(cubdata)
    mlab.figure(1, bgcolor=(1.0,1.0,1.0), size=figSize)
    #mlab.clf()    
    engine=mlab.get_engine();
    if useRotation:
        transform_data_filter = TransformData()
        Rtl = rotMat3D(rotAxis, rotAngle) # in homogeneous coordinates
        transform_data_filter.transform.matrix.__setstate__({'elements': Rtl})
        transform_data_filter.widget.set_transform(transform_data_filter.transform)
        transform_data_filter.filter.update()
        transform_data_filter.widget.enabled = False   # disable the rotation control further.
    
    cubreal_pos=(cubreal+np.abs(cubreal))/2
    cubreal_neg=np.abs((cubreal-np.abs(cubreal))/2)
    source_pos = mlab.pipeline.scalar_field(cubreal_pos)
    if useRotation:
        engine.add_filter(transform_data_filter, source_pos)
    if cubreal_neg.max()-cubreal_neg.min()>1e-8:
        source_neg = mlab.pipeline.scalar_field(cubreal_neg)
        if useRotation:
            engine.add_filter(transform_data_filter, source_pos)
    min_real = min(cubreal_pos.min(),cubreal_neg.min())
    max_real = min(cubreal_pos.max(),cubreal_neg.max())
    if max_real<1e-6:
        max_real= max(cubreal_pos.max(),cubreal_neg.max())
    print('(min_pos,max_pos);(min_neg,max_neg)')
    print(cubreal_pos.min(),cubreal_pos.max(),cubreal_neg.min(),cubreal_neg.max())
    range_real=max_real - min_real      
    ##Prep for Imag Part
    cubimag_pos=np.abs((cubimag+np.abs(cubimag))/2)
    cubimag_neg=np.abs((cubimag-np.abs(cubimag))/2)
    source_imag_pos = mlab.pipeline.scalar_field(cubimag_pos)
    source_imag_neg = mlab.pipeline.scalar_field(cubimag_neg)
    min_imag = min(cubimag_pos.min(),cubimag_neg.min())
    print('min_imag:')
    print(min_imag)
    max_imag = max(cubimag_pos.max(),cubimag_neg.max())
    min_all=min(min_real,min_imag);
    max_all=max(max_real,max_imag);
    #print (min_all,max_all)
    range_all=max(max_imag-min_imag,range_real)
    print (min_all,max_all)
    volcontours=(min_all+relContours*range_all).tolist()
    thr_cut=volcontours[0] #print volcontours
    #Plot cut plane first:
    if useCutPlane==True:
        thr = mlab.pipeline.threshold(source_pos,low=thr_cut)
        cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                plane_orientation=planeA,
                                colormap='Reds',vmin=min_all,vmax=max_all)
        cut_plane.implicit_plane.origin = planeOrigin;
        cut_plane.implicit_plane.widget.enabled = False;
        cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                plane_orientation=planeB,
                                colormap='Reds',vmin=min_all,vmax=max_all)
        cut_plane.implicit_plane.origin = planeOrigin;
        cut_plane.implicit_plane.widget.enabled = False;
    source_posA = mlab.pipeline.extract_grid(source_pos);
    if useCutPlane==True:
        source_posA.set(x_max=limitA[0],y_max=limitA[1],z_max=limitA[2]);
    vol1 = mlab.pipeline.iso_surface(source_posA,colormap='Reds',vmin=min_all,vmax=max_all,opacity=1.0) #No need ot use opacity with wireframes
    #See https://mail.scipy.org/pipermail/scipy-user/2007-March/011466.html
    vol1.contour.set(auto_contours=False,number_of_contours=3)
    vol1.contour.contours = volcontours
    vol1.actor.property.representation = rep
    vol1.actor.property.lighting = useLighting
    vol1.actor.property.line_width = lineWidth
    vol1.actor.actor.force_opaque=useOpaque
    ##"B" surfaces:
    if useCutPlane==True:
        source_posB = mlab.pipeline.extract_grid(source_pos);
        source_posB.set(x_max=limitB[0],y_max=limitB[1],z_max=limitB[2]);
        vol1b = mlab.pipeline.iso_surface(source_posB,colormap='Reds',vmin=min_all,vmax=max_all,opacity=1.0) #No need ot use opacity with wireframes
        #See https://mail.scipy.org/pipermail/scipy-user/2007-March/011466.html
        vol1b.contour.set(auto_contours=False,number_of_contours=3)
        vol1b.contour.contours = volcontours
        vol1b.actor.property.representation = rep
        vol1b.actor.property.lighting = useLighting
        vol1b.actor.property.line_width = lineWidth
        vol1b.actor.actor.force_opaque=useOpaque
    if cubreal_neg.max()-cubreal_neg.min()>1e-8:
        if useCutPlane==True:
            thr = mlab.pipeline.threshold(source_neg,low=thr_cut)
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeA,
                                    colormap='Blues',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeB,
                                    colormap='Blues',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
        source_negA = mlab.pipeline.extract_grid(source_neg);
        if useCutPlane==True:
            source_negA.set(x_max=limitA[0],y_max=limitA[1],z_max=limitA[2]);    
        vol2 = mlab.pipeline.iso_surface(source_negA,colormap='Blues',vmin=min_all,vmax=max_all,opacity=1.0)
        vol2.contour.set(auto_contours=False,number_of_contours=3)
        vol2.contour.contours = volcontours
        vol2.actor.property.representation = rep
        vol2.actor.property.lighting = useLighting
        vol2.actor.property.line_width = lineWidth
        vol2.actor.actor.force_opaque=useOpaque
        ##"B" surfaces
        if useCutPlane==True:
            source_negB = mlab.pipeline.extract_grid(source_neg);
            source_negB.set(x_max=limitB[0],y_max=limitB[1],z_max=limitB[2]);    
            vol2b = mlab.pipeline.iso_surface(source_negB,colormap='Blues',vmin=min_all,vmax=max_all,opacity=1.0)
            vol2b.contour.set(auto_contours=False,number_of_contours=3)
            vol2b.contour.contours = volcontours
            vol2b.actor.property.representation = rep
            vol2b.actor.property.lighting = useLighting
            vol2b.actor.property.line_width = lineWidth
            vol2b.actor.actor.force_opaque=useOpaque
    ##Imag Part (Postive First)
    if max_imag-min_imag>1e-8:
        source_imag_posA=mlab.pipeline.extract_grid(source_imag_pos)
        if useCutPlane==True:
            source_imag_posA.set(x_max=limitA[0],y_max=limitA[1],z_max=limitA[2]);
        vol3 = mlab.pipeline.iso_surface(source_imag_posA,colormap='YlOrBr',vmin=min_all,vmax=max_all,opacity=1.0)
        vol3.contour.set(auto_contours=False,number_of_contours=3)
        vol3.contour.contours = volcontours
        vol3.actor.property.representation = rep
        vol3.actor.property.lighting = useLighting
        vol3.actor.property.line_width = lineWidth
        vol3.actor.actor.force_opaque=useOpaque
        #PlaneB
        if useCutPlane==True:
            source_imag_posB=mlab.pipeline.extract_grid(source_imag_pos)
            source_imag_posB.set(x_max=limitB[0],y_max=limitB[1],z_max=limitB[2]);
            vol3b = mlab.pipeline.iso_surface(source_imag_posA,colormap='YlOrBr',vmin=min_all,vmax=max_all,opacity=1.0)
            vol3b.contour.set(auto_contours=False,number_of_contours=3)
            vol3b.contour.contours = volcontours
            vol3b.actor.property.representation = rep
            vol3b.actor.property.lighting = useLighting
            vol3b.actor.property.line_width = lineWidth
            vol3b.actor.actor.force_opaque=useOpaque
        if useCutPlane==True:
            thr = mlab.pipeline.threshold(source_imag_pos, low=thr_cut)
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeA,
                                    colormap='YlOrBr',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeB,
                                    colormap='YlOrBr',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
        #Negtive Imag Part
        source_imag_negA=mlab.pipeline.extract_grid(source_imag_neg)
        if useCutPlane==True:
            source_imag_negA.set(x_max=limitA[0],y_max=limitA[1],z_max=limitA[2])
        vol4 = mlab.pipeline.iso_surface(source_imag_negA,colormap='Greens',vmin=min_all,vmax=max_all,opacity=1.0)
        vol4.contour.set(auto_contours=False,number_of_contours=3)
        vol4.contour.contours = volcontours
        vol4.actor.property.representation = rep
        vol4.actor.property.lighting = useLighting
        vol4.actor.property.line_width = lineWidth
        vol4.actor.actor.force_opaque=useOpaque
        if useCutPlane==True:
            #PlaneB
            source_imag_negB=mlab.pipeline.extract_grid(source_imag_neg)
            source_imag_negB.set(x_max=limitB[0],y_max=limitB[1],z_max=limitB[2])
            vol4b = mlab.pipeline.iso_surface(source_imag_negB,colormap='Greens',vmin=min_all,vmax=max_all,opacity=1.0)
            vol4b.contour.set(auto_contours=False,number_of_contours=3)
            vol4b.contour.contours = volcontours
            vol4b.actor.property.representation = rep
            vol4b.actor.property.lighting = useLighting
            vol4b.actor.property.line_width = lineWidth
            vol4b.actor.actor.force_opaque=useOpaque
        if useCutPlane==True:
            thr = mlab.pipeline.threshold(source_imag_neg, low=thr_cut)
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeA,
                                    colormap='Greens',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
            cut_plane = mlab.pipeline.scalar_cut_plane(thr,
                                    plane_orientation=planeB,
                                    colormap='Greens',vmin=min_all,vmax=max_all)
            cut_plane.implicit_plane.origin = planeOrigin;
            cut_plane.implicit_plane.widget.enabled = False;
    #mlab.view(132, 54, 45, [21, 20, 21.5])
    currS=engine.current_scene.scene;
    currS.parallel_projection=True
    currS.show_axes=True
    #currS.x_plus_view()
    #currS.camera.azimuth(30)
    #currS.camera.elevation(15)
    currS.isometric_view()
    #currS.camera.view_up = [0.0, 0.0, 1.0]
    currS.camera.zoom(zoomIn)
    currS.save(file2save)
    mlab.show()
    #no meaning to return currS b/c mlab.show() won't finish unless the window is closed!
    return range_all
