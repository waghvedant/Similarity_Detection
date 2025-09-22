
def LSA():
    import sklearn
    from sklearn.decomposition import TruncatedSVD
    from sklearn.preprocessing import Normalizer
    import numpy as np
    import sqlite3
    from sklearn.feature_extraction.text import CountVectorizer 
    from sklearn.feature_extraction.text import TfidfVectorizer

    def create():
        con = sqlite3.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS LSA")
        cur.execute("CREATE TABLE IF NOT EXISTS LSA(ID INTEGER PRIMARY KEY,FILES TEXT)")
        con.commit()
        con.close()

    def add_fname(f):
        con = sqlite3.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("INSERT INTO LSA (FILES) VALUES(?)", (f,))
        con.commit()
        con.close()

    def add_col(f):
        con = sqlite3.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("ALTER TABLE LSA ADD COLUMN {} INTEGER".format(f))
        con.commit()
        con.close()

    def select():
        create()
        d1 = []
        d2 = []
        COL = []
        C = []
        con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cursor = cur.execute("SELECT * from bow")
        cursor.description
        cols = cursor.description
        for col in cols:
            if col[0] == 'ID' or col[0] == 'WORDS':
                pass
            else:
                add_col(col[0])
                con = sqlite3.connect('COSINE_SIMILARITY.db')
                cur = con.cursor()
                cur.execute("SELECT FILES from LSA")
                f_n = cur.fetchall()
                for f in f_n:
                    temp = str(f).strip("[(',')]")

                    if temp not in COL:
                        COL.append(temp)

                if col[0] not in COL:
                    add_fname(col[0])

                for c in cols:
                    if c[0] == 'ID' or col[0] == 'WORDS':
                        pass
                    elif col[0] == c[0]:
                        pass
                    else:
                        con = sqlite3.connect('COSINE_SIMILARITY.db')
                        cur = con.cursor()
                        cur.execute("SELECT FILES from LSA")
                        fn = cur.fetchall()

                        for ff in fn:
                            temp = str(ff).strip("[(',')]")
                            #print('temp: ', temp)
                            if temp not in C:
                                C.append(temp)

                        if c[0] not in C:
                            if c[0] == 'WORDS':
                                pass
                            else:
                                add_fname(c[0])

    select()

    '''con = sqlite3.connect('INPUT_FILES.db')
    cur = con.cursor()
    cur.execute("SELECT File_Name FROM FILES")
    f = cur.fetchall()'''
    '''con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
    cur = con.cursor()
    temp=cur.execute("SELECT * FROM doc_cal")
    temp.description
    cols = temp.description

    FILES = []

    for i in cols:        
        FILES.append(i[0])

    joined_string = ",".join(FILES)

    con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
    cur = con.cursor()
    cursor = cur.execute('select * from BOW ')
    co = cursor.fetchall()
    con.close()

    C = len(co[0]) - 2
    R = len(co)
    con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
    cur = con.cursor()
    sample = []

    for i in range(1, R + 1):
        cursor = cur.execute(f'select {joined_string} from BOW WHERE ID={i}')
        co = cursor.fetchall()
        sample.append(co)

    out = [item for t in sample for item in t]
    out2 = [item for t in out for item in t]

    arr = np.array(out)

    result = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
    x = np.array(result)'''
    DATA=[]
    con = sqlite3.connect('INPUT_FILES.db')
    cur = con.cursor()
    cur.execute("select MAX(ID) from files")
    max_id = cur.fetchall()
    count = str(max_id).strip("[(',')]")
    for i in range(1,int(count)+1):
        cur.execute("select content from files WHERE ID=?",(i,))
        cont = cur.fetchall()
        data = str(cont).strip("[(',')]")
        DATA.append(data)
    vectorizer=CountVectorizer(min_df=1,stop_words='english')
    dtm=vectorizer.fit_transform(DATA)
    lsa = TruncatedSVD(2, algorithm='randomized')
    dtm_lsa = lsa.fit_transform(dtm)
    dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)

    similarity = np.asarray(np.asmatrix(dtm_lsa) * np.asmatrix(dtm_lsa).T)
    column_list = []
    counter = -1

    def insert(col_super, col_sub, k):
        con = sqlite3.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("UPDATE LSA SET '{}'=? WHERE FILES=?".format(col_sub), (k, col_super))
        con.commit()
        con.close()

    con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
    cur = con.cursor()
    cursor = cur.execute("SELECT * from bow")
    cursor.description
    cols = cursor.description

    for i in cols:
        if i[0] == 'ID' or i[0] == 'WORDS':
            pass
        else:
            column_list.append(i[0])

    for col_super in column_list:
        counter = counter + 1
        for col_sub, k in zip(column_list, similarity[counter]):
            insert(col_super, col_sub, k)


