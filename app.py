from flask import Flask,render_template,request,redirect,url_for
import pymysql
app=Flask(__name__)

db=None
cur=None

def connectDB():
    global db
    global cur
    db=pymysql.connect(host="localhost",
                       user="root",
                       password="",
                       database="assignment")
    cur=db.cursor()
def disconnectDB():
    cur.close()
    db.close()
    
def readallrecords():
    connectDB()
    selectquery="select * from employee"
    cur.execute(selectquery)
    result=cur.fetchall()
    disconnectDB()
    return result
    
@app.route("/")
def index():
    data=readallrecords()
    return render_template('index.html',data=data)

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/insertrecord')
def insertrecord():
    connectDB()
    name=request.args.get('name')
    department=request.args.get('department')
    salary=request.args.get('salary')
    insertquery='insert into employee(name,department,salary) values("{}","{}","{}")'.format(name,department,salary)
    cur.execute(insertquery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    connectDB()
    deletequery='delete from employee where id={}'.format(id)
    cur.execute(deletequery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

def readonerecord(id):
    connectDB()
    selectquery="select * from employee where id={}".format(id)
    cur.execute(selectquery)
    result=cur.fetchone()
    disconnectDB()
    return result

@app.route('/update/<id>')
def update(id):
    data=readonerecord(id)
    return render_template('update.html',data=data)

@app.route('/updaterecord/<id>', methods=['GET','POST'])
def updaterecord(id):
    connectDB()
    name= request.form['name']
    department=request.form['department']
    salary=request.form['salary']
    updatequery='update employee set name="{}",department="{}",salary="{}" where id={}'.format(name,department,salary,id)
    cur.execute(updatequery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)