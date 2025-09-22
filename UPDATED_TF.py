def TF_CAL():
    import sqlite3 as sq
    WORD_COUNT=[]

    WORDS_TF=[]   
    con=sq.connect('INPUT_FILES.db')
    cur=con.cursor()

    cur.execute("SELECT File_Name  FROM PRE_FILES WHERE  ID = (SELECT MAX(ID)  FROM PRE_FILES) ")
    f=cur.fetchall()
    for i in zip(f):
        c=str(i).strip("[(,)]")
        c=c[4:-5]
        

    def create_tf():
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS TF (ID INTEGER PRIMARY KEY , WORDS text)")
        con.commit()
        con.close()

    create_tf()

    def INSERT_TF_WORDS():
        new_list=[]
        TF_DEMO=[]
        con=sq.connect('DOCUMENT_SIMILARITY.db')
        cur=con.cursor()
        cur.execute('SELECT words from BOW ')
        tf_words=cur.fetchall()
        cur.execute('SELECT words from TF ')
        r=cur.fetchall()
        conn=len(r)
        if conn == 0:   
            for i in tf_words:
                WORDS_TF.append(i)
            for w in WORDS_TF:
                cur=con.cursor()            
                cur.execute("INSERT INTO TF(WORDS) VALUES(?)",(w))
                con.commit()
            #print("1st doc")
            #print("WORDS_TF:",WORDS_TF)
        else: 
            cur=con.cursor()
            cur.execute('SELECT WORDS from BOW ')
            tf_words=cur.fetchall()
            cur.execute('SELECT WORDS from TF ')
            new_tfidf=cur.fetchall()        
            for i in tf_words:
                TF_DEMO.append(i)
            for j in new_tfidf:
                new_list.append(j)
            #print("TF_DEMO: ",TF_DEMO)
            for words in TF_DEMO:
                    if words not in new_list:
                        #print(words)
                        cur=con.cursor()
                        cur.execute("INSERT INTO TF(WORDS) VALUES(?)",(words))              
            #print("ELSE NEW_TF EXECUTED")
            con.commit()
            con.close()  
                
                    

    INSERT_TF_WORDS()




    def insert_tf(t,tf_val,no):
        conn = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = conn.cursor()
        
        #print("tf inserted")
        cursor = cur.execute('select * from TF')
        cursor.description
        colnames = cursor.description
        col_count =len(colnames)
        if col_count>=3:
            cur.execute("UPDATE TF SET {}=? WHERE ID=?".format(t), (tf_val, no))
            # print("if value inserted") 
            
        conn.commit()
        conn.close()
            
    #TF_CALCULATION
    def computeTf(t):
        connection = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = connection.cursor()
        #print("Connected to SQLite")
        sqlite_select_query = """SELECT * from BOW"""
        cur.execute(sqlite_select_query)
        total_rows = cur.fetchall()
        j=1
        
        for j in range(1,len(total_rows)+1):
            cur.execute(f"SELECT {t} FROM BOW WHERE ID={j}")
            records_count = cur.fetchall()
            count_list = [item for v in records_count for item in v]
            length=length_cal(c)  
            #print("length:",length)
            cal_tf=count_list[0]/length
            insert_tf(t,cal_tf,j)     
            #print("tf:",cal_tf)  
        connection.commit()
        connection.close()

    def length_cal(temp):
        WORD_COUNT=[]
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("SELECT {} FROM BOW".format(temp,))
        l=cur.fetchall()
        for i in l:
            st=str(i).strip("(',')")
            #print('st: ',st)
            WORD_COUNT.append(int(st))
        total=sum(WORD_COUNT)
        return total

    #updateTFIDFtable    
    def update_tf(temp):
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("ALTER TABLE TF add COLUMN {} FLOAT".format(temp,))
        computeTf(temp)  # function calling with passing file name
        con.commit()
        con.close()
        
        
    update_tf(c)

    def col_count():
        COL_NAME=[]
        con=sq.connect('DOCUMENT_SIMILARITY.db')
        cur=con.cursor()
        cursor = cur.execute('select * from TF')
        cursor.description
        colnames = cursor.description
        for row in colnames:
            if row[0] == 'WORDS' or row[0] == 'ID' :
                pass
            else:
                #print(row[0])
                COL_NAME.append(row[0])
        for i in COL_NAME:
            cur.execute("SELECT ID FROM TF WHERE {} IS NULL ".format(i))
            k=cur.fetchall()
            conn=len(k)
            #print(conn) 
            if conn ==0:
                pass
            else:
                for f in k:
                    temp=str(f).strip("(',')")
                    cur.execute("UPDATE TF SET {} =0 WHERE ID=?".format(i),(temp,))
                    con.commit()
        con.commit()
        con.close()
        
    col_count()

def CAL_IDF():
    import sqlite3 as sq
    import math
    from sqlite3 import Error
    l=[]
    ID=[]
    a=[]
#to create and alter table named IDF            
    def ALTER():
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS IDF")
        cur.execute("CREATE TABLE IF NOT EXISTS IDF AS SELECT ID,WORDS from BOW")
        cur.execute("ALTER TABLE IDF ADD COLUMN 'LOG_IDF' TEXT")
        cur.execute("ALTER TABLE IDF ADD COLUMN 'IDF' FLOAT")
        con.commit()
        con.close()
        #print("COLUMN ADDED")
#inserting values into IDF
    def insert_IDF(T,S,V):
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("update  IDF SET {}=?,{}=?  WHERE ID=? ".format('LOG_IDF','IDF'),(T,S,V))
        con.commit()
        con.close()

#calculating IDF    
    def IDF():
        ALTER()
        conn = sq.connect('DOCUMENT_SIMILARITY.db')
        c = conn.cursor()
        columns=[]
        cursor = c.execute("SELECT *   FROM BOW ")
        cursor.description
        cursor = c.execute("SELECT ID FROM BOW;")
        d=cursor.fetchall()                          #fetching all the words in table TF
        for i in d:
            temp=str(i).strip("[(',')]")
            ID.append(temp) 
        cursor = c.execute("SELECT * FROM BOW;")
        m=[desc[0] for desc in cursor.description]     #gets all the column names
        for n in m:
            if n =='ID' :
                pass
            elif n =='WORDS':
                pass
            else:
                l.append(n)             #appending the only columns which are to be compared for IDF
        for k in ID:
            a.clear()
            for i in l:
                cursor = c.execute("SELECT {} FROM BOW where ID=? ;".format(i),[k]) #passing K as NUMBER and i as column
                e=cursor.fetchall()
                strip=str(e).strip("[(',')]")
            
            
                if int(strip) == 0:
                    pass
                else:
                    a.append(strip)
                #print('id: ',k,' col: ',i)
            
            idf = (math.log(len(l)/len(a)))
            j = ('log({}/{})'.format(len(l),len(a)))
        #print(j)
       # print(idf)
            insert_IDF(j,idf,k) #to insert or to update table
            conn.commit()
        #print("DATA INSERTED")
        
    IDF() # calling the function
