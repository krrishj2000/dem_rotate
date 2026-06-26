from osgeo import gdal, osr

# INPUTS 
input_file = "Masked_Bhima_DEM.tif"
output_file = "Rotated_Bhima_DEM.tif"
rotation_degrees_clockwise = 45 # Clockwise is taken as positive unfortunately

def dem_rotate(input_file, output_file, rotation_degrees_clockwise=90):
    
    '''
    input_file: DEM of any projection
    output_file: Rotated DEM of some projection
    rotation_degrees_clockwise: input degrees how much you want to rotate the dem in clockwise direction
    '''
    
    ds = gdal.Open(input_file)
    if not ds:
        raise FileNotFoundError(f"The file couldn't be opened: {input_file}")
    
    # Here, we will extract the CRS of the DEM
    native_srs_txt = ds.GetProjection()
    native_srs = osr.SpatialReference()
    native_srs.ImportFromWkt(native_srs_txt)
    
    # The function GetGeoTransform returns (top_left_x, pixel_width, row_rotation, top_left_y, col_rotation, pixel_height)
    gt = ds.GetGeoTransform()
    width = ds.RasterXSize
    height = ds.RasterYSize
    
    # Finding the centre in native CRS
    center_x = gt[0] + (width / 2.0) * gt[1] + (height / 2.0) * gt[2]
    center_y = gt[3] + (width / 2.0) * gt[4] + (height / 2.0) * gt[5]
    
    # The main idea of transforming to wgs thing was just to get the rotation stuff, so here we will only transform the centre as it is only required for that purpose
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)

    # Some stuff to handle this GDAL version issue
    if int(gdal.VersionInfo()[0]) >= 3:
        wgs84_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    
    transform = osr.CoordinateTransformation(native_srs, wgs84_srs)
    lon, lat, _ = transform.TransformPoint(center_x, center_y)
    
    print(f"Centre Lat and Lon is: {lat},{lon}")
    
    # Here we will simply define the projection strings
    proj_tmerc = f"+proj=tmerc +lat_0={lat} +lon_0={lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    proj_omerc = f"+proj=omerc +lat_0={lat} +lonc={lon} +alpha={rotation_degrees_clockwise} +k=1 +x_0=0 +y_0=0 +gamma=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    
    # Now the main part, we want to bypass this temp file generation. So we execute that in gdal's memory. I don't know how memory efficient that is; need to dig deeper
    temp_vrt = '/vsimem/temp_tmerc.tif'
    
    # Warping to the Transverse Mercator stuff
    warp_options = gdal.WarpOptions(dstSRS=proj_tmerc, format='GTiff')
    in_memory_ds = gdal.Warp(temp_vrt, ds, options=warp_options)
    
    # Checking if the warping is done successfully or not
    if in_memory_ds is None:
        raise RuntimeError("GDAL Warp failed")
        
    # Now we transform it to the Oblique guy
    translate_options = gdal.TranslateOptions(outputSRS=proj_omerc, format='GTiff')
    final_ds = gdal.Translate(output_file, in_memory_ds, options=translate_options)
    
    # Checking if the transformation is done successfully or not
    if final_ds is None:
        raise RuntimeError("GDAL Translate failed")
        
    # Dunno if this part is good or not, but from my C programming lessons, it is always a good practice to free up memory
    ds = None
    in_memory_ds = None
    final_ds = None
    gdal.Unlink(temp_vrt)
       
# FUNCTION CALL:
dem_rotate(input_file=input_file, output_file=output_file, rotation_degrees_clockwise=rotation_degrees_clockwise)