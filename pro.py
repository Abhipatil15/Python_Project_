
from logging import exception
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

con=None
cur=None

myflask=Flask(__name__)

def connect():
    global con, cur
    con=pymysql.connect(host="localhost",user="root", password="root", database="web_project")
    cur=con.cursor()

def disconnect():
    cur.close()
    con.close()

def getdata():
    connect()
    selectquery = "select * from employees;"
    cur.execute(selectquery)
    data = cur.fetchall()
    disconnect()
    return data

def insertdata(id_no, full_name, Gmail, DOB=None):
    try:
        connect()
        insertquery = "insert into employees (id_no, full_name, Gmail, DOB) values (%s,%s,%s,%s);"
        cur.execute(insertquery, (id_no, full_name, Gmail, DOB))
        con.commit()
        disconnect()
        return True
    except:
        disconnect()
        return False

def getOne(id_no):
    connect()
    selectquery = "SELECT * FROM employees WHERE id_no=%s;"
    cur.execute(selectquery,(id_no, ))
    data = cur.fetchone()
    disconnect()
    return data

def updatedata(full_name,Gmail,id_no,DOB=None):
    try:
        connect()
        updateQuery = "UPDATE employees SET full_name=%s, Gmail=%s, DOB=%s WHERE id_no=%s;"
        cur.execute(updateQuery, (full_name, Gmail, DOB, id_no))
        print(id_no, full_name, Gmail, DOB)
        con.commit()
        disconnect()
        return True
    except :
        disconnect()
        return False

def deletedata(id_no):
    try:
        connect()
        deleteQuery = "DELETE FROM employees WHERE id_no=%s;"
        cur.execute(deleteQuery, (id_no, ))
        con.commit()
        disconnect()
        return True
    except:
        disconnect()
        return False

@myflask.route("/")
@myflask.route("/index/")
def index():
    if request.method=="GET":
        data = getdata()
        return render_template("index.html", data=data)
    return render_template("index.html")

@myflask.route("/add/", methods=['GET','POST'])
def addemployee():
    if request.method =="POST":
        data = request.form
        if insertdata(data['txtid_no'], data['txtfull_name'], data['txtGmail'], data['txtDOB']):
            message="Record inserted successfully"
        else:
            message="Due to some issue could't insert record"
        return render_template('insert.html', message=message)
    return render_template("insert.html")

@myflask.route("/edit/",methods=['GET','POST'])
def updateemployee():
    
    id_no=request.args.get('id',type=int,default=1)
    data=getOne(id_no)
    if request.method =="POST":
        fdata = request.form
        if updatedata(fdata['txtfull_name'], fdata['txtGmail'], id_no, fdata['txtDOB']):
         message="Record updated successfully"
        else:
         message="Due to some issue could't update record"
        return render_template('update.html', message=message)
    return render_template("update.html",data=data)

@myflask.route("/delete/")
def deleteemployee():
        
    id_no=request.args.get('id',type=int,default=1)
    deletedata(id_no)
    return redirect(url_for("index"))
      

if __name__=="__main__":
    myflask.run(debug=True)