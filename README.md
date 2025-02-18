dem_rotate(input_geotiff, output_geotiff, rotation_angle)


**Credits**: https://gis.stackexchange.com/questions/131465/gdal-rotate-dem

It converts the file first into [transverse mercator](https://en.wikipedia.org/wiki/Transverse_Mercator_projection) for the given longitude.
then it reprojects into a [oblique mercator](https://en.wikipedia.org/wiki/Oblique_Mercator_projection) projection, whose azimuthal angle is alpha.
so it is like rotating the earth below

![image](https://github.com/user-attachments/assets/311f3b78-7e25-4547-a241-dda3ee3c2ab9)
