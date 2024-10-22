from osgeo import gdal
import os
    
def orthorectify_dem_rpc(input, output, DEM, dtype=None):
    """ Orthorectify raster using rational polynomial coefficients and a DEM

    *Parameters*
    
    input : str
        Path to image to orthorectify
    output : str
        Path to output image
    DEM : str
        Path to DEM 
    dtype : int
        GDAL data type for output image (UInt16=2, Float32=6 etc.)
    
    *Returns*
    
    boolean
        True if it completes sucessfully
    """
    
    if dtype is None:
        dtype =  max([input.GetRasterBand(i + 1).DataType for i in range(input.RasterCount)])
      
    # set warp options
    optns = gdal.WarpOptions(
                transformerOptions = ["RPC_DEM={}".format(DEM)],
                creationOptions = ["TILED=YES", "BLOCKXSIZE=256", "BLOCKYSIZE=256"],
                rpc = True,
                multithread=True,
                outputType=dtype)
    
    # run warp
    gdal.Warp(output, input, options=optns)
    
    return(True)


def orthorectify_otb(input, output, DEMFolder, gridspacingx):
    """ Orthorectify raster using orfeotoolbox Ortho

    Parameters
    ----------
    input : str
        Path to image to orthorectify
    output : str
        Path to output image
    DEM : str
        Path to DEM
    gridspacing : float
        pixel size of deformation grid used for the ortho

    Returns
    -------
    """
    command = '''otbcli_OrthoRectification -io.in {} -io.out {} -map wgs -elev.dem {} -interpolator linear -opt.ram 2000 -opt.gridspacing {}'''.format(
        str(input), str(output), str(DEMFolder), str(gridspacingx))
    ok = os.system(command)
    print("Command result: {}".format(ok))
    

