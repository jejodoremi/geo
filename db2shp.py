# Import libraries
import os
import psycopg2
import ogr

# Open database connection
conn = psycopg2.connect("dbname=test user=postgres password=postgres")
cur = conn.cursor()

# Create new shapefile (see https://gdal.org/drivers/vector/index.html for formats)
os.chdir('C:/temp')
driver = ogr.GetDriverByName( 'ESRI Shapefile' )
fOut = driver.CreateDataSource('meteostations.shp')

# Create layer definition
outLayer = fOut.CreateLayer('meteostations', geom_type=ogr.wkbPoint)
outLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
outLayer.CreateField(ogr.FieldDefn('hoogte', ogr.OFTReal))
outLayer.CreateField(ogr.FieldDefn('naam', ogr.OFTString))        
featureDefn = outLayer.GetLayerDefn()

# Select all rows from database
sql = 'select meteostationid, alt, name, ST_AsText(location) from meteostation'
cur.execute(sql)
rows = cur.fetchall()
i = 0

# Loop through row, create feature and write to shapefile
for row in rows :
    meteostationid = int(row[0])
    alt = float(row[1])
    name = str(row[2])
    geom = str(row[3])
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetField('id', meteostationid)
    outFeature.SetField('hoogte', alt)        
    outFeature.SetField('naam', name)
    outFeature.SetGeometry(ogr.CreateGeometryFromWkt(geom))
    outLayer.CreateFeature(outFeature)
    i = i + 1

print(str(i) + ' rijen opgeslagen in shapefile')

# Close shapefile
fOut.Destroy()

# Close database connection
conn.close()

print('End of script')

