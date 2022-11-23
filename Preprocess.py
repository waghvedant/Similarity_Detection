
def prepro():
    import re
    import nltk
    from nltk.corpus import stopwords as sw
    from nltk.tokenize import word_tokenize as wt
    from nltk.stem import WordNetLemmatizer as wnl
    import os
    import glob as gb
    import sqlite3 as sq
    d = wnl()
    document = []
    File_Name = []
    '''def pdftotext():
        global input1
        global output
        input1=gb.glob('./*.pdf')
        for i in input1:
                temp=i.replace('pdf','txt')
                output=temp
                os.system("pdftotext '%s' '%s'" % (i, output))
                if os.path.exists(i):
                    os.remove(i)
    pdftotext()'''
    '''def doctotxt():
        file_list=gb.glob('./*.docx')
        for k in file_list:
            document = Document(k)
            txt_file=k.replace('docx','txt')
            with io.open(txt_file,'w', encoding="utf-8") as textFile:
                    for para in document.paragraphs: 
                             textFile.write(para.text)
            if os.path.exists(k):
                    os.remove(k)  
    doctotxt()'''

    file_list = gb.glob('./*.txt')
    for k in file_list:
        with open(k, 'r', encoding="utf-8") as obj:
            data = obj.read()
            data = data.lower()
            cleaning_d = re.sub('[^\w\s]', ' ', data)
            stop_w = set(sw.words('english'))
            tokens = wt(cleaning_d)
        with open(k.replace('txt', 'out'), 'a', encoding="utf-8") as appendFile:
            appendFile.seek(0)
            appendFile.truncate()
        for w in tokens:
            if w not in stop_w:
                nextt = w
                ddd = nltk.word_tokenize(nextt)
                for j in ddd:
                    with open(k.replace('txt', 'out'), 'a', encoding="utf-8") as appendFile:
                        appendFile.write(" " + d.lemmatize(j))
        if os.path.exists(k):
            os.remove(k)

    def create():
        con = sq.connect('INPUT_FILES.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS PRE_FILES(ID INTEGER PRIMARY KEY ,File_Name TEXT,Content TEXT)")
        #print("Data Base Created")
        con.commit()
        con.close()

    create()
    def select_fn():
        con = sq.connect('INPUT_FILES.db')
        cur = con.cursor()
        cur.execute("SELECT File_Name FROM PRE_FILES")
        f = cur.fetchall()
        if len(f) == 0:
            pass
        else:
            for i in f:
                temp = str(i).strip("[('')]")
                if temp not in File_Name:
                    # temp=temp[:-2]
                    File_Name.append(temp)
                else:
                    pass
        con.commit()

    def insert():
        con = sq.connect('INPUT_FILES.db')
        cur = con.cursor()
        file_list = gb.glob('./*.out')

        select_fn()
        for i in file_list:
            # print("i: ",i)
            if i not in File_Name:
                #i = i[2:-4]
                # print("fn: ",File_Name)
                with open(i, 'r', encoding='utf-8') as obj:
                    data = obj.read()
                    cur.execute('INSERT INTO PRE_FILES(File_Name,Content) values(?,?)', (i, data))
                    con.commit()
                    con.close()
                    #if os.path.exists(i):
                     #    os.remove(i)
            else:
                pass
        con.close()
    insert()
    # It removes all the processed files from directory
    test = os.listdir("./")
    for i in test:
        if i.endswith(".out"):
            os.remove(i)
        if i.endswith(".pdf"):
            os.remove(i)
        if i.endswith(".docx"):
            os.remove(i)
prepro()
print("Preprocessing Done !!")