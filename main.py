from flask import Flask,render_template,session,request,redirect,url_for,flash
import mysql.connector,hashlib
import matplotlib.pyplot as plt
import numpy as np
import math



mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='rakesh007',
  database = 'DBMS_PROJECT'
)
mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
@app.route("/home",methods = ['POST','GET'])
def home():
    if not session.get('login'):
        return render_template('login.html'),401
    else:
        # if session.get('isAdmin') :
        return render_template('home.html',username=session.get('username'))
        # else :
        #     return home_student()

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method=='POST' :
        query = """SELECT * FROM login WHERE username = '%s'""" %(request.form['username'])
        mycursor.execute(query)
        res = mycursor.fetchall()
        if mycursor.rowcount == 0:
            return home()
        if request.form['password'] != res[0][1]:
            return render_template('login.html')
        else:
            session['login'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            # session['isAdmin'] = (request.form['username']=='admin')
            return home()
    return render_template('login.html')

@app.route("/show_update_detail",methods=['POST','GET'])
def show_update_detail():
    if not session.get('login'):
        return redirect( url_for('home') )
    if request.method=='POST':
        if request.form['User_ID'] =='':
            return render_template("search_detail.html")
        qry = "Select * from User where User.User_ID = %s" %(request.form['User_ID'])
        qry1 = "Select * from User_phone_no where User_ID = %s" %(request.form['User_ID'])
        mycursor.execute(qry)
        not_found=False
        res=()
        if(mycursor.rowcount > 0):
            res = mycursor.fetchone()
        else:
            not_found=True
        fields = mycursor.column_names
        qry_upd = "Select * from User where User_ID = %s" %(request.form['User_ID'])
        mycursor.execute(qry_upd)
        upd_res = ()
        if(mycursor.rowcount > 0):
            upd_res = mycursor.fetchone()
        fields_upd = mycursor.column_names
        mycursor.execute(qry1)
        phone_no = mycursor.fetchall()
        qry_pat = "select orphanage_ID, donation_camp_req, reason_of_procurement, Doctor_name from orphanage inner join Doctor on Doctor.Doctor_ID = orphanage.Doctor_ID and User_ID = %s" %(request.form['User_ID'])
        qry_don = "select Donor_ID, donation_camp_donated, reason_of_donation, Branch_name from Donor inner join Branch on Branch.Branch_ID = Donor.Branch_ID and User_ID = %s" %(request.form['User_ID'])
        qry_trans = "select distinct Transaction.orphanage_ID, Transaction.Donor_ID, donation_camp_ID, Date_of_transaction, Status from Transaction, orphanage, Donor where (orphanage.User_ID = %s and orphanage.orphanage_ID = Transaction.orphanage_ID) or (Donor.User_Id= %s and Donor.Donor_ID = Transaction.Donor_ID)" %((request.form['User_ID']),(request.form['User_ID']))
        #
        res_pat = ()
        res_dnr = ()
        res_trans = ()
        mycursor.execute(qry_pat)
        if(mycursor.rowcount > 0):
            res_pat = mycursor.fetchall()
        fields_pat = mycursor.column_names
        #
        mycursor.execute(qry_don)
        if(mycursor.rowcount > 0):
            res_dnr = mycursor.fetchall()
        fields_dnr = mycursor.column_names
        #
        mycursor.execute(qry_trans)
        if(mycursor.rowcount > 0):
            res_trans = mycursor.fetchall()
        fields_trans = mycursor.column_names
        print(res_trans)
        if("show" in request.form):
            return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no, res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
        if("update" in request.form):
            return render_template('update_detail.html',res = upd_res,fields = fields_upd, not_found=not_found)
        if "delete" in request.form:
            if not_found:
                return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no,  res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
            else:
                qry2 = "DELETE FROM User where User_ID = %s" %(request.form['User_ID'])
                mycursor.execute(qry2)
                mydb.commit()
                return render_template("home.html")

@app.route("/search_detail",methods = ['POST','GET'])
def search_detail():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('search_detail.html')

#--------------Adding Information----------------------------

@app.route("/add_<id>_page",methods = ['POST','GET'])
def add_page(id):
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from " + id.capitalize()
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('add_page.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_login", methods=['POST','GET'])
def add_login():
    print("test user")
    # if not session.get('login'):
    #     return redirect( url_for('login') )
    qry = "SELECT * from login"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        # if field not in ['orphanage_ID','User_ID','Doctor_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO login Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='login', error=error,success=success))

@app.route("/add_User_phone_no", methods=['POST','GET'])
def add_User_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from User_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['User_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO User_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='User_phone_no', error=error,success=success))

@app.route("/add_orphanage", methods=['POST','GET'])
def add_orphanage():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from orphanage"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        # if field not in ['orphanage_ID','User_ID','Doctor_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO orphanage Values (%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='orphanage', error=error,success=success))

@app.route("/add_orphanage_stats", methods=['POST','GET'])
def add_orphanage_stats():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from orphanage_stats"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        # if field not in ['orphanage_ID','User_ID','Doctor_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO orphanage_stats Values (%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='orphanage_stats', error=error,success=success))

@app.route("/add_Donor", methods=['POST','GET'])
def add_Donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        # if field not in ['Donor_ID','User_ID','Branch_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)
    # mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Donor Values (%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : Donor not Inserted")
        error = True
        success = False
        return redirect(url_for('add_page', id='Donor', error=error,success=success))
    mydb.commit()

    item_temp = request.form.get('Items_donated')
    print(item_temp)
    list_item = item_temp.replace(" ",'').split(',')

    # list_item = [i.split(':') for i in item_temp.split(',')]
    # print(list_item)
    qry2 = "SELECT Item_ID from Item"
    try:
        mycursor.execute(qry2)
    except:
        print("Error : Item not Updated")
        error = True
        success = False
        return redirect(url_for('add_page', id='Donor', error=error,success=success))
    list1 = mycursor.fetchall()
    print(list1)
    list2 = []
    for i in list1:
        list2.append(i[0])
    print(list2)
    for i in list_item:
        j = i.split(':')
        if j[0] in list2:
            print(j[0], j[1])
            qry3 = "update item set Item_count=Item_count+"+j[1]+" where Item_id = \'"+j[0]+"\';"
            mycursor.execute(qry3)
            print(qry3)
    mydb.commit()
    
    

    # print(fields2)
    

    # qry_insert = "insert into donation_camp (donation_camp_name, Donor_ID) Values (%s,%s) "%(val[1],val[0])

    # mycursor.execute(qry_insert)

    # mycursor.execute("COMMIT;")

    # mydb.commit()

    return redirect(url_for('add_page', id='Donor', error=error,success=success))

@app.route("/add_Doctor", methods=['POST','GET'])
def add_Doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Branch_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor Values (%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor', error=error,success=success))

@app.route("/add_Doctor_phone_no", methods=['POST','GET'])
def add_Doctor_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor_phone_no', error=error,success=success))

@app.route("/add_donation_camp", methods=['POST','GET'])
def add_donation_camp():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from donation_camp"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        # if field not in ['donation_camp_ID','Donor_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO donation_camp Values (%s,%s,%s, %s, %s, %s, %s, %s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='donation_camp', error=error,success=success))


@app.route("/add_Branch", methods=['POST','GET'])
def add_Branch():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Branch"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        # if field not in ['Branch_ID'] and temp != '':
        if temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)
    # print(val)

    qry = "INSERT INTO Branch Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Branch', error=error,success=success))

@app.route("/add_Branch_phone_no", methods=['POST','GET'])
def add_Branch_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Branch_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Branch_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Branch_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Branch_phone_no', error=error,success=success))

@app.route("/add_Branch_head", methods=['POST','GET'])
def add_Branch_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Branch_head"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Employee_ID','Term_length','Branch_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Branch_head Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Branch_head', error=error,success=success))

@app.route("/add_Transaction", methods=['POST','GET'])
def add_Transaction_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['orphanage_ID','Donor_ID','Status','donation_camp_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Transaction Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    qry_insert = "delete from donation_camp where donation_camp_ID = %s "%val[1]

    mycursor.execute(qry_insert)

    mycursor.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_page', id='Transaction', error=error,success=success))

#------------------------Update details-------------------------------------		#-------------------------------------------------------------

@app.route("/update_user_page",methods = ['POST','GET'])
def update_user_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from User"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_user_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_user_details",methods = ['GET','POST'])
def update_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from User")
    fields = mycursor.column_names
    qry = "UPDATE User SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Medical_insurance']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE User_ID = %s;" %(request.form['User_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from User where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    qry = "Select * from User where User.User_ID = %s" %(request.form['User_ID'])
    qry1 = "Select * from User_phone_no where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry)
    not_found=False
    res=()
    if(mycursor.rowcount > 0):
        res = mycursor.fetchone()
    else:
        not_found=True
    fields = mycursor.column_names
    qry_upd = "Select * from User where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry_upd)
    upd_res = ()
    if(mycursor.rowcount > 0):
        upd_res = mycursor.fetchone()
    fields_upd = mycursor.column_names
    mycursor.execute(qry1)
    phone_no = mycursor.fetchall()
    qry_pat = "select orphanage_ID, donation_camp_req, reason_of_procurement, Doctor_name from orphanage inner join Doctor on Doctor.Doctor_ID = orphanage.Doctor_ID and User_ID = %s" %(request.form['User_ID'])
    qry_don = "select Donor_ID, donation_camp_donated, reason_of_donation, Branch_name from Donor inner join Branch on Branch.Branch_ID = Donor.Branch_ID and User_ID = %s" %(request.form['User_ID'])
    qry_trans = "select distinct Transaction.orphanage_ID, Transaction.Donor_ID, donation_camp_ID, Date_of_transaction, Status from Transaction, orphanage, Donor where (orphanage.User_ID = %s and orphanage.orphanage_ID = Transaction.orphanage_ID) or (Donor.User_Id= %s and Donor.Donor_ID = Transaction.Donor_ID)" %((request.form['User_ID']),(request.form['User_ID']))
    #
    res_pat = ()
    res_dnr = ()
    res_trans = ()
    mycursor.execute(qry_pat)
    if(mycursor.rowcount > 0):
        res_pat = mycursor.fetchall()
    fields_pat = mycursor.column_names
    #
    mycursor.execute(qry_don)
    if(mycursor.rowcount > 0):
        res_dnr = mycursor.fetchall()
    fields_dnr = mycursor.column_names
    #
    mycursor.execute(qry_trans)
    if(mycursor.rowcount > 0):
        res_trans = mycursor.fetchall()
    fields_trans = mycursor.column_names
    # if("show" in request.form):
    return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no, res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
    # return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_orphanage_page",methods = ['POST','GET'])
def update_orphanage_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from orphanage"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_orphanage_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_orphanage_details",methods = ['GET','POST'])
def update_orphanage_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from orphanage")
    fields = mycursor.column_names
    qry = "UPDATE orphanage SET "
    for field in fields:
        if request.form[field] not in ['None','Orphanage_ID', 'Branch_ID']:
            # if field in ['User_ID','Doctor_ID','orphanage_ID']:
            #     qry = qry + "%s = %s , " %(field,request.form[field])
            # else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            pass
            # qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Orphanage_ID = \'%s\' and Branch_ID = \'%s\';" %(request.form['Orphanage_ID'],request.form['Branch_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from orphanage WHERE orphanage_ID = \'%s\' and Branch_ID = \'%s\';" %(request.form['Orphanage_ID'],request.form['Branch_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_donor_page",methods = ['POST','GET'])
def update_donor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Donor"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_donor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_donor_details",methods = ['GET','POST'])
def update_donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from donor")
    fields = mycursor.column_names
    qry = "UPDATE donor SET "
    for field in fields:
        if request.form[field] not in ['None','Donor_ID', 'DC_ID']:
            # if field in ['User_ID','Doctor_ID','orphanage_ID']:
            #     qry = qry + "%s = %s , " %(field,request.form[field])
            # else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            pass
            # qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Donor_ID = \'%s\' and DC_ID = \'%s\';" %(request.form['Donor_ID'],request.form['DC_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from donor WHERE donor_ID = \'%s\' and DC_ID = \'%s\';" %(request.form['Donor_ID'],request.form['DC_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

# @app.route("/update_donor_details",methods = ['GET','POST'])
# def update_donor_details():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     mycursor.execute("SELECT * from Donor")
#     fields = mycursor.column_names
#     qry = "UPDATE Donor SET "
#     for field in fields:
#         if request.form[field] not in ['Donor_ID','DC_ID', 'None', '']:
#             # if field in ['User_ID','Branch_ID','Donor_ID']:
#             #     qry = qry + "%s = %s , " %(field,request.form[field])
#             # else:
#                 qry = qry + " %s = \'%s\', " %(field,request.form[field])
#         else:
#             pass
#             # qry = qry + "%s = NULL , " %(field)
#     qry = qry[:-2]
#     qry = qry + "WHERE Donor_ID = \'%s\' and dc_id = \'%s\';" %(request.form['Donor_ID'],request.form['DC_ID'])
#     print(qry)
#     try:
#         mycursor.execute(qry)
#     except:
#         print("update error")
#     mydb.commit()
#     qry2 = "donor from  WHERE Donor_ID = \'%s\' and DC_id = \'%s\';" %(request.form['Donor_ID'],request.form['DC_ID'])
#     mycursor.execute("select * "+ qry2)
#     res = mycursor.fetchone()
#     print(res)
#     # print(qry2)
#     return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_branch_page",methods = ['POST','GET'])
def update_doctor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Branch"
    print('1')
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_branch_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_branch_details",methods = ['GET','POST'])
def update_doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Branch")
    fields = mycursor.column_names
    qry = "UPDATE Branch SET "
    for field in fields:
        if request.form[field] not in ['None','Branch_ID']:
            # if field in ['Branch_ID']:
            #     qry = qry + "%s = %s , " %(field,request.form[field])
            # else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            pass
            # qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Branch_ID = \'%s\';" %(request.form['Branch_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Branch WHERE Branch_ID = \'%s\';" %(request.form['Branch_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_donation_camp_page",methods = ['POST','GET'])
def update_donation_camp_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from donation_camp"
    print('2')
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_donation_camp_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_donation_camp_details",methods = ['GET','POST'])
def update_donation_camp_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from donation_camp")
    fields = mycursor.column_names
    qry = "UPDATE donation_camp SET "
    for field in fields:
        if request.form[field] not in ['None','DC_ID','BRANCH_ID']:
            # if field in ['DC_ID','Government_approved']:
            #     qry = qry + "%s = %s , " %(field,request.form[field])
            # else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            pass
            # qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE DC_ID = \'%s\' ;" %(request.form['DC_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from donation_camp WHERE DC_ID = \'%s\';" %(request.form['DC_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)
# @app.route("/update_donation_camp_head_page",methods = ['POST','GET'])
# def update_donation_camp_head_page():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     qry_upd = "Select * from Branch_head"
#     mycursor.execute(qry_upd)
#     fields_upd = mycursor.column_names
#     upd_res=[None]*len(fields_upd)
#     return render_template('update_donation_camp_head_page.html',fields = fields_upd,res = upd_res)
# @app.route("/update_donation_camp_head_details",methods = ['GET','POST'])
# def update_donation_camp_head_details():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     mycursor.execute("SELECT * from Branch_head")
#     fields = mycursor.column_names
#     qry = "UPDATE Branch_head SET "
#     for field in fields:
#         if request.form[field] not in ['None','']:
#             if field in ['Branch_ID','Employee_ID','Term_length']:
#                 qry = qry + "%s = %s , " %(field,request.form[field])
#             else:
#                 qry = qry + " %s = \'%s\' , " %(field,request.form[field])
#         else:
#             qry = qry + "%s = NULL , " %(field)
#     qry = qry[:-2]
#     qry = qry + "WHERE Branch_ID = %s and Employee_ID = %s;" %(request.form['Branch_ID'],request.form['Employee_ID'])
#     print(qry)
#     try:
#         mycursor.execute(qry)
#     except:
#         return render_template('error_page.html',qry=qry)
#     mydb.commit()
#     qry2 = "select * from Branch WHERE Branch_ID = %s and Employee_ID = %s;" %(request.form['Branch_ID'],request.form['Employee_ID'])
#     mycursor.execute(qry2)
#     res = mycursor.fetchone()
#     return render_template("show_detail.html",res = res,fields=fields,not_found = False)

#----------------------------Logout-----------------------------------------
@app.route("/logout", methods=['POST','GET'])
def logout():
    session['login'] = False
    # session['isAdmin'] = False
    return redirect("/login")

#-----------------------Searching Information------------------------------

@app.route("/search_User_details",methods=['GET','POST'])
def search_User_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from User"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_orphanage_details",methods=['GET','POST'])
def search_orphanage_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from orphanage"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_orphanage_stats_details",methods=['GET','POST'])
def search_orphanage_stats_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from orphanage_stats"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_item_details",methods=['GET','POST'])
def search_item_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Item"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Donor_details",methods=['GET','POST'])
def search_Donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_donation_camp_details",methods=['GET','POST'])
def search_donation_camp_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from donation_camp"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Branch_details",methods=['GET','POST'])
def search_Branch_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Branch"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Branch_head_details",methods=['GET','POST'])
def search_Branch_head_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Branch_head"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Doctor_details",methods=['GET','POST'])
def search_Doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Transaction",methods=['GET','POST'])
def search_Transaction_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_log",methods=['GET','POST'])
def search_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

#---------------------Remove Pages--------------------------------------

@app.route('/remove_user',methods=['GET','POST'])
def remove_user():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_user.html')

@app.route('/remove_orphanage',methods=['GET','POST'])
def remove_hostel():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_orphanage.html')

@app.route('/remove_donor',methods=['GET','POST'])
def remove_room():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_donor.html')

# @app.route('/remove_branch',methods=['GET','POST'])
# def remove_branch():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     return render_template('/remove_branch.html')

@app.route('/remove_branch',methods=['GET','POST'])
def remove_branch():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_branch.html')

@app.route('/remove_donation_camp',methods=['GET','POST'])
def remove_donation_camp():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_donation_camp.html')


#----------------Actual Deletion from database------------------------

@app.route('/del_user',methods=['GET','POST'])
def del_hostel():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from User where User_ID="+str(request.form['User_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )

@app.route('/del_orphanage',methods=['GET','POST'])
def del_orphanage():
    if not session.get('login'):
        return redirect( url_for('home') )
    # qry = "delete from orphanage where orphanage_ID="+request.form['orphanage_ID']+" and donation_camp_req=\'%s\'"%(request.form['donation_camp_req'])
    temp=str(request.form['orphanage_ID'])
    qry = "delete from orphanage where orphanage_ID="+"\'"+temp+"\'"
    print(temp)
    success = True
    error = False
    # try:
    #     mycursor.execute(qry)
    # except:
    #     print("Error : User not Inserted")
    #     error = True
    #     success = False
    # mydb.commit()

    # return redirect(url_for('add_page', id='Branch', error=error,success=success))

    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
        error=True
        success=False
    mydb.commit()
    return redirect(url_for('home') )

@app.route('/del_donor',methods=['GET','POST'])
def del_donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from donor where Donor_ID=\'%s\'"%(request.form['Donor_ID'])+" and DC_ID=\'%s\'" %request.form['DC_ID']
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_doctor',methods=['GET','POST'])
def del_doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Doctor where Doctor_ID="+str(request.form['Doctor_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_branch',methods=['GET','POST'])
def del_branch():
    if not session.get('login'):
        return redirect( url_for('home') )
    temp = str(request.form['Branch_ID'])
    qry = "delete from Branch where Branch_ID="+ "\'" + temp + "\'"
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('remove_branch') )


@app.route('/del_donation_camp',methods=['GET','POST'])
def del_donation_camp_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    # qry = "delete from Branch_head where Branch_ID="+str(request.form['Branch_ID'])+" and Employee_ID="+str(request.form['Employee_ID'])
    temp = str(request.form['DC_ID'])
    qry = "delete from donation_camp where DC_ID=" + "\'" + temp + "\'"
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('remove_donation_camp') )
#------------------------------------------------------------------------

@app.route('/contact_admin_page',methods=['GET','POST'])
def contact_admin_page():
    print(session.get('isAdmin'))
    if not session.get('login') or session.get('isAdmin'):
        return redirect( url_for('home') )
    return render_template('contact_admin_page.html')

@app.route('/contact_admin',methods=['GET','POST'])
def contact_admin():
    if not session.get('login') or session.get('isAdmin'):
        return redirect( url_for('home') )
    username = session.get('username')
    message = request.form['message']

    qry = "insert into Messages (username,message) values (\'"+username+"\',\'"+message+"\')"

    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error")
        error = True
        success = False
    mydb.commit()

    return render_template('contact_admin_page.html',error=error,success=success)


@app.route('/see_messages',methods=['GET','POST'])
def see_messages():
    if not session.get('login') or not session.get('isAdmin'):
        return redirect( url_for('home') )

    qry = "Select * from Messages"
    mycursor.execute(qry)
    msg = mycursor.fetchall()

    return render_template('see_messages.html',msg=msg)

@app.route('/seen_message',methods=['GET','POST'])
def seen_message():
    if not session.get('login') or not session.get('isAdmin'):
        return redirect( url_for('home') )

    print(request.form['id'])

    msg_id = request.form['id']

    qry = "delete from Messages where message_id=\'"+msg_id+"\'"
    mycursor.execute(qry)
    mydb.commit()

    return redirect(url_for('see_messages'))

#-------------------------------------------------------------------------------------------
def func(pct, allvals):
        absolute = round(pct/100.*np.sum(allvals))
        # if(absolute)
        return "{:.1f}%\n({:d})".format(pct,absolute)


@app.route('/statistics', methods=['GET','POST'])
def stats():
    # if not session.get('login') or not session.get('isAdmin'):
    #     return redirect( url_for('home') )
    qry = "select DC_ID, Amount_Collected, count(DC_ID) from Donation_camp group by Amount_Collected"
    mycursor.execute(qry)
    stats_donor = mycursor.fetchall()
    A = []
    B = []
    C = []
    for Amount_donated in stats_donor:
        # A.append(donation_camp[0])
        # B.append(donation_camp[1])
        C.append(Amount_donated[0])
        A.append(Amount_donated[1])
        B.append(Amount_donated[2])
    # plt.pie(B, labels = A)
    plt.pie(A, autopct=lambda pct: func(pct, A), labels = C)
    print(C)
    print(A)
    print(B)
    
    plt.savefig('./static/donor_stat.png')
    # plt.show()
    plt.close()
    A.clear()
    B.clear()

    # qry = "select Orphanage_ID, Amount_Donated, count(Orphanage_ID) from Orphanage_stats "
    qry = "select Orphanage_ID, Amount_Donated from Orphanage_stats "

    mycursor.execute(qry)
    stats_donor = mycursor.fetchall()
    A = []
    B = []
    C = []
    X = []
    Y = []
    for Amount_donated in stats_donor:
        # A.append(donation_camp[0])
        # B.append(donation_camp[1])
        C.append(Amount_donated[0])
        A.append(Amount_donated[1])
        # B.append(Amount_donated[2])
    # plt.pie(B, labels = A)
    print(C)
    print(A)
    D = set(C)
    for i in D:
        qry2 = "select orphanage_id, sum(amount_donated) from orphanage_stats where orphanage_id=\'"+i+"\';"
        mycursor.execute(qry2)
        stats_donor1 = mycursor.fetchall()
        for Amount_donated in stats_donor1:
        # A.append(donation_camp[0])
        # B.append(donation_camp[1])
            X.append(Amount_donated[0])
            Y.append(int(Amount_donated[1]))
        # B.append(Amount_donated[2])
    # plt.pie(B, labels = A)
    print(X)
    print(Y)


    plt.pie(Y, autopct=lambda pct: func(pct, Y), labels = X)
    
    # print(B)
    
    plt.savefig('./static/orphanage_stats.png')
    # plt.show()
    plt.close()
    A.clear()
    B.clear()
    D.clear()
    X.clear()
    Y.clear()

    qry = "select No_Boys, No_Girls, count(orphanage_Id) from orphanage group by No_Boys, No_Girls"
    mycursor.execute(qry)
    stats_orphanage = mycursor.fetchall()
    A = []
    B = []
    C = []
    
    for orphanage in stats_orphanage:
        # A.append(orphanage[0])
        # B.append(orphanage[1])
        A.append(orphanage[0])
        print(A)
        B.append(orphanage[1])
        print(B)
        C.append(orphanage[2])
    # plt.pie(B, labels = A)
    d= [sum(A), sum(B)]
    e = ['Boys', 'Girls']
    plt.pie(d, autopct=lambda pct: func(pct, d),labels = e)
    plt.savefig('./static/orphanage_stat1.jpeg')
    # plt.show()
    plt.close()
    # plt.pie(C, autopct=lambda pct: func(pct,C),labels = B)
    # plt.savefig('./static/orphanage_stat2.jpeg')
    # # plt.show()
    # plt.close()
    # qry = "select distinct donation_camp_donated from Transaction inner join Donor on Transaction.Donor_ID = Donor.Donor_ID"
    # mycursor.execute(qry)
    # list = mycursor.fetchall()
    # donation_camp_list = []
    # for donation_camp in list:
    #     print(donation_camp)
    #     donation_camp_list.append(donation_camp[0])
    # print(donation_camp)
    A.clear()
    B.clear()

    qry = "select ITEM_ID, ITEM_COUNT from Item group by ITEM_ID, ITEM_COUNT;"
    mycursor.execute(qry)
    stats_item = mycursor.fetchall()
    A = []
    B = []
    for Amount_donated in stats_item:
        # A.append(donation_camp[0])
        # B.append(donation_camp[1])
        A.append(Amount_donated[0])
        B.append(Amount_donated[1])
    # plt.pie(B, labels = A)
    print(A)
    print(B)
    
    plt.pie(B, autopct=lambda pct: func(pct, B), labels = A)
    plt.savefig('./static/item_stat.jpeg')
    # plt.show()
    plt.close()
    A.clear()
    B.clear()
    # for donation_camp in donation_camp_list:
    #     qry = "select count(*) from Transaction inner join Donor on Donor.Donor_ID = Transaction.Donor_ID where donation_camp_donated = '%s' and Status = 1" %donation_camp
    #     print(qry)
    #     mycursor.execute(qry)
    #     a = mycursor.fetchone()
    #     A.append(a[0])
    #     qry = "select count(*) from Transaction inner join Donor on Donor.Donor_ID = Transaction.Donor_ID where donation_camp_donated = '%s' and Status = 0" %donation_camp
    #     print(qry)
    #     mycursor.execute(qry)
    #     b = mycursor.fetchone()
    #     B.append(b[0])
    # print(A)
    # print(B)
    # print(donation_camp_list)
    # N = len(donation_camp_list)
    # fig, ax = plt.subplots()
    # ind = np.arange(N)
    # width = 0.05
    # plt.bar(ind, A, width, label='SUCCESS')
    # plt.bar(ind + width, B, width,label='FAILURE')
    # plt.ylabel('Number of transplantation')
    # plt.xlabel('donation_camp')
    # plt.title('SUCCESS V/S FAILURE IN donation_camp TRANSPLANTATION')
    # plt.xticks(ind + width / 2, donation_camp_list)
    # plt.legend(loc='best')
    # plt.savefig('./static/success.jpeg')
    return render_template('statistics.html')

if __name__ == "__main__":
    app.secret_key = 'sec key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
