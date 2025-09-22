'''def before():
import sqlite3 as sq
import final_bow as bow
import Updated_prepro as up
import UPDATED_TF as tfidf
import Document_Cal as dc
import cosine_sim as cs
import Latent as lsa
import graph_oTm as otm
import graph_oTo as oto

    #print('\nFile cannot be uploaded :( \n')
    dc.DOC_CAL()
    cs.cs_cal()
    lsa.LSA()
    otm.oTm()
    oto.oTo()'''
def after():
    import Document_Cal as dc
    import cosine_sim as cs
    import Latent as lsa
    import graph_oTm as otm
    import graph_oTo as oto

    #print('\nFile cannot be uploaded :( \n')
    dc.DOC_CAL()
    cs.cs_cal()
    lsa.LSA()
    otm.oTm()
    oto.oTo()

def before():
    import sqlite3 as sq
    import final_bow as bow
    import Updated_prepro as up
    import UPDATED_TF as tfidf

    up.prepro()

    TABLE_CONTENT=[]

    con=sq.connect('INPUT_FILES.db')
    cur=con.cursor()

    cur.execute("SELECT File_Name FROM PRE_FILES WHERE  ID = (SELECT MAX(ID)  FROM PRE_FILES) ")
    f=cur.fetchall()

    cur.execute("SELECT Content  FROM PRE_FILES WHERE  ID = (SELECT MAX(ID)  FROM PRE_FILES) ")
    r=cur.fetchall()

    for i,k in zip(f,r):
        #print('i: ',i)
        fileName=str(i).strip("[(,)]")
        #print('filename: ',fileName,'\n')
        fileName=fileName[4:-5]
        #print('filename after: ',fileName,'\n')
        TABLE_CONTENT=list(k)
        new_list1 = [y for x in TABLE_CONTENT for y in x.split(' ')]
        bow.CREATE()
        bow.colChecker(new_list1)
        bow.wordPresentChecker(new_list1)
        bow.wordCount(new_list1,fileName)
        bow.update_null()
        tfidf.TF_CAL()
        tfidf.CAL_IDF()
'''else:
    up.prepro()

    TABLE_CONTENT=[]

    con=sq.connect('INPUT_FILES.db')
    cur=con.cursor()

    cur.execute("SELECT File_Name  FROM PRE_FILES WHERE  ID = (SELECT MAX(ID)  FROM PRE_FILES) ")  
    f=cur.fetchall()

    cur.execute("SELECT Content  FROM PRE_FILES WHERE  ID = (SELECT MAX(ID)  FROM PRE_FILES) ")
    r=cur.fetchall()

    for i,k in zip(f,r):
        #print('i: ',i)
        fileName=str(i).strip("[(,)]")
        #print('filename: ',fileName,'\n')
        fileName=fileName[3:-5]
        #print('filename after: ',fileName,'\n')
        TABLE_CONTENT=list(k)
        new_list1 = [y for x in TABLE_CONTENT for y in x.split(' ')]
        bow.CREATE()
        bow.colChecker(new_list1)
        bow.wordPresentChecker(new_list1)
        bow.wordCount(new_list1,fileName)
        bow.update_null()
        tfidf.TF_CAL()
        tfidf.CAL_IDF()'''
