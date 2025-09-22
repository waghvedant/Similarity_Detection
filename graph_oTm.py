def oTm():

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import sqlite3 as sq
    import glob as gb
    import os
    '''def graph(fileName,percent,singleFileName,temp):
        conn = sqlite3.connect("Project.db")  # Replace 'Project.db' with the correct path to your SQLite database file
        
        
        
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


        #plt.show()
    def demo():
        import sqlite3 as sq
        con=sq.connect('COSINE_SIMILARITY.db')   
        cur=con.cursor()
        cur.execute("Select * from cs")
        rows=cur.fetchall()
        cur.execute("Select * from LSA")
        rows_LSA=cur.fetchall()
        fileName=[]
        percent=[]
        percent_LSA=[]
        index=0
        for x in range(1,len(rows)+1):
            cur.execute("Select FILES FROM cs WHERE ID!=?",(x,))
            files=cur.fetchall()
            #print('files: ',files)
            cur.execute("Select FILES FROM cs WHERE ID=?",(x,))
            singleFile=cur.fetchall()
            print('singleFile: ',singleFile[0][0])
            singleFileName=singleFile[0][0]
            fileName.clear()
            for col in range(len(files)):
                    fileName.append(files[col][0])
            print('FileName: ',fileName)
            cur.execute("Select * FROM cs WHERE ID=?",(x,))
            data=cur.fetchall()
            cur.execute("Select * FROM LSA WHERE ID=?",(x,))
            data_LSA=cur.fetchall()
            #print(len(data[0]))
            #print('rows: ',data[0])
            percent.clear()
            percent_LSA.clear()
            for j in range(2,len(data[0])):
                    #print('j: ',j)
                    #print('index: ',index)
                    if j==x+1:

                        pass
                    else:
                        s=data[0][j]
                        s*=100
                        s_LSA=data_LSA[0][j]
                        s_LSA*=100
                        percent.append(s)
                        percent_LSA.append(s_LSA)

            print('percent: ',percent)
            index+=1
            graph(fileName,percent,singleFileName,0) 
            graph(fileName,percent_LSA,singleFileName,1) 


        con.close()
    demo()
    '''
    def create():
        import sqlite3 as sq
        con=sq.connect('GRAPH.db')   
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS oTm_CS(ID INTEGER PRIMARY KEY,PHOTO BLOB NOT NULL,SRC TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS oTm_LSA(ID INTEGER PRIMARY KEY,PHOTO BLOB NOT NULL,SRC TEXT)")
        con.commit()
        con.close()

    def insertion(text,src,temp):
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

        def insertPhoto(photo,src):

                con = sq.connect('GRAPH.db')
                cursor =con.cursor()
                xPhoto = convertData(photo)
                if temp==0:
                    cursor.execute("INSERT INTO oTm_CS (photo,src) VALUES(?,?)",(xPhoto,src))
                elif temp==1:
                    cursor.execute("INSERT INTO oTm_LSA (photo,src) VALUES(?,?)",(xPhoto,src))
                con.commit()
                con.close()

                #print("Inserted :)")
                dltPhoto()
        insertPhoto(text,src)

    def graph(fileName,percent,singleFileName,temp):
        index=np.arange(len(fileName))
        color_list=['#FF66CC','#3399CC']
        graph=plt.bar(index,percent,color=color_list,width=0.3,edgecolor='black')
        fig=plt.figure(facecolor='yellow')
        plt.rcParams['savefig.facecolor']='yellow'
        x_pos = [i for i, _ in enumerate(fileName)]
        #print('xpos: ',x_pos)

        graphh,ax =plt.subplots()

        rects1 = ax.bar(x_pos, percent,color=color_list,width=0.3,edgecolor='black')


        ax = plt.gca()
        ax.set_facecolor('xkcd:mint green')
        #for i in range(len(fileName)):
            #plt.annotate(percent[i], (-0.1 + i, percent[i] + j))
        if temp==0:
            plt.ylim(0,110)
        elif temp==1:
            plt.ylim(-100,110)
        plt.title('Bar plot of Document: '+singleFileName)
        plt.xlabel('Documents')

        #axx = plt.axes()
        #axx.set_facecolor("#1CC4AF")
        plt.ylabel('Percentage')
        plt.xticks(x_pos,fileName)

        #plt.bar(fileName, percent)
        for rect in rects1:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                    '%i' % float(height),
            ha='center', va='bottom')

        #for index, value in enumerate(percent):



            #plt.text(value, index, str(value))
        if temp==0:
            photoName=singleFileName+'_CS'+'.jpg'
            
            plt.savefig(singleFileName+'_CS'+'.jpg')
            insertion(photoName,singleFileName,0)
            plt.clf() 
        elif temp==1:
            photoName=singleFileName+'_LSA'+'.jpg'
            
            plt.savefig(singleFileName+'_LSA'+'.jpg')
            insertion(photoName,singleFileName,1)
            plt.clf() 

        #plt.show()
    def demo():
        create()
        con=sq.connect('COSINE_SIMILARITY.db')   
        cur=con.cursor()
        cur.execute("Select * from cs")
        rows=cur.fetchall()
        cur.execute("Select * from LSA")
        rows_LSA=cur.fetchall()
        fileName=[]
        percent=[]
        percent_LSA=[]

        for x in range(1,len(rows)+1):
            cur.execute("Select FILES FROM cs WHERE ID!=?",(x,))
            files=cur.fetchall()
            #print('files: ',files)
            cur.execute("Select FILES FROM cs WHERE ID=?",(x,))
            singleFile=cur.fetchall()
            #print('singleFile: ',singleFile[0][0])
            singleFileName=singleFile[0][0]
            fileName.clear()
            for col in range(len(files)):
                    fileName.append(files[col][0])
            #print('FileName: ',fileName)
            cur.execute("Select * FROM cs WHERE ID=?",(x,))
            data=cur.fetchall()
            cur.execute("Select * FROM LSA WHERE ID=?",(x,))
            data_LSA=cur.fetchall()
            #print(len(data[0]))
            #print('rows: ',data[0])
            percent.clear()
            percent_LSA.clear()
            for j in range(2,len(data[0])):
                    #print('j: ',j)
                    #print('index: ',index)
                    if j==x+1:

                        pass
                    else:
                        s=data[0][j]
                        s*=100
                        s_LSA=data_LSA[0][j]
                        s_LSA*=100
                        percent.append(int(s))
                        percent_LSA.append(int(s_LSA))

            #print('percent: ',percent)
            graph(fileName,percent,singleFileName,0) 
            graph(fileName,percent_LSA,singleFileName,1) 


        con.close()
    demo()
