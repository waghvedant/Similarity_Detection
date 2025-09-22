import sqlite3 as sq
def saveTofile(data, filename):
    
    with open(filename, 'wb') as file:
        file.write(data)
    print("Photo saved @: ", filename, "\n")

def getPhoto(src,des,temp):
        con = sq.connect('GRAPH.db')
        cur = con.cursor()
        print("Above OTO",src,"   ",des)
        if temp==0:
            cur.execute("SELECT * FROM oTo_CS WHERE (src= ? AND dest=?) OR (src=? AND dest=?)",(src,des,des,src))
        
            #cur.execute("SELECT * FROM oTo_LSA WHERE (src= ? AND dest=?) OR (src=? AND dest=?)",(src,des,des,src))
            record = cur.fetchall()
            for row in record:
                print('Im in OTO')
                photo = row[1]         
                photoPath = "G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend/static/"+"oTocs"+".jpeg"
                saveTofile(photo, photoPath)
        elif temp==1:
            #cur.execute("SELECT * FROM oTo_CS WHERE (src= ? AND dest=?) OR (src=? AND dest=?)",(src,des,des,src))
        
            cur.execute("SELECT * FROM oTo_LSA WHERE (src= ? AND dest=?) OR (src=? AND dest=?)",(src,des,des,src))
            record = cur.fetchall()
            for row in record:
                print('Im in OTO')
                photo = row[1]
                photoPath = "G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend/static/" + "oTolsa" + ".jpeg"
                saveTofile(photo, photoPath)
            

        con.close()

#getPhoto('Third','Fourth',0)
