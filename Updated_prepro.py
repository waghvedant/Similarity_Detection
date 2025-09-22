def prepro():

    import re
    import nltk    
    from nltk.corpus import stopwords as sw
    from nltk.tokenize import word_tokenize as wt
    from nltk.stem import WordNetLemmatizer as wnl
    import os
    import glob as gb
    import sqlite3 as sq
    import File_Remove as fr
    d=wnl()

    UPLOAD_FOLDER = 'G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend'

    File_Name=[]

    file_list=gb.glob('./*.txt')
    for k in file_list:
        with open(k,'r') as obj:
            data=obj.read()
            data=data.lower()
            cleaning_d=re.sub('[^\w\s]',' ',data)
            stop_w=set(sw.words('english'))
            tokens=wt(cleaning_d)
        with open (k.replace('txt','out'),'a')as appendFile:
            appendFile.seek(0)
            appendFile.truncate()
        for w in tokens:
            if w not in stop_w:
                nextt=w
                ddd=nltk.word_tokenize(nextt)
                for j in ddd:
                    with open (k.replace('txt','out'),'a')as appendFile:
                        appendFile.write(" "+d.lemmatize(j))
        if os.path.exists(k):
            os.remove(k)




    def create():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS PRE_FILES(ID INTEGER PRIMARY KEY ,File_Name TEXT,Content TEXT)")
        con.commit()
        con.close()
    create()


    def select_fn():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()
        cur.execute("SELECT File_Name FROM PRE_FILES")
        f=cur.fetchall()
        if len(f)==0:
            pass
        else:
            for i in f:
                temp=str(i).strip("[('')]")
                if temp not in File_Name:
                    #temp=temp[:-2]
                    File_Name.append(temp)
                else:
                    pass
            
    
    def insert():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()    
        file_list=gb.glob('./*.out')

        select_fn()
        for i in file_list:
            #print("i: ",i)
            if i not in File_Name:
                #print("fn: ",File_Name)
                with open(i,'r') as obj:
                    data=obj.read()             

                    cur.execute('INSERT INTO PRE_FILES(File_Name,Content) values(?,?)',(i,data))
                    con.commit()
                    #if os.path.isfile(i):
                     #   os.remove(i)
            else:
                pass
            
        con.close()
    insert()
    # Specify the folder path containing the .out files
    folder_path = "G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend"

    # Call the function to remove .out files
    fr.remove_out_files(folder_path)



