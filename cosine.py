def cs_cal():
    import sqlite3 as sq
    def numerator(d1, d2, col1, col2):
        # multiplying d1[0] with d2[0], d1[1] with d2[1] n so on

        product_of_doc = []
        for i, j in zip(d1, d2):
            a = i * j
            product_of_doc.append(a)
        #print('pro_of_doc:', product_of_doc)

        add_n(product_of_doc, d1, d2, col1, col2)

    def add_n(product_of_doc, d1, d2, col1, col2):
        # adding results of previous function
        k = 0
        addition = 0
        for f in product_of_doc:
            addition = addition + product_of_doc[k]
            k = k + 1
        #print('addition:', addition)

        denominator(d1, d2, addition, col1, col2)

    def denominator(d1, d2, addition, col1, col2):
        # squaring d1[0] , B[0] n so on
        sq_d1 = []
        sq_d2 = []
        for i, j in zip(d1, d2):
            s_d1 = i * i
            s_d2 = j * j
            sq_d1.append(s_d1)
            sq_d2.append(s_d2)
        #print('Sq_one:', sq_d1, 'Sq_two:', sq_d2)
        add_d(sq_d1, sq_d2, addition, col1, col2)

    def add_d(sq_d1, sq_d2, addition, col1, col2):
        # adding results of previous function
        k = 0
        addition_1 = 0
        addition_2 = 0
        for f, l in zip(sq_d1, sq_d2):
            addition_1 = addition_1 + sq_d1[k]
            addition_2 = addition_2 + sq_d2[k]
            k = k + 1
        #print('add_one_d:', addition_1, 'add_two_d', addition_2)

        sq_root(addition_1, addition_2, addition, col1, col2)


    def sq_root(addition_1, addition_2, addition, col1, col2):
        # taking sq root pf previous function's result n multiplying it

        addition_1 = addition_1 ** 0.5
        addition_2 = addition_2 ** 0.5
        mul = addition_1 * addition_2
        #print('add:', addition, 'mul:', mul)
        # dividing numerator denominator n inserting result into table
        try:
           # mult = round(addition / mul, 2)
            mult = round(addition / mul, 2)
        except:
            mult=addition   # mul =0.0
        #print('mult:', mult)
        insert(col1, col2, mult)

    def insert(col1, col2, mult):
        con = sq.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("UPDATE CS SET '{}'=? WHERE FILES=?".format(col1), (mult, col2))
        con.commit()
        con.close()
        update_null(col1)

    def update_null(col1):
        con = sq.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("SELECT FILES FROM CS WHERE {} IS NULL ".format(col1))
        k = cur.fetchall()
        for f in k:
            temp = str(f).strip("(',')")
            cur.execute("UPDATE CS SET {} =1 WHERE FILES=?".format(col1), (temp,))
            con.commit()
        con.close()

    def create():
        con = sq.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS CS")
        cur.execute("CREATE TABLE IF NOT EXISTS CS(ID INTEGER PRIMARY KEY,FILES TEXT)")
        con.commit()
        con.close()

    def add_fname(f):
        con = sq.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("INSERT INTO CS (FILES) VALUES(?)", (f,))
        con.commit()
        con.close()

    def add_col(f):
        con = sq.connect('COSINE_SIMILARITY.db')
        cur = con.cursor()
        cur.execute("ALTER TABLE CS ADD COLUMN {} INTEGER".format(f))
        con.commit()
        con.close()

    def select():
        # selecting columns from doc_cal table and comparing each column with every other column
        create()
        d1 = []
        d2 = []
        COL = []
        C = []
        con = sq.connect('DOCUMENT_SIMILARITY.db')
        cur = con.cursor()
        cursor = cur.execute("SELECT * from doc_cal")
        cursor.description
        cols = cursor.description
        for col in cols:
            if col[0] == 'ID':
                pass
            else:
                add_col(col[0])
                con = sq.connect('COSINE_SIMILARITY.db')
                cur = con.cursor()
                cur.execute("SELECT FILES from CS")
                f_n = cur.fetchall()
                for f in f_n:
                    temp = str(f).strip("[(',')]")
                    if temp not in COL:
                        COL.append(temp)

                if col[0] not in COL:
                    add_fname(col[0])

                for c in cols:
                    if c[0] == 'ID':
                        pass
                    elif col[0] == c[0]:
                        pass
                    else:
                        con = sq.connect('COSINE_SIMILARITY.db')
                        cur = con.cursor()
                        cur.execute("SELECT FILES from CS")
                        fn = cur.fetchall()

                        for ff in fn:
                            temp = str(ff).strip("[(',')]")

                            if temp not in C:
                                C.append(temp)

                        if c[0] not in C:
                            add_fname(c[0])

                        con = sq.connect('DOCUMENT_SIMILARITY.db')
                        cur = con.cursor()
                        cur.execute("SELECT {} from doc_cal".format(col[0]))
                        m = cur.fetchall()

                        cur.execute("SELECT {} from doc_cal".format(c[0]))
                        n = cur.fetchall()
                        d1.clear()
                        d2.clear()
                        d2.clear()

                        for i, j in zip(m, n):
                            temp = str(i).strip("[(',')]")
                            tempp = str(j).strip("[(',')]")
                            #print(temp, tempp)
                            d1.append(float(temp))
                            d2.append(float(tempp))
                        numerator(d1, d2, col[0], c[0])

    select()
cs_cal()

print("Cosine similarity Detected !!")