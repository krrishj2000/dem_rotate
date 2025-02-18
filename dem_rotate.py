import rasterio as rs
import xarray as xa
import rasterio.warp as wrp
from rasterio.transform import rowcol

input_file='/home/krish/Documents/GLOF/Nare/gp_elev_4326.tif'
output_file='/home/krish/Documents/GLOF/Nare/gp_elev_rot.tif'

def dem_rotate(input_file,output_file,temp_file="temp.tif",rotation_degrees=90):
    raster=rs.open(input_file)

    width = raster.width 
    height = raster.height
    row, col = height // 2, width // 2  
    lon, lat = raster.xy(row, col) 
    print(f"Latitude: {lat}, Longitude: {lon}")
    raster.close()

    command1='gdalwarp -overwrite -s_srs EPSG:4326 -t_srs "+proj=tmerc +lat_0='+str(lat)+' +lon_0='+str(lon)+' +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -of GTiff '+input_file+' '+temp_file
    command2='gdal_translate -a_srs "+proj=omerc +lat_0='+str(lat)+' +lonc='+str(lon)+' +alpha='+str(rotation_degrees)+' +k=1 +x_0=0 +y_0=0 +gamma=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -of GTiff '+temp_file+' '+output_file

    import os
    os.system(command=command1)
    os.system(command=command2)


# modify as per your need below
dem_rotate(input_file='/home/krish/Documents/GLOF/Nare/gp_elev_4326.tif',output_file='/home/krish/Documents/GLOF/Nare/gp_elev_rot.tif',temp_file='/home/krish/Documents/GLOF/Nare/gp_elev_temp.tif',rotation_degrees=-15)
