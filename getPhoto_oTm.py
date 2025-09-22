import sqlite3 as sq
def saveTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Photo saved @: ", filename, "\n")

def getPhoto(src,temp):
        con = sq.connect('GRAPH.db')
        cur = con.cursor()
        if temp==0:
            cur.execute("SELECT * FROM oTm_CS WHERE src= ? ",(src,))
        
            #cur.execute("SELECT * FROM oTm_LSA WHERE src= ? ",(src,))
            record = cur.fetchall()
            for row in record:
            
                photo = row[1]         
                photoPath = "G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend/static/"+"oTmcs"+".jpeg"
                saveTofile(photo, photoPath)
        elif temp==1:
            #cur.execute("SELECT * FROM oTm_CS WHERE src= ? ",(src,))
        
            cur.execute("SELECT * FROM oTm_LSA WHERE src= ? ",(src,))
            record = cur.fetchall()
            for row in record:
            
                photo = row[1]
                photoPath = "G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend/static/" + "oTmlsa" + ".jpeg"
                saveTofile(photo, photoPath)
            

        con.close()

#getPhoto('Third',0)
