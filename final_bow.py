import sqlite3 as sq

BAG_OF_WORDS_OLD={}

BAG_OF_WORDS = {}

BAG_OF_WORDS_LIST = []

COL_NAME=[]

def colChecker(doc):
   #selecting col names n performing operations on respective cols
   j=0
   con=sq.connect('DOCUMENT_SIMILARITY.db')
   cur=con.cursor()
   cursor = cur.execute('select * from BOW')
   cursor.description
   colnames = cursor.description
   for row in colnames:
    if len(colnames) == 2 and row[0] == 'ID':
        #when first doc is added
        newColBOW(doc)
        
    elif row[0] == 'WORDS' or row[0] == 'ID' :
        pass
        
    else:
        # if table has more than 1 doc in it
        COL_NAME.append(row[0])
        previousColValues(row[0])
        newColBOW(doc)
        updatePreviousCol(doc,row[0])
    con.close()


def newColBOW(Doc):
    #appending words of Doc in BAG_OF_WORDS_LIST if not present 
    for word in Doc :
        if word in BAG_OF_WORDS_LIST:
            pass
        else:
            if word == '':
                pass
            else:
                BAG_OF_WORDS_LIST.append(word)
    #print('\nnewColBOW:\n ',BAG_OF_WORDS_LIST,)


      
def previousColValues(row):
    #print('previous: \n')
    con=sq.connect('DOCUMENT_SIMILARITY.db')

    cur=con.cursor()

    cur.execute('SELECT WORDS from BOW ')

    r=cur.fetchall()
    
    conn=len(r)
    #no need of if else

    if conn == 0:
        pass
        
    else:
        #fetching words from previous column n appending them in BAG_OF_WORDS_LIST if not present

        cur.execute("SELECT {} from BOW".format(row))        

        f=cur.fetchall()
        
        for i in r:
            temp=str(i).strip("(',')")
            if temp in BAG_OF_WORDS_LIST:
                pass
                
            else:            
                BAG_OF_WORDS_LIST.append(temp)
        
        BAG_OF_WORDS_OLD.clear()   
        for k,j in zip(r,f):
            #add new words of new doc to dictionary
            temp=str(k).strip("(',')")
            tempp=str(j).strip("(',')")
           
            BAG_OF_WORDS_OLD[temp]=tempp
    #print(BAG_OF_WORDS_LIST,'\n\n',BAG_OF_WORDS_OLD,'\n')
           	
    con.close()
    

def updatePreviousCol(doc,row):

    for word in doc:
    #assigning 0 to the word in doc which is not present in previous col

        if word not in BAG_OF_WORDS_OLD.keys():
            BAG_OF_WORDS_OLD[word] = 0

        else:
            pass
    INSERT_OLD(row)
    
    

def isKeyPresent(dict, key): 
    #to check whether the word is present or not as a key in a dictionary 

    if key in dict.keys(): 

        return True

    else: 

        return False 


def wordPresentChecker(Doc):

    j=0
    for word in BAG_OF_WORDS_LIST:

        if word not in Doc:
            BAG_OF_WORDS[word] = 0
            

        else:
            BAG_OF_WORDS[word]=1
    #print('\nwordPresentChecker: \n',BAG_OF_WORDS)
            
        

def wordCount(Doc,fileName):
    word=0
    for k in Doc:
        #taking count of the appearance of specific word present in doc            
        i=Doc.count(Doc[word])        

        if i > 1:    
            tempWord=Doc[word]
            
            if isKeyPresent(BAG_OF_WORDS, tempWord):
                BAG_OF_WORDS[tempWord] =i
                
            word+=1            
        else:
            word+=1
    #print('\nwordCount: \n',BAG_OF_WORDS)
    
    INSERT_NEW(fileName)
    
def update_null():
   #updating NULL values in a col to 0
   con=sq.connect('DOCUMENT_SIMILARITY.db')
   cur=con.cursor()

   for i in COL_NAME:
       cur.execute("SELECT ID FROM BOW WHERE {} IS NULL ".format(i))
       k=cur.fetchall()
       conn=len(k)
       #print(conn) 
       if conn ==0:
           pass
       else:
           for f in k:
               temp=str(f).strip("(',')")
               cur.execute("UPDATE BOW SET {} =0 WHERE ID=?".format(i),(temp,))
               con.commit()
   con.close()
    
    
def CREATE():
   con=sq.connect('DOCUMENT_SIMILARITY.db')
   cur=con.cursor()
   cur.execute("CREATE TABLE IF NOT EXISTS BOW(ID INTEGER PRIMARY KEY,WORDS TEXT)")
   con.commit()
   con.close()

def INSERT_NEW(fileName):
    #when new doc is uploaded
    
    update_col(fileName)
    con=sq.connect('DOCUMENT_SIMILARITY.db')
    cur=con.cursor()
    cur.execute('SELECT WORDS from BOW ')

    r=cur.fetchall()
    conn=len(r)

    if conn == 0:
        #for very first doc
        k=0
        for i,j in zip(BAG_OF_WORDS_LIST,BAG_OF_WORDS.values()):

            cur=con.cursor()
            
            cur.execute("INSERT INTO BOW(WORDS,'{}') VALUES(?,?)".format(fileName),(i,j))
            con.commit()
        con.close()
    else:
        #inserting count of words of new doc
        k=0
        for i in BAG_OF_WORDS.values():
            k=k+1
            cur=con.cursor()
            cur.execute("UPDATE BOW SET '{}'=? WHERE ID=?".format(fileName),(i,k))

            con.commit()
    
        con.close()


def INSERT_OLD(fileName):
    #updating count n word col of previous doc whenever new doc is added
    BAG_DEMO=[]
    con=sq.connect('DOCUMENT_SIMILARITY.db')
    cur=con.cursor()
    cur.execute('SELECT WORDS FROM BOW ')
    r=cur.fetchall()    
    
    for i in r:
        temp=str(i).strip("(',')")
        BAG_DEMO.append(temp)
        
    for word in BAG_OF_WORDS_LIST:
        if word not in BAG_DEMO:
            temp=BAG_OF_WORDS_OLD[word]
            cur.execute("INSERT INTO BOW(WORDS,'{}') VALUES(?,?)".format(fileName),(word,temp))
            con.commit()
    

    con.close()

def update_col(fileName):
   con=sq.connect('DOCUMENT_SIMILARITY.db')
   cur=con.cursor()
   cur.execute("ALTER TABLE BOW add COLUMN '{}' INTEGER".format(fileName))
   con.commit()
   con.close()
