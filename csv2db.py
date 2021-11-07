# Import libraries
import os
import psycopg2

# Open database connection
conn = psycopg2.connect("dbname=test user=postgres password=postgres")
cur = conn.cursor()

# Open file
os.chdir('C:/Temp')
csv_file = open('meteo_stations.csv')

# Loop through file and insert into database
lijn_nummer = 0
for lijn in csv_file :
    
    if lijn_nummer > 0 :
        
        # Get attributes from line
        kolom_nummer = 1
        for kolom in lijn.split(',') :
            if kolom_nummer == 1 :
                alt = float(kolom)
            if kolom_nummer == 2 :
                lat = float(kolom)
            if kolom_nummer == 3 :
                lon = float(kolom)
            if kolom_nummer == 4: 
                meteostationid = int(kolom)
            if kolom_nummer == 5 :
                name = str(kolom)
            kolom_nummer = kolom_nummer + 1
            
        # Insert into database
        insert_stmt = 'insert into meteostation ( meteostationid, alt, name, location ) values ( %s, %s, %s, ST_Transform(ST_SetSRID(ST_MakePoint(%s,%s),4326),28992))' 
        cur.execute ( insert_stmt, ( meteostationid, alt, name, lon, lat ) )
    
    lijn_nummer = lijn_nummer + 1

print (str(lijn_nummer) + ' lijnen opgeslagen in database')

# Close file
csv_file.close()

# Commit and close database connection
conn.commit()
conn.close()

print('End of script')

