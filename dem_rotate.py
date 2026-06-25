import rasterio as rs
import xarray as xa
import rasterio.warp as wrp
from rasterio.transform import rowcol

input_file_4326='dem_4326.tif'
output_file='dem_rot.tif'


def dem_rotate(input_file_4326,output_file,rotation_degrees_clockwise=90):
    """input file is a DEM in EPSG:4326 projection. rotation is in clockwise direction """
    temp_file="temp.tif"
    raster=rs.open(input_file_4326)

    width = raster.width 
    height = raster.height
    row, col = height // 2, width // 2  
    lon, lat = raster.xy(row, col) 
    print(f"Latitude: {lat}, Longitude: {lon}")
    raster.close()

    command1='gdalwarp -overwrite -s_srs EPSG:4326 -t_srs "+proj=tmerc +lat_0='+str(lat)+' +lon_0='+str(lon)+' +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -of GTiff '+input_file_4326+' '+temp_file
    command2='gdal_translate -a_srs "+proj=omerc +lat_0='+str(lat)+' +lonc='+str(lon)+' +alpha='+str(rotation_degrees_clockwise)+' +k=1 +x_0=0 +y_0=0 +gamma=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -of GTiff '+temp_file+' '+output_file

    import os
    os.system(command=command1)
    os.system(command=command2)
    os.remove(temp_file)

# modify as per your need below
dem_rotate(input_file_4326=input_file_4326,output_file=output_file,rotation_degrees_clockwise=45)
