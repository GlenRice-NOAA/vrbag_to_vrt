# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 15:24:38 2022
"""
import os, sys
from glob import glob
from osgeo import gdal
gdal.UseExceptions()


def vrbag_to_vrt(infilename:str):
    """
    Export Variable Resolution Bathymetric Attributed Grid Super Cells to
    GeoTIFFs and build a VRT.
    ToDo : Building overviews does not appear to work?
    """
    path, bag_name = os.path.split(infilename)
    # get the paths to the
    ds = gdal.OpenEx(infilename, open_options=["MODE=LIST_SUPERGRIDS"])
    subds = ds.GetSubDatasets()
    flist = []
    for sg in subds:
        subgroupname = os.path.join(path, sg[0])
        flist.append(subgroupname)
    del ds
    # Build the VRT
    vrt_path = infilename + '.vrt'
    vrt = gdal.BuildVRT(vrt_path, flist, resampleAlg='near', resolution="highest")
    band1 = vrt.GetRasterBand(1)
    band1.SetDescription('Elevation')
    band2 = vrt.GetRasterBand(2)
    band2.SetDescription('Uncertainty')
    del vrt
    vrt = gdal.Open(vrt_path, 0)
    vrt.BuildOverviews()
    vrt = None
    

def main(infilename):
    vrbag_to_vrt(infilename)


if __name__=='__main__':
    if len(sys.argv) > 1:
        infilename = sys.argv[1]
        if os.path.exists(infilename):
            main(infilename)
        else:
            raise ValueError(f'{infilename} not found')