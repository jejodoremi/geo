# Import bibliotheken
import os, sys
import psycopg2

# Import ogr to read shapefile
import ogr

# Get driver for file type (list of codes: http://www.gdal.org/ogr_formats.html)
driver = ogr.GetDriverByName('ESRI Shapefile')

# Make database connection
conn = psycopg2.connect("dbname=test user=postgres password=postgres")

# Get cursor
cur = conn.cursor()

# Go to directory
os.chdir('C:/Temp')

# Open shape file
fIn = driver.Open('gemeentes.shp', 0)

# Get layer from shape file
layer = fIn.GetLayer(0)

# Loop over features
i = 0
for feature in layer:

    # Get attribute values
    i = i + 1
    gemnaam = feature.GetFieldAsString('gemeentenaam')
    geometrie = feature.GetGeometryRef()
    wkt_geometrie = str(geometrie.ExportToWkt())
    
    # Insert row into database, convert wkt from epsg 28992 to 4326
    insert_stmt = 'insert into gemeentes ( id, geom, naam ) values ( %s, ST_GeomFromText(%s, 28992), %s )' 
    cur.execute ( insert_stmt, ( i, wkt_geometrie, gemnaam ) )
    print ('Gemeente ' + str(gemnaam) + ' inserted')

    # Destroy feature and get next feature
    feature.Destroy()

# Close file
fIn.Destroy()    

# Commit and close database connection
conn.commit()
conn.close()

print('End of script')


