#Execute after uploading user file(result_fileupload.html)
#Storing user file into Input_FILES DB
def user_file():

    import re
    import os
    import glob as gb
    import sqlite3 as sq
    from docx import Document
    import io

    File_Name=[]
    def pdftotext():
        global input1
        global output
        input1=gb.glob('./*.pdf')
        for i in input1:
                temp=i.replace('pdf','txt')
                output=temp
                os.system("pdftotext '%s' '%s'" % (i, output))
                if os.path.exists(i):
                    os.remove(i)
    pdftotext()
    def doctotxt():
        file_list=gb.glob('./*.docx')
        for k in file_list:
            document = Document(k)
            txt_file=k.replace('docx','txt')
            with io.open(txt_file,'w', encoding="utf-8") as textFile:
                    for para in document.paragraphs: 
                            textFile.write(para.text)
            if os.path.exists(k):
                    os.remove(k)  
    doctotxt()

    def create_uf():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS FILES(ID INTEGER PRIMARY KEY AUTOINCREMENT,File_Name TEXT,Content TEXT)")
        con.commit()
        con.close()
        
    create_uf()


    def select_uf():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()
        cur.execute("SELECT File_Name FROM FILES")
        f=cur.fetchall()
        if len(f)==0:
            pass
        else:
            #strip filename(e.g doc1.txt->doc1)
            for i in f:
                temp=str(i).strip("[('')]")
                if temp not in File_Name:
                    #temp=temp[2:-2]
                    File_Name.append(temp)
                else:
                    pass
            
    
    def insert_uf():
        con=sq.connect('INPUT_FILES.db')
        cur=con.cursor()    
        file_list=gb.glob('./*.txt')
        select_uf()
        for i in file_list:
            if i not in File_Name:
                with open(i,'r') as obj:
                    data=obj.read()             
                    i=i[2:-4]
                    cur.execute('INSERT INTO FILES(File_Name,Content) values(?,?)',(i,data))
                    con.commit()
            else:
                pass
        con.close()
    insert_uf()
    

#user_file()
