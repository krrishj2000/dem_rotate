dem_rotate(input_geotiff, output_geotiff, rotation_angle)

**Use case**: For GIS based processes where rotation of a digital elevation model/any other geotiff is required.
**Example**: For flood modelling, it doesnt matter what the orientation of the valley is. If you could rotate the DEM, it can be cropped more tightly (orienting the valley along the diagonal of a rectangle, for example). This helps reduce the size  of the input tif file, which directly controls how fast the model can run.

**Credits**: https://gis.stackexchange.com/questions/131465/gdal-rotate-dem

**Logic:**
It converts the file first into [transverse mercator](https://en.wikipedia.org/wiki/Transverse_Mercator_projection) for the given longitude.
then it reprojects into a [oblique mercator](https://en.wikipedia.org/wiki/Oblique_Mercator_projection) projection, whose azimuthal angle is alpha.
so it is like rotating the earth below

![image](https://github.com/user-attachments/assets/311f3b78-7e25-4547-a241-dda3ee3c2ab9)
