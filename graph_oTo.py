def oTo():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plot
    import sqlite3 as sq
    import glob as gb
    import os
    '''def graph(percent,fileNames,x,j,temp):
        size_of_groups=[100-percent,percent]
        percent2=str(percent)+'%'
        print('percent: ',percent2)
        # Create a pieplot
        #plt.pie(size_of_groups,colors=['grey','red'],='55')
        plt.pie(size_of_groups,colors=['green','red'], startangle=90)

        # add a circle at the center to transform it in a donut chart
        my_circle=plt.Circle( (0,0), 0.7, color='white')
        plt.text(0.1,-0.3,percent2,fontsize=40,ha='center',va='bottom')
        p=plt.gcf()
        p.gca().add_artist(my_circle)

        if temp==0:
            plt.savefig(fileNames[x]+'-'+fileNames[j]+'_CS'+'.png')
        elif temp==1:
            plt.savefig(fileNames[x]+'-'+fileNames[j]+'_LSA'+'.png')
        plt.show()

    def demo():

        con=sq.connect('COSINE_SIMILARITY.db')   
        cur=con.cursor()
        cur.execute("Select * from cs")
        rows=cur.fetchall()
        cur.execute("Select * from LSAA")
        rows_LSA=cur.fetchall()
        fileNames=[]
        index=0
        cur.execute("Select FILES FROM cs ")
        data=cur.fetchall()
        for i in data:
            fileNames.append(i[0])
        for x in range(1,len(rows)+1):
            conn = sqlite3.connect("Project.db")  # Replace 'Project.db' with the correct path to your SQLite database file
            
            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()
                
                # Define the SQL query to fetch column names
                columns_query = "PRAGMA table_info('Graph')"
                cursor.execute(columns_query)
            
            # Fetch all rows from the result
            columns_info = cursor.fetchall()
            
            # Extract column names from the fetched rows
            columns = [col[1] for col in columns_info if col[1] not in ('id', 'Files')]  # Exclude 'id' and 'Files' columns
            
            # Construct the SELECT query dynamically
            columns_str = ', '.join(columns)
            query = f"SELECT {columns_str} FROM Graph"
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch all rows from the result
            rows = cursor.fetchall()
            
            # Close the cursor
            cursor.close()
            
            # Close the database connection
            conn.close()
            
            # Create a DataFrame from the fetched rows
            df = pd.DataFrame(rows, columns=columns)
            
            # Plot bar graphs for each row in the DataFrame
            for i, row in df.iterrows():
                plt.bar(row.index, row.values)
                plt.title(f'Row {i+1}')
                plt.xlabel('Names')
                plt.ylabel('Values')
                plt.show()


    demo()'''
    def create():
        import sqlite3 as sq
        con=sq.connect('GRAPH.db')   
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS oTo_CS(ID INTEGER PRIMARY KEY,PHOTO BLOB NOT NULL,SRC TEXT,DEST TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS oTo_LSA(ID INTEGER PRIMARY KEY,PHOTO BLOB NOT NULL,SRC TEXT,DEST TEXT)")
        con.commit()
        con.close()
    def insertion(text,src,des,temp):
        def dltPhoto():
            photo=gb.glob('./*.jpg')
            for i in photo:
                if os.path.exists(i):
                    os.remove(i)
        def convertData(filename):
            # Convert digital data to binary format
            with open(filename, 'rb') as file:
                #print(filename)
                blobData = file.read()

            return blobData

        def insertPhoto(photo,src,dest):

                con = sq.connect('GRAPH.db')
                cursor =con.cursor()
                xPhoto = convertData(photo)
                if temp==0:
                    cursor.execute("INSERT INTO oTo_CS (photo,src,dest) VALUES(?,?,?)",(xPhoto,src,dest))
                elif temp==1:
                    cursor.execute("INSERT INTO oTo_LSA (photo,src,dest) VALUES(?,?,?)",(xPhoto,src,dest))
                con.commit()
                con.close()

                #print("Inserted :)")
                dltPhoto()
        insertPhoto(text,src,des)

    def graph(percent,fileNames,x,j,temp):
        size_of_groups=[100-percent,percent]
        percent2=str(percent)+'%'
        # Create a pieplot
        #plt.pie(size_of_groups,colors=['grey','red'],='55')
        plot.rcParams['savefig.facecolor']='#33ffcc'
        if percent<=50:
            plot.pie(size_of_groups,colors=['white','green'], startangle=90)
        elif percent>=51 and percent <=75:
            plot.pie(size_of_groups,colors=['white','orange'], startangle=90)
        else:
            plot.pie(size_of_groups,colors=['white','red'], startangle=90)

        # add a circle at the center to transform it in a donut chart
        my_circle=plot.Circle( (0,0), 0.7, color='white')
        frame=plot.text(0.1,-0.25,percent2,fontsize=40,ha='center',va='bottom')
        p=plot.gcf()
        p.gca().add_artist(my_circle)

        if temp==0:
            photoName=fileNames[x]+'-'+fileNames[j]+'_CS'+'.jpg'
             
            plot.savefig(fileNames[x]+'-'+fileNames[j]+'_CS'+'.jpg')
            insertion(photoName,fileNames[x],fileNames[j],0)
            frame.remove()
            plot.clf()
        elif temp==1:
            photoName=fileNames[x]+'-'+fileNames[j]+'_LSA'+'.jpg'
             
            plot.savefig(fileNames[x]+'-'+fileNames[j]+'_LSA'+'.jpg')
            insertion(photoName,fileNames[x],fileNames[j],1)
            frame.remove()
            plot.clf()
        #plt.show()

    def demo():
        create()
        con=sq.connect('COSINE_SIMILARITY.db')   
        cur=con.cursor()
        cur.execute("Select * from CS")
        rows=cur.fetchall()
        cur.execute("Select * from LSA")
        rows_LSA=cur.fetchall()
        fileNames=[]
        index=0
        cur.execute("Select FILES FROM CS ")
        data=cur.fetchall()
        for i in data:
            fileNames.append(i[0])
        for x in range(1,len(rows)):
            cur.execute("Select * FROM CS WHERE ID=?",(x,))
            data=cur.fetchall()
            cur.execute("Select * FROM LSA WHERE ID=?",(x,))
            data_LSA=cur.fetchall()
            #print('original: ',data[0])
            #print(len(data[0]))
            for j in range(x+2,len(data[0])):
                if j==x+1:
                    pass
                else:
                    percent=(data[0][j])
                    percent*=100
                    #print('xx: ',x-1," jj: ",j-2)
                    percent_LSA=(data_LSA[0][j])
                    percent_LSA*=100
                    #print('percent: ',data[0][j])
                    #print('x: ',x-1,'j: ',j-2)
                    graph(int(percent),fileNames,x-1,j-2,0)
                    graph(int(percent_LSA),fileNames,x-1,j-2,1)



    demo()
