#from werkzeug.utils import secure_filename
#from flask_sqlalchemy import SQLAlchemy
import userfile_upload as user
import getPhoto_oTo as oTo
from datetime import date
import getPhoto_oTm as oTm
import glob as gb
import sqlite3
import sqlite3 as sql
import os
import plagiarism as plag
import urllib.request
from werkzeug.utils import secure_filename
from flask import *
STATIC_DIR = os.path.abspath('../static')

import sqlite3 as sq

import os
#import magic
import urllib.request


# 1st run this function before execution of before_deadline.py
def create_userdata():
    con = sq.connect('USER_DETAILS.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS USER_DATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,email TEXT, File_Name TEXT)")
    print("Table created successfully")
    con.commit()
    con.close()

create_userdata()
U_name=[]

#FOLDER PATH
UPLOAD_FOLDER ='G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend'

app = Flask(__name__,static_folder=STATIC_DIR)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# app=Flask(__name__)

app = Flask(__name__, template_folder='templates')
name_list = []
selectedFile=[]
dead_line = date(2023,4,28)
current_date = date.today()

#before deadline execution---\/----

if current_date < dead_line:

	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	#home page
	@app.route('/')
	def home():
	   return render_template('index.html')
	#welcome page
	@app.route('/welcome')
	def welcome():
	   return render_template('welcome.html')
	#admin page
	@app.route('/')
	def admin():
	   return render_template('')

	#help page
	@app.route('/help')
	def help1():
	   return render_template('help.html')

	#feedback page
	@app.route('/feedback')
	def feedback():
	   return render_template('feedback.html')

	#facts page
	@app.route('/facts')
	def facts():
	   return render_template('facts.html')

	#contacts page
	@app.route('/contact')
	def contacts():
	   return render_template('contact.html')

	#user login
	@app.route('/login')
	def log():
	   return render_template('log.html')
	#login validation
	@app.route('/checklogin',methods = ['POST', 'GET'])
	def checklogin():
		if request.method == 'POST':
		    nm = request.form['nm']
		    ps = request.form['ps']
		    U_name.append(nm)
		    with sql.connect("USER_DETAILS.db") as con:
		        cur = con.cursor()
		        cur.execute("SELECT * from USER_DATA where username=? AND password=?",(nm,ps))
		        user=cur.fetchone()
		                          
		        if user is not None:
		            #if file is already uploded
		            if cur.execute("SELECT File_Name FROM USER_DATA where File_Name is NOT NULL AND username=? ",[nm]).fetchone():
		                return render_template("result1_fileupload.html")
		            else:
		                cur.execute("select File_Name from USER_DATA")
		           
		                name = cur.fetchall()
		               
		                name_list.clear()
		                for i in name:
		                    name_list.append(i[0])
		    
		                return render_template("file.html",name=name_list)
		               
		          
		        else:
		            error = "Sorry :( Login failed"  
		            return render_template('log.html',error=error)  
		            con.commit()
		    con.close()
		    
	#upload user file to folder
	@app.route('/upload_file', methods=['POST'])
	def upload_file():
		   
		if request.method == 'POST':

		    password1=request.form['psw']
		    file_name= request.form['name']
		    print(file_name[-4:])
		    with sql.connect("USER_DETAILS.db") as con:           
		        if con.execute("SELECT * FROM USER_DATA WHERE password = ? ",[password1]).fetchone():      
		            if 'file' not in request.files:
		                flash('No file part')
		                return redirect(request.url)
		    
		            file_name= request.form['name']
		            if file_name[-4:]=='.txt'or file_name[-4:]=='.doc'or file_name[-4:]=='.pdf' :
		        
		                file_name=file_name[0:-4]
		
		            elif file_name[-5:]=='.docx':
		        
		                file_name=file_name[0:-5]
		            else:
		                pass
		            file = request.files['file']
		            if file.filename == '':
		                flash('No file selected for uploading')
		                return redirect(request.url)
		            #if file name is same
		            if con.execute("SELECT * FROM USER_DATA WHERE file_Name = ? ",[file_name]).fetchone(): 
		                msg="File already exist!! Change your file name"
		                return render_template("file.html",msg=msg,name=name_list)
		            elif file and allowed_file(file.filename):
		                print(request.files)
		                filename = secure_filename(file.filename)
		               
		                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		                #storing file_name into USER_DATA
		                file.save(os.path.join(UPLOAD_FOLDER, filename))
		                con.execute("Update USER_DATA set file_Name=? where username=?",(file_name,U_name[len(U_name) - 1]))

		                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                
		                user.user_file()
		                plag.before()
		                U_name.clear()

						# Ethe Loadin add karaychi aahe till file uploaded sucess yet to paryant

		                return render_template('result1_fileupload.html')
		            else:
		                #if file extension is different
		                msg2="File type is not allowed!!!--> ALLOWED EXTENSIONS(.txt,.pdf,.docx,.doc)"
		                return render_template("file.html",msg2=msg2,name=name_list)
		        else:
		            msg1="Incorrect password"
		            return render_template('file.html',msg1=msg1,name=name_list)
		            con.commit()
		    con.close()
		    
	@app.route('/signup')
	def new_login():
	   return render_template('sign.html')
	@app.route('/signup_user',methods = ['POST', 'GET'])
	def signup_user():
		if request.method == 'POST':
		    nm = request.form['nm']
		    ps = request.form['ps']
		    email=request.form['em']
		    with sql.connect("USER_DETAILS.db") as con:
		        cur = con.cursor()
		       
		        cur.execute("SELECT * from USER_DATA where username=? AND password=?",(nm,ps))
		        if cur.fetchone() is None:
		            cur.execute("INSERT INTO USER_DATA (username,password,email) VALUES (?,?,?)",(nm,ps,email))
		            msg = "Record successfully added"
		            return render_template("log.html",msg = msg)
		        else:
		            msg= "This record already exists!!! "
		            return render_template("sign.html",msg=msg)
		    con.commit()  
		    con.close()
		    
	#------------------------------Admin----------------------------
	@app.route('/AdminLogin')      # AdminLogin page Before Deadline
	def AdminLogin():
		return render_template("AdminLogin.html")



	@app.route('/cslsa')   # for selecting defualt file name
	def cslsa():
		con = sql.connect("INPUT_FILES.db")
		cur = con.cursor()
		cur.execute(f"select File_Name from FILES WHERE ID={n}")    # here give table name as USER_FILES
		de = cur.fetchall()
		naaa = str(de).strip("[(',')]")
		#naaa =naa[:-4]
		con = sql.connect("COSINE_SIMILARITY.db")
		cur = con.cursor()

		cur.execute(f"select FILES from CS where id = {n}")

		defa = cur.fetchall()

		cur.execute(f"select {naaa} from CS where id={n}")  # ethe id sarkhi condition deun value retrive krta yeil

		NM=[]
		val = cur.fetchall()
		cur.execute(f"select {naaa} from LSA where id={n}")
		valu = cur.fetchall()
		con = sql.connect("INPUT_FILES.db")
		cur = con.cursor()
		cur.execute("select File_Name from FILES")  # here give table name as USER_FILES
		# document chi list provide krnya sathi
		name = cur.fetchall()
		for i in zip(name):
		    c = str(i).strip("[(',')]")
		    c = c[:-4]
		    NM.append(c)
	#        print(c)

		cur.execute(f"select Content from USER_FILES where id={n}")    # here give table name as USER_FILES for orignal file content
		cont = cur.fetchall()
		cur.execute("select Content from USER_FILES where id=1")
		cont2 = cur.fetchall()
		return render_template("cslsa.html", defa=defa[0][0], name=NM, val=val[0][0], valu=valu[0][0],cont=cont[0][0],cont2=cont2[0][0])


	@app.route('/IdPwd')            # displaying ID Passwords of users to admin
	def IdPwd():
		con = sql.connect("USER_DETAILS.db")
		con.row_factory = sql.Row
		cur = con.cursor()  # aplya id and password chya table sathi


		NM = []
		cur.execute("PRAGMA table_info(USER_DATA)")
		x = cur.fetchall()
		for i in x:
		    NM.append(i[1])
		    # print(i[1])
		cur.execute("Select * from USER_DATA")
		v = cur.fetchall()
		# print(NM)

		return render_template("IdPwd.html", name=NM,v=v)


	@app.route('/Ofiles')           # displaying uploaded files for plag to admin
	def Ofiles():
		city_list = []
		con = sql.connect("INPUT_FILES.db")
		# con.row_factory = sqlite3.Row
		cur = con.cursor()  # aplya file show karnya sathi chya table sathi

		cur.execute("select File_Name from FILES ")    # here give table name as USER_FILES for orignal file
		name = cur.fetchall()

		cur.execute("select ID, File_Name from FILES ")
		namo = cur.fetchall()

		for i in name:
		    city_list.append(i[0])
		return render_template("Ofiles.html", name=city_list , namo=namo)


	@app.route('/CSdata')     # displaying CS Data
	def CSdata():
		con = sql.connect("COSINE_SIMILARITY.db")
		#con.row_factory = sqlite3.Row
		cur = con.cursor()  # aplya cs cha data show karnya sathi chya table sathi

		NM = []
		cur.execute("PRAGMA table_info(CS)")
		x = cur.fetchall()
		for i in x:
		    NM.append(i[1])
		    #print(i[1])
		cur.execute("Select * from CS")
		v = cur.fetchall()
		#print(NM)
		return render_template("CSdata.html", name=NM,v=v)


	@app.route('/lsadata')    # displaying LSA Data
	def lsadata():
		con = sql.connect("COSINE_SIMILARITY.db")
		# con.row_factory = sqlite3.Row
		cur = con.cursor()  # aplya cs cha data show karnya sathi chya table sathi

		NM = []
		cur.execute("PRAGMA table_info(LSA)")
		x = cur.fetchall()
		for i in x:
		    NM.append(i[1])
		    # print(i[1])

		# print(NM)
		cur.execute("Select * from LSA")
		v = cur.fetchall()
		return render_template("lsadata.html", name=NM, v= v)


	@app.route('/admin_log')
	def admin_log():
		return render_template('admin_log.html')
	@app.route('/admin_log_next')
	def admin_log_next():
		return render_template('admin_log_next.html')


	# by giving here validation for date redirect the admin pages to Adminlogin1.html i.e. before deadline
	@app.route('/checklog',methods = ['POST', 'GET'])
	def checklog():
		if request.method == 'POST':
		    em=request.form['em']
		    ps = request.form['ps']
		    dummy="Incorrect Password...Please try again"
		try:
		    if ps == "Admin55"and em=="admin11@gmail.com":
		        return render_template('AdminLogin.html')
		    else:
		        error =dummy
		        #flash('Incorrect Password...Plzz try again')
		        return render_template('admin_log_next.html', error=error)
		except:
		    error = "Incorrect Password...Please try again"
		    flash('Incorrect Password...Please try again')
		    return render_template('admin_log_next.html', error=error)



	@app.route('/AdminLogin1')
	def AdminLogin1():
		return render_template('AdminLogin1.html')

	@app.route('/cont',methods=['POST', 'GET']) # for showing content of files to admin after giving id
	def cont():
		if request.method == 'POST':
		    n = request.form['no']

		    city_list = []
		    con = sql.connect("INPUT_FILES.db")

		    cur = con.cursor()  # aplya file show karnya sathi chya table sathi

		    cur.execute("select File_Name from FILES ")  # here give table name as USER_FILES for orignal file
		    name = cur.fetchall()

		    cur.execute("select ID, File_Name from FILES ")
		    namo = cur.fetchall()

		    for i in name:
		        city_list.append(i[0])


		    con = sql.connect("INPUT_FILES.db")
		    cur = con.cursor()
		    cur.execute("Select  COUNT(*) from FILES")
		    d = cur.fetchall()
		    c = str(d).strip("[(',')]")
		    if n <=c:
		        con = sql.connect("INPUT_FILES.db")
		        cur = con.cursor()
		        try:
		            cur.execute(f"select Content from FILES WHERE ID={n}")  # for showing orignal file content
		            oc = cur.fetchall()
		            oc=oc[0][0]
		           # ocon = str(oc).strip("[(',')]")

		            cur.execute(f"select Content from PRE_FILES WHERE ID={n}")# for showing prepro file content
		            pc = cur.fetchall()
		            pcon = str(pc).strip("[(',')]")

		            return render_template('contents.html', id=n, ocon=oc, pcon=pcon)
		        except:
		            error =""
		            return render_template('Ofiles.html',error=error,name=city_list , namo=namo)

		    else:
		        error = "Enter the ID of Uploaded Files Only..!"
		        return render_template('Ofiles.html', error=error,name=city_list , namo=namo)
		else:
		    return render_template('Ofiles.html')


	@app.route('/contents')
	def contents():
		return render_template('contents.html')

############################################################################################################
else:
    
    @app.route('/')
    def home():
        plag.after()
        return render_template('index.html')
    #welcome page
    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')
    #admin page
    @app.route('/')
    def admin():
        return render_template('')

    #help page
    @app.route('/help')
    def help1():
        return render_template('help.html')

    #feedback page
    @app.route('/feedback')
    def feedback():
        return render_template('feedback.html')

    #facts page
    @app.route('/facts')
    def facts():
        return render_template('facts.html')

    #contacts page
    @app.route('/contact')
    def contacts():
        return render_template('contact.html')
    
    @app.route('/login')
    def log():
        return render_template('UserLoginAD.html')
    @app.route('/check',methods=['POST', 'GET'])
    def check():
        if request.method == 'POST':
            nm = request.form['nm']
            ps = request.form['ps']
            print("NM PS: ",nm," ",ps)
            try:
                with sql.connect("USER_DETAILS.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT ID from USER_DATA where username=? AND password=?", (nm, ps))
                    user = cur.fetchall()
                    global temp
                    temp=user[0][0]
                    #print("TEMP: ",temp)


                    #n = str(user).strip("[(',')]")
                    con = sql.connect("INPUT_FILES.db")
                    cur = con.cursor()
                    cur.execute("select File_Name from files WHERE ID=?",(temp,))  # ya thikani user ch doc by defualt select pahije asel tr
                    defualt = cur.fetchall()
                    #print("DEFAULT: ",defualt[0][0])
                    dummy=defualt[0][0]
                    # mg id nusar home page la query dyavi

                    # defualt file name gheu shkto

                    cur.execute("select File_Name from files where ID!=?",(temp,))
                    # document chi list provide krnya sathi
                    name = cur.fetchall()
                    #print("NAMES: ",name)
                    # print('name: ',name[0:])
                    name_list.clear()
                    for i in name:
                        name_list.append(i[0])
                    print('list: ',name_list)
                    return render_template("homepage.html", deff=dummy, name=name_list)
            except:
                eror =" Enter Correcr ID Password :)"
                return render_template('UserLoginAD.html',error=eror)
            con.close()



    @app.route('/Second')
    def Second():
        con = sql.connect("INPUT_FILES.db")
        cur = con.cursor()
        cur.execute("select File_Name from files WHERE ID=?",(temp,))  # ya thikani user ch doc by defualt select pahije asel tr
        defualt = cur.fetchall()
        #print("DEFAULT: ",defualt[0][0])
        dummy=defualt[0][0]
        return render_template("homepage.html",name=name_list,deff=dummy)


    @app.route('/homepage')
    def homepage():
        return render_template("homepage.html")


    @app.route('/UserLoginAD')
    def UserLoginAD():
        return render_template("UserLoginAD.html")


    @app.route('/CSlsa', methods=['POST','GET'])
    def CSlsa():
        if request.method == 'POST':
            selectedFile.clear()
            selected= request.form['cars']
            selectedFile.append(selected)
            con = sqlite3.connect("INPUT_FILES.db")
            cur = con.cursor()
            cur.execute(f"select File_Name from files WHERE ID={temp}")
            fName= cur.fetchall()
            src=fName[0][0]
            dest=selectedFile[0]
            photo_list=gb.glob('G:/Degree/B.Tech/Final_Year/PLAG/PlagiarismProject/final_backend/static/*.jpeg')
            for k in photo_list:
                if os.path.exists(k):
                    os.remove(k)
            #print("CSALSA\n",src,"  ",dest)
            oTo.getPhoto(src,dest,0)
            oTm.getPhoto(src,0)
            oTo.getPhoto(src,dest,1)
            oTm.getPhoto(src,1)
            
            return render_template("CSGraphOTM.html")


    @app.route('/CSoto')
    def CSoto():
        dummy=selectedFile[0]
        dummy=dummy.upper()
        con = sql.connect("INPUT_FILES.db")
        cur = con.cursor()
        cur.execute("select File_Name from files WHERE ID=?",(temp,))
        default = cur.fetchall()
        name=default[0][0]
        name=name.upper()
        return render_template("CSGraphOTO.html",selected=dummy,name=name)



    @app.route('/CSotm')
    def CSGraphOTM():
        con = sql.connect("INPUT_FILES.db")
        cur = con.cursor()
        cur.execute("select File_Name from files WHERE ID=?",(temp,))
        default = cur.fetchall()
        name=default[0][0]
        name=name.upper()
        
        return render_template("CSGraphOTM.html",name=name)

    @app.route('/LSAoto')
    def LSAGraphOTO():
        dummy=selectedFile[0]
        dummy=dummy.upper()
        con = sql.connect("INPUT_FILES.db")
        cur = con.cursor()
        cur.execute("select File_Name from files WHERE ID=?",(temp,))
        default = cur.fetchall()
        name=default[0][0]
        name=name.upper()
        return render_template("LSAGraphOTO.html",selected=dummy,name=name)

    @app.route('/LSAotm')
    def LSAGraphOTM():
        con = sql.connect("INPUT_FILES.db")
        cur = con.cursor()
        cur.execute("select File_Name from files WHERE ID=?",(temp,))
        default = cur.fetchall()
        name=default[0][0]
        name=name.upper()
        
        return render_template("LSAGraphOTM.html",name=name)





    @app.route('/File')
    def File():
            con = sqlite3.connect("INPUT_FILES.db")
            cur = con.cursor()   
            cur.execute(f"select Content from files where id={temp}")    # here give table name as USER_FILES for orignal file content
            cont = cur.fetchall()
            cur.execute(f"select File_Name from files where id={temp}")
            file1=cur.fetchall()
            file2_id=selectedFile[0]
            #print("IDTWO: ",file2_id)
            cur.execute("select Content from files where File_Name=?",(file2_id,))

            cont2 = cur.fetchall()
            #print("FILETWO: ",cont2[0])
            return render_template('FileContent.html', cont=cont[0][0],cont2=cont2[0][0],file1=file1[0][0],file2=file2_id)
            #return render_template('FileContent.html')
            
    @app.route('/cslsa')   # for selecting defualt file name
    def cslsa():
            con = sql.connect("INPUT_FILES.db")
            cur = con.cursor()
            cur.execute(f"select File_Name from FILES WHERE ID={n}")    # here give table name as USER_FILES
            de = cur.fetchall()
            naaa: str = str(de).strip("[(',')]")
            #naaa =naa[:-4]
            con = sql.connect("COSINE_SIMILARITY.db")
            cur = con.cursor()

            cur.execute(f"select FILES from CS where id = {n}")

            defa = cur.fetchall()

            cur.execute(f"select {naaa} from CS where id={n}")  # ethe id sarkhi condition deun value retrive krta yeil

            NM=[]
            val = cur.fetchall()
            cur.execute(f"select {naaa} from LSA where id={n}")
            valu = cur.fetchall()
            con = sql.connect("INPUT_FILES.db")
            cur = con.cursor()
            cur.execute("select File_Name from FILES")  # here give table name as USER_FILES
            # document chi list provide krnya sathi
            name = cur.fetchall()
            for i in zip(name):
                c = str(i).strip("[(',')]")
                c = c[:-4]
                NM.append(c)
        #        print(c)

            cur.execute(f"select Content from FILES where id={n}")    # here give table name as USER_FILES for orignal file content
            cont = cur.fetchall()
            cur.execute("select Content from FILES where id=1")
            cont2 = cur.fetchall()
            return render_template("cslsa.html", defa=defa[0][0], name=NM, val=val[0][0], valu=valu[0][0],cont=cont[0][0],cont2=cont2[0][0])


    @app.route('/IdPwd')            # displaying ID Passwords of users to admin
    def IdPwd():
            con = sql.connect("USER_DETAILS.db")
            con.row_factory = sql.Row
            cur = con.cursor()  # aplya id and password chya table sathi


            NM = []
            cur.execute("PRAGMA table_info(USER_DATA)")
            x = cur.fetchall()
            for i in x:
                NM.append(i[1])
                # print(i[1])
            cur.execute("Select * from USER_DATA")
            v = cur.fetchall()
            # print(NM)
            return render_template("AfIdPwd.html", name=NM,v=v)


    @app.route('/Ofiles')           # displaying uploaded files for plag to admin
    def Ofiles():
            city_list = []
            con = sql.connect("INPUT_FILES.db")
            # con.row_factory = sqlite3.Row
            cur = con.cursor()  # aplya file show karnya sathi chya table sathi

            cur.execute("select File_Name from FILES ")    # here give table name as USER_FILES for orignal file
            name = cur.fetchall()

            cur.execute("select ID, File_Name from FILES ")
            namo = cur.fetchall()

            for i in name:
                city_list.append(i[0])
            return render_template("AfOfiles.html", name=city_list , namo=namo)


    @app.route('/CSdata')     # displaying CS Data
    def CSdata():
            con = sql.connect("COSINE_SIMILARITY.db")
            #con.row_factory = sqlite3.Row
            cur = con.cursor()  # aplya cs cha data show karnya sathi chya table sathi

            NM = []
            cur.execute("PRAGMA table_info(CS)")
            x = cur.fetchall()
            for i in x:
                NM.append(i[1])
                #print(i[1])
            cur.execute("Select * from CS")
            v = cur.fetchall()
            #print(NM)
            return render_template("AfCSdata.html", name=NM,v=v)


    @app.route('/lsadata')    # displaying LSA Data
    def lsadata():
            con = sql.connect("COSINE_SIMILARITY.db")
            # con.row_factory = sqlite3.Row
            cur = con.cursor()  # aplya cs cha data show karnya sathi chya table sathi

            NM = []
            cur.execute("PRAGMA table_info(LSA)")
            x = cur.fetchall()
            for i in x:
                NM.append(i[1])
                # print(i[1])

            # print(NM)
            cur.execute("Select * from LSA")
            v = cur.fetchall()
            return render_template("Aflsadata.html", name=NM, v= v)
    @app.route('/admin_log')
    def admin_log():
            return render_template('admin_log.html')
    @app.route('/admin_log_next')
    def admin_log_next():
            return render_template('admin_log_next.html')


        # by giving here validation for date redirect the admin pages to Adminlogin1.html i.e. before deadline
    @app.route('/checklog',methods = ['POST', 'GET'])
    def checklog():
            if request.method == 'POST':
                em=request.form['em']
                ps = request.form['ps']
                dummy="Incorrect Password...Please try again"
            try:
                if ps == "Admin55"and em=="admin11@gmail.com":
                    return render_template('AdminLogin1.html')
                else:
                    error =dummy
                    #flash('Incorrect Password...Plzz try again')
                    return render_template('admin_log_next.html', error=error)
            except:
                error = "Incorrect Password...Please try again"
                flash('Incorrect Password...Please try again')
                return render_template('admin_log_next.html', error=error)



    @app.route('/AdminLogin1')
    def AdminLogin1():
            return render_template('AdminLogin1.html')

    @app.route('/cont',methods=['POST', 'GET']) # for showing content of files to admin after giving id
    def cont():
            if request.method == 'POST':
                n = request.form['no']

                city_list = []
                con = sql.connect("INPUT_FILES.db")
                # con.row_factory = sqlite3.Row
                cur = con.cursor()  # aplya file show karnya sathi chya table sathi

                cur.execute("select File_Name from FILES ")  # here give table name as USER_FILES for orignal file
                name = cur.fetchall()

                cur.execute("select ID, File_Name from FILES ")
                namo = cur.fetchall()

                for i in name:
                    city_list.append(i[0])


                con = sql.connect("INPUT_FILES.db")
                cur = con.cursor()
                cur.execute("Select  COUNT(*) from FILES")
                d = cur.fetchall()
                c = str(d).strip("[(',')]")
                if n <=c:
                    con = sql.connect("INPUT_FILES.db")
                    cur = con.cursor()
                    try:
                        cur.execute(f"select Content from FILES WHERE ID={n}")  # for showing orignal file content
                        oc = cur.fetchall()
                        oc=oc[0][0]
                       # ocon = str(oc).strip("[(',')]")

                        cur.execute(f"select Content from PRE_FILES WHERE ID={n}")  # for showing prepro file content
                        pc = cur.fetchall()
                        pcon = str(pc).strip("[(',')]")

                        return render_template('Afcontents.html', id=n, ocon=oc, pcon=pcon)
                    except:
                        error =""
                        return render_template('AfOfiles.html',error=error,name=city_list , namo=namo)

                else:
                    error = "Enter the ID of Uploaded Files Only..!"
                    return render_template('AfOfiles.html', error=error,name=city_list , namo=namo)
            else:
                return render_template('AfOfiles.html')


    @app.route('/contents')
    def contents():
            return render_template('Afcontents.html')



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)


