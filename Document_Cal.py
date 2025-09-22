import sqlite3
def DOC_CAL():

    COL_NAME = []

    con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
    cur = con.cursor()
    cursor = cur.execute('select * from TF')
    colnames = cursor.description
    for row in colnames:
        if row[0] == 'ID' or row[0] == 'WORDS':
            pass
        else:
            COL_NAME.append(row[0])


    # Table creation if not exist
    def create():
        cur.execute("DROP TABLE IF EXISTS DOC_CAL")
        cur.execute("CREATE TABLE IF NOT EXISTS DOC_CAL (ID INTEGER PRIMARY KEY)")
        con.commit()

    # function taking value as fileName
    def doc_cal(t):
        conn = sqlite3.connect('DOCUMENT_SIMILARITY.db')
        c = conn.cursor()
        c.execute("SELECT * FROM TF")
        count = c.fetchall()
        j = 1
        for j in range(1, len(count) + 1):  # for records 1 to total no. of records in table(TF)
            c.execute(f"SELECT {t} FROM TF WHERE id={j}")
            data1 = c.fetchall()
            # converting tuple values into normal list
            res = [item for v in data1 for item in v]

            c.execute(f"SELECT IDF FROM IDF WHERE id={j}")
            data2 = c.fetchall()
            # converting tuple values into normal list
            res2 = [item for v in data2 for item in v]

            s = (res[0] * res2[0])  # calculate Tf*IDF
            insert(t, s, j)  # calling function to insert Tf*idf in DOC_CAL table
        conn.commit()

    # function of taking value as fileName,Tf*idf,id
    def insert(te, sa, j):
        conn = sqlite3.connect('DOCUMENT_SIMILARITY.db')
        c = conn.cursor()

        # Inserting Tfidf into doc_cal table with proper id

        c.execute("UPDATE DOC_CAL SET '{}'=? WHERE ID =?".format(te), (sa, j))
        conn.commit()

    def UPDATE_ID():
        # code for updating id in doc_cal table
        con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
        cu = con.cursor()
        cu.execute("SELECT * FROM TF")
        f = cu.fetchall()

        for j in range(1, len(f) + 1):
            con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
            cur = con.cursor()
            cur.execute("INSERT INTO DOC_CAL (ID) VALUES(?)", (j,))
            con.commit()
            con.close()


    # function taking value as FileName for update column in DOC_CAL Table
    def update_col(temp):
        con = sqlite3.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("ALTER TABLE DOC_CAL ADD COLUMN '{}' REAL".format(temp))
        #print("RECORDS ARE ADDING OF  " + temp + " file..!")
        #print("NEW COLUMN ADDED INTO THE TABLE")
        doc_cal(temp)  # function calling with passing file name
        #print("DATA CALCULATED AND INSERTED OF "+temp+" FILE\n\n")
        con.commit()
        con.close()

    #print("FOLLOWING COLUMNS WILL BE ADDED FOR CALCULATION")
    #print(COL_NAME)

    create()
    #print("DOC_CAL TABLE IS CREATED...!")
    UPDATE_ID()
    #print("ID UPDATED SUCCESSFULLY FOR DOC_CAL TABLE...!\n\n")
    for i in COL_NAME:
        update_col(i)
    #print("CONGO...!! ALL RECORDS ARE ADDED")
#DOC_CAL()
